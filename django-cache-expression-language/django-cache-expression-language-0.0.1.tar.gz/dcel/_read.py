from datetime import timedelta
from functools import wraps
from inspect import Signature
from typing import Callable

from django.core.cache import DEFAULT_CACHE_ALIAS

from dcel._base import BaseCacheDecorator


class ReadCache(BaseCacheDecorator):

    def __init__(self, *, key: str, duration: timedelta, alias: str = DEFAULT_CACHE_ALIAS):
        super().__init__(key, alias)
        self.duration = duration

    def __call__(self, function: Callable) -> Callable:
        signature = Signature.from_callable(function)

        @wraps(function)
        def wrapper(*args, **kwargs) -> object:
            key = self._get_key(signature, *args, **kwargs)
            value = self.cache.get_or_set(
                key=key,
                default=lambda: function(*args, **kwargs),
                timeout=self.duration.total_seconds(),
            )

            return value

        return wrapper
