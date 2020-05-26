#!/usr/bin/env python
# -*- coding: utf-8 -*-

################
## loggers.py ##
################

# type = module
# full name = rktools.loggers 

#############
## Imports ##
#############

import logging
from logging.handlers import RotatingFileHandler

###################
## init_logger() ##
###################

def init_logger(name="_NO_NAME_", config = None, level=logging.DEBUG):
    """
    Init the logger.

    Parameters
    -----------
    name: string
        The logger name
    level: value
        A value among
            logging.DEBUG,
            logging.INFO,
            logging.WARNING,
            ...
    config: dict
        The configuration parameters. Generally a Yaml file 
        parsed and converted to a dictionary object

    Returns
    -------
        _logger: logging.logger instance
    """

    _logger=logging.getLogger(name)
    if not len(_logger.handlers):
        # TODO the level can be set from the config object too
        _logger.setLevel(level)
        logger_format= config["logger"]["log_format"]
        formatter = logging.Formatter(logger_format)

        # console handler
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        _logger.addHandler(ch)

        # if a log file is provided, then create a filehandler:
        if len(config["logger"]["log_file"]) > 0:
            # add a rotating handler
            fh = RotatingFileHandler(config["logger"]["log_file"], 
                                            maxBytes=config["logger"]["log_maxBytes"],
                                            backupCount=config["logger"]["log_backupCount"])
            fh.setFormatter(formatter)
            _logger.addHandler(fh)

    _logger.info("logger successfully initialized!")

    return _logger



