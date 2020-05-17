"""Deserializers for primitive types."""

from typing import Any, Callable, Dict, FrozenSet, List, NoReturn, Type, TypeVar, cast

import attr

from . import factories, pretty_printer, type_utils
from .errors import (
    ErrorDisplayStrategy,
    InternalDeserializationError,
    InternalDeserializerFactoryError,
)
from .types import DeserializableType, Deserializer, NotNonePrimitive, Primitive, T


class PrimitiveDeserializationError(InternalDeserializationError):
    """Raised when deserializing a primitive fails due to a type mismatch."""


class _PrimitiveMismatchError(Exception):
    pass


@attr.s(auto_attribs=True, frozen=True)
class PrimitiveDeserializer(Deserializer[T]):
    """Deserializer for a primitive type."""

    _primitive_t: DeserializableType
    _deserializer: Callable[[Primitive], object]

    def __call__(self, value: Primitive) -> T:
        """Deserialize a primitive value."""
        try:
            return cast(T, self._deserializer(value))
        except _PrimitiveMismatchError as e:
            raise PrimitiveDeserializationError(
                value,
                self._primitive_t,
                msg=str(e),
                display_strategy=ErrorDisplayStrategy.ALWAYS_DISPLAY,
            )


class PrimitiveDeserializerFactoryError(InternalDeserializerFactoryError):
    """Raised when failing to create a primitive deserializer."""


@attr.s(auto_attribs=True, frozen=True)
class PrimitiveDeserializerFactory(factories.TypeDeserializerFactory):
    """Create deserializer for a primitive type."""

    coerce_strings: bool
    true_strings: FrozenSet[str]
    false_strings: FrozenSet[str]

    def create_deserializer(
        self,
        _recurse_factory: factories.InternalDeserializerFactory,
        type_: DeserializableType,
    ) -> Deserializer[T]:
        """Create a deserializer for the specified primitive type."""
        if type_ in cast(
            List[type], type_utils.get_type_parameters(Primitive)  # type: ignore[misc]
        ) + [
            Any,  # type: ignore[list-item]
            bool,
        ]:
            if self.coerce_strings:
                deserialize_int = _deserialize_int_from_string
                deserialize_float = _deserialize_float_from_string

                def inner(value: Primitive) -> bool:
                    return _deserialize_bool_from_string(
                        self.true_strings, self.false_strings, value
                    )

                deserialize_bool = inner
            else:
                deserialize_int = _deserialize_int
                deserialize_float = _deserialize_float
                deserialize_bool = _deserialize_bool

            return PrimitiveDeserializer(
                type_,
                {
                    Any: lambda x: x,
                    str: _deserialize_str,
                    int: deserialize_int,
                    float: deserialize_float,
                    dict: _deserialize_dict,
                    list: _deserialize_list,
                    bool: deserialize_bool,
                    type(None): _deserialize_none,
                }[type_],
            )
        raise PrimitiveDeserializerFactoryError(type_, "not a primitive type")


def _deserialize_str(value: Primitive) -> str:
    """Deserialise a primitive as a string."""
    return _to_primitive(value, str)


def _deserialize_int(value: Primitive) -> int:
    """
    Deserialise a primitive as an int.

    Union[bool, int] will be collapsed into int, so special-case bools.
    TODO - deserialize with best match
    """
    if isinstance(value, bool):
        return value
    return _to_primitive(value, int)


def _deserialize_int_from_string(value: Primitive) -> int:
    value = _assert_string(value, int).lower()
    try:
        return int(value)
    except ValueError:
        raise _PrimitiveMismatchError(f"could not coerce value '{value}' to type 'int'")


def _deserialize_float(value: Primitive) -> float:
    """
    Deserialize a primitive as a float.

    Both ints and floats are acceptable input values.
    """
    try:
        return _to_primitive(value, int)
    except _PrimitiveMismatchError:
        return _to_primitive(value, float)


def _deserialize_float_from_string(value: Primitive) -> float:
    value = _assert_string(value, float).lower()
    try:
        return float(value)
    except ValueError:
        raise _PrimitiveMismatchError(
            f"could not coerce value '{value}' to type 'float'"
        )


def _deserialize_dict(value: Primitive) -> Dict[str, Any]:
    """Deserialize a primitive as an untyped dict."""
    return _to_primitive(value, dict)


def _deserialize_list(value: Primitive) -> List[Any]:
    """Deserialize a primitive as an untyped list."""
    return _to_primitive(value, list)


def _deserialize_bool(value: Primitive) -> bool:
    """Deserialize a primitive as a bool."""
    return _to_primitive(value, bool)


def _deserialize_bool_from_string(
    true_values: FrozenSet[str], false_values: FrozenSet[str], value: Primitive
) -> bool:
    """Deserialize a string as a bool."""
    value = _assert_string(value, bool).lower()
    if value in true_values:
        return True
    elif value in false_values:
        return False
    else:
        raise _PrimitiveMismatchError(
            "could not coerce value '{}' to type 'bool' (expected one of {})".format(
                value, set(true_values | false_values)
            )
        )


def _deserialize_none(value: Primitive) -> None:
    """Deserialize a primitive as None."""
    if value is None:
        return value
    _raise_type_mismatch(value, type(None))


S = TypeVar("S", bound=NotNonePrimitive)


def _to_primitive(value: Primitive, primitive_t: Type[S]) -> S:
    if isinstance(value, primitive_t):
        return cast(S, primitive_t(value))
    _raise_type_mismatch(value, primitive_t)


def _assert_string(value: Primitive, type_: type) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, bool) or isinstance(value, int) or isinstance(value, float):
        raise _PrimitiveMismatchError(
            "type mismatch - value '{}' has type '{}', "
            "expected 'str' (as coerce_strings is set)".format(
                pretty_printer.print_primitive(value),
                pretty_printer.print_type_name(type(value)),
            )
        )
    _raise_type_mismatch(value, type_)


def _raise_type_mismatch(value: Primitive, type_: type) -> NoReturn:
    raise _PrimitiveMismatchError(
        "type mismatch - value '{}' has type '{}', expected '{}'".format(
            pretty_printer.print_primitive(value),
            pretty_printer.print_type_name(type(value)),
            pretty_printer.print_type_name(type_),
        )
    )
