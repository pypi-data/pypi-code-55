#!/usr/bin/env python3

"""Functions for printing info to terminal."""

from os.path import abspath


def truncate_path(path: str = None, base_path: str = None) -> str:
    """
    Return a shortened version of a given path string.

    Removes the base path string from the path to be truncated.

    Parameters:
        path (str): Path to truncate
        base_path (str): Base path to omit from the main path
    Returns:
        str: Shortened path string for the given path
    """
    if path is None:
        return ""
    path_str = abspath(path)
    if base_path is None:
        return path_str
    base_str = abspath(base_path)
    if path_str.startswith(base_str):
        return "..." + path_str[len(base_str):]
    return path_str


def print_paths(paths: list = None, base_path: str = None):
    """
    Print a list of paths.

    Parameters:
        paths (list): Paths to print
        base_path (str): Base path used for truncating path strings
    """
    if paths is not None:
        for path in paths:
            print(truncate_path(path, base_path))
