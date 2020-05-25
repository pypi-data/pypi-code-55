# -*- coding: utf-8 -*-

from .scrape import Load
from .scrape import Scan
from .scrape import Session

from .futures import FLoad
from .futures import FScan


__title__ = 'monapy'
__description__ = 'Declarative scraping tools'
__version__ = '0.2.11'
__author__ = 'Andriy Stremeluk'
__license__ = 'MIT'
__copyright__ = 'Copyright 2020 Andriy Stremeluk'


__all__ = ['Load', 'Scan', 'Session', 'FLoad', 'FScan']
