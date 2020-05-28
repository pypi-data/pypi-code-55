# -*- coding: utf-8 -*-
import sys
import time
import logging
from logging import handlers
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
    logger.debug('log filename:{0}'.format(filename))
    path = os.path.dirname(filename)
    if not os.path.exists(path):
        os.makedirs(path)
    trfh = handlers.TimedRotatingFileHandler(filename=filename,when='D',backupCount=30,encoding='utf-8')
    trfh.setLevel(logging.DEBUG)
    trfh.setFormatter(logformat)
    logger.addHandler(trfh)

if __name__ == '__main__':

    log2file(r"D:\logs\test\strategy.log")
    logger.error("test error")
    logger.critical("test critical")
    logger.debug("test debug")
    logger.info("test info")