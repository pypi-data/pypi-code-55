#!/usr/bin/env python3

from dataclasses import dataclass
from enum import Enum
from typing import Optional


@dataclass
class AptInstallablePackage:
    name: str
    apt_repository: Optional[str] = None

    def install_command(self) -> str:
        result = ""
        if self.apt_repository:
            result += f"add-apt-repository {self.apt_repository}; apt-get -q update; "
        result += f"apt-get -q -y install {self.name}"
        return result


class Dependency(Enum):
    DOCKER = AptInstallablePackage("docker.io")
    DOCKER_COMPOSE = AptInstallablePackage("docker-compose")
    JAVA11 = AptInstallablePackage("openjdk-11-jdk-headless")
    JAVA8 = AptInstallablePackage("openjdk-8-jdk-headless")
    MAVEN = AptInstallablePackage(name="maven")
    NODEJS = AptInstallablePackage(name="npm")
    PYTHON36 = AptInstallablePackage(
        name="python3.6", apt_repository="ppa:deadsnakes/ppa"
    )
    PYTHON37 = AptInstallablePackage(
        name="python3.7", apt_repository="ppa:deadsnakes/ppa"
    )
    PYTHON38 = AptInstallablePackage("python3.8")
