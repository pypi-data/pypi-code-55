"""Automatically deserialize complex objects from simple Python types."""

from typing import (
    Callable,
    Dict,
    FrozenSet,
    Generic,
    Iterable,
    Iterator,
    List,
    Mapping,
    MutableMapping,
    MutableSequence,
    Optional,
    Sequence,
    Set,
    Tuple,
    Type,
)

import attr
from typing_extensions import TypedDict

from . import (
    classes,
    dicts,
    enums,
    errors,
    factories,
    keyed_deserializer,
    literals,
    metadata,
    newtypes,
    primitives,
    sequences,
    tuples,
    type_utils,
    typed_dicts,
    unions,
)
from .types import DeserializableType, Deserializer, Primitive, T

DEFAULT_TRUE_STRINGS = frozenset({"yes", "on", "true", "1"})
DEFAULT_FALSE_STRINGS = frozenset({"no", "off", "false", "0"})
DEFAULT_EXCEPTION_TYPES_TO_HANDLE: FrozenSet[Type[Exception]] = frozenset()


def deserialize_into(
    type_: DeserializableType,
    value: Primitive,
    *,
    coerce_strings: bool = False,
    true_strings: FrozenSet[str] = DEFAULT_TRUE_STRINGS,
    false_strings: FrozenSet[str] = DEFAULT_FALSE_STRINGS,
    handle_exception_types: FrozenSet[
        Type[Exception]
    ] = DEFAULT_EXCEPTION_TYPES_TO_HANDLE,
    handle_reentrancy: bool = False,
    _experimental_metadata: Optional[
        Mapping[DeserializableType, metadata.Metadata]
    ] = None
) -> T:
    """
    Deserialize a primitive as a value of the specified type.

    :param `type_`: Deserialize into this type.
    :param `value`: Primitive value to attempt to deserialize.
    :param `coerce_strings`: If set, attempt to convert :python:`str` values to
        :python:`bool`, :python:`int`, or :python:`float` where the latter are required.
        For example:

        >>> deserialize_into(int, "1")
        Traceback (most recent call last):
            ...
        terramare.errors.DeserializationError: ...
        >>> deserialize_into(int, "1", coerce_strings=True)
        1

        Note that setting this option will cause :python:`terramare` to reject
        non-string primitives where a :python:`bool`, :python:`int`, or :python:`float`
        is required.
        For example:

        >>> deserialize_into(int, 1)
        1
        >>> deserialize_into(int, 1, coerce_strings=True)
        Traceback (most recent call last):
            ...
        terramare.errors.DeserializationError: ...

        This option defaults to :python:`False`.

    :param `true_strings`: Set of strings to convert to :python:`True` when convering a
        :python:`str` value to a :python:`bool`. Case is ignored.

        This value defaults to :python:`{"yes", "on", "true", "1"}`.

    :param `false_strings`: Set of strings to convert to :python:`False` when convering
        a :python:`str` value to a :python:`bool`. Case is ignored.

        This value defaults to :python:`{"no", "off", "false", "0"}`.

    :param `handle_exception_types`: Set of additional exception types that
        :python:`terramare` should catch and handle rather than propogating.

        Generally this will still result in an exception being raised. However, it will
        be a :python:`terramare` exception containing additional context.

        This option is useful when the deserialization target provides some form of
        additional validation. For example:

        >>> from typing import Union
        >>> import attr
        >>>
        >>> @attr.s
        ... class Paint:
        ...    color: str = attr.ib(validator=attr.validators.in_(["red", "blue"]))

        When no exception types are provided, context is lost when deserializing into a
        single type:

        >>> deserialize_into(Paint, "green")
        Traceback (most recent call last):
        ...
        ValueError: 'color' must be in ['red', 'blue'] (got 'green')

        When the exception type is provided, that context is preserved:

        >>> deserialize_into(Paint, "green", handle_exception_types={ValueError})
        Traceback (most recent call last):
        ...
        terramare.errors.DeserializationError: cannot read value '"green"' into 'Paint': 'color' must be in ['red', 'blue'] (got 'green')

        The exception is when the deserialization target is a union type, where
        :python:`terramare` will continue to try further union variants - as it would
        when encountering a deserialization failure.

        When no exception types are provided, :python:`terramare` cannot try further
        union variants if one fails due to a validation error:

        >>> deserialize_into(Union[Paint, str], "green")
        Traceback (most recent call last):
        ...
        ValueError: 'color' must be in ['red', 'blue'] (got 'green')

        When the exception type is provided, :python:`terramare` continues and
        successfully deserializes into a later variant.

        >>> deserialize_into(Union[Paint, str], "green", handle_exception_types={ValueError})
        'green'

    :param `handle_reentrancy`: This option determines :python:`terramare`'s behaviour
        when deserializing into a class or function that itself invokes
        :python:`terramare`:

        - If set to :python:`True`, :python:`terramare` will catch and handle exceptions
          raised by calls back into :python:`terramare`. This setting is useful when
          deserializing in several stages, common when the type of some later member
          depends on the value of an earlier one.

        - If set to :python:`False`, :python:`terramare` will not catch these exceptions,
          propogating them as normal. This is a safer setting when the expectation is
          that deserializion will not have multiple stages, that is, when
          :python:`terramare` exceptions raised by re-entrancy are unexpected and should
          be propogated.

        For example:

        >>> from typing import Any, List, Union
        >>> import attr
        >>>
        >>> @attr.s(auto_attribs=True)
        ... class PythonConfig:
        ...    pip_path: str
        >>>
        >>> @attr.s(auto_attribs=True)
        ... class BashConfig:
        ...     set_options: List[str]
        >>>
        >>> def load_language_config(
        ...     language: str,
        ...     **remainder: Any
        ... ) -> "Union[PythonConfig, BashConfig]":
        ...     if language == "python":
        ...         return deserialize_into(PythonConfig, remainder)
        ...     elif language == "bash":
        ...         return deserialize_into(PythonConfig, remainder)
        ...     else:
        ...         raise NotImplementedError
        >>>
        >>> data = {"language": "python", "set_options": "xe"}

        When handling re-entrancy is disabled, the :python:`load_language_context` is
        lost:

        >>> deserialize_into(load_language_config, data)
        Traceback (most recent call last):
        ...
        terramare.errors.DeserializationError: cannot read value ... into 'PythonConfig':
        ...

        When handling re-entrancy is enabled, that context is preserved:

        >>> deserialize_into(load_language_config, data, handle_reentrancy=True)
        Traceback (most recent call last):
        ...
        terramare.errors.DeserializationError: cannot read value ... into 'load_language_config':
        ...

    :param _experimental_metadata: See :ref:`experimental-features-metadata`.

    :raises terramare.DeserializerFactoryError: if a deserializer for :python:`type_`
        cannot be created.
    :raises terramare.DeserializationError: if the deserializer fails to deserialize a
        value of :python:`type_` from :python:`value`.
    """  # noqa: F401, E501
    return create_deserializer_factory(
        coerce_strings=coerce_strings,
        true_strings=true_strings,
        false_strings=false_strings,
        handle_exception_types=handle_exception_types,
        handle_reentrancy=handle_reentrancy,
        _experimental_metadata=_experimental_metadata,
    ).deserialize_into(type_, value)


