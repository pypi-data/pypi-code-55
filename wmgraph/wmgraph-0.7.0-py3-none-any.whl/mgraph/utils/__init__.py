import logging
import json
import os


def jdump(data, caller=None):
    try:
        logging.info(f'{caller}\n{json.dumps(data, indent=2)}')
    except:
        logging.info(f'{caller}\n{repr(data)}')

def jdebug(data, caller=None):
    try:
        logging.debug(f'{caller}\n{json.dumps(data, indent=2)}')
    except:
        logging.debug(f'{caller}\n{repr(data)}')
