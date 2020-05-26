# -*- coding: utf-8 -*-

__version__ = '0.2.0'

import logging
from .cli import main

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    main()
