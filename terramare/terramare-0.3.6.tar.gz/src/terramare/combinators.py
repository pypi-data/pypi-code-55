"""Deserializer combinators."""

import itertools
from functools import partial
from typing import (
    Any,
    Callable,
    Generic,
    Hashable,
    Mapping,
    Optional,
    Sequence,
    TypeVar,
)

import attr
from typing_extensions import Protocol

from . import exception_formatter, iterator_utils
from .errors import ErrorDisplayStrategy, InternalDeserializationError
from .types import DeserializableType, Deserializer, Primitive, T


class _ErrorT(Protocol):
    def __call__(
        self,
        value: Primitive,
        target_t: DeserializableType,
        cause: exception_formatter.Cause[Exception],
        display_strategy: ErrorDisplayStrategy = ErrorDisplayStrategy.DEFAULT,
    ) -> InternalDeserializationError:  # pragma: no cover
        ...


@attr.s(auto_attribs=True, frozen=True)
class OneOfDeserializer(Deserializer[T]):
    """Deserialize with one of the supplied set of deserializers."""

    _target_t: DeserializableType
    _deserializers: Mapping[str, Deserializer]
    _error_t: _ErrorT

    def __call__(self, value: Primitive) -> T:
        """Deserialize a primitive by trying several deserializers in turn."""
        errors_ = {}
        for desc, ds in self._deserializers.items():
            try:
                return ds(value)
            except InternalDeserializationError as e:
                errors_[desc] = e
        raise self._error_t(
            value,
            self._target_t,
            cause=errors_ if len(errors_) > 1 else list(errors_.values())[0],
        )


@attr.s(auto_attribs=True, frozen=True)
class SequenceDeserializer(Deserializer[T]):
    """Deserialize a list using a sequence of deserializers."""

    _target_t: DeserializableType
    _untyped_list_deserializer: Deserializer[list]

    _required_elt_deserializers: Sequence[Deserializer]
    _optional_elt_deserializers: Sequence[Deserializer]
    _var_elt_deserializer: Optional[Deserializer]

    _construct_fn: Callable[[Primitive, Sequence[Any]], T]
    _error_t: _ErrorT

    def __call__(self, value: Primitive) -> T:
        """
        Deserialize a primitive using a sequence of deserializers.

        Each list element is matched with a deserializer based on its index.
        From the start of the list:
        - Elements are first matched with the required element deserializers,
          raising an error if there are too few elements;
        - Additional elements are then matched with the optional element
          deserializers;
        - Any remaining elements are matched with the var element deserializer,
          if supplied. Otherwise, an error is raised.
        """
        try:
            elts = self._untyped_list_deserializer(value)
        except InternalDeserializationError as e:
            raise self._error_t(
                value,
                self._target_t,
                cause=e,
                display_strategy=ErrorDisplayStrategy.ALWAYS_COLLAPSE,
            )

        try:
            zipped = (
                partial(  # type: ignore[operator]
                    iterator_utils.zip_strict_extra, self._var_elt_deserializer
                )
                if self._var_elt_deserializer
                else iterator_utils.zip_strict
            )(self._required_elt_deserializers, self._optional_elt_deserializers, elts,)
        except ValueError as e:
            raise self._error_t(value, self._target_t, cause=e)

        results, errors = iterator_utils.accumulate_errors_l(
            InternalDeserializationError, iter(zipped),
        )

        if errors:
            raise self._error_t(
                value, self._target_t, cause={f"at index {i}": e for i, e in errors},
            )
        return self._construct_fn(value, [v for _, v in results])


K = TypeVar("K", bound=Hashable)


@attr.s(auto_attribs=True, frozen=True)
class MappingDeserializer(Generic[K, T], Deserializer[T]):
    """Deserialize a dictionary using a mapping of keys to deserializers."""

    _target_t: DeserializableType
    _untyped_dict_deserializer: Deserializer[dict]

    _key_deserializer: Deserializer[K]
    _required_elt_deserializers: Mapping[K, Deserializer]
    _optional_elt_deserializers: Mapping[K, Deserializer]
    _var_elt_deserializer: Optional[Deserializer]

    _construct_fn: Callable[[Primitive, Mapping[K, Any]], T]
    _error_t: _ErrorT

    def __call__(self, value: Primitive) -> T:
        """
        Deserialize a primitive using a mapping of keys to deserializers.

        Each dictionary element is matched with a deserializer based on its key.
        An error will be raised if the dictionary is missing keys corresponding
        to required element deserializers.
        An error will also be raised if the dictionary contains keys that do not
        correspond to either required or optional element deserializers, and
        no var element deserializer is supplied.
        """
        try:
            elts = self._untyped_dict_deserializer(value)
        except InternalDeserializationError as e:
            raise self._error_t(
                value,
                self._target_t,
                cause=e,
                display_strategy=ErrorDisplayStrategy.ALWAYS_COLLAPSE,
            )

        keys, key_errors = iterator_utils.accumulate_errors_l(
            InternalDeserializationError,
            zip(itertools.repeat(self._key_deserializer), elts.keys()),
        )

        if key_errors:
            raise self._error_t(
                value, self._target_t, cause={f"at index {i}": e for i, e in key_errors}
            )

        elts = dict(zip((k for _, k in keys), elts.values()))

        try:
            zipped = (
                partial(  # type: ignore[operator]
                    iterator_utils.zip_strict_dict_extra, self._var_elt_deserializer
                )
                if self._var_elt_deserializer
                else iterator_utils.zip_strict_dict
            )(self._required_elt_deserializers, self._optional_elt_deserializers, elts,)
        except ValueError as e:
            raise self._error_t(value, self._target_t, cause=e)

        results, errors = iterator_utils.accumulate_errors_d(
            InternalDeserializationError, zipped
        )

        if errors:
            raise self._error_t(
                value,
                self._target_t,
                cause={f'at key "{k}"': e for k, e in errors.items()},
            )
        return self._construct_fn(value, results)
