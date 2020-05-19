"""
Metadata for Tyrannosaurus.
"""

import logging
from pathlib import Path

# importlib.metadata is compat with Python 3.8 only
from importlib_metadata import PackageNotFoundError, metadata as __load

from decorateme.abcd import *

logger = logging.getLogger("decorate-me")

try:
    metadata = __load(Path(__file__).parent.name)
    __status__ = "Development"
    __copyright__ = "Copyright 2017–2020"
    __date__ = "2020-05-18"
    __uri__ = metadata["home-page"]
    __title__ = metadata["name"]
    __summary__ = metadata["summary"]
    __license__ = metadata["license"]
    __version__ = metadata["version"]
    __author__ = metadata["author"]
    __maintainer__ = metadata["maintainer"]
    __contact__ = metadata["maintainer"]
except PackageNotFoundError:
    logger.error("Failed to import from decorateme", exc_info=True)
