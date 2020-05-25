"""Cachalot is a minimal persistent memoization cache, that uses TinyDB."""

import functools
import hashlib
import inspect
import os
import time
import json
from typing import Any, Callable

import jsonpickle
import tinydb  # pylint: disable=wrong-import-order
import tinydb_smartcache


VERSION = (1, 4, 0)

__title__ = 'cachalot'
__description__ = 'Minimal persistent memoization cache'
__url__ = 'http://gitlab.com/radek-sprta/cachalot'
__download_url__ = 'https://gitlab.com/radek-sprta/cachalot/repository/archive.tar.gz?ref=master'
__version__ = '.'.join(map(str, VERSION))
__author__ = 'Radek Sprta'
__author_email__ = 'mail@radeksprta.eu'
__license__ = 'MIT License'
__copyright__ = "Copyright 2018 Radek Sprta"


class Cache:  # pylint: disable=too-many-instance-attributes
    """Offline cache for search results.

    Attributes:
        path: Defaults to .cache.json. Path to the database file.
        timeout: Defaults to infinite. Period after which results should expire.
        size: Defaults to infinite. Maximum number of cached results.
        filesize: Defaults to infinite. Maximum size of databytes in bytes.
        storage: Defaults to JSONStorage. Storage type for TinyDB.
        retry: Defaults to True. Whether to retry on empty data.
        renew_on_read: Defaults to True. Whether to refresh timestamps on reads.
    """

    def __init__(self,
                 *,
                 path: str = '.cache.json',
                 timeout: int = 0,
                 size: int = 0,
                 filesize: int = 0,
                 storage: tinydb.storages.Storage = tinydb.storages.JSONStorage,
                 retry: bool = False,
                 renew_on_read: bool = True) -> None:
        self.path = os.path.abspath(os.path.expanduser(path))
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        self.timeout = timeout
        self.size = size
        self.filesize = filesize
        self.retry = retry
        self.renew_on_read = renew_on_read
        self.storage = storage
        try:
            self.db = tinydb.TinyDB(self.path, storage)
        except json.decoder.JSONDecodeError:
            # Database is corrupted
            self._recreate_db()
        self.db.table_class = tinydb_smartcache.SmartCacheTable

    def calculate_hash(self, function: Callable[..., Any]) -> str:
        """Calculate hash of a function call.

        Args:
            function: Function to calculate hash of.

        Returns:
            Hash of function call with given arguments

        Example:
            >>> cache.calculate_hash(len)('teststring')
            '6249462f58db797109850acbf20ac5c6'
        """

        def wrapped(function, *args, **kwargs):
            seed_args = args[1:] if self._is_method(function) else args
            seed = function.__name__ + \
                jsonpickle.encode(seed_args) + jsonpickle.encode(kwargs)
            return hashlib.md5(seed.encode('utf8')).hexdigest()
        return functools.partial(wrapped, function)

    def clear(self) -> None:
        """Clear the cache."""
        try:
            self.db.purge()
        except json.decoder.JSONDecodeError:
            # Database is corrupted
            self._recreate_db()

    def expiry(self) -> float:
        """Return expiration time for cached results."""
        return time.time() + self.timeout

    def get(self, key: str) -> Any:
        """Get torrent from database.

        Args:
            key: Key hash.

        Returns:
            Cached object.
        """
        self._remove_expired()
        entry = tinydb.Query()
        value = self.db.get(entry.key == key)
        if value:
            if self.renew_on_read:
                self.db.update({'time': self.expiry()}, entry.key == key)
            return jsonpickle.decode(value['value'])
        return None

    def insert(self, key: str, entry: Any) -> None:
        """Insert entry into cache.

        Args:
            key: Key hash of the entry to store.
            entry: Object to cache.
        """
        value = jsonpickle.encode(entry)
        try:
            self.db.insert({'key': key, 'time': self.expiry(), 'value': value})
            if self.size > 0 and len(self.db) > self.size:
                self._remove_oldest()
            if self.filesize > 0:
                while os.stat(self.path).st_size > self.filesize and len(self.db) > 0:
                    self._remove_oldest()
        except json.decoder.JSONDecodeError:
            # Database is corrupted
            self._recreate_db()
            self.db.insert({'key': key, 'time': self.expiry(), 'value': value})

    @staticmethod
    def _is_method(function: Callable[..., Any]) -> bool:
        """Check if function is actually a method.

        Args:
            function: Function to check the state of.

        Returns:
            True if function is method, false otherwise.
        """
        try:
            if '.' in function.__qualname__ and inspect.getfullargspec(function).args[0] == 'self':
                return True
            return False
        except IndexError:
            # For functions with no arguments
            return False

    def remove(self, key: str) -> None:
        """Delete key from cache.

        Args:
            key: Hash key to delete from the cache.
        """
        entry = tinydb.Query()
        try:
            self.db.remove(entry.key == key)
        except json.decoder.JSONDecodeError:
            # Database is corrupted
            self._recreate_db()

    def _remove_expired(self) -> None:
        """Remove old entries."""
        if self.timeout < 1:
            return

        entry = tinydb.Query()
        now = time.time()
        try:
            self.db.remove(entry.time < now)
        except json.decoder.JSONDecodeError:
            # Database is corrupted
            self._recreate_db()

    def _recreate_db(self) -> None:
        if os.path.exists(self.path):
            os.remove(self.path)
        self.db = tinydb.TinyDB(self.path, self.storage)

    def _remove_oldest(self) -> None:
        """Remove oldest entry."""
        try:
            oldest = self.db.all()[0]['key']
            self.remove(oldest)
        except json.decoder.JSONDecodeError:
            # Database is corrupted
            self._recreate_db()

    def __call__(self, function: Callable[..., Any]):
        """Decorator for caching function results.

        Args:
            function: Function to decorate.

        Returns:
            Cached function.
        """
        @functools.wraps(function)
        def wrapped(*args, **kwargs):
            """Cache function."""
            result = ''
            key = self.calculate_hash(function)(*args, **kwargs)
            result = self.get(key)
            if result is None:
                result = function(*args, **kwargs)
                self.insert(key, result)
            return result
        return wrapped
