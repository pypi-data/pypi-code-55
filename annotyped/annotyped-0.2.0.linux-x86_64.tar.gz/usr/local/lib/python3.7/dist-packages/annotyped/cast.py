import inspect

from . import errors
from .accumulate import accumulate


# DEFAULT_CONVERTERS contains all usable default converters.
# You can overwrite any of these if you pass a new converter to @typer.cast()
# eg: @typer.cast(str=custom_str_func)
DEFAULT_CONVERTERS = {
    'str': str,
    'int': int,
    'float': float,
    'bool': bool,
    'list': list,
    'tuple': tuple,
    'dict': dict,
}

# CAST_ERROR is a tuple of errors to catch for both param conversion attempts
# and return value conversion attempts. Used to remove duplicate error code below.
CAST_ERROR = (TypeError, ValueError)


def cast(func):

    # Inspect the signature and params for later lookup.
    sig = inspect.signature(func)
    prms = dict(sig.parameters.items())

    def decorate(*args, **kwargs):
        for name, value, param in accumulate(args, kwargs, prms):
            try:
                value = param.annotation(value)
                kwargs[name] = value
            except CAST_ERROR as e:
                raise errors.TypeCast(f"Param '{name}' could not convert to '{param.annotation}' from '{type(value)}': {e}")

        # Store the return value for now, we may need it.
        return_value = func(**kwargs)

        if sig.return_annotation == sig.empty:
            return return_value

        try:
            return_value = sig.return_annotation(return_value)
        except CAST_ERROR as e:
            raise errors.TypeCast(f"Return value could not convert to '{param.annotation}' from '{type(return_value)}': {e}")

        return return_value
    return decorate
