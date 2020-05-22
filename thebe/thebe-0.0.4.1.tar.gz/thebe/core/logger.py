import time, sys, datetime, glob, re, sys, time, os, copy, logging, threading
logging.StreamHandler(stream=None)

def getLogger(fileLoc, name):
    logger = logging.getLogger(name)
    file_handler = logging.FileHandler('%s/logs/%s'%(os.path.dirname(__file__), fileLoc))
    file_handler.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)
    return logger

