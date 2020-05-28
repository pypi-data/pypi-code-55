from typing import Any, Callable

from .err import Err
from .ok import Ok
from .result import Result


class Match:

    def __init__(self, result: Result):
        self._result: Result = result
        self._return: Any = None

    def ok(self, op: Callable, *op_args, **op_kwargs):
        if isinstance(self._result, Ok):
            if op:
                self._return = op(*op_args, **op_kwargs)

        return self

    def err(self, op: Callable, *op_args, **op_kwargs):
        if isinstance(self._result, Err):
            if op:
                self._return = op(*op_args, **op_kwargs)

        return self

    def collect(self) -> Any:
        return self._return
