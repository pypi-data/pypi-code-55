import distutils.spawn
import logging
import os
import re
import shutil
import subprocess
import tarfile
import uuid
from abc import abstractmethod
from io import BytesIO
from pathlib import Path, PurePath
from typing import TYPE_CHECKING, Generic, Iterable, List, Mapping, Optional, Pattern

import attr
from semantic_version import SimpleSpec, Version

from bento.error import DockerFailureException, ToolRunException
from bento.tool.tool import R, Tool
from bento.util import Memo


def __extract_use_binary() -> Optional[bool]:
    e = os.environ.get("BENTO_USE_BINARY")
    return e == "1" if e is not None else None


DOCKER_INSTALLED = Memo[bool](lambda: shutil.which("docker") is not None)
DEFAULT_VERSION_PATTERN = re.compile(r"(.*)")
USE_BINARY = __extract_use_binary()

if TYPE_CHECKING:
    import docker.client
    from docker.models.containers import Container


def get_docker_client() -> "docker.client.DockerClient":
    """Checks that docker client is reachable"""
    # import inside def for performance
    import docker

    try:
        client = docker.from_env()
        client.info()
        return client
    except Exception as e:
        logging.debug(e)
        raise DockerFailureException()


def copy_into_container(
    paths: Mapping[Path, str], container: "Container", destination_path: PurePath
) -> None:
    """Copy local ``paths`` to ``destination_path`` within ``container``.

    The ``container`` is assumed to be running.
    If ``destination_path`` does not exist, it will be created.
    """
    tar_buffer = BytesIO()
    with tarfile.open(mode="w", fileobj=tar_buffer) as archive:
        for p, loc in paths.items():
            archive.add(str(p), arcname=loc)
    tar_buffer.seek(0)
    tar_bytes = tar_buffer.read()

    logging.info(f"sending {len(tar_bytes)} bytes to {container}")
    container.put_archive(str(destination_path), tar_bytes)


