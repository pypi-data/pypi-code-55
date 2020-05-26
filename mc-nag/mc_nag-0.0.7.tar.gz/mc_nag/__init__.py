"""Set behavior of mc_nag."""

import sys
from mc_nag.base_utils.exceptions import quiet_exception_hook

sys.excepthook = quiet_exception_hook

__version__ = '0.0.7'
