
from . import core
from .core import *

from . import datasets
from .datasets import *

from . import math
from .math import *

from . import statistics
from .statistics import *

from ._version import __version__
from .classification import *
from .defaults import *
from .eda import *
from .features import *
from .io import *
from .misc import *
from .regression import *
from .tests import *
from .viz import *

# TODO pandas.modin for speedup? Make this an option
__all__ = ['__version__']
__all__.extend(core.__all__)
__all__.extend(datasets.__all__)
__all__.extend(math.__all__)
__all__.extend(statistics.__all__)
