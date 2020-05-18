
from . import core
from . import datasets

from .classification import *
from .core import *
from .datasets import *
from .defaults import *
from .eda import *
from .features import *
from .io import *
from .misc import *
from .regression import *
from .tests import *
from .version import __version__
from .viz import *

# TODO pandas.modin for speedup? Make this an option
__all__ = []
__all__.extend(core.__all__)
__all__.extend(datasets.__all__)
