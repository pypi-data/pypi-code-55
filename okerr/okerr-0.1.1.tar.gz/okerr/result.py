from abc import ABC, abstractmethod
from typing import Any


class Result(ABC):

    def __init__(self, value: Any = True):
        self._value = value

    @property
    def value(self) -> Any:
        return self._value

    @abstractmethod
    def contains(self, other: Any) -> bool:
        """Return True if the result is an Ok containing the given value."""

    @abstractmethod
    def contains_err(self, other: Any) -> bool:
        """Return True if the result is an Err containing the given value."""

    @abstractmethod
    def expect(self, message: str) -> Any:
        """Returns the contained Ok value."""

    @abstractmethod
    def is_err(self) -> bool:
        """Return if the response is an error"""

    @abstractmethod
    def is_ok(self) -> bool:
        """Return if the response is ok"""

    @abstractmethod
    def unwrap(self) -> Any:
        """Return the Ok value"""

    @abstractmethod
    def unwrap_err(self) -> Any:
        """Return the Err value"""

    @abstractmethod
    def unwrap_or(self, default: Any) -> Any:
        """Return the Ok value or default"""
