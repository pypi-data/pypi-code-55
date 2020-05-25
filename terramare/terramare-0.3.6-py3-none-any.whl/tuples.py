"""Deserializer for a (typed) tuple."""

import itertools
from typing import Optional, Tuple, cast

import attr

from . import combinators, factories, iterator_utils, type_utils
from .errors import InternalDeserializationError, InternalDeserializerFactoryError
from .types import DeserializableType, Deserializer, T


class TupleDeserializationError(InternalDeserializationError):
    """Raised when a primitive cannot be deserialized as a tuple."""


class TupleDeserializerFactoryError(InternalDeserializerFactoryError):
    """Raised when failing to create a tuple deserializer."""


@attr.s(auto_attribs=True, frozen=True)
class TupleDeserializerFactory(factories.TypeDeserializerFactory):
    """Create deserializer for a tuple type."""

    def create_deserializer(
        self,
        recurse_factory: factories.InternalDeserializerFactory,
        type_: DeserializableType,
    ) -> Deserializer[T]:
        """Create a deserializer for the specified tuple type."""
        if not type_utils.get_base_of_generic_type(type_) == Tuple:
            raise TupleDeserializerFactoryError(type_, "not a tuple type")

        type_params = type_utils.get_type_parameters(type_)
        deserializers, errors = iterator_utils.accumulate_errors_l(
            InternalDeserializerFactoryError,
            zip(
                itertools.repeat(recurse_factory.create_type_deserializer),
                (tp for tp in type_params if tp != Ellipsis),
            ),
        )
        if errors:
            raise TupleDeserializerFactoryError(
                type_,
                TupleDeserializerFactoryError.cannot_create_msg("tuple"),
                {f"at index {i}": e for i, e in errors},
            )

        var_deserializer: Optional[Deserializer] = None
        if type_params and type_params[-1] == Ellipsis:
            _, var_deserializer = deserializers[-1]
            required_deserializers = deserializers[:-1]
        else:
            required_deserializers = deserializers

        return combinators.SequenceDeserializer(
            type_,
            recurse_factory.create_type_deserializer(list),
            [ds for _, ds in required_deserializers],
            [],
            var_deserializer,
            lambda _, v: cast(T, tuple(v)),
            TupleDeserializationError,
        )
