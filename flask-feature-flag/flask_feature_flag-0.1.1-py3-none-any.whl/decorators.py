import functools
from .use_cases import GetFeature
from .utils import (
    response_command,
    response_not_found,
    response_use_case
    )


def is_enabled(response, feature):
    """Decorator to enable or disable a feature.

    Args:
        response: Function that returns object to return.
        feature: Environment variable name.

    Returns:
        response: Decorated function or function error.
    """
    def _decorator(func):
        @functools.wraps(func)
        def _wrapper(*args, **kwargs):
            use_case = GetFeature()
            feature_name = use_case.handle(feature)
            if feature_name:
                return func(*args, **kwargs)
            return response()
        return _wrapper
    return _decorator


def command_enabled(feature: str):
    """Decorator to enable or disable a command.

    Args:
        feature: Environment variable name.

    Returns:
        response: Decorated function or response_command.
    """
    def _decorator(func):
        @functools.wraps(func)
        def _wrapper(*args, **kwargs):
            use_case = GetFeature()
            feature_name = use_case.handle(feature)
            if feature_name:
                return func(*args, **kwargs)
            return response_command()
        return _wrapper
    return _decorator


def route_enabled(feature: str):
    """Decorator to enable or disable a route.

    Args:
        feature: Environment variable name.

    Returns:
        response: Decorated function or response_not_found.
    """
    def _decorator(func):
        @functools.wraps(func)
        def _wrapper(*args, **kwargs):
            use_case = GetFeature()
            feature_name = use_case.handle(feature)
            if feature_name:
                return func(*args, **kwargs)
            return response_not_found()
        return _wrapper
    return _decorator


def use_case_enabled(feature: str):
    """Decorator to enable or disable a use case.

    Args:
        feature: Environment variable name.

    Returns:
        response: Decorated function or response_use_case.
    """
    def _decorator(func):
        @functools.wraps(func)
        def _wrapper(*args, **kwargs):
            use_case = GetFeature()
            feature_name = use_case.handle(feature)
            if feature_name:
                return func(*args, **kwargs)
            return response_use_case()
        return _wrapper
    return _decorator
