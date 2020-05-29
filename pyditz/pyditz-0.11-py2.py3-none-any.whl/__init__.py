"""
Python implementation of Ditz (http://rubygems.org/gems/ditz).
"""

__url__ = "http://pypi.python.org/pypi/pyditz"
__version__ = "0.11"

from .plugin import loader
from .config import get_modulefile

pluginpath = get_modulefile("plugins")
loader.add_path(pluginpath)
