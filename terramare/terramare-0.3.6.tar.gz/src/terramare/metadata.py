"""Terramare-specific metadata for attrs classes."""

import abc
from typing import Generic, Mapping, Optional

import attr

from . import factories
from .errors import InternalDeserializerFactoryError
from .keyed_deserializer import K, S
from .types import DeserializableType, Deserializer, T

_METADATA_KEY = f"__{__package__}"


class InternalMetadata(abc.ABC, Generic[T]):
    """Terramare-specific class member metadata."""

    def deserialize_with(
        self,
        recurse_factory: factories.InternalDeserializerFactory,  # pylint: disable=unused-argument
    ) -> Optional[Deserializer[T]]:
        """
        Deserialize this member with the returned deserializer.

        Returning None causes the member to be deserialized by type as normal.
        """
        return None


def get_member_metadata(type_: DeserializableType, name: str) -> InternalMetadata[T]:
    """Retrieve terramare-specific metadata for a class member variable."""
    if not hasattr(type_, "__attrs_attrs__"):
        return InternalMetadata()
    attrs = type_.__attrs_attrs__  # type: ignore[union-attr]
    return {a.name: a.metadata for a in attrs}[name].get(
        _METADATA_KEY, InternalMetadata()
    )


Metadata = Mapping[str, InternalMetadata]


class MetadataDeserializerFactoryError(InternalDeserializerFactoryError):
    """Raised when failing to create a deserializer from metadata."""


@attr.s(auto_attribs=True, frozen=True)
class MetadataDeserializerFactory(factories.TypeDeserializerFactory):
    """Create a deserializer from metadata."""

    metadata: Mapping[DeserializableType, Metadata]

    def create_deserializer(
        self,
        recurse_factory: factories.InternalDeserializerFactory,
        type_: DeserializableType,
    ) -> Deserializer[T]:
        """Create a deserializer for the specified type."""
        try:
            # Don't attept to look up non-hashable types.
            hash(type_)
        except TypeError:
            raise MetadataDeserializerFactoryError(type_, "no metadata present")
        if type_ not in self.metadata:
            raise MetadataDeserializerFactoryError(type_, "no metadata present")
        try:
            ds = extract_metadata(self.metadata[type_]).deserialize_with(
                recurse_factory
            )
        except InternalDeserializerFactoryError as e:
            raise MetadataDeserializerFactoryError(
                type_, "encountered metadata error", e
            )
        if not ds:
            raise MetadataDeserializerFactoryError(
                type_, "no deserializer created using metadata"
            )
        return ds


def make_metadata(metadata: InternalMetadata) -> Metadata:
    """Create externally-facing metadata."""
    return {_METADATA_KEY: metadata}


def extract_metadata(metadata: Metadata) -> InternalMetadata:
    """Extract from externally-facing metadata."""
    return metadata.get(_METADATA_KEY, InternalMetadata())


@attr.s(auto_attribs=True, frozen=True)
class KeyedMetadata(Generic[K, S, T], InternalMetadata[T]):
    """Deserialize a field into a type determined by the value of a key."""

    key_field: K
    mapping: Mapping[S, DeserializableType]
    target_t: Optional[DeserializableType] = None

    def deserialize_with(
        self, recurse_factory: factories.InternalDeserializerFactory,
    ) -> Optional[Deserializer[T]]:
        """Deserialize this member with the returned deserializer."""

        return recurse_factory.create_keyed_deserializer(
            self.key_field, self.mapping, self.target_t
        )


def keyed(
    key_field: K,
    mapping: Mapping[S, DeserializableType],
    *,
    target_t: Optional[DeserializableType] = None,
) -> Metadata:
    """
    Metadata to deserialize into a type determined by the value of a key in the input dictionary.

    :param `key_field`: Use the value of this field to determine the target type.
    :param `mapping`: Mapping of possible key values to target types.
    :param `target_t`: Override the automatically deduced target type to provide more
        useful error messages. The deduced target type will be a union of the types
        appearing in :python:`mapping`; it may be more informative to set target_t to
        a common base class, for example.

    Example usage:

    >>> from typing import Any
    >>> import attr
    >>> import terramare
    >>>
    >>> class Variant:
    ...     pass
    >>>
    >>> @attr.s(auto_attribs=True)
    ... class IntVariant(Variant):
    ...     integer: int
    >>>
    >>> @attr.s(auto_attribs=True)
    ... class StrVariant(Variant):
    ...     string: str
    >>>
    >>> terramare.deserialize_into(
    ...     Variant,
    ...     {"type": 0, "integer": 1},
    ...     _experimental_metadata={
    ...         Variant: keyed("type", {0: IntVariant, 1: StrVariant}, target_t=Variant)
    ...     },
    ... )
    IntVariant(integer=1)
    >>>
    >>> terramare.deserialize_into(
    ...     Variant,
    ...     {"type": 1, "string": "string"},
    ...     _experimental_metadata={
    ...         Variant: keyed("type", {0: IntVariant, 1: StrVariant}, target_t=Variant)
    ...     },
    ... )
    StrVariant(string='string')

    """
    return make_metadata(KeyedMetadata(key_field, mapping, target_t))
