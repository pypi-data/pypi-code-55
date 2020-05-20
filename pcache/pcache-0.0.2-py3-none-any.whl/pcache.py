import shelve
import threading
import time


class PersistentCache():
    """A simple implementation of persistent cache

    Parameters:
        filename: File for storing the cache data
    """
    __EXPIRE_KEY = "__expire_list"
    __RESTRICTED_KEYS = (__EXPIRE_KEY,)

    def __init__(self, filename):
        self.__filename = filename
        self.__wlock = threading.Lock()
        with shelve.open(self.__filename) as cache:
            if self.__EXPIRE_KEY not in cache:
                cache[self.__EXPIRE_KEY] = {}

    def __getitem__(self, key):
        if key in self.__RESTRICTED_KEYS:
            return None
        with shelve.open(self.__filename) as cache:
            if key in cache[self.__EXPIRE_KEY]:
                _ts = cache[self.__EXPIRE_KEY][key]["timestamp"]
                _ttl = cache[self.__EXPIRE_KEY][key]["ttl"]
                if time.time() - _ts > _ttl:
                    with self.__wlock:
                        del cache[key]
                    return None
            return cache.get(key)

    def __setitem__(self, key, value):
        if key in self.__RESTRICTED_KEYS:
            raise AttributeError()
        with self.__wlock:
            with shelve.open(self.__filename) as cache:
                cache[key] = value

    def __delitem__(self, key):
        if key in self.__RESTRICTED_KEYS:
            raise AttributeError()
        with self.__wlock:
            with shelve.open(self.__filename) as cache:
                del cache[key]

    def __str__(self):
        return "{}".format({k: v for k, v in self.items()})

    def items(self):
        with shelve.open(self.__filename) as cache:
            return [(k, cache[k]) for k in cache.keys()
                    if self.__getitem__(k)]

    def expire(self, key, ttl=10):
        with self.__wlock:
            with shelve.open(self.__filename) as cache:
                expire_list = cache[self.__EXPIRE_KEY]
                expire_list[key] = {
                    "ttl": ttl,
                    "timestamp": time.time()
                }
                cache[self.__EXPIRE_KEY] = expire_list
