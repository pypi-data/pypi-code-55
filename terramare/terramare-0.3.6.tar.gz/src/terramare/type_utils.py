"""Common utility functions for dealing with generic types."""

import contextlib
from collections import abc
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
    Type,
)

from typing_extensions import Literal, TypedDict

from .types import DeserializableType, LiteralMeta, TypedDictMeta


def get_base_of_generic_type(type_: DeserializableType) -> Optional[Type]:
    """Return the generic type of which a type_ is an instance."""
    type_ = _normalize_type(type_)
    for attribute in ("__origin__", "__class__"):
        if hasattr(type_, attribute):
            return _coalesce_type(getattr(type_, attribute))
    return None  # pragma: no cover


def get_type_parameters(from_type: DeserializableType) -> List[Type]:
    """Extract the type parameters from a parametrized type."""

    def extract_type_parameters(type_: DeserializableType) -> List[Type]:
        type_ = _normalize_type(type_)
        with contextlib.suppress(AttributeError):
            if type_.__args__ is not None:  # type: ignore[union-attr]
                return list(type_.__args__)  # type: ignore[union-attr]
        with contextlib.suppress(AttributeError):
            if type_.__values__ is not None:  # type: ignore[union-attr]
                return list(type_.__values__)  # type: ignore[union-attr]
        return []

    from_type = _normalize_type(from_type)
    type_params = extract_type_parameters(_normalize_type(from_type))
    if getattr(from_type, "__class__", None) is LiteralMeta:
        # Special-case Literal types, as Literal[()] != Literal[]
        return type_params
    return type_params if type_params != [()] else []


def _normalize_type(type_: Any) -> Any:
    type_ = _coalesce_type(type_)
    try:
        return {
            Callable: Callable[..., Any],
            Dict: Dict[str, Any],
            FrozenSet: FrozenSet[Any],
            Iterable: Iterable[Any],
            Iterator: Iterator[Any],
            List: List[Any],
            Mapping: Mapping[str, Any],
            MutableMapping: Mapping[str, Any],
            MutableSequence: MutableSequence[Any],
            Sequence: Sequence[Any],
            Set: Set[Any],
            Tuple: Tuple[Any, ...],
        }[type_]
    except (KeyError, TypeError):
        return type_


def _coalesce_type(type_: Any) -> Any:
    try:
        return {
            abc.Callable: Callable,
            abc.Iterable: Iterable,
            abc.Iterator: Iterator,
            abc.Mapping: Mapping,
            abc.MutableMapping: MutableMapping,
            abc.MutableSequence: MutableSequence,
            abc.Sequence: Sequence,
            abc.Set: Set,
            dict: Dict,
            frozenset: FrozenSet,
            list: List,
            LiteralMeta: Literal,
            set: Set,
            tuple: Tuple,
            TypedDictMeta: TypedDict,
        }[type_]
    except (KeyError, TypeError):
        return type_
