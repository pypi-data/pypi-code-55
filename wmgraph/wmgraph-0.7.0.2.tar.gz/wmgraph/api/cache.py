import os
import json
import logging
import functools


class Cache:
    args = None
    data = {}

    def __init__(self, args):
        self.args = args
        self.statedir = args.statedir or '.'
        self.filename = os.path.join(self.statedir, 'apicache.json')
        self.load()

    def load(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as filep:
                    self.data = json.loads(filep.read())
            except Exception as ex: #pylint: disable=broad-except
                logging.error(f'Error reading api cache {ex}')

    def save(self):
        try:
            with open(self.filename, 'w') as filep:
                filep.write(json.dumps(self.data))
        except Exception as ex: #pylint: disable=broad-except
            logging.error(f'Error writing api cache {ex}')

    def __contains__(self, item):
        return item in self.data

    def __setitem__(self, key, value):
        self.data[key] = value
        self.save()

    def __getitem__(self, key):
        return self.data.get(key)

    def purge(self):
        self.data = {}
        self.save()


def memoized(obj):
    '''decorate class methods with caching.
    Requires the class to have a dict-like attribute used as storage
    '''

    @functools.wraps(obj)
    def memoizer(*args, **kwargs):
        if hasattr(args[0], 'cache') and args[0].cache:
            cache = args[0].cache
        else:
            return obj(*args, **kwargs)

        key = str(args[1:]) + str(kwargs)
        if key not in cache:
            cache[key] = obj(*args, **kwargs)
        return cache[key]
    return memoizer
