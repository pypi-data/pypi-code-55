"""
Contains functions to create an instance of a config class and to load the
configuration files.
"""
import ast
import dataclasses
import logging
from configparser import ConfigParser
from typing import Tuple, Type, Dict, get_origin, Union, get_args, Any, Optional

from autoconfiguration.exceptions.data_type_errors import (
    UnableToConvertConfigValueToTypeError,
)
from autoconfiguration.helpers.modify_class import (
    make_singleton,
    add_contains_getattribute_getitem_get_methods_to,
    freeze_class,
    MISSING_VALUE,
)

LOG = logging.getLogger(__name__)


class _HasDefaultValue:
    """Used to check if a field has a default value."""


HAS_DEFAULT_VALUE = _HasDefaultValue()


def create_config_instance(
    config_class: Type[Any], config_files: Tuple[str, ...]
) -> Any:
    """
    Creates an instance of the passed config class with the values of the passed
    config files. The data types of the config class and the types of its attributes
    are validated. The values of the config files are converted to the specified data
    types.

    :param config_class: The class that should be initialized with the values of the
        config files. This class and the types of its attributes have to be dataclasses.
    :param config_files: The files containing the config values for the config class
    :return: The initialized instance of the config class with the values of the
        config files
    """
    config = ConfigParser()
    config.read(config_files)

    sections = {
        _valid_name(section): {
            _valid_name(key): value for key, value in config[section].items()
        }
        for section in config.sections()
    }

    LOG.debug("Generated config with sections: %s", sections)

    return _create_config_class_instance(config_class, sections)


def _valid_name(name: str) -> str:
    """
    Returns a valid name for a Python variable. Used to ensure that all fields of the
    config class are valid Python names.

    :param name: The name that should be converted to a valid Python name
    :return: The valid name
    """
    return name.replace("-", "_")


def _create_config_class_instance(
    config_class: Type[Any], sections: Dict[str, Dict[str, str]]
) -> Any:
    """
    Creates and returns the instance of the passed config class.

    :param config_class: The config class
    :param sections: The sections of the config files containing the values for the
        instance of the config class
    :return: The instance of the config class
    """
    instances = {}
    for field in dataclasses.fields(config_class):
        instance = _get_value_of_field(field, sections)
        if instance is HAS_DEFAULT_VALUE:
            continue

        add_contains_getattribute_getitem_get_methods_to(field.type)
        instances[field.name] = instance

    make_singleton(config_class)

    instance = config_class(**instances)
    setattr(instance, "_sections", sections)

    add_contains_getattribute_getitem_get_methods_to(config_class)
    freeze_class(instance)

    return instance


def _get_value_of_field(
    field: dataclasses.Field, sections: Dict[str, Dict[str, str]]
) -> Any:
    """
    Returns the value of a field of the config class. The value of the field is
    returned if the passed sections contain the field. None is returned if the field
    is Optional and has no default value. HAS_DEFAULT_VALUE is returned if the field
    is not Optional. Otherwise MISSING_VALUE is returned.

    :param field: The field of the config class
    :param sections: The sections of the config files containing the values for the
        instance of the config class
    :return: Section value, None, HAS_DEFAULT_VALUE or MISSING_VALUE depending on the
        field and the sections
    """
    if field.name in sections:
        values = _get_values_of_sub_fields(field, sections)
        instance = field.type(**values)
        freeze_class(instance)
        return instance

    if _is_optional(field.type) and not _has_default(field):
        return None

    return HAS_DEFAULT_VALUE if _has_default(field) else MISSING_VALUE


def _get_values_of_sub_fields(
    field: dataclasses.Field, sections: Dict[str, Dict[str, str]]
) -> Dict[str, Any]:
    """
    Returns the values of all fields of the passed field. The value of the field is
    used if the passed sections contain the field. None is used if the field
    is Optional and has no default value. The default value is used if the field
    is not Optional. Otherwise MISSING_VALUE is used.

    :param field: The field containing all sub fields
    :param sections: The sections of the config files containing the values for the
        instance of the config class
    :return: Values of all fields of the passed field
    """
    values = {}
    for sub_field in dataclasses.fields(field.type):
        if sub_field.name in sections[field.name]:
            value = _convert_to_correct_type(
                sections[field.name][sub_field.name], sub_field.type
            )
        elif _is_optional(sub_field.type) and not _has_default(sub_field):
            value = None
        elif _has_default(sub_field):
            continue
        else:
            value = MISSING_VALUE

        values[sub_field.name] = value
    return values


def _convert_to_correct_type(value: str, expected_type: Type[Any]) -> Any:
    """
    Tries to convert the passed value to the passed expected type.

    :param value: The value that should be converted to the passed type
    :param expected_type: The expected type for the value
    :return: The converted value
    """
    origin_type = get_origin(expected_type)
    if expected_type is str or (
        origin_type is Union and get_args(expected_type)[0] is str
    ):
        return value

    result = ast.literal_eval(value)
    if (origin_type is None and not isinstance(result, expected_type)) or (
        origin_type is not None and not isinstance(result, origin_type)
    ):
        raise UnableToConvertConfigValueToTypeError(value, expected_type)

    return result


def _is_optional(annotation_type: Type[Any]) -> bool:
    """
    Checks if the passed type is Optional.

    :param annotation_type: The type that should be checked
    :return: True if the type is Optional
    """
    return (
        annotation_type is Optional
        or get_origin(annotation_type) is Union
        and get_args(annotation_type)[-1] is type(None)
    )


def _has_default(field: dataclasses.Field) -> bool:
    """
    Checks if the passed field has a default value.

    :param field: The field that should be checked
    :return: True if the field has a default value
    """
    return (
        field.default is not dataclasses.MISSING
        or getattr(field, "default_factory") is not dataclasses.MISSING
    )
