'''
moreutils
---------
'''

__title__ = 'moreutils'
__version__ = '0.0.2'
__all__ = (
    'Config',
    'add_log_error',
    'create_logger',
    'retry',
)
__author__ = 'Johan Nestaas <johannestaas@gmail.com>'
__license__ = 'GPLv3'
__copyright__ = 'Copyright 2020 Johan Nestaas'

from .config import Config
from .log import add_log_error, create_logger
from .retry import retry
