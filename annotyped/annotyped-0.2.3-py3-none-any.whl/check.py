import inspect

from . import errors
from .accumulate import accumulate


def checker(equality):
    def check(func):

        sig = inspect.signature(func)
        prms = dict(sig.parameters.items())

        def decorate(*args, **kwargs):
            for name, value, param in accumulate(args, kwargs, prms):

                try:
                    eq = bool(equality(value, param.annotation))
                except Exception as err:
                    raise errors.TypeCheck(f"Param '{name}' failed in equality check for '{param.annotation}', given value '{value}'")

                if not eq:
                    raise errors.TypeCheck(f"Param '{name}' does not satisfy '{param.annotation}', given value '{value}'")

            return_value = func(*args, **kwargs)

            if sig.return_annotation == sig.empty:
                return return_value

            try:
                eq = bool(equality(return_value, sig.return_annotation))
            except Exception as err:
                raise errors.TypeCheck(f"Return value failed in equality check for '{sig.return_annotation}', given value '{return_value}'")

            if not eq:
                raise errors.TypeCheck(f"Return value does not satisfy '{sig.return_annotation}', given value '{return_value}'")

            return return_value

        return decorate
    return check


cast = checker(lambda value, annotation: annotation(value))
instance = checker(isinstance)
