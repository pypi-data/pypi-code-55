
import toml
from typing import Any

"""
Toml File

This module contains a utility class for working with TOML files.
"""


class TomlFile:
    """
    TOML File

    This class represents a TOML file and provides
    some useful properties/methods for accessing the
    file data.
    """

    def __init__(self, path: str, data: dict = None):
        self._path = path
        self._data = data or {}

    @property
    def path(self) -> str:
        return self._path

    @property
    def data(self) -> dict:
        return self._data

    def get_value(self, path: str) -> Any:
        """
        Get value

        Get an attribute of the toml file. Nested
        values can be accessed using a dotted key.
        """
        data = self.data
        keys = path.split(".")
        for key in keys:
            if isinstance(data, dict):
                data = data[key]

        return data

    def set_value(self, path: str, value: Any) -> None:
        """
        Set value

        Set an attribute of the toml file. Nested
        values can be accessed using a dotted key.
        """
        data = self.data
        keys = path.split(".")
        parent = None
        for key in keys:
            if isinstance(data, dict):
                parent = data
                data = data[key]

        parent[key] = value

    def read(self) -> None:
        """
        Read data from disk.
        """
        self._data = read_toml(str(self.path))

    def write(self) -> None:
        """
        Write data to disk.
        """
        write_toml(str(self.path), self.data)


def read_toml(path: str) -> dict:
    """
    Read project file (i.e. pyproject.toml)
    """
    with open(path, "r") as project_file:
        return toml.load(project_file)


def write_toml(path: str, data: dict) -> None:
    """
    Write project file (i.e. pyproject.toml)
    """
    with open(path, "w") as project_file:
        toml.dump(data, project_file)
