"""Deserializer for an enum."""

import enum
from typing import Any

import attr

from . import combinators, factories, iterator_utils
from .errors import (
    ErrorDisplayStrategy,
    InternalDeserializationError,
    InternalDeserializerFactoryError,
)
from .types import DeserializableType, Deserializer, Primitive, T


class EnumDeserializationError(InternalDeserializationError):
    """Raised when a primitive cannot be deserialized as any value of an enum."""


@attr.s(auto_attribs=True, frozen=True)
class _SingleEnumValueDeserializer(Deserializer[T]):
    enum_t: DeserializableType
    deserializer: Deserializer
    variant: Any

    def __call__(self, value: Primitive) -> T:
        v = self.deserializer(value)
        if v == self.variant.value:
            return self.variant
        raise EnumDeserializationError(
            v,
            self.variant,
            msg=f"value mismatch {repr(v)} - expected {repr(self.variant.value)}",
            display_strategy=ErrorDisplayStrategy.ALWAYS_DISPLAY,
        )


class EnumDeserializerFactoryError(InternalDeserializerFactoryError):
    """Raised when failing to create an enum deserializer."""


@attr.s(auto_attribs=True, frozen=True)
class EnumDeserializerFactory(factories.TypeDeserializerFactory):
    """Create deserializer for an enum type."""

    def create_deserializer(
        self,
        recurse_factory: factories.InternalDeserializerFactory,
        type_: DeserializableType,
    ) -> Deserializer[T]:
        """Create deserializer for the specified enum type."""
        if not (isinstance(type_, type) and issubclass(type_, enum.Enum)):
            raise EnumDeserializerFactoryError(type_, "not an enum type")

        deserializers, errors = iterator_utils.accumulate_errors_d(  # type: ignore[var-annotated]
            InternalDeserializerFactoryError,
            {  # type: ignore[var-annotated]
                f"variant <{variant.name}: {repr(variant.value)}>": (
                    lambda v: _SingleEnumValueDeserializer(
                        enum_t=type_,
                        deserializer=recurse_factory.create_type_deserializer(
                            type(v.value)
                        ),
                        variant=v,
                    ),
                    variant,
                )
                for variant in list(type_)
            },
        )
        if errors:
            raise EnumDeserializerFactoryError(
                type_, EnumDeserializerFactoryError.cannot_create_msg("enum"), errors,
            )
        return combinators.OneOfDeserializer(
            type_, deserializers, EnumDeserializationError
        )
