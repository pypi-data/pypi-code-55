# -*- encoding: utf-8 -*-
# ! python3

import functools
import logging
import sys

from loguru import logger


class InterceptHandler(logging.Handler):
    def emit(self, record):
        # https://loguru.readthedocs.io/en/stable/overview.html#entirely-compatible-with-standard-logging
        # Retrieve context where the logging call occurred, this happens to be in the 6th frame upward
        logger_opt = logger.opt(depth=6, exception=record.exc_info)
        logger_opt.log(record.levelno, record.getMessage())


def loguru_setup(quiet, verbose):
    logger.remove()
    logging.basicConfig(handlers=[InterceptHandler()], level=0)
    logger.add(sys.stderr, level=max(logging.WARNING + (quiet - verbose), logging.NOTSET))


def setup_command_loguru(func):
    @functools.wraps(func)
    def wrapper_do_twice(*args, **kwargs):
        loguru_setup(
            quiet=kwargs.pop('quiet'),
            verbose=kwargs.pop('verbose')
        )
        logger.debug('Loguru configured')
        return func(*args, **kwargs)

    return wrapper_do_twice
