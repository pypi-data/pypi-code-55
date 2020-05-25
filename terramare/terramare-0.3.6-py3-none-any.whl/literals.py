"""Deserializer for a literal."""

from functools import partial
from typing import Any

import attr
from typing_extensions import Literal

from . import combinators, factories, iterator_utils, type_utils
from .errors import (
    ErrorDisplayStrategy,
    InternalDeserializationError,
    InternalDeserializerFactoryError,
)
from .types import DeserializableType, Deserializer, Primitive, T


class LiteralDeserializationError(InternalDeserializationError):
    """Raised when a primitive cannot be deserialized as a literal."""


@attr.s(auto_attribs=True, frozen=True)
class _SingleLiteralDeserializer(Deserializer[T]):
    deserializer: Deserializer
    value: Any

    def __call__(self, value: Primitive) -> T:
        v = self.deserializer(value)
        if v == self.value:
            return v
        raise LiteralDeserializationError(
            value,
            Literal[self.value],
            msg="value mismatch - expected '{}', got '{}'".format(self.value, v),
        )


class LiteralDeserializerFactoryError(InternalDeserializerFactoryError):
    """Raised when failing to create a literal deserializer."""


@attr.s(auto_attribs=True, frozen=True)
class LiteralDeserializerFactory(factories.TypeDeserializerFactory):
    """Create deserializer for a literal type."""

    def create_deserializer(
        self,
        recurse_factory: factories.InternalDeserializerFactory,
        type_: DeserializableType,
    ) -> Deserializer[T]:
        """Create a deserializer for the specified literal type."""
        if not type_utils.get_base_of_generic_type(type_) == Literal:
            raise LiteralDeserializerFactoryError(type_, "not a literal type")

        deserializers, errors = iterator_utils.accumulate_errors_d(  # type: ignore[var-annotated]
            InternalDeserializerFactoryError,
            {
                f"variant {type_param}": (
                    lambda l: _SingleLiteralDeserializer(
                        deserializer=recurse_factory.create_type_deserializer(
                            _get_literal_t(l)
                        ),
                        value=l,
                    ),
                    type_param,
                )
                for type_param in type_utils.get_type_parameters(type_)
            },
        )
        if errors:
            raise LiteralDeserializerFactoryError(
                type_,
                LiteralDeserializerFactoryError.cannot_create_msg("literal"),
                errors,
            )
        return combinators.OneOfDeserializer(
            type_,
            deserializers,
            partial(
                LiteralDeserializationError,
                display_strategy=ErrorDisplayStrategy.ALWAYS_DISPLAY,
            ),
        )


def _get_literal_t(type_: type) -> type:
    if type_utils.get_base_of_generic_type(type_) == Literal:
        return type_
    return type(type_)
