import io
import os
import pathlib
import logging
import structlog
import subprocess
import sys
import tarfile

import docker

from . import utils
from .shell import Shell


logger = structlog.get_logger(__name__)


class Environment:
    """
    Environment

    This class represents a container-based environment.
    """

    @classmethod
    def from_image_id(cls, image_id):
        image = utils.get_image(image_id)
        print(">>> image", image)
        if image:
            return cls.from_image(image)

    @classmethod
    def from_image(cls, image):
        name = image.tags[0]
        instance = cls(name)
        instance._image = image
        return instance

    def __init__(self, name):
        self._name = name
        self._image = None

    @property
    def docker(self):
        return utils.get_docker()

    @property
    def name(self):
        return self._name

    @property
    def image(self):
        if not self._image:
            self._image = utils.get_image(self.name)

        return self._image

    def shell(self):
        """
        Get shell
        """
        return Shell(self.image)

    def exists(self):
        return bool(self.image)

    def pull(self):
        """
        Pull environment from remote repository (i.e. DockerHub)
        """
        if not self.image:
            print(">>> here", self.image)
            output = self.docker.api.pull(self.name, stream=True, decode=True)
            for item in output:
                yield item

    def init(self):
        """
        Initialize

        Initialize the environment. If the image for the environment
        doesn't exist locally, this method will download it.
        """
        report = {}
        for item in self.pull():
            uid = item.get("id", "")
            status = item.get("status", "")
            progress = item.get("progress")
            if not uid:
                continue

            report[uid] = (status, progress)
            for uid, (status, progress) in report.items():
                msg = f"{uid}: {status}"
                msg = f"{msg}: {progress}" if progress else msg
                logger.info(msg)

            utils.clear_lines(len(report))

    def delete(self):
        """
        Delete

        Delete the image associated to this environment.
        """
        filters = {"ancestor": self.name}
        containers = self.docker.containers.list(filters=filters)
        for container in containers:
            container.remove(v=True, force=True)
            logger.debug(f"Removed container: {container.id}")

        self.docker.images.remove(self.name, force=True)
        logger.debug(f"Removed image: {self.name}")

        self._image = None
