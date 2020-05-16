"""
A library for 5C data analysis.

Subpackage structure:

* :mod:`lib5c.algorithms` - main algorithms for analysis
* :mod:`lib5c.contrib` - integrations with third-party packages
* :mod:`lib5c.parsers` - file parsing
* :mod:`lib5c.plotters` - data visualization
* :mod:`lib5c.tools` - command line interface for ``lib5c``
* :mod:`lib5c.util` - various utility functions
* :mod:`lib5c.writers` - file writing
"""

from lib5c._version import get_version

__version__ = get_version()
