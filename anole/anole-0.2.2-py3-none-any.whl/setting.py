# -*- coding: utf-8 -*-
# @author: leesoar

"""settings"""

import logging
import os
import tempfile

__version__ = "0.2.2"

logger = logging.getLogger(__package__)

UA_CACHE_PATH = os.path.join(tempfile.gettempdir(), f"anole_{__version__}.json")

UA_CACHE_URL = f"https://www.leesoar.com/file/anole_{__version__}.json"

NAME_CACHE_PATH = os.path.join(tempfile.gettempdir(), f"anole_name_{__version__}.json")

NAME_CACHE_URL = f"https://www.leesoar.com/file/anole_name_{__version__}.json"

SHORTCUTS = {
    'internet explorer': 'internetexplorer',
    'ie': 'internetexplorer',
    'msie': 'internetexplorer',
    'edge': 'internetexplorer',
    'gg': 'chrome',
    'google': 'chrome',
    'googlechrome': 'chrome',
    'ff': 'firefox',
}

HTTP_RETRY = 5
