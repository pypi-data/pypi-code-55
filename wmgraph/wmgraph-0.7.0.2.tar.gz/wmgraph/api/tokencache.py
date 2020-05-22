# pylint: disable=logging-format-interpolation
import os
import atexit
import logging

import msal


class TokenCache:
    cache = None
    cache_file = None

    def __init__(self, args):
        self.cache_file = os.path.join(args.statedir, "tokencache.bin")
        self.cache = msal.SerializableTokenCache()  # pylint: disable=invalid-name
        if os.path.exists(self.cache_file):
            self.cache.deserialize(open(self.cache_file, "r").read())
            logging.debug(f'Loaded cache {self.cache_file}')
        atexit.register(
                        self.__atexit
                        )

    def __atexit(self):
        if self.cache.has_state_changed:
            cachedir = os.path.dirname(self.cache_file)
            if not os.path.isdir(cachedir):
                os.makedirs(cachedir)

            try:
                open(self.cache_file, "w").write(self.cache.serialize())
            except FileNotFoundError as ex:
                logging.error(f'Could not write tokencache {ex}')