@attr.s
class DockerTool(Generic[R], Tool[R]):
    UUID = str(uuid.uuid4())[:8]

    binary_command_root = attr.ib(type=List, init=False)
    uses_binary = attr.ib(type=bool, init=False)

    def __attrs_post_init__(self) -> None:
        bc = self.binary_command()
        self.uses_binary = bc is not None
        self.binary_command_root = [] if bc is None else bc

    def binary_command(self) -> Optional[List[str]]:
        """
        If present, this command will be used to run the tool instead of Docker
        :return:  The binary run command, or None to always use Docker
        """
        return None

    @property
    @abstractmethod
    def docker_image(self) -> str:
        """
        Returns the name of the docker image
        """
        pass

    @property
    @abstractmethod
    def docker_command(self) -> List[str]:
        """
        Returns the command to run in the docker image
        """
        pass

    @property
    def use_remote_docker(self) -> bool:
        """Return whether the Docker daemon is remote.

        We need to know because volume mounting doesn't work with remote daemons.
        """
        return (
            os.getenv("BENTO_REMOTE_DOCKER", "0") == "1"
            or os.getenv("R2C_USE_REMOTE_DOCKER", "0") == "1"
        )

    @property
    def additional_file_targets(self) -> Mapping[Path, str]:
        """
        Additional files, beyond the files to check, that should be copied to the Docker container

        For example, this might include configuration files.

        Format is mapping of local path objects to remote path strings.
        """
        return {}

    @property
    @abstractmethod
    def remote_code_path(self) -> str:
        """
        Where to locate remote code within the docker container
        """
        pass

    @property
    def local_volume_mapping(self) -> Mapping[str, Mapping[str, str]]:
        """The volumes to bind when Docker is running locally"""
        return {str(self.base_path): {"bind": self.remote_code_path, "mode": "ro"}}

    def is_allowed_returncode(self, returncode: int) -> bool:
        """Returns true iff the Docker container's return code indicates no error"""
        return returncode == 0

    def assemble_full_command(self, targets: Iterable[str]) -> List[str]:
        """Creates the full command to send to the docker container from file targets"""
        return self.docker_command + list(targets)

    def _prepull_image(self) -> None:
        """
        Pulls the docker image from Docker hub
        """
        client = get_docker_client()

        if not any(i for i in client.images.list() if self.docker_image in i.tags):
            client.images.pull(self.docker_image)
            logging.info(f"Pre-pulled {self.tool_id()} image")

    def _create_container(self, targets: Iterable[str]) -> "Container":
        """
        Creates and returns the Docker container
        """

        client = get_docker_client()

        vols = {} if self.use_remote_docker else self.local_volume_mapping
        full_command = self.assemble_full_command(targets)

        logging.info(f"starting new {self.tool_id()} container")

        container: "Container" = client.containers.create(
            self.docker_image,
            command=full_command,
            auto_remove=True,
            volumes=vols,
            detach=True,
            working_dir=self.remote_code_path,
        )
        logging.info(f"started container: {container!r}")

        return container

    def _setup_remote_docker(
        self, container: "Container", expanded: Mapping[Path, str]
    ) -> None:
        """Copies files into the remote Docker container"""
        copy_into_container(expanded, container, PurePath(self.remote_code_path))
        copy_into_container(
            self.additional_file_targets, container, PurePath(self.remote_code_path)
        )

    def _run_container(self, files: Iterable[str]) -> subprocess.CompletedProcess:
        logging.info(f"Running {self.tool_id()} using Docker image")
        targets: Iterable[Path] = [Path(p) for p in files]
        is_remote = self.use_remote_docker
        expanded = {t: str(t.relative_to(self.base_path)) for t in targets}

        container = self._create_container(expanded.values())

        if is_remote:
            self._setup_remote_docker(container, expanded)

        # Python docker does not allow -a, so use subprocess.run
        return subprocess.run(
            ["docker", "start", "-a", str(container.id)],
            encoding="utf-8",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def _run_binary(self, files: Iterable[str]) -> subprocess.CompletedProcess:
        logging.info(f"Running {self.tool_id()} using installed binary")
        command = self.binary_command_root + self.assemble_full_command(files)
        return subprocess.run(
            command, encoding="utf-8", stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

    def run_command(self, files: Iterable[str]) -> subprocess.CompletedProcess:
        """
        Run this tool, either in a local binary or Docker container
        """
        result = (
            self._run_binary(files) if self.uses_binary else self._run_container(files)
        )

        logging.info(
            f"{self.tool_id()}: Returned code {result.returncode} with stdout[:4000]:\n"
            f"{result.stdout[:4000]}\nstderr[:4000]\n{result.stderr[:4000]}"
        )

        if not self.is_allowed_returncode(result.returncode):
            raise subprocess.CalledProcessError(
                cmd=self.docker_command,
                returncode=result.returncode,
                output=result.stdout,
                stderr=result.stderr,
            )

        return result

    def matches_project(self, files: Iterable[Path]) -> bool:
        return (
            DOCKER_INSTALLED.value or self.uses_binary
        ) and self.project_has_file_paths(files)

    def setup(self) -> None:
        if not self.uses_binary:
            self._prepull_image()

    @staticmethod
    def has_allowed_binary_version(
        binary: str,
        spec: SimpleSpec,
        match: Pattern = DEFAULT_VERSION_PATTERN,
        version_query: Optional[List[str]] = None,
    ) -> bool:
        """
        Queries the version of a locally installed binary to determine if Docker can be skipped

        :param binary: The name of the binary executable
        :param spec: Allowed range of versions for skipping Docker
        :param match: Pattern used to extract the binary version from the query result
        :param version_query: Flags to pass to the executable to query the version, defaults to ["--version"]
        :return: If Docker can be skipped
        """
        if USE_BINARY is False:
            logging.debug(
                f"Using Docker for {binary} due to passed BENTO_USE_BINARY flag."
            )
            return False
        version_query = ["--version"] if version_query is None else version_query
        executable = distutils.spawn.find_executable(binary)
        if not executable:
            logging.debug(f"Binary for '{binary}' not in path")
            if USE_BINARY is True:
                raise ToolRunException(f"Could not find {binary} in the path.")
            return False
        cmd = [executable] + version_query
        query_output = subprocess.run(
            cmd, stdout=subprocess.PIPE, encoding="utf-8", check=True
        ).stdout.rstrip()
        version_match = match.search(query_output)
        logging.debug(
            f"'{binary}' version string is '{version_match}' in\n{query_output}"
        )
        if not version_match or len(version_match.groups()) < 1:
            if USE_BINARY is True:
                raise ToolRunException(
                    f"Could not read version from '{' '.join(cmd)}' (got '{query_output}')."
                )
            return False
        if Version(version_match[1]) not in spec:  # type: ignore
            if USE_BINARY is True:
                raise ToolRunException(
                    f"Version for '{binary}' is '{version_match[1]}', expected a version in the range '{spec}'."
                )
            return False
        return True
