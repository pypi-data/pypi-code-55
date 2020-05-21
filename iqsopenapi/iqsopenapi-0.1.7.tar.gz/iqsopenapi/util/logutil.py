# -*- coding: utf-8 -*-
import sys
import time
import logging
from datetime import datetime
import os

logger = logging.getLogger('iqsopenapilogger')
logger.setLevel(logging.INFO)

logformat = logging.Formatter('%(asctime)-15s %(levelname)s [%(filename)s:%(lineno)d] %(message)s')

console_handler = logging.StreamHandler(stream=sys.stdout)
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(logformat)
logger.addHandler(console_handler)

def log2file(filename):
    path = os.path.dirname(filename)
    if not os.path.exists(path):
        os.makedirs(path)
    file_handler = logging.FileHandler(filename)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logformat)
    logger.addHandler(file_handler)

if __name__ == '__main__':
    
    log2file();

    logger.error("test error")
    logger.critical("test critical")
    logger.debug("test debug")
    logger.info("test info")