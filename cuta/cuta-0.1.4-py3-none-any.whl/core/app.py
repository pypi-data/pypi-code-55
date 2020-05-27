
import codecs
import configparser
import dataclasses
import json
import pathlib
import re
import shutil
import structlog
import subprocess
import yaml
import uuid

import docker

from .envs import Environment, Shell, build_image, get_container
from .package import Package


logger = structlog.get_logger(__name__)


class App:
    """
    Application

    This class represents an application.
    """

    def __init__(self, root):
        self._root = pathlib.Path(root)
        self._info = None
        self._package = None
        self._shell = None

    @property
    def root(self):
        return self._root

    @property
    def info(self):
        if not self._info:
            self._info = self._get_info() or {}

        return self._info

    def _get_info(self):
        path = self.root.joinpath(".cuta", "info.yml")
        if path.exists():
            return yaml.safe_load(path.read_text())

    @property
    def id(self):
        return self.info.get("id")

    @property
    def runtime(self):
        return self.info.get("runtime")

    @property
    def package(self):
        if not self._package:
            self._package = self._get_package()

        return self._package

    def _get_package(self):
        path = self.root.joinpath("pyproject.toml")
        return Package.from_path(path) if path.exists() else None

    @property
    def name(self):
        return self.root.name

    @property
    def version(self):
        return self.package.version if self.package else None

    @property
    def envs(self):
        envs = []
        for info in self.info.get("envs", {}).values():
            image_id = info.get("image")
            if image_id:
                env = Environment.from_image_id(image_id)
                envs.append(env)

        return envs

    @property
    def shell(self):
        if self._shell is None:
            self._shell = self._get_shell()

        return self._shell

    def _get_shell(self):
        dev_info = self.info.get("envs", {}).get("dev", {})
        container_id = dev_info.get("container")
        container = get_container(container_id)
        if container:
            shell = Shell.from_container(container)
            shell.activate()
            return shell
        else:
            return self._create_shell()

    def _create_shell(self, update_info=True):
        env = self.get_environment("dev")
        shell = env.shell()
        shell.workdir = f"/home/cuta/{self.name}"
        shell.mount(self.root, f"/home/cuta/{self.name}")
        shell.activate()

        if update_info:
            self._info["envs"]["dev"] = {
                "image": shell.image.id,
                "container": shell.container.id
            }

            path = self.root.joinpath(".cuta", "info.yml")
            content = yaml.dump(self._info)
            path.write_text(content)

        return shell

    def init(self, runtime):
        """
        Initialize

        Initialize application. This method will create the
        base/build environment required to manage the app.
        """
        if self.id:
            return

        # Initialize development environment.
        build_args = {"PLATFORM": "aws", "RUNTIME": runtime}
        self.build_environment("dev", build_args=build_args)

        self._shell = self._create_shell(update_info=False)

        info = {
            "id": str(uuid.uuid4()),
            "platform": "aws",
            "runtime": runtime,
            "envs": {
                "dev": {
                    "image": self.shell.image.id,
                    "container": self.shell.container.id
                }
            }
        }

        path = self.root.joinpath(".cuta", "info.yml")
        content = yaml.dump(info)
        path.write_text(content)
        self._info = info

        self._create_package()
        self.lock()

    def _create_package(self):
        logger.debug(f"Creating package", name=self.name)
        cmd = ["poetry", "init", f"--no-interaction", f"--name={self.name}"]
        self.execute(cmd)

    def get_environment(self, env="dev"):
        """
        Get environment

        Get the environment with the given name. If the environment
        does not exist, try to build it and then return it.
        """
        name = f"{self.name}:{env}"
        if not Environment(name).exists():
            self.build_environment(env)

        return Environment(name)

    def build_environment(self, env="dev", build_args=None):
        """
        Build environment

        Build the image used to define the given environment.
        """
        tag = f"{self.name}:{env}"
        path = self.get_image_file(env)

        logger.info("Building image", tag=tag, path=str(path))

        relpath = path.relative_to(self.root)
        build_args = build_args or {"APP": self.name}
        outputs = build_image(
            path=str(self.root),
            dockerfile=str(relpath),
            tag=tag,
            rm=True,
            decode=True,
            buildargs=build_args
        )
        for output in outputs:
            logger.info(output)

        env = Environment(f"{self.name}:{env}")
        return env

    def get_image_file(self, env="dev"):
        """
        Get image file

        Get the file used to build an image for the given environment.
        """
        return self.root.joinpath(".cuta", "envs", env, "Dockerfile")

    def lock(self):
        """
        Lock dependencies

        Create lock file containing the current dependencies.
        """
        self.execute(["poetry", "lock"])

    def add_dependencies(self, deps, env=None):
        """
        Add dependencies

        Add dependencies to the given environment.
        """
        logger.info("Adding dependencies", env=env, deps=deps)

        if not env:
            self._add_dependencies(deps)

        elif env == "dev":
            self._add_development_dependencies(deps)

    def _add_development_dependencies(self, deps):
        self.execute(["poetry", "add", "--dev", *deps])

    def _add_dependencies(self, deps):
        self.execute(["poetry", "add", *deps])

    def remove_dependencies(self, deps, env=None):
        """
        Remove dependencies

        Remove dependencies from the given environment.
        """
        logger.info("Removing dependencies", env=env, deps=deps)

        if not env:
            self._remove_dependencies(deps)

        elif env == "dev":
            self._remove_development_dependencies(deps)

    def _remove_development_dependencies(self, deps):
        self.execute(["poetry", "remove", "--dev", *deps])

    def _remove_dependencies(self, deps):
        self.execute(["poetry", "remove", *deps])

    def build(self):
        """
        Build

        Build application
        """
        source = "app.py"
        target = "../.cuta/build/function.zip"

        cmd1 = "cd app"
        cmd2 = f"zip {target} {source}"
        cmd = ["sh", "-c", f"{cmd1} && {cmd2}"]
        self.execute(cmd)
        self._build_resources()

    def _build_resources(self):
        # @todo: dynamically create function resources using templates
        # @todo: dynamically set terraform variables.
        tfvars = {
            "runtime": self.runtime,
            "function_name": "hello",
            "function_handler": "app.handler",
            "function_version": "0.1.0",
            "function_archive": "../build/function.zip"
        }

        text = json.dumps(tfvars, indent=2)
        path = self.root.joinpath(".cuta", "resources", ".tfvars.json")
        path.write_text(text)

    def deploy(self):
        """
        Deploy

        Deploy application
        """
        cmd1 = "cd .cuta/resources"
        cmd2 = "terraform init"
        cmd3 = "terraform apply -auto-approve -var-file=.tfvars.json"
        cmd = ["sh", "-c", f"{cmd1} && {cmd2} && {cmd3}"]
        environment = self._get_env_vars()
        self.execute(cmd, environment=environment)

    def destroy(self):
        """
        Destroy

        Destroy application deployment
        """
        cmd1 = "cd .cuta/resources"
        cmd2 = "terraform destroy -auto-approve -var-file=.tfvars.json"
        cmd = ["sh", "-c", f"{cmd1} && {cmd2}"]

        environment = self._get_env_vars()
        self.execute(cmd, environment=environment)

    def _get_env_vars(self):
        environment = {}
        home = pathlib.Path.home()
        creds = home.joinpath(".aws", "credentials")
        if creds.exists():
            parser = configparser.ConfigParser()
            parser.read(creds)
            keys = ["aws_access_key_id", "aws_secret_access_key"]
            for key in keys:
                environment[key.upper()] = parser.get("default", key)

        return environment

    def execute(self, cmd, **options):
        """
        Execute

        Execute the given command inside the development environment.
        """
        logger.debug("Execute", cmd=" ".join(cmd))
        _, chunks = self.shell.execute(cmd, stream=True, **options)
        for chunk in chunks:
            output = chunk.decode("utf-8")
            for line in output.splitlines():
                logger.info(line)

    def interact(self):
        """
        Create interactive shell environment.
        """
        self.shell.interact()

    def clean(self):
        """
        Clean

        Clean out environments.
        """
        for env in self.envs:
            env.delete()

    def delete(self):
        """
        Delete

        Delete the application along with any associated environments.
        """
        self.clean()
        shutil.rmtree(str(self.root), ignore_errors=True)
