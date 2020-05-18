"""Top-level package for tfields."""

__author__ = """Daniel Böckenhoff"""
__email__ = 'dboe@ipp.mpg.de'
__version__ = '0.3.0'

from . import core  # NOQA
from . import bases  # NOQA
from . import lib  # NOQA

# methods:
from .core import dim, rank  # NOQA
from .mask import evalf  # NOQA
from .lib import *  # NOQA

# classes:
from .core import Tensors, TensorFields, TensorMaps, Container, Maps  # NOQA
from .points3D import Points3D  # NOQA
from .mesh3D import Mesh3D  # NOQA
from .triangles3D import Triangles3D  # NOQA
from .planes3D import Planes3D  # NOQA
from .bounding_box import Node  # NOQA
