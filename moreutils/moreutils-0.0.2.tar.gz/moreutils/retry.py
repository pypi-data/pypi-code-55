"""
moreutils.retry
--------------

This is a retry decorator that will do exponential + random sleep backoff.
It can optionally log the exception message, retry any number of times or even
forever, and otentially call a callback function you pass it with optional args
and keyword args.

The base decorator will use the default of 3 retries with
0.1 seconds + 2**i + random(0, 0.1 * 2**i)::

    @retry
    def some_failing_func(...):
        ...

Or specify explicitly::

    @retry(retries=5, seconds=2, exc=ValueError, log=logger)
    def failing_func(...):
        ...
"""
from time import sleep
from random import uniform
from functools import wraps


def retry(
    *args,  # if it's used without arguments, @retry alone, then use defaults
    retries=3,
    seconds=0.1,
    base=2,
    random_coef=1,
    exc=Exception,
    log=None,
    log_message=None,
    callback=None,
    callback_args=None,
    callback_kwargs=None,
):

    def decorator(func):

        @wraps(func)
        def decorated(*args, **kwargs):
            retry_i = 0
            while True:
                wait = seconds * base**retry_i
                if random_coef:
                    wait += uniform(0, random_coef * wait)
                try:
                    return func(*args, **kwargs)
                except exc:
                    if callable(callback):
                        cargs = callback_args or ()
                        ckwargs = callback_kwargs or {}
                        callback(
                            *cargs,
                            wait=wait,
                            attempt=retry_i,
                            **ckwargs,
                        )
                    retry_i += 1
                    if log is not None:
                        log.exception(log_message or func.__qualname__)
                    if retries is not None and retry_i <= retries:
                        if log is not None:
                            log.warning(
                                f'retry {retry_i}, sleeping {wait:.03}s'
                            )
                        sleep(wait)
                    else:
                        raise
        return decorated

    if args:
        return decorator(args[0])

    return decorator
