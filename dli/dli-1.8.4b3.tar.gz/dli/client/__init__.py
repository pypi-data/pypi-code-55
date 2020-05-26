import logging
import sys
# from logging.handlers import RotatingFileHandler
# from pathlib import Path

from pythonjsonlogger import jsonlogger  # noqa: I900


def _setup_logging(where_level):
    logger = logging.getLogger('global')

    json_format = jsonlogger.JsonFormatter(
        '%(asctime)s - %(levelname)s - %(name)s - %(message)s',
        json_indent=2
    )

    handler = None
    chosen_level = None
    switcher = {
        "error": logging.ERROR,
        "warn": logging.WARNING,
        "debug": logging.DEBUG,
        "info": logging.INFO
    }

    if where_level:
        # If debug - create a log file or stdout
        to, _, level = str(where_level).partition(":")

        if to == "stdout":
            handler = logging.StreamHandler(stream=sys.stdout)

        chosen_level = switcher.get(level.lower(), logging.DEBUG)

    # if not handler:
    #     log_folder = "logs/"
    #     Path(log_folder).mkdir(parents=True, exist_ok=True)
    #
    #     handler = RotatingFileHandler(
    #         f'{log_folder}sdk.log', mode='w', backupCount=3)
    #     chosen_level = logging.DEBUG

    # handler.setFormatter(json_format)
    # handler.setLevel(chosen_level)
    # logger.addHandler(handler)
    logger.setLevel(chosen_level)
    return logger
