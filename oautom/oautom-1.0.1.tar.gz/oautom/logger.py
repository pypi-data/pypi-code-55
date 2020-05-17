import logging


def get_logger() -> logging.Logger:
    logger = logging.getLogger('oautom')
    return logger
