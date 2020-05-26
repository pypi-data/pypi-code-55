from .curry.curry import curry

def _map(function, iterables):
    return map(function, iterables)

cmap = curry(_map)
