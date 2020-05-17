"""This module contains all necessary definitions for all classes for the parser."""

from abc import ABCMeta, abstractmethod
from contextlib import contextmanager
from typing import Dict, Iterator, Optional

from ..core.amnes_object import AmnesObject


@contextmanager
def _parse_key_context(key: str) -> Iterator[None]:
    """Catch all exception and raise a ParsingError with exception as cause.

    Args:
        key (str): Key which is passed to the raised ParsingError for a specific
                    exception message.

    Yields:
        None: No yield value available.

    Raises:
        ParsingError: If any exception occurs.
    """
    try:
        yield
    except Exception as exc:
        raise ParsingError(key=key) from exc


# pylint: disable=too-few-public-methods
class YamlParsable(metaclass=ABCMeta):
    """Interface which is implemented by all classes that can be parsed.

    All classes that can be parsed from a YAML configuration, represented
    by a nested dictionary, must implement this interface and its methods.
    """

    @staticmethod
    @abstractmethod
    def parse(config: Dict) -> AmnesObject:
        """Abstract parse method that is overwritten by the implementing classes.

        Implementations will always be given a dictionary with exactly one key
        as parameter, which is used as slug.
        As return type the specific class must be used.

        Implementations should call: `YamlParsable._parse_check(config)`.

        Args:
            config (Dict): Dictionary from which the corresponding object is created.
        """

    @staticmethod
    def _parse_check(config: Dict) -> None:
        """Internal method for running basic checks on config dictionary for parsing.

        Args:
            config (Dict): Dictionary from which the corresponding object
                           should be created.

        Raises:
            ParsingError: If any check fails for `config`.
        """
        if not isinstance(config, Dict):
            raise ParsingError(plain=True) from TypeError(
                "Given config is not of type Dict."
            )
        if len(config.keys()) != 1:
            raise ParsingError(message="Config dictionary contains more than one key.")

    _parse_key_context = _parse_key_context


class ParsingError(Exception):
    """Error which is raised when a parsing operation exception occurs.

    This error can be customized by setting specific parameters on creation.
    If `plain` is set to True on creation, the printed error string will be empty.
    Otherwise, the error string will be constructed with `message` and `key` if set.

    >>> ParsingError()
    "ParsingError: Error occured while parsing."

    >>> ParsingError(plain=True)
    "ParsingError"

    >>> ParsingError(message="Custom message.")
    "ParsingError: Could not parse: Custom message."

    >>> ParsingError(key="my.key")
    "ParsingError: Could not parse key 'my.key'."

    >>> ParsingError(message="Custom message.", key="my.key")
    "ParsingError: Could not parse key 'my.key': Custom message."

    >>> ParsingError(message="Custom message.", key="my.key", plain=True)
    "ParsingError"

    Attributes:
        message (str): More precise error message which describes the parsing error.
        key (str): Specific config key which caused the error.
        plain (bool): If plain error (empty error string) should be created.
    """

    def __init__(self, message: str = "", key: str = "", plain: bool = False) -> None:
        """Parsing Error class constructor method.

        Args:
            message (str): More precise error message which describes the parsing error.
            key (str): Specific config key which caused the error.
            plain (bool): If plain error (empty error string) should be created.
        """
        super().__init__()
        self.__plain = False
        if plain:
            self.__plain = True
            self.__message = ""
            self.__key = ""
        else:
            self.__message = message
            self.__key = key

    @property
    def message(self) -> Optional[str]:
        """str: More precise error message which describes the parsing error.

        Returns:
            message (str): More precise error message which describes the parsing error.
        """
        return self.__message

    @property
    def key(self) -> Optional[str]:
        """str: Specific config key which caused the error.

        Returns:
            key (str): Specific config key which caused the error.
        """
        return self.__key

    @property
    def plain(self) -> bool:
        """bool: True if plain error (empty error string) should be created.

        Returns:
            bool: True if plain error (empty error string) should be created.
        """
        return self.__plain

    def __str__(self) -> str:
        """Overwrite magic string method of the super class.

        Overrides the string method of `Exception` by additionally
        returning the key that could not be parsed as a message.

        Returns:
            str: Custom error message constructed with set attributes.
        """
        if self.plain:
            return ""
        if self.message and (not self.message.isspace()):
            if self.key and (not self.key.isspace()):
                return "Could not parse key '{}': {}".format(self.key, self.message)
            return "Could not parse: {}".format(self.message)
        if self.key and (not str(self.key).isspace()):
            return "Could not parse key '{}'.".format(self.key)
        return "Error occured while parsing."
