"""This module contains helper classes and functions for raising and handling errors."""

from typing import Type, TypeVar

_NotTypeErrorClass = TypeVar("_NotTypeErrorClass")


def noftc(identifier: str, etype: Type[_NotTypeErrorClass]) -> TypeError:
    """Create and return a TypeError with preset 'not of type' error message.

    Args:
        identifier (str): Identifier name which does not have the correct type.
        etype (Type[CLASS]): Expected class for the object named by the identifier.

    Returns:
        TypeError: Error with preset 'not of type' error message.
    """
    return noft(identifier, etype.__name__)


def noft(identifier: str, etype: str) -> TypeError:
    """Create and return a TypeError with preset 'not of type' error message.

    Args:
        identifier (str): Identifier name which does not have the correct type.
        etype (str): Expected class as string for the object named by the identifier.

    Returns:
        TypeError: Error with preset 'not of type' error message.
    """
    return TypeError(f"Given {identifier} is not of type {etype}.")
