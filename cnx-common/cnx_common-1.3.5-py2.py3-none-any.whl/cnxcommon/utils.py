# -*- coding: utf-8 -*-
import functools


def ensure_unicode(f):
    @functools.wraps(f)
    def inner(*args, **kwargs):
        args = list(args)
        for i, arg in enumerate(args):
            if isinstance(arg, bytes):
                args[i] = arg.decode('utf-8')
        for kw, arg in kwargs.items():
            if isinstance(arg, bytes):
                kwargs[kw] = arg.decode('utf-8')
        return f(*args, **kwargs)

    return inner
