import dataclasses
import io
import pathlib
import subprocess
import tarfile

import docker
import structlog

from . import utils


logger = structlog.get_logger(__name__)


class Shell:
    """
    Shell

    A shell environment based on a docker image. When the shell is
    activated, it starts a container based on the image and
    keeps it running until the shell is deactivated.
    """

    @classmethod
    def from_container_id(cls, container_id):
        """
        Create shell instance from the given container ID.
        """
        container = utils.get_container(container_id)
        return cls.from_container(container)

    @classmethod
    def from_container(cls, container):
        """
        Create shell instance from the given container.
        """
        instance = cls(container.image)
        instance._container = container

        config = container.attrs.get("Config", {})
        instance._workdir = config.get("WorkingDir")

        volumes = {}
        for mount in container.attrs.get("Mounts", []):
            if mount["Type"] == "bind":
                source = mount["Source"]
                target = mount["Destination"]
                volumes[source] = {"bind": target, "mode": mount["Mode"]}

        instance._volumes = volumes

        return instance

    def __init__(self, image):
        self._image = image
        self._container = None
        self._workdir = "/home/cuta"
        self._volumes = {}
        self._docker = None

    @property
    def docker(self):
        if not self._docker:
            self._docker = docker.from_env()

        return self._docker

    @property
    def image(self):
        return self._image

    @property
    def container(self):
        return self._container

    @property
    def workdir(self):
        return self._workdir

    @workdir.setter
    def workdir(self, workdir):
        self._workdir = workdir

    @property
    def volumes(self):
        return self._volumes

    def mount(self, source, target=None, mode="rw"):
        target = target or self.workdir
        self._volumes[source] = {"bind": target, "mode": mode}

    def unmount(self, source):
        self._volumes.pop(source, None)

    @property
    def status(self):
        return self.container.status if self.container else None

    @property
    def active(self):
        """
        Check if the shell is active.

        The shell is considered active when its container is running.
        """
        return self.status == "running"

    def activate(self):
        """
        Activate the shell (i.e. start container)
        """
        if self.active:
            return

        command = ["sleep", "infinity"]
        self._container = self.docker.containers.create(
            self.image,
            command=command,
            volumes=self.volumes,
            working_dir=self.workdir,
            auto_remove=True,
        )
        self._container.start()
        self._container.reload()

        logger.info(f"Shell activated", container_id=self.container.id)

    def deactivate(self):
        """
        Deactive

        Deactivate the shell (i.e. kill and remove container)
        """
        if not self.active:
            return

        container_id = self.container.id
        self.container.kill()
        self._container = None

        logger.info(f"Shell deactivated", container_id=container_id)

    def __enter__(self):
        self.activate()
        return self

    def __exit__(self, *exc_details):
        self.deactivate()

    def execute(self, cmd, **kwargs):
        """
        Execute the given command

        Execute the given command inside the container.
        """
        if not self.container:
            raise RuntimeError("Shell must be activated")

        return self.container.exec_run(cmd, **kwargs)

    def interact(self):
        """
        Interact

        Start the shell in interactive mode.
        """
        if self.container:
            self._exec_interactive()
        else:
            self._run_interactive()

    def _run_interactive(self):
        exe = "bash"
        cmd = [
            "docker",
            "run",
            "--interactive",
            "--tty",
            "--rm",
        ]

        if self.volumes:
            for source, value in self.volumes.items():
                target = value["bind"]
                args = ["--volume", f"{source}:{target}"]
                cmd.extend(args)

        if self.workdir:
            cmd.extend(["--workdir", str(self.workdir)])

        cmd.extend([self.image.tags[0], exe])

        subprocess.run(cmd)

    def _exec_interactive(self):
        exe = "bash"
        cmd = [
            "docker",
            "exec",
            "--interactive",
            "--tty",
        ]

        cmd.extend([self.container.id, exe])
        subprocess.run(cmd)

    def get_file(self, source, target):
        """
        Get file

        Copy source file to the given target location.
        """
        if not self.container:
            raise RuntimeError("Shell must be activated")

        # Get archive (tar) from the container.
        stream = io.BytesIO()
        chunks, _ = self.container.get_archive(str(source))
        for chunk in chunks:
            stream.write(chunk)

        # Move cursor back to the beginning of the file.
        stream.seek(0)

        # Extract file data and write it to the target.
        source = pathlib.Path(source)
        target = pathlib.Path(target)
        tar = tarfile.TarFile(fileobj=stream)
        extracted = tar.extractfile(source.name)
        with target.open("wb") as file_:
            data = extracted.read()
            file_.write(data)

        logger.info(f"Copied {self.container.id}:{source} to {target}")

        return target


