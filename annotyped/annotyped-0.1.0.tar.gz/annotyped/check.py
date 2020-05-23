import inspect

from . import errors
from .accumulate import accumulate


def check(func):
    '''check creates a typecheck decorator which performs type checks
    on any function arguments or return types with type annotations.
    '''

    sig = inspect.signature(func)
    prms = dict(sig.parameters.items())

    def decorate(*args, **kwargs):
        for name, value, param in accumulate(args, kwargs, prms):

            if not isinstance(value, param.annotation):
                raise errors.TypeCheck(f"Param '{name}' requires type '{param.annotation}', found '{type(value)}'")

        return_value = func(**kwargs)
        if sig.return_annotation != sig.empty and not isinstance(return_value, sig.return_annotation):
            raise errors.TypeCheck(f"Return value requires type '{sig.return_annotation}', found '{type(return_value)}'")

        return return_value

    return decorate
