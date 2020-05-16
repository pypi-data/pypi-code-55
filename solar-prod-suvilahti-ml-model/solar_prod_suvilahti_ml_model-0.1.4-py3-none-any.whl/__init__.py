import logging

from regression_model.config import config
from regression_model.config import logging_config

VERSION_PATH = config.PACKAGE_ROOT / 'VERSION'

#configure the logger for use in  the package
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging_config.get_console_handler())
logger.propagate = False

with open(VERSION_PATH, 'r') as file_version:
    __version__ = file_version.read().strip()
