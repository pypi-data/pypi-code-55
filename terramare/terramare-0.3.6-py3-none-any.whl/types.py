"""Common types and re-exports."""

import abc
from typing import Any, Callable, Generic, Type, TypeVar, Union

from typing_extensions import Literal

# pylint: disable=unused-import
try:  # pragma: no cover
    from typing import _TypedDictMeta  # type: ignore[attr-defined]

except ImportError:
    from typing_extensions import (  # type: ignore[attr-defined]  # noqa: F401
        _TypedDictMeta,
    )

TypedDictMeta = _TypedDictMeta

try:
    from typing_extensions import _Literal  # type: ignore[attr-defined]

    LiteralMeta = _Literal
except ImportError:  # pragma: no cover
    LiteralMeta = Literal

T = TypeVar("T")


NotNonePrimitive = Union[str, int, float, dict, list, bool]
Primitive = Union[NotNonePrimitive, None]

DeserializableType = Union[Type[Any], Callable[..., Any]]


class Deserializer(abc.ABC, Generic[T]):
    """Interface implemented by deserializers."""

    @abc.abstractmethod
    def __call__(self, value: Primitive) -> T:
        """Deserialize a value."""


class TerramareError(Exception):
    """Base class for exceptions raised by terramare."""
