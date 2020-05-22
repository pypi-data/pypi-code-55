"""Contains helper functions to modify classes that overwrite specific methods."""
import dataclasses
from typing import Type, Dict, Any

from autoconfiguration.exceptions.config_class_errors import ConfigClassAttributeError


class _MissingValue:
    """Used to check if a value of a field of the config class is missing."""


MISSING_VALUE = _MissingValue()


class Constants:
    """Used to save the instance of the config class."""

    config_instance = None


def make_singleton(obj: Type[Any]) -> None:
    """
    Modifies the passed type to ensure that only one instance of the type can be
    created.

    :param obj: The type that should be a singleton
    """

    def __new__(cls: Type[Any], *args: Any, **kwargs: Any) -> Any:
        # pylint: disable=unused-argument
        if not hasattr(Constants, "config_instance") or not Constants.config_instance:
            Constants.config_instance = object.__new__(cls)
        return Constants.config_instance

    setattr(obj, "__new__", __new__)


def add_contains_getattribute_getitem_get_methods_to(
    cls: Type[Any], available_attributes: Dict[str, Any]
) -> None:
    """
    Adds implementations to the passed instance of a class for the following methods:

    - __contains__: Checks if _sections of the instance contains the passed str
    - __getattribute__: Used to raise an exception if no value was specified for an
        attribute
    - __getitem__: Returns the value by the passed key of _sections of the instance
    - get: Returns the value by the passed key of _sections of the instance. Has a
        second parameter for a default value (default: None)

    :param cls: The class to which the methods should be added
    :param available_attributes: A dict containing available attributes of the class
    """
    setattr(cls, "__contains__", lambda self, item: item in available_attributes)
    setattr(cls, "__getitem__", lambda self, item: self.__dict__[item])
    setattr(
        cls,
        "get",
        lambda self, section_name, default_value=None: self[section_name]
        if section_name in self
        else default_value,
    )

    def __getattribute__(self: Any, item: str) -> Any:
        value = object.__getattribute__(self, item)
        if value == MISSING_VALUE:
            raise ConfigClassAttributeError(item)
        return value

    setattr(cls, "__getattribute__", __getattribute__)


def freeze_class(cls: Type[Any]) -> None:
    """
    Freezes a class by adding implementations for the following methods:
    - __delattr__: Raises a FrozenInstanceError
    - __setattr__: Raises a FrozenInstanceError

    :param cls: The class that should be frozen
    """

    def __delattr__(self: Any, name: str) -> None:
        raise dataclasses.FrozenInstanceError()

    setattr(cls, "__delattr__", __delattr__)

    def __setattr__(self: Any, name: str, value: Any) -> None:
        raise dataclasses.FrozenInstanceError()

    setattr(cls, "__setattr__", __setattr__)
