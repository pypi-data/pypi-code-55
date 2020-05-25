"""Deserializer for a dictionary."""

from typing import Dict, List, Mapping, MutableMapping, Set, cast

import attr

from . import combinators, factories, iterator_utils, pretty_printer, type_utils
from .errors import InternalDeserializationError, InternalDeserializerFactoryError
from .types import DeserializableType, Deserializer, T


class DictDeserializationError(InternalDeserializationError):
    """Raised when a primitive cannot be deserialized as a dict."""


class DictDeserializerFactoryError(InternalDeserializerFactoryError):
    """Raised when failing to create a dict deserializer."""


@attr.s(auto_attribs=True, frozen=True)
class DictDeserializerFactory(factories.TypeDeserializerFactory):
    """Create deserializer for a dictionary of values of the same type."""

    def create_deserializer(
        self,
        recurse_factory: factories.InternalDeserializerFactory,
        type_: DeserializableType,
    ) -> Deserializer[T]:
        """Create a deserializer for the specified dictionary type."""
        if type_utils.get_base_of_generic_type(type_) not in {
            Dict,
            Mapping,
            MutableMapping,
        }:
            raise DictDeserializerFactoryError(type_, "not a dict type")

        key_type, value_type = type_utils.get_type_parameters(type_)
        if not _is_hashable(key_type):
            raise DictDeserializerFactoryError(
                type_,
                "unhashable key type: '{}'".format(
                    pretty_printer.print_type_name(key_type)
                ),
            )

        deserializers, errors = iterator_utils.accumulate_errors_d(
            InternalDeserializerFactoryError,
            {
                "key": (recurse_factory.create_type_deserializer, key_type),
                "value": (recurse_factory.create_type_deserializer, value_type),
            },
        )
        if errors:
            raise DictDeserializerFactoryError(
                type_,
                DictDeserializerFactoryError.cannot_create_msg("dict"),
                {f"{k} type": e for k, e in errors.items()},
            )
        return combinators.MappingDeserializer(
            type_,
            recurse_factory.create_type_deserializer(dict),
            deserializers["key"],
            {},
            {},
            deserializers["value"],
            lambda _, v: cast(T, dict(v)),
            DictDeserializationError,
        )


def _is_hashable(type_: DeserializableType) -> bool:
    return (
        "__hash__" in dir(type_)
        and "__eq__" in dir(type_)
        and type_utils.get_base_of_generic_type(type_) not in {Dict, List, Set}
    )
