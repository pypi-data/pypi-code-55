"""Pretty-printer for error messages."""

import contextlib
from typing import (
    Any,
    Callable,
    Dict,
    FrozenSet,
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
    Union,
)

from typing_extensions import Literal

from . import type_utils
from .types import DeserializableType, Primitive


def print_primitive(
    value: Primitive,
    short: bool = False,
    max_string_length: int = 16,
    max_dict_length: int = 3,
    max_list_length: int = 3,
) -> str:
    """Pretty-print a primitive value."""
    if isinstance(value, str):
        if len(value) > max_string_length:
            value = value[: max_string_length - 3] + "..."
        return '"{}"'.format(value)
    if not value:
        return str(value)
    if isinstance(value, dict):
        if short:
            return "{...}"
        else:
            elts = [
                print_primitive(k) + ": " + print_primitive(v, short=True)
                for k, v in value.items()
            ]
            if len(elts) > max_dict_length:
                elts = elts[: max_dict_length - 1] + ["..."]
            return "{{{}}}".format(", ".join(elts))
    if isinstance(value, list):
        if short:
            return "[...]" if value else "[]"
        else:
            elts = [print_primitive(v, short=True) for v in value]
            if len(elts) > max_list_length:
                elts = elts[: max_list_length - 1] + ["..."]
            return "[{}]".format(", ".join(elts))
    return str(value)


def print_type_name(type_: Any) -> str:
    """Return the best available user-facing name for a type."""
    overrides: Dict[DeserializableType, str] = {
        dict: "dict",
        frozenset: "frozenset",
        set: "set",
        list: "list",
        tuple: "tuple",
    }
    if type_ in overrides:
        return overrides[type_]
    base = type_utils.get_base_of_generic_type(type_)
    if base in {
        Callable,
        Dict,
        FrozenSet,
        Iterable,
        Iterator,
        Literal,
        List,
        Mapping,
        MutableMapping,
        MutableSequence,
        Optional,
        Sequence,
        Set,
        Tuple,
        Union,
    }:
        return (
            _get_type_name(base)
            + "["
            + ", ".join(
                [print_type_name(t) for t in type_utils.get_type_parameters(type_)]
            )
            + "]"
        )
    return _get_type_name(type_)


def _get_type_name(type_: Any) -> str:
    overrides = {Any: "Any", Ellipsis: "...", Literal: "Literal", Union: "Union"}
    if type_ in overrides:
        return overrides[type_]
    with contextlib.suppress(AttributeError):  # pragma: no cover TODO
        # pylint: disable=protected-access
        if type_._name is not None:
            return type_._name
    with contextlib.suppress(AttributeError):
        return type_.__name__
    with contextlib.suppress(AttributeError):
        return type_.__qualname__
    if hasattr(type_, "__origin__"):  # pragma: no cover TODO
        return _get_type_name(type_.__origin__)
    return str(type_)
