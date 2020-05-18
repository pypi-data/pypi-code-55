"""Top-level package for w7x."""

__author__ = """Daniel Böckenhoff"""
__email__ = 'dboe@ipp.mpg.de'
__version__ = '0.2.0'

from .geo import GeoSet, getGeoSet  # NOQA
from .config import *  # NOQA
from .core import is_w7x_instance, get_server, get_ws_class, run_service  # NOQA
from . import transcodings  # NOQA
from . import flt  # NOQA
from .flt import MagneticConfig, Machine, Points3D  # NOQA
from . import vmec  # NOQA
from . import extender  # NOQA
from . import plotting  # NOQA
from . import evaluation  # NOQA TODO: evaluation in w7x is too specific.
# from .plotting.poincare import plot_poincare_surfaces, plot_poincare_geometries
# from .plotting.tile_loads import plot_tile_loads
# from .plotting.vmec import plot_fourier
from . import batch  # NOQA


def switch_offline():
    """Allows loading old results without calling the web-service."""
    from . import core
    core.get_ws_class = lambda x, y: type(None)
