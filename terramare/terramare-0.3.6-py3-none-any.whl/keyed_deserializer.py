"""Deserializer implementing dynamic dispatch based on the value of a dictionary key."""

from typing import Any, Generic, Hashable, Mapping, NoReturn, Optional, TypeVar, Union

import attr

from . import exception_formatter, factories, iterator_utils
from .errors import (
    ErrorDisplayStrategy,
    InternalDeserializationError,
    InternalDeserializerFactoryError,
)
from .pretty_printer import print_type_name
from .types import DeserializableType, Deserializer, Primitive, T


class KeyedDeserializerFactoryError(InternalDeserializerFactoryError):
    """Raised when attempting to create a KeyedDeserializer fails."""


K = TypeVar("K", bound=Hashable)
S = TypeVar("S", bound=Hashable)


@attr.s(auto_attribs=True, frozen=True)
class KeyedDeserializerFactory(factories.KeyedDeserializerFactory):
    """Create a keyed deserializer."""

    def create_deserializer(
        self,
        recurse_factory: factories.InternalDeserializerFactory,
        key_field: K,
        mapping: Mapping[S, DeserializableType],
        target_t: Optional[DeserializableType],
    ) -> "KeyedDeserializer[K, S, T]":
        """
        Create a KeyDeserializer from a specified key field and mapping of key values to types.
        """
        if not mapping:
            raise KeyedDeserializerFactoryError(
                type(None), "cannot create keyed deserializer with empty mapping"
            )
        if target_t is None:
            target_t = Union[tuple(mapping.values())]
        key_field_type = type(key_field)
        try:
            dict_deserializer = recurse_factory.create_type_deserializer(
                Mapping[key_field_type, Any]  # type: ignore[misc, valid-type]
            )
        except InternalDeserializerFactoryError as e:
            raise KeyedDeserializerFactoryError(
                target_t,
                "cannot create keyed deserializer with key field type: "
                f"{print_type_name(key_field_type)}",
                cause=e,
            )

        key_type = Union[tuple(type(k) for k in mapping.keys())]  # type: ignore[misc]
        try:
            key_deserializer = recurse_factory.create_type_deserializer(key_type)
        except InternalDeserializerFactoryError as e:
            raise KeyedDeserializerFactoryError(
                target_t,
                "cannot create keyed deserializer with mapping key type "
                f"{print_type_name(key_type)}",
                cause=e,
            )

        deserializers, errors = iterator_utils.accumulate_errors_d(
            InternalDeserializerFactoryError,
            {
                k: (recurse_factory.create_type_deserializer, v)
                for k, v in mapping.items()
            },
        )
        if errors:
            raise KeyedDeserializerFactoryError(
                target_t,
                KeyedDeserializerFactoryError.cannot_create_msg("keyed"),
                {f"key '{k}'": e for k, e in errors.items()},
            )
        return KeyedDeserializer(
            target_t, dict_deserializer, key_field, key_deserializer, deserializers,
        )


class KeyedDeserializationError(InternalDeserializationError):
    """Raised when a KeyedDeserializer fails."""


@attr.s(auto_attribs=True, frozen=True)
class KeyedDeserializer(Generic[K, S, T], Deserializer[T]):
    """Deserialize a dictionary based on the value of one of its keys."""

    _target_t: DeserializableType
    _dict_deserializer: Deserializer[Mapping[K, Any]]

    _key_field: K
    _key_deserializer: Deserializer[S]

    _remainder_deserializers: Mapping[S, Deserializer[T]]

    def __call__(self, value: Primitive) -> T:
        """Deserialize a dictionary based on the value of one of its keys."""

        def raise_(
            cause: Optional[exception_formatter.Cause[Exception]],
            msg: Optional[str] = None,
        ) -> NoReturn:
            raise KeyedDeserializationError(
                value,
                self._target_t,
                cause=cause,
                display_strategy=ErrorDisplayStrategy.ALWAYS_DISPLAY,
                msg=msg,
            )

        try:
            elts = self._dict_deserializer(value)
        except InternalDeserializationError as e:
            raise_(e)
        if self._key_field not in elts:
            raise_(Exception(f"missing key: '{self._key_field}'"))
        try:
            key = self._key_deserializer(elts[self._key_field])
        except InternalDeserializationError as e:
            raise_(e)
        if key not in self._remainder_deserializers:
            raise_(
                Exception(
                    f"unexpected value for key '{self._key_field}' ('{key}'), "
                    f"expected one of '{set(self._remainder_deserializers.keys())}'"
                )
            )
        try:
            return self._remainder_deserializers[key](
                {k: v for k, v in elts.items() if k != self._key_field}
            )
        except InternalDeserializationError as e:
            raise_(
                e.cause,
                msg=f"{e._get_msg()} (variant '{key}' of '{print_type_name(self._target_t)}')",
            )
