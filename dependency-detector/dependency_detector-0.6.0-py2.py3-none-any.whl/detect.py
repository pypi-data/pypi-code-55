#!/usr/bin/env python3

import os
import sys
from typing import List

from detector.dependency import Dependency
from detector.detect_docker import detect_docker
from detector.detect_java import detect_java
from detector.detect_nodejs import detect_nodejs
from detector.detect_python import detect_python

detect_methods = [detect_docker, detect_java, detect_python, detect_nodejs]


def detect_dependencies(directory_path: str) -> List[Dependency]:
    result = []
    for detect_method in detect_methods:
        result.extend(detect_method(directory_path))
    return result


def cli():
    if len(sys.argv) < 1:
        print("Usage: ./detect.py DIRECTORY")
        sys.exit(1)

    directory = sys.argv[1]
    if not os.path.isdir(directory):
        sys.exit(f"Not a directory: {directory}")

    packages_to_install = detect_dependencies(directory)

    result = ""
    for package in packages_to_install:
        if result != "":
            result += "; "
        result += package.value.install_command()
    print(result)
