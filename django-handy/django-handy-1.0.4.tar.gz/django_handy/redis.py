import contextlib
import hashlib
import logging
from collections import Iterable
from collections import Mapping
from functools import wraps
from typing import Callable
from typing import Optional

from django.core.cache import cache
from django.utils.encoding import force_bytes
from redis.exceptions import LockError


logger = logging.getLogger(__name__)
redis_client = cache.client

NO_CACHE = object()
DEFAULT_LOCK_TIMEOUT = 10
KeyMakerType = Callable[[Iterable, Mapping], str]


def _make_key_id(*args, **kwargs):
    return ':'.join((
        *(str(value) for value in args),
        *(f'{key}={value}' for key, value in kwargs.items())
    ))


def _hash(key):
    return hashlib.md5(force_bytes(key)).hexdigest()  # noqa: S303


@contextlib.contextmanager
def use_lock(key, timeout=DEFAULT_LOCK_TIMEOUT, blocking_timeout=None):
    if timeout is None:  # Prevent locks without timeout set - it is too dangerous if the process dies
        timeout = DEFAULT_LOCK_TIMEOUT

    try:
        with redis_client.lock(f'use_lock:{key}', timeout=timeout, blocking_timeout=blocking_timeout):
            yield
    except LockError as exc:
        message = str(exc)
        if 'Unable to acquire lock within the time specified' not in message:
            logger.exception(message)


def use_lock_decorator(
    timeout,
    prefix=None,
    blocking_timeout=None,
    key_maker: KeyMakerType = _make_key_id
):
    def factory(func):
        @wraps(func)
        def decorator(*args, **kwargs):
            key_prefix = prefix or func.__name__
            key_id = _hash(key_maker(*args, **kwargs))
            with use_lock(f'{key_prefix}:{key_id}', timeout, blocking_timeout):
                return func(*args, **kwargs)

        return decorator

    return factory


def ensure_single(key, timeout):
    return use_lock(key, timeout, blocking_timeout=0)


def ensure_single_decorator(timeout, prefix=None, key_maker: KeyMakerType = _make_key_id):
    return use_lock_decorator(timeout, prefix, blocking_timeout=0, key_maker=key_maker)


def cache_memoize(
    timeout: Optional[int] = None,
    prefix: Optional[int] = None,
    key_maker: KeyMakerType = _make_key_id,
    lock_timeout=None,
):
    def factory(func):
        key_prefix = f'cache_memoize:{prefix or func.__name__}'

        def _make_cache_key(*args, **kwargs):  # noqa: WPS430
            cache_key = _hash(key_maker(*args, **kwargs))
            return f'{key_prefix}:{cache_key}'

        @wraps(func)
        def decorator(*args, **kwargs):
            cache_key = _make_cache_key(*args, **kwargs)
            result = cache.get(cache_key, NO_CACHE)

            if result is NO_CACHE:
                with use_lock(cache_key, timeout=lock_timeout):
                    result = cache.get(cache_key, NO_CACHE)
                    if result is NO_CACHE:
                        result = func(*args, **kwargs)
                        cache.set(cache_key, result, timeout)
            return result

        def invalidate(*args, **kwargs):  # noqa: WPS430
            cache_key = _make_cache_key(*args, **kwargs)
            cache.delete(cache_key)

        decorator.invalidate = invalidate
        return decorator

    return factory
