from loguru import logger
import sys

def AddLogger(log_location="backup_log_{time}.log", log_mode="INFO") :
    def wrap(func) :
        def wrap_f(*arg, **kargs) :
            logger.add(log_location, format="{time} {level} {message}", filter="backup", level=log_mode)
            result = func(*arg, **kargs)

            return result
        return wrap_f
    return wrap