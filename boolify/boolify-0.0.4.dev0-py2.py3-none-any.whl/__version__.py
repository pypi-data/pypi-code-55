#!/usr/bin/env python
# encoding: utf-8
# -*- coding: utf-8 -*-

from datetime import datetime
__author__ = 'Luis (Lugg) Gustavo'
__author_email__ = 'the.nonsocial@gmail.com'
__copyright__ = f'2019-{datetime.utcnow().year}, {__author__}'
__description__ = 'Convert common strings into bool values.'
__license__ = 'MIT'
__package_name__ = 'boolify'
__url__ = f'https://github.com/luissilva1044894/{__package_name__}'
VERSION = (0, 0, 4, 'dev0')
__version__ = '.'.join(map(str, VERSION))
version = __version__

__release_level = [ 'alpha', 'beta', 'candidate', 'final' ]

from collections import namedtuple
version_info = namedtuple('VersionInfo', 'major minor micro releaselevel serial')(major=VERSION[0], minor=VERSION[1], micro=VERSION[2], releaselevel=__release_level[1], serial=0)

__all__ = (
  '__description__',
  '__url__',
  '__version__',
  '__author__',
  '__author_email__',
  '__license__',
  '__copyright__',
  '__package_name__',
  'version_info',
)

authors = (
  (__author__, __author_email__),
)
__authors__ = ', '.join('{} <{}>'.format(*_) for _ in authors)