@attr.s(auto_attribs=True, frozen=True)
class ExternalDeserializerFactory(Generic[T]):
    """External interface for a factory class used to create Deserializers."""

    _factory: factories.InternalDeserializerFactory

    def deserialize_into(self, type_: DeserializableType, value: Primitive) -> T:
        """Deserialize a primitive as a value of the specified type."""
        try:
            return self.create_type_deserializer(type_)(value)
        except errors.InternalDeserializationError as e:  # pragma: no cover
            raise errors.DeserializationError(**vars(e))

    def create_type_deserializer(self, type_: DeserializableType) -> Deserializer[T]:
        """Create a deserializer for the specified type."""
        try:
            return self._factory.create_type_deserializer(type_)
        except errors.InternalDeserializerFactoryError as e:  # pragma: no cover
            raise errors.DeserializerFactoryError(**vars(e))


def create_deserializer_factory(
    coerce_strings: bool = False,
    true_strings: FrozenSet[str] = DEFAULT_TRUE_STRINGS,
    false_strings: FrozenSet[str] = DEFAULT_FALSE_STRINGS,
    handle_exception_types: FrozenSet[
        Type[Exception]
    ] = DEFAULT_EXCEPTION_TYPES_TO_HANDLE,
    handle_reentrancy: bool = False,
    _experimental_metadata: Optional[
        Mapping[DeserializableType, metadata.Metadata]
    ] = None,
) -> ExternalDeserializerFactory:
    """Create a DeserializerFactory using sensible defaults which may be overridden."""

    def class_deserializer_enable_if(t: DeserializableType) -> bool:
        # Explicitly disable class deserializer creation for typing types.
        # They are technically callable, so the class deserializer factory will
        # create a deserializer, but this will always raise if called.
        return type_utils.get_base_of_generic_type(t) not in {
            Callable,
            Dict,
            FrozenSet,
            Iterable,
            Iterator,
            List,
            Mapping,
            MutableMapping,
            MutableSequence,
            Sequence,
            Set,
            Tuple,
            TypedDict,
        }

    return ExternalDeserializerFactory(
        factories.InternalDeserializerFactory(
            factories.SequenceTypeDeserializerFactory(
                {
                    "metadata": metadata.MetadataDeserializerFactory(
                        _experimental_metadata if _experimental_metadata else {}
                    ),
                    "newtype": newtypes.NewTypeDeserializerFactory(),
                    "primitive": primitives.PrimitiveDeserializerFactory(
                        coerce_strings=coerce_strings,
                        true_strings=frozenset(s.lower() for s in true_strings),
                        false_strings=frozenset(s.lower() for s in false_strings),
                    ),
                    "literal": literals.LiteralDeserializerFactory(),
                    "enum": enums.EnumDeserializerFactory(),
                    "union": unions.UnionDeserializerFactory(),
                    "tuple": tuples.TupleDeserializerFactory(),
                    "sequences": sequences.HomogeneousSequenceDeserializerFactory(),
                    "typeddict": typed_dicts.TypedDictDeserializerFactory(),
                    "dict": dicts.DictDeserializerFactory(),
                    "class": classes.ClassDeserializerFactory(
                        enable_if=class_deserializer_enable_if,
                        handle_exception_ts=handle_exception_types
                        | frozenset(
                            {errors.DeserializationError} if handle_reentrancy else {}
                        ),
                    ),
                }
            ),
            keyed_deserializer.KeyedDeserializerFactory(),
        )
    )
