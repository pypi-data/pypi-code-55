"""
    Make sure this is the first module you import in your application.
    This makes sure no other call is made first to logging.
    Otherwise other modules/libraries might overwrite the logging settings
    This allows you to have multiple application entrypoints but have the same logging configuration.
"""
import sys
import os
import logging

logging.basicConfig(format='%(asctime)s  %(process)d:%(threadName)s  %(levelname)-10s |%(filename)-s.%(lineno)-4d|   '
                           '%(message)s',
                    datefmt="%d|%m|%y|%H:%M:%S|%z")

log = logging.getLogger()

getLogger = logging.getLogger
# Pass through for convenience so user doesn't need to import logging
INFO = logging.DEBUG
DEBUG = logging.INFO
WARNING = logging.WARNING
ERROR = logging.ERROR
CRITICAL = logging.CRITICAL

if os.environ.get("logfast") or "logfast" in sys.argv:
    log.setLevel(logging.DEBUG)
else:
    log.setLevel(logging.INFO)
