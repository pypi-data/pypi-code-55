import contextlib
import hashlib
import logging
from functools import wraps
from typing import Callable
from typing import Iterable
from typing import Mapping
from typing import Optional

from django.core.cache import cache
from django.utils.encoding import force_bytes
from redis.exceptions import LockError


logger = logging.getLogger(__name__)

NO_CACHE = object()
DEFAULT_LOCK_TIMEOUT = 10
KeyMakerType = Callable[[Iterable, Mapping], str]


def redis_client(write=True):
    return cache.client.get_client(write=write)


def _make_key_id(*args, **kwargs):
    return ':'.join((
        *(str(value) for value in args),
        *(f'{key}={value}' for key, value in kwargs.items())
    ))


def _hash(key):
    return hashlib.md5(force_bytes(key)).hexdigest()  # noqa: S303


@contextlib.contextmanager
def use_lock(key, timeout=DEFAULT_LOCK_TIMEOUT, blocking_timeout=None):
    """
    If blocking_timeout is specified, will proceed after
    blocking_timeout even without the lock obtained.
    Check the return value and abort if needed.
    """

    if timeout is None:  # Prevent locks without timeout set - it is too dangerous if the process dies
        timeout = DEFAULT_LOCK_TIMEOUT

    lock = redis_client().lock(f'use_lock:{key}', timeout=timeout, blocking_timeout=blocking_timeout)
    acquired = lock.acquire(blocking=True)
    try:
        yield acquired
    finally:
        if not acquired:
            return

        # Don't want failed lock release to break the whole application
        try:
            lock.release()
        except LockError as exc:
            logger.exception(str(exc))


def with_lock(
    key,
    timeout,
    blocking_timeout=None,
    proceed_without_lock=False,
):
    """
    If blocking_timeout is specified, and the lock is not obtained after blocking_timeout,
    behavior will depend on the proceed_without_lock.
    """

    def factory(func):
        @wraps(func)
        def decorator(*args, **kwargs):
            with use_lock(key, timeout, blocking_timeout) as acquired:
                if not (acquired or proceed_without_lock):
                    return None
                return func(*args, **kwargs)

        return decorator

    return factory


def ensure_single(key, timeout):
    """Ensure function executes only single time simultaneously, other executions are aborted immediately"""
    return with_lock(key, timeout, blocking_timeout=0, proceed_without_lock=False)


def cache_memoize(
    timeout: Optional[int] = None,
    prefix: Optional[int] = None,
    key_maker: KeyMakerType = _make_key_id,
    calculation_time=None,
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
                with use_lock(cache_key, timeout=calculation_time):
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
