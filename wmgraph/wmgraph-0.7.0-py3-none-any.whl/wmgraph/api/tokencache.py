# pylint: disable=logging-format-interpolation
import os
import atexit
import logging

import msal


class TokenCache:
    cache = None

    def __init__(self, args):
        cache_file = os.path.join(args.statedir, "tokencache.bin")
        cache = self.cache = msal.SerializableTokenCache() # pylint: disable=invalid-name
        if os.path.exists(cache_file):
            self.cache.deserialize(open(cache_file, "r").read())
            logging.debug(f'Loaded cache {cache_file}')
        atexit.register(lambda:
                        open(cache_file, "w").write(cache.serialize())
                        # Hint: The following optional line persists only when state changed
                        if cache.has_state_changed else None
                        )
