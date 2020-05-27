
import importlib.metadata

__version__ = importlib.metadata.version("cuta")
version = __version__

from . import api
from . import core

from .api import from_env


__all__ = ["api", "from_env", "core"]


