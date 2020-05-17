"""Terramare-specific metadata for attrs classes."""

import abc
from typing import Any, Dict, Generic, Mapping, Optional

import attr

from . import factories
from .keyed_deserializer import K, S
from .types import DeserializableType, Deserializer, T

ATTRS_METADATA_KEY = f"__{__package__}"

AttrsMetadata = Dict[str, Any]


class MemberMetadata(abc.ABC, Generic[T]):
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


@attr.s(auto_attribs=True, frozen=True)
class KeyedMetadata(Generic[K, S, T], MemberMetadata[T]):
    """Deserialize a field into a type determined by the value of a key."""

    key_field: K
    mapping: Mapping[S, DeserializableType]
    target_t: Optional[DeserializableType]

    def deserialize_with(
        self, recurse_factory: factories.InternalDeserializerFactory,
    ) -> Optional[Deserializer[T]]:
        """Deserialize this member with the returned deserializer."""

        return recurse_factory.create_keyed_deserializer(
            self.key_field, self.mapping, self.target_t
        )


def get_metadata(type_: DeserializableType, name: str) -> MemberMetadata[T]:
    """Retrieve terramare-specific metadata for a class member variable."""
    if not hasattr(type_, "__attrs_attrs__"):
        return MemberMetadata()
    attrs = type_.__attrs_attrs__  # type: ignore[union-attr]
    return {a.name: a.metadata for a in attrs}[name].get(
        ATTRS_METADATA_KEY, MemberMetadata()
    )


def keyed(
    key_field: K,
    mapping: Mapping[S, DeserializableType],
    *,
    target_t: Optional[DeserializableType] = None,
) -> AttrsMetadata:
    """
    Deserialize into a type determined by the value of a key in the input dictionary.

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
    >>> @attr.s(auto_attribs=True)
    ... class IntVariant:
    ...     integer: int
    >>>
    >>> @attr.s(auto_attribs=True)
    ... class StrVariant:
    ...     string: str
    >>>
    >>>
    >>> @attr.s(auto_attribs=True)
    ... class Container:
    ...     value: Any = attr.ib(metadata=keyed("type", {0: IntVariant, 1: StrVariant}))
    >>>
    >>> terramare.deserialize_into(Container, {"value": {"type": 0, "integer": 0}})
    Container(value=IntVariant(integer=0))
    >>>
    >>> terramare.deserialize_into(Container, {"value": {"type": 1, "string": "string"}})
    Container(value=StrVariant(string='string'))

    """
    return _make_metadata(KeyedMetadata(key_field, mapping, target_t))


def _make_metadata(metadata: MemberMetadata) -> AttrsMetadata:
    return {ATTRS_METADATA_KEY: metadata}
