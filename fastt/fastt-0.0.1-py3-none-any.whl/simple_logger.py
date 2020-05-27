import logging
import os
import time

APP_NAME = os.getenv('APP_NAME')

logger = logging.getLogger(APP_NAME)
logger.setLevel(logging.DEBUG)
# Adds Logging Console Handler
log_format = "".join(["[%(asctime)s] %(levelname)s -- %(message)s"])

formatter = logging.Formatter(fmt=log_format)
# Format UTC Time
formatter.converter = time.gmtime
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)
