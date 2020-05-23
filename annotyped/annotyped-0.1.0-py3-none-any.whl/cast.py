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
}

# CAST_ERROR is a tuple of errors to catch for both param conversion attempts
# and return value conversion attempts. Used to remove duplicate error code below.
CAST_ERROR = (TypeError, ValueError)


def cast(**user_converters):
    '''cast creates a casting decorator with custom converters.
    This will attempt to convert any params and return values that have
    type annotations.

    Cast loads the global default converters and will overwrite them if the user
    has specified one with the same name.
    '''

    converters = DEFAULT_CONVERTERS
    converters.update(user_converters)

    def caster(func):
        # Inspect the signature and params for later lookup.
        sig = inspect.signature(func)
        prms = dict(sig.parameters.items())

        def decorate(*args, **kwargs):
            # Iterate over the accumulated args / kwargs and attempt to find their annotation converter, 
            # if one was found then attempt to convert the value.
            for name, value, param in accumulate(args, kwargs, prms):
                annotation = getattr(param.annotation, '__name__', param.annotation)

                converter = converters.get(annotation, None)
                if converter is None:
                    raise errors.MissingConverter(f"Param '{name}' requires type converter '{param.annotation}' but none were found")

                try:
                    value = converter(value)
                    kwargs[name] = value
                except CAST_ERROR:
                    raise errors.TypeCast(f"Param '{name}' could not convert to '{param.annotation}' from '{type(value)}': {value}")

            # Store the return value for now, we may need it.
            return_value = func(**kwargs)

            if sig.return_annotation == sig.empty:
                return return_value

            # Attempt to find a converter for and convert the return value
            converter = converters.get(sig.return_annotation, None)
            if converter is None:
                    raise errors.MissingConverter(f"Return value requires type converter '{param.annotation}' but none were found")

            try:
                return_value = converter(return_value)
            except CAST_ERROR:
                raise errors.TypeCast(f"Return value could not convert to '{param.annotation}' from '{type(return_value)}': {return_value}")

            return return_value
        return decorate
    return caster
