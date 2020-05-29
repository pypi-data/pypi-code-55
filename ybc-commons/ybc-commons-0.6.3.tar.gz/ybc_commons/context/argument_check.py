import inspect
from functools import wraps
from inspect import Parameter
from typing import Callable

from ybc_exception import ParameterTypeError
from ybc_exception import ParameterValueError


def check_argument_types(fn, parameters, arguments):
    illegal_arguments = [
        (name, value)
        for name, value in arguments
        if (name in parameters
            and parameters[name].annotation is not Parameter.empty
            and not isinstance(value, parameters[name].annotation))
    ]

    if illegal_arguments:
        raise ParameterTypeError(
            fn.__name__,
            '、'.join("'%s'" % k for k, v in illegal_arguments))


def check_argument_values(fn, predicates, arguments):
    illegal_arguments = [
        (name, value)
        for name, value in arguments
        if name in predicates and not predicates[name](value)
    ]

    if illegal_arguments:
        raise ParameterValueError(
            fn.__name__,
            '、'.join("'%s'" % k for k, v in illegal_arguments))


class ArgumentsChecker:
    def __init__(self, predicates):
        self.predicates = predicates

    def __call__(self, fn: Callable):
        sig = inspect.signature(fn)

        @wraps(fn)
        def wrapper(*args, **kwargs):
            arguments = sig.bind(*args, **kwargs).arguments.items()

            check_argument_types(fn, sig.parameters, arguments)
            check_argument_values(fn, self.predicates, arguments)

            return fn(*args, **kwargs)

        return wrapper
