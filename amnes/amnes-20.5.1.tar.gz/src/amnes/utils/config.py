"""This module contains all classes and functions for basic app configurations.

Classes:
    BaseConfiguration: Abstract base class for component configurations.
    BaseConfigTree: Abstract base class for configuration trees.
    ConfigurationError: Error which is raised by configuration classes and
                        functions on exceptions.
"""

from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import Dict, Type, TypeVar

import yaml

BaseConfigurationBoundType = TypeVar(
    "BaseConfigurationBoundType", bound="BaseConfiguration"
)


class BaseConfiguration(metaclass=ABCMeta):  # pylint: disable=too-few-public-methods
    """Abstract base class for component configurations.

    Every configuration class for an AMNES component must inherit from this class.
    """

    @classmethod
    @abstractmethod
    def from_yamldict(
        cls: Type[BaseConfigurationBoundType], yamlconfig: Dict
    ) -> BaseConfigurationBoundType:
        """Abstract method for creating a configuration object from a YAML dictionary.

        This method must be implemented by all subclasses of `BaseConfiguration` and
        will be called by subclasses implementations for chaining configuration parsing.

        Args:
            yamlconfig (Dict): Dictionary representation of an YAML file from which the
                               configuration object should be created.
        """


class BaseConfigTree(metaclass=ABCMeta):  # pylint: disable=too-few-public-methods
    """Abstract base class for configuration trees.

    YAML configuration file for a subclass derived from `BaseConfiguration` consists
    of multiple first level keys which correspond to a configuration tree which must
    inherit this class.

    Example YAML configuration:

    ```yaml
    fooconfig:
      key1: val1
      key2: val2
    bartree:
      keyA: valA
      keyB: valB
    ```

    The given example contains the two first level keys "fooconfig and "bartree", each
    of them representing a configuration tree.
    """

    @classmethod
    @abstractmethod
    def parse(cls, cfgdict: Dict) -> BaseConfigTree:
        """Parse dictionary under the first level key and create configuration tree.

        This method must be implemented by all subclasses of `BaseConfigTree` and
        should be called by the corresponding configuration implementation of
        `BaseConfiguration.from_yamldict()`.

        Args:
            cfgdict (Dict): Part of configuration dictionary which is located under the
                            corresponding first level key of the configuration tree.
        """


class ConfigurationError(Exception):
    """Error which is raised by configuration classes and functions on exceptions.

    This error can be customized by setting specific parameters on creation.
    If `message` is set, this message is used as the error message.
    If `obj` is set, a default prefix is used and the object is appended to it.
    Otherwise, a default string for an unspecified configuration error is used.
    The value of `obj` is ignored if `message` is set.

    >>> ConfigurationError()
    "ConfigurationError: Unspecified configuration error occured while processing
     configuration."

    >>> ConfigurationError(message="An example error was found.")
    "ConfigurationError: An example error was found."

    >>> ConfigurationError(obj="example config")
    "ConfigurationError: Error occured while processing example config."

    >>> ConfigurationError(message="A message.", obj="example config")
    "ConfigurationError: A message."

    >>> ConfigurationError(plain=True)
    "ConfigurationError"
    """

    def __init__(
        self, *, message: str = "", obj: str = "", plain: bool = False
    ) -> None:
        """Configuration Error class constructor method.

        Args:
            message (str): More precise custom error message.
            obj (str): Object string appended to default message prefix.
            plain (bool): If plain error (empty error string) should be created.
        """
        super().__init__()
        self.__plain = plain
        self.__message = message
        self.__obj = obj

    def __str__(self) -> str:
        """Overwrite magic string method of the super class.

        Overrides the string method of `Exception` by modifing the exception
        message with a more precise description.

        Returns:
            str: Custom error message constructed with set attributes.
        """
        if self.__plain:
            return ""
        if self.__message and (not self.__message.isspace()):
            return self.__message
        if self.__obj and (not self.__obj.isspace()):
            return f"Error occured while processing {self.__obj}."
        return "Unspecified configuration error occured while processing configuration."


def load_configuration(
    filepath: str, configcls: Type[BaseConfigurationBoundType]
) -> BaseConfigurationBoundType:
    """Create configuration object by loading a corresponding YAML file from filesystem.

    Args:
        filepath (str): Path to YAML config file on filesystem.
        configcls (Type[BaseConfigurationBoundType]): Class reference of the
                                                      configuration type which should be
                                                      created from the YAML config file.

    Returns:
        Configuration object created from the given YAML file with the specified
        configuration type.

    Raises:
        ConfigurationError: If any file or configuration error occurs.
    """
    try:
        with open(filepath, mode="rt") as stream:
            yamldoc = yaml.safe_load(stream)
            return configcls.from_yamldict(yamldoc)
    except Exception as exc:
        raise ConfigurationError(
            message=f"Could not load '{filepath}' as '{configcls.__name__}'"
            + " from filesystem.'"
        ) from exc
