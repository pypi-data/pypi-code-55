import sys
import json
import logging
import logging.config


def init_logger(name, log_dir, config_dir):
    config_dict = json.load(open(config_dir + 'config.json'))
    config_dict['handlers']['file_handler']['filename'] = log_dir + name.replace('.', '')
    logging.config.dictConfig(config_dict)
    logger = logging.getLogger(name)

    std_out_format = '%(asctime)s - [%(levelname)s] - %(message)s'
    consoleHandler = logging.StreamHandler(sys.stdout)
    consoleHandler.setFormatter(logging.Formatter(std_out_format))
    logger.addHandler(consoleHandler)

    return logger
