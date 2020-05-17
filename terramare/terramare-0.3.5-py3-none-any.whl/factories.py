"""Factories used to create deserializers."""

import abc
from typing import Dict, Generic, Hashable, Mapping, Optional, TypeVar

import attr
from typing_extensions import final

from .errors import ErrorDisplayStrategy, InternalDeserializerFactoryError
from .pretty_printer import print_type_name
from .types import DeserializableType, Deserializer, T

K = TypeVar("K", bound=Hashable)
S = TypeVar("S", bound=Hashable)


@attr.s(auto_attribs=True, frozen=True)
class InternalDeserializerFactory(abc.ABC, Generic[K, S, T]):
    """Internal interface for deserializer factory classes."""

    _type_factory: "TypeDeserializerFactory[T]"
    _keyed_factory: "KeyedDeserializerFactory[K, S, T]"

    @final
    def create_type_deserializer(self, type_: DeserializableType) -> Deserializer[T]:
        """Create a deserializer for the given type."""
        return self._type_factory.create_deserializer(self, type_)

    @final
    def create_keyed_deserializer(
        self,
        key_field: K,
        mapping: Mapping[S, DeserializableType],
        target_t: Optional[DeserializableType],
    ) -> Deserializer[T]:
        """
        Create a keyed dictionary deserializer.

        This deserializer produces values of a type that depends on the value of
        a particular key.
        """
        return self._keyed_factory.create_deserializer(
            self, key_field, mapping, target_t
        )


class TypeDeserializerFactory(abc.ABC, Generic[T]):
    """
    Interface for factory classes creating a deserializer for a given type.
    """

    @abc.abstractmethod
    def create_deserializer(
        self, recurse_factory: "InternalDeserializerFactory", type_: DeserializableType
    ) -> Deserializer[T]:
        """
        Create a deserializer for the given type, recursing with the supplied factory.
        """


class KeyedDeserializerFactory(abc.ABC, Generic[K, S, T]):
    """Interface for factory classes creating a keyed deserializer."""

    @abc.abstractmethod
    def create_deserializer(
        self,
        recurse_factory: "InternalDeserializerFactory",
        key_field: K,
        mapping: Mapping[S, DeserializableType],
        target_t: Optional[DeserializableType],
    ) -> Deserializer[T]:
        """Create a keyed dictionary deserializer."""


@attr.s(auto_attribs=True, frozen=True)
class SequenceTypeDeserializerFactory(TypeDeserializerFactory):
    """Type deserializer factory that tries a sequence of factories in turn."""

    _factories: Mapping[str, TypeDeserializerFactory]

    def create_deserializer(
        self, recurse_factory: InternalDeserializerFactory, type_: DeserializableType
    ) -> Deserializer[T]:
        """Create a deserializer for the specified type."""
        errors_: Dict[str, InternalDeserializerFactoryError] = {}
        for desc, deserializer_factory in self._factories.items():
            try:
                return deserializer_factory.create_deserializer(recurse_factory, type_)
            except InternalDeserializerFactoryError as e:
                errors_[desc] = e
        raise InternalDeserializerFactoryError(
            type_,
            "cannot create deserializer for type '{}'".format(print_type_name(type_)),
            errors_,
            display_strategy=ErrorDisplayStrategy.ALWAYS_DISPLAY,
        )
