import asyncio
import functools
import inspect
import linecache
import logging
import os
import random
import sys
import traceback
from contextlib import contextmanager

from lemmings.utils.timer import Timer

timer = Timer("timed_execution", module="", clazz="unknown", method="unknown")


def random_by_weight(list, weight_func):
    weight_total = sum(weight_func(i) for i in list)
    n = random.uniform(0, weight_total)
    for idx, item in enumerate(list):
        if n < weight_func(item):
            return item
        n = n - weight_func(item)
    return None


def timed_execution(f):
    if asyncio.iscoroutinefunction(f):
        @functools.wraps(f)
        async def wrap(*args, **kwargs):
            clazz = args[0].__class__.__name__ if is_method(f) else "unknown"
            with timer(module=f.__module__, clazz=clazz, method=f.__name__):
                return await f(*args, **kwargs)
    else:
        @functools.wraps(f)
        def wrap(*args, **kwargs):
            clazz = args[0].__class__.__name__ if is_method(f) else "unknown"
            with timer(module=f.__module__, clazz=clazz, method=f.__name__):
                return f(*args, **kwargs)

    return wrap


def ignore_exception(func):
    @functools.wraps(func)
    def function_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except BaseException as e:
            logging.exception("ignored exception")

    return function_wrapper


def is_method(fn):
    try:
        return inspect.getfullargspec(fn)[0][0] == 'self'
    except:
        return False


@contextmanager
def debug(file=sys.stdout):
    """usage:
        with debug(filename) as file:
            file.print(....)
        it will catch and print exceptions for debug
    """
    try:
        yield file
    except BaseException as e:
        print(e)
        traceback.print_stack(file=file)
        raise


def exception_with_line(e, root_cause=True):
    original = e
    if root_cause:
        while e.__cause__ is not None:
            e = e.__cause__
    msg = f"'{e}'"
    lines = get_traceback(e)
    if len(lines) > 0:
        _, filename, lineno, line = lines[len(lines) - 1]
        return f'{msg} @ {filename}:{lineno} "{first_chars(line, 20)}"'
    return msg


def first_chars(s, i=100):
    return s.ljust(i)[:i].strip()


def get_traceback(e):
    lines = []
    tb = e.__traceback__
    while tb is not None:
        path = tb.tb_frame.f_code.co_filename
        file = os.path.basename(path)
        linecache.checkcache(path)
        line = linecache.getline(path, tb.tb_lineno, tb.tb_frame.f_globals)
        lines.append((path, file, tb.tb_lineno, line.strip()))
        tb = tb.tb_next
    return lines
