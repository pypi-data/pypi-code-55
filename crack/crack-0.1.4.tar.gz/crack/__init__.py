# -*- coding: utf-8 -*-
# @author: leesoar

"""something."""
import sys

from crack.util import *
from crack.setting import __version__

__all__ = ["util", "__version__"]

if sys.version_info >= (3, 6):
    from secrets import *

