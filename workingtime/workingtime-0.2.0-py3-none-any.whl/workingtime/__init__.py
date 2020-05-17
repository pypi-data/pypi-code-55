"""

# TODO main description

"""
import errno as _errno

from .workingtime import WorkingTime, Time

import os as _os

try:
    with open(_os.path.join(_os.path.dirname(__file__),
                            '..', 'VERSION'), 'r') as version_file:
        __version__ = version_file.read().strip()
except IOError as e:
    if e.errno != _errno.ENOENT:
        raise

    __version__ = "0.0"
