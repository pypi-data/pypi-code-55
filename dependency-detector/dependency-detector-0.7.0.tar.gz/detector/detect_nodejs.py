from os import path
from typing import List

from detector.dependency import Dependency


def detect_nodejs(directory_path: str) -> List[Dependency]:
    result: List[Dependency] = []
    packages_json = f"{directory_path}/package.json"
    if path.exists(packages_json):
        result.append(Dependency.NODEJS)
    return result
