import inspect

from . import errors
from .accumulate import accumulate


def cast(func):

    # Inspect the signature and params for later lookup.
    sig = inspect.signature(func)
    prms = dict(sig.parameters.items())

    def decorate(*args, **kwargs):
        args = list(args)
        for index, (name, value, param) in enumerate(accumulate(args, kwargs, prms)):
            try:
                value = param.annotation(value)
            except Exception as err:
                raise errors.TypeCast(f"Param '{name}' could not convert to '{param.annotation}' from '{type(value)}': {err}") from err

            if index < len(args):
                args[index] = value
            else:
                kwargs[name] = value

        # Store the return value for now, we may need it.
        return_value = func(*args, **kwargs)

        if sig.return_annotation == sig.empty:
            return return_value

        try:
            return_value = sig.return_annotation(return_value)
        except Exception as err:
            raise errors.TypeCast(f"Return value could not convert to '{param.annotation}' from '{type(return_value)}': {err}") from err

        return return_value
    return decorate
