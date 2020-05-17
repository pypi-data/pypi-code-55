# coding: utf-8

from typing import (List, TextIO)

import os
from sys import stdout, stderr
from pathlib import Path

from .betterprint import printerror

__all__ = [
    "which",
    "check_dir",
]


def which(command: str) -> str:
    """Return the absolute path to the command.

    Args:
        command (str): command to resolve

    Returns:
        str: absolute path

    Raises:
        Exception: if the path cannot be resolved
    """
    abs_path = Path(command).absolute()
    if Path(command).exists():
        return str(abs_path)

    for path in os.getenv("PATH").split(os.pathsep):
        abs_path = Path(path, command)
        if abs_path.is_file() and os.access(abs_path, os.X_OK):
            return str(abs_path)

    printerror(f"{command} is not a valid command!")
    raise Exception


def check_dir(path: Path):
    """Check if given path points to a directory.

    Args:
        path (Path): path to check

    Raises:
        Exception: if not a directory
    """
    if not path.is_dir():
        printerror(f"{path} is not a valid directory!")
        raise Exception
