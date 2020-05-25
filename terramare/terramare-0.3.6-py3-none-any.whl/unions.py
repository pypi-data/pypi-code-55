"""Deserializer for a union of types."""

from typing import Union

import attr

from . import combinators, factories, iterator_utils, pretty_printer, type_utils
from .errors import InternalDeserializationError, InternalDeserializerFactoryError
from .types import DeserializableType, Deserializer, T


class UnionDeserializationError(InternalDeserializationError):
    """Raised when a primitive cannot be deserialized as any type in a union."""


class UnionDeserializerFactoryError(InternalDeserializerFactoryError):
    """Raised when failing to create a union deserializer."""


@attr.s(auto_attribs=True, frozen=True)
class UnionDeserializerFactory(factories.TypeDeserializerFactory):
    """Create deserializer for a union of several types."""

    def create_deserializer(
        self,
        recurse_factory: factories.InternalDeserializerFactory,
        type_: DeserializableType,
    ) -> Deserializer[T]:
        """Create a deserializer for the specified union type."""
        if not type_utils.get_base_of_generic_type(type_) == Union:
            raise UnionDeserializerFactoryError(type_, "not a union type")

        deserializers, errors = iterator_utils.accumulate_errors_d(
            InternalDeserializerFactoryError,
            {
                f"variant {pretty_printer.print_type_name(type_param)}": (
                    recurse_factory.create_type_deserializer,
                    type_param,
                )
                for type_param in type_utils.get_type_parameters(type_)
            },
        )
        if errors:
            raise UnionDeserializerFactoryError(
                type_, UnionDeserializerFactoryError.cannot_create_msg("union"), errors,
            )
        return combinators.OneOfDeserializer(
            type_, deserializers, UnionDeserializationError
        )
