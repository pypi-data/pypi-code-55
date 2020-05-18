import inspect
from typing import Callable

from starlette.responses import JSONResponse

from spell.serving.exceptions import InvalidPredictor


class BasePredictor:
    def health(self):
        return JSONResponse({"status": "ok"})

    @classmethod
    def validate(cls) -> None:
        for func_name in ("__init__", "predict"):
            func = cls._get_func_or_raise(func_name)
            args = inspect.getfullargspec(func).args
            if len(args) != 2:
                raise InvalidPredictor(
                    f"Invalid signature for {func_name} function. Expected 2 arguments, "
                    f"but found {len(args)}."
                )
        health = getattr(cls, "health", None)
        if health:
            health_args = inspect.getfullargspec(health).args
            if len(health_args) != 1:
                raise InvalidPredictor(
                    "Invalid signature for health function. Expected 1 argument, "
                    f"but found {len(health_args)}."
                )

    @classmethod
    def _get_func_or_raise(cls, func_name: str) -> Callable:
        func = getattr(cls, func_name, None)
        if not func:
            raise InvalidPredictor(f'Required function "{func_name}" is not defined')
        if not callable(func):
            raise InvalidPredictor(f'"{func_name}" is defined, but is not a function')
        return func
