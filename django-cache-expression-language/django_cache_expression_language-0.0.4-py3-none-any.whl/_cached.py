from datetime import timedelta
from functools import wraps
from inspect import Signature
from typing import Callable, Any

from django.core.cache import DEFAULT_CACHE_ALIAS

from dcel._base import BaseCacheDecorator


class Cached(BaseCacheDecorator):
    no_value = object()

    def do_nothing(self, *args, **kwargs):
        pass

    def __init__(
            self, *,
            key: str,
            duration: timedelta = None,
            alias: str = DEFAULT_CACHE_ALIAS,
            on_hit: Callable[[str, Any], None] = do_nothing,
            on_miss: Callable[[str, Any], None] = do_nothing
    ):
        super().__init__(key, alias)
        self.duration = duration
        self.on_hit = on_hit
        self.on_miss = on_miss

    def __call__(self, function: Callable) -> Callable:
        signature = Signature.from_callable(function)

        @wraps(function)
        def wrapper(*args, **kwargs) -> object:
            key = self._get_key(signature, *args, **kwargs)
            value = self.cache.get(key=key, default=self.no_value)

            if value is self.no_value:
                value = function(*args, **kwargs)
                self.cache.set(
                    key=key,
                    value=value,
                    timeout=self.duration and self.duration.total_seconds()
                )
                self.on_miss(key, value)

            else:
                self.on_hit(key, value)

            return value

        return wrapper
