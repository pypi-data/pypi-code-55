from typing import Any, NoReturn

from .result import Result
from .unwrap_err import UnwrapErr


class Ok(Result):

    def __init__(self, value: Any = True):
        super().__init__(value)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Ok):
            return False

        return self.value == other.value

    def __hash__(self) -> int:
        return hash(self._value)

    def __ne__(self, other: Any) -> bool:
        if not isinstance(other, Ok):
            return True

        return self.value != other.value

    def __repr__(self) -> str:
        return f'Ok({repr(self._value)})'

    def __str__(self) -> str:
        return f'Ok: {str(self._value)}'

    def contains(self, other: Any) -> bool:
        return self._value == other

    def contains_err(self, other: Any) -> bool:
        return False

    def expect(self, message: str) -> Any:
        return self._value

    def is_err(self) -> bool:
        return False

    def is_ok(self) -> bool:
        return True

    def unwrap(self) -> Any:
        return self._value

    def unwrap_err(self) -> NoReturn:
        raise UnwrapErr("Can't unwrap error from an Ok result.")

    def unwrap_or(self, default: Any) -> Any:
        return self._value
