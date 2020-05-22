import logging


def log_params(func):
    """decorator to debug a function params"""

    def wrapper(*args, **kwargs):
        logging.debug("{}(): args={}, kwargs={}".format(func.__name__, args, kwargs))
        return func(*args, **kwargs)

    return wrapper
