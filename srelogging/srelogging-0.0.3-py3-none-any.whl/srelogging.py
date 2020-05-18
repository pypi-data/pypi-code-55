import logging.config
import time
from typing import Optional

import yaml

DEFAULT_LOGGING_CONFIG = {
    "version": 1,
    "formatters": {
        "default": {
            "class": "srelogging.UTCFormatter",
            "format":
            "%(asctime)s.%(msecs)03dZ [%(levelname)s] <%(module)s.py:%(lineno)d> %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "default",
            "stream": "ext://sys.stdout"
        }
    },
    "root": {
        "level": "INFO",
        "handlers": ["console"]
    }
}
"""The default config used for logging if no file specified."""


class UTCFormatter(logging.Formatter):
    """Subclass of logging.Formatter to allow UTC formatting of times in config.
    """
    converter = time.gmtime


def configure_logging(path: Optional[str] = None) -> None:
    """Configure logging with an optional YAML config file. This should be 
    called on application start.

    Args:
        path: The path to the YAML config file. If None, default config is used.
    """
    log_config = DEFAULT_LOGGING_CONFIG
    file_load_error = None

    # attempt to load the logging config from a YAML file if given
    if path is not None:
        try:
            with open(path, 'r') as log_config_file:
                log_config = yaml.safe_load(log_config_file)
        except (OSError, yaml.YAMLError) as err:
            # defer printing of the error until after logging has been configured
            file_load_error = err

    # configure the logging
    logging.config.dictConfig(log_config)

    # log the deferred file load error if it occurred
    if file_load_error is not None:
        logging.error(
            f"error loading logging config: {file_load_error} - using default instead"
        )