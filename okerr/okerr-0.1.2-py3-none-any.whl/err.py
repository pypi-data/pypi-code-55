from typing import Any, NoReturn

from .result import Result
from .unwrap_err import UnwrapErr


class Err(Result):

    def __init__(self, value: Any = False):
        super().__init__(value)

    def __str__(self) -> str:
        return f'Err: {str(self._value)}'

    def __repr__(self) -> str:
        return f'Err({repr(self._value)})'

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Err):
            return False

        return self.value == other.value

    def __hash__(self) -> int:
        return hash(self._value)

    def __ne__(self, other: Any) -> bool:
        if not isinstance(other, Err):
            return True

        return self.value != other.value

    def contains(self, other: Any) -> bool:
        return False

    def contains_err(self, other: Any) -> bool:
        return self._value == other

    def expect(self, message: str) -> Any:
        raise Exception(message)

    def is_err(self) -> bool:
        return True

    def is_ok(self) -> bool:
        return False

    def unwrap(self) -> NoReturn:
        raise UnwrapErr("Can't unwrap from an Err result.")

    def unwrap_err(self) -> Any:
        return self._value

    def unwrap_or(self, default: Any) -> Any:
        return default
