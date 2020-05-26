from .identity import identity
from .curry.curry import curry
from .curry.placeholder import placeholder, p
from .compose import compose, rcompose
from .map import cmap

map = cmap

__version__ = '0.1.5'

__all__ = [
    'identity',
    'curry',
    'placeholder',
    'p',
    'compose',
    'rcompose',
    'cmap',
    'map',
]
