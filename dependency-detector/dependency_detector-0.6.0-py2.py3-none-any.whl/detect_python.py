from os import path
from typing import List

import toml
from detector.dependency import Dependency


def detect_python(directory_path: str) -> List[Dependency]:
    result: List[Dependency] = []
    possibly_pipfile = f"{directory_path}/Pipfile"
    if path.exists(possibly_pipfile):
        pipfile = toml.load(possibly_pipfile)
        if "requires" in pipfile:
            requires = pipfile["requires"]
            if "python_version" in requires:
                python_version = requires["python_version"]
                if python_version == "3.6":
                    result.append(Dependency.PYTHON36)
                elif python_version == "3.7":
                    result.append(Dependency.PYTHON37)
                elif python_version == "3.8":
                    result.append(Dependency.PYTHON38)
    return result
