#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2020, Bruno Sanchez, Vanessa Daza,
#                     Juan B Cabral, Marcelo Lares,
#                     Nadia Luczywo, Dante Paz, Rodrigo Quiroga,
#                     Martín de los Ríos, Federico Stasyszyn
#                     Cristian Giuppone.
# License: BSD-3-Clause
#   Full Text: https://raw.githubusercontent.com/ivco19/libs/master/LICENSE


# =============================================================================
# DOCS
# =============================================================================

"""Cache abstractions for arcovid19

"""

__all__ = [
    "DEFAULT_CACHE_DIR",
    "CACHE",
    "CACHE_EXPIRE",
    "from_cache"]


# =============================================================================
# IMPORTS
# =============================================================================

import os

import diskcache as dcache


# =============================================================================
# CACHE CONF
# =============================================================================

ARCOVID19_DATA = os.path.expanduser(os.path.join('~', 'arcovid19_data'))

#: Default cache location, (default=~/arcovid_19_data/_cache_)
DEFAULT_CACHE_DIR = os.path.join(ARCOVID19_DATA, "_cache_")

#: Default cache instance
CACHE = dcache.Cache(directory=DEFAULT_CACHE_DIR, disk_min_file_size=0)

#: Time to expire of every load_cases call in seconds
CACHE_EXPIRE = 60 * 60  # ONE HOUR


# =============================================================================
# FUNCTIONS
# =============================================================================

def from_cache(tag, function, force=False, *args, **kwargs):
    """Simple cache orchestration.

    Parameters
    ----------

    tag: str
        Normally every function call the cache with their own tag.
        We sugest "module.function" or "module.Class.function"

    function: callable
        The function to be cached

    force: bool (default=False)
        If the vale of the cache must be ignored and re-execute the
        function.

    args and kwargs:
        All the parameters needed to execute the function.

    """
    # start the cache orchestration
    key = dcache.core.args_to_key(
        base=("arcodiv19", tag), args=args, kwargs=kwargs, typed=False)

    with CACHE as cache:
        cache.expire()

        value = (
            dcache.core.ENOVAL if force else
            cache.get(key, default=dcache.core.ENOVAL, retry=True))

        if value is dcache.core.ENOVAL:
            value = function(**kwargs)
            cache.set(
                key, value, expire=CACHE_EXPIRE,
                tag=f"{tag}", retry=True)

    return value
