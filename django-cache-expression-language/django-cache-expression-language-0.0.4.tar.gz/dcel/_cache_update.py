from datetime import timedelta
from functools import wraps
from inspect import Signature
from typing import Callable

from django.core.cache import DEFAULT_CACHE_ALIAS

from dcel._base import BaseCacheDecorator


class CacheUpdate(BaseCacheDecorator):

    def __init__(
            self, *,
            key: str,
            duration: timedelta = None,
            alias: str = DEFAULT_CACHE_ALIAS
    ):
        super().__init__(key, alias)
        self.duration = duration

    def __call__(self, function: Callable) -> Callable:
        signature = Signature.from_callable(function)

        @wraps(function)
        def wrapper(*args, **kwargs) -> object:
            value = function(*args, **kwargs)
            key = self._get_key(signature, *args, **kwargs)
            self.cache.set(
                key=key,
                value=value,
                timeout=self.duration and self.duration.total_seconds()
            )

            return value

        return wrapper
