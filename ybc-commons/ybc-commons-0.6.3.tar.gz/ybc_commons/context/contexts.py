import sys

if sys.platform == 'skulpt':
    from .argument_check_for_skulpt import ArgumentsChecker

    def check_arguments(fn_or_predicates):
        if callable(fn_or_predicates):
            fn = fn_or_predicates
            return ArgumentsChecker({})(fn)
        else:
            predicates = fn_or_predicates
            return ArgumentsChecker(predicates)

else:
    from .argument_check import ArgumentsChecker
    from functools import wraps
    from typing import Callable

    def check_arguments(fn_or_predicates):
        if isinstance(fn_or_predicates, Callable):
            fn = fn_or_predicates
            return ArgumentsChecker({})(fn)
        else:
            predicates = fn_or_predicates
            return ArgumentsChecker(predicates)

    class ReturnValue(Exception):
        def __init__(self, value):
            self.value = value

    def catch_return_value(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                return fn(*args, **kwargs)
            except ReturnValue as rv:
                return rv.value

        return wrapper
