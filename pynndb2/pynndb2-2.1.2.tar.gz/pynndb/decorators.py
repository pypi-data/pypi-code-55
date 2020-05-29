#####################################################################################
#
#  Copyright (c) 2020 - Mad Penguin Consulting Ltd
#
#####################################################################################
from typing import Any, Callable, Generator
import functools


def wrap_writer(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapped(*args, **kwargs) -> Any:
        if 'txn' in kwargs and kwargs['txn']:
            return func(*args, **kwargs)
        with args[0].env.begin(write=True) as kwargs['txn']:
            return func(*args, **kwargs)
    return wrapped


def wrap_reader_yield(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapped(*args, **kwargs) -> Generator[Any, None, None]:
        if 'txn' in kwargs and kwargs['txn']:
            yield from func(*args, **kwargs)
        else:
            with args[0].env.begin() as kwargs['txn']:
                yield from func(*args, **kwargs)
    return wrapped


def wrap_reader(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapped(*args, **kwargs) -> Any:
        if 'txn' in kwargs and kwargs['txn']:
            return func(*args, **kwargs)
        else:
            with args[0].env.begin() as kwargs['txn']:
                return func(*args, **kwargs)
    return wrapped
