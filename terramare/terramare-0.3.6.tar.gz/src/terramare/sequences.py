"""Deserializer for a generalized homogenous sequence."""

from typing import FrozenSet, Iterable, Iterator, List, MutableSequence, Sequence, Set

import attr

from . import combinators, factories, pretty_printer, type_utils
from .errors import InternalDeserializationError, InternalDeserializerFactoryError
from .types import DeserializableType, Deserializer, T


class HomogenousSequenceDeserializationError(InternalDeserializationError):
    """Raised when failing to deserialize a (typed) generalized sequence."""


class HomogeneousSequenceDeserializerFactoryError(InternalDeserializerFactoryError):
    """Raised when failing to create a (typed) generalized sequence deserializer."""


@attr.s(auto_attribs=True, frozen=True)
class HomogeneousSequenceDeserializerFactory(factories.TypeDeserializerFactory):
    """Create deserializer for a generalized homogenous sequence type."""

    def create_deserializer(
        self,
        recurse_factory: factories.InternalDeserializerFactory,
        type_: DeserializableType,
    ) -> Deserializer[T]:
        """Create a deserializer for the specified homogeneous sequence type."""
        sequence_constructors = {
            FrozenSet: set,
            Iterable: list,
            Iterator: iter,
            List: list,
            MutableSequence: list,
            Sequence: list,
            Set: set,
        }
        base = type_utils.get_base_of_generic_type(type_)
        if base not in sequence_constructors:
            raise HomogeneousSequenceDeserializerFactoryError(
                type_, "not a sequence type"
            )

        [value_type] = type_utils.get_type_parameters(type_)
        try:
            deserializer = recurse_factory.create_type_deserializer(value_type)
        except InternalDeserializerFactoryError as e:
            raise HomogeneousSequenceDeserializerFactoryError(
                type_,
                HomogeneousSequenceDeserializerFactoryError.cannot_create_msg(
                    pretty_printer.print_type_name(base)
                ),
                e,
            )

        return combinators.SequenceDeserializer(
            type_,
            recurse_factory.create_type_deserializer(list),
            [],
            [],
            deserializer,
            lambda _, v: sequence_constructors[base](v),  # type: ignore[index, operator]
            HomogenousSequenceDeserializationError,
        )
