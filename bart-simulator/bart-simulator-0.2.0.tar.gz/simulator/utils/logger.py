""" module to utils of logger app """
import os
from logging import config as l_config


def configure_logger():

    SUB_DICT_CONFIG = {"level": "DEBUG", "handlers": [], "propagate": False}

    l_config.dictConfig(
        {
            "version": 1,
            "formatters": {
                "default": {
                    "format": "%(asctime)s %(levelname)-5.5s [%(name)s] %(message)s",
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                }
            },
            "handlers": {
                "console": {
                    "level": "DEBUG",
                    "class": "logging.StreamHandler",
                    "formatter": "default",
                    "stream": "ext://sys.stdout",
                }
            },
            "loggers": {"faker.factory": SUB_DICT_CONFIG,},
            "root": {"level": "DEBUG", "handlers": ["console"]},
        }
    )
