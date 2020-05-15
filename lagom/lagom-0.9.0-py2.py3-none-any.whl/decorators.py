"""
This module provides decorators for hooking an
application into the container.s
"""
import inspect
from typing import List, Type

from .definitions import Singleton
from .container import Container
from .util.reflection import RETURN_ANNOTATION


def bind_to_container(container: Container, shared: List[Type] = None):
    """Decorates the function so that it's uses the container to construct things

    >>> from tests.examples import SomeClass
    >>> c = Container()
    >>> @bind_to_container(c)
    ... def say_hello_from(sayer: SomeClass):
    ...    return f"hello from {sayer}"
    >>> say_hello_from()
    'hello from <tests.examples.SomeClass object at ...>'

    """

    def _decorator(func):
        return container.partial(func, shared=shared)

    return _decorator


def dependency_definition(container: Container, singleton: bool = False):
    """ Registers the provided function with the container
    The return type of the decorated function will be reflected and whenever
    the container is asked for this type the function will be called

    >>> from tests.examples import SomeClass, SomeExtendedClass
    >>> c = Container()
    >>> @dependency_definition(c)
    ... def build_some_class_but_extended() -> SomeClass:
    ...    return SomeExtendedClass()
    >>> c.resolve(SomeClass)
    <tests.examples.SomeExtendedClass object at ...>

    """

    def _decorator(func):
        try:
            arg_spec = inspect.getfullargspec(func)
            return_type = arg_spec.annotations[RETURN_ANNOTATION]
        except KeyError:
            raise SyntaxError("Function used as a definition must have a return type")
        if singleton:
            container.define(return_type, Singleton(func))
        else:
            container.define(return_type, func)
        return func

    return _decorator
