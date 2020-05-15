import logging

from cleo.config import ApplicationConfig
from loguru import logger

from pyadr.cli.io import ClikitDebuggerHandler, ClikitHandler


class LoggingAppConfig(ApplicationConfig):
    def create_io(self, *args, **kwargs):
        # remove loguru's default handler
        logger.remove(0)

        # add cli's own handler
        io = super().create_io(*args, **kwargs)
        logger.add(ClikitDebuggerHandler(io), colorize=True, level=logging.DEBUG)
        logger.add(ClikitHandler(io), format="{message}", level=logging.INFO)
        logger.debug("Logger initialized.")

        return io
