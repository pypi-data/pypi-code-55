"""Deserializer for a TypedDict."""

from functools import partial
from typing import Any, Mapping, cast

import attr
from typing_extensions import TypedDict

from . import combinators, factories, iterator_utils, type_utils
from .errors import (
    ErrorDisplayStrategy,
    InternalDeserializationError,
    InternalDeserializerFactoryError,
)
from .types import DeserializableType, Deserializer, Primitive, T


class TypedDictDeserializationError(InternalDeserializationError):
    """Raised when a primitive cannot be deserialized as a TypedDict."""


class TypedDictDeserializerFactoryError(InternalDeserializerFactoryError):
    """Raised when failing to create a TypedDict deserializer."""


@attr.s(auto_attribs=True, frozen=True)
class TypedDictDeserializerFactory(factories.TypeDeserializerFactory):
    """Create deserializer for a TypedDict."""

    def create_deserializer(
        self,
        recurse_factory: factories.InternalDeserializerFactory,
        type_: DeserializableType,
    ) -> Deserializer[T]:
        """Create a deserializer for the specified TypedDict type."""
        if type_utils.get_base_of_generic_type(type_) != TypedDict:
            raise TypedDictDeserializerFactoryError(type_, "not a TypedDict type")

        deserializers, errors = iterator_utils.accumulate_errors_d(
            InternalDeserializerFactoryError,
            {
                field_name: (recurse_factory.create_type_deserializer, field_type)
                for field_name, field_type in type_.__annotations__.items()
            },
        )

        def construct_fn(_value: Primitive, args: Mapping[str, Any]) -> T:
            return cast(T, args)

        if errors:
            raise TypedDictDeserializerFactoryError(
                type_,
                TypedDictDeserializerFactoryError.cannot_create_msg("TypedDict"),
                {f'field "{k}""': e for k, e in errors.items()},
            )
        return combinators.MappingDeserializer(
            type_,
            recurse_factory.create_type_deserializer(dict),
            recurse_factory.create_type_deserializer(str),
            deserializers,
            {},
            None,
            construct_fn,
            partial(
                TypedDictDeserializationError,
                display_strategy=ErrorDisplayStrategy.EAGERLY_COLLAPSE,
            ),
        )
