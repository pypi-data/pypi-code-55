from os import path
from typing import List

from detector.dependency import Dependency


def detect_docker(directory_path: str) -> List[Dependency]:
    result: List[Dependency] = []

    if path.exists(f"{directory_path}/Dockerfile"):
        result.append(Dependency.DOCKER)

    if path.exists(f"{directory_path}/docker-compose.yml"):
        result.append(Dependency.DOCKER_COMPOSE)

    return result
