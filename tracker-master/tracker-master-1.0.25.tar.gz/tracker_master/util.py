import logging
import logging.config
import time
import os
import json
from tracker_master import config as CFG
import datetime

__COM_PORT_LOGGER_NAME = 'com_port'


def setup_logging(default_path='logging.json', default_level=logging.INFO, env_key='LOG_CFG'):
    # Setup logging configuration
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        print('Configure logging from %s' % default_path)
        with open(path, 'rt') as f:
            config = json.load(f)

        # todo refactor
        try:
            # Read log file name from app configuration
            print('Application log: %s' % CFG.log_file())
            config['handlers']['app_log']['filename'] = CFG.log_file()
        except KeyError:
            pass
        try:
            print('Com port log: %s' % CFG.com_port_log_file())
            config['handlers']['com_port']['filename'] = CFG.com_port_log_file()
        except KeyError:
            pass

        logging.config.dictConfig(config)
    else:
        print('WARN! Use default logging')
        logging.basicConfig(level=default_level)


def format_current_time(pattern):
    x = datetime.datetime.now()
    return x.strftime(pattern)


def unix_time():
    return int(time.time())


def get_com_port_logger():
    return logging.getLogger(__COM_PORT_LOGGER_NAME)
