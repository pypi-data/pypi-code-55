"""Deserializer for a newtype alias."""

import attr

from . import factories
from .errors import InternalDeserializationError, InternalDeserializerFactoryError
from .types import DeserializableType, Deserializer, Primitive, T


class NewTypeDeserializationError(InternalDeserializationError):
    """Raised when a primitive cannot be deserialized as a newtype."""


@attr.s(auto_attribs=True, frozen=True)
class NewTypeDeserializer(Deserializer[T]):
    """Deserializer for a newtype."""

    _newtype_t: DeserializableType
    _deserializer: Deserializer[T]

    def __call__(self, value: Primitive) -> T:
        """Deserialize a primitive as a newtype."""
        try:
            return self._deserializer(value)
        except InternalDeserializationError as e:
            raise NewTypeDeserializationError(
                value, self._newtype_t, cause=e,
            )


class NewTypeDeserializerFactoryError(InternalDeserializerFactoryError):
    """Raised when failing to create a newtype deserializer."""


@attr.s(auto_attribs=True, frozen=True)
class NewTypeDeserializerFactory(factories.TypeDeserializerFactory):
    """Create a newtype deserializer."""

    def create_deserializer(
        self,
        recurse_factory: factories.InternalDeserializerFactory,
        type_: DeserializableType,
    ) -> Deserializer[T]:
        """Create a deserializer for the specified newtype."""
        if not getattr(type_, "__qualname__", None) == "NewType.<locals>.new_type":
            raise NewTypeDeserializerFactoryError(
                type_, "not a newtype",
            )
        try:
            return NewTypeDeserializer(
                type_,
                recurse_factory.create_type_deserializer(
                    type_.__supertype__  # type: ignore[union-attr]
                ),
            )
        except InternalDeserializerFactoryError as e:
            raise NewTypeDeserializerFactoryError(
                type_, NewTypeDeserializerFactoryError.cannot_create_msg("newtype"), e
            )
