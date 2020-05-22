from typing import List, Optional
import logging
from sysapi.env import read_params


def get_xfer_logger(level= logging.INFO) -> logging.Logger:
    params = read_params()
    dbpath = params['dbpath']

    # create logger
    logger = logging.getLogger('xfer')
    logger.setLevel(level)

    ch = logging.FileHandler(filename=dbpath + 'backend.logs', delay=False)
    ch.setLevel(level)

    # create formatter
    formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt= '%m/%d/%Y-%H:%M:%S')

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)

    return logger
    
def get_xfer_status(filesystem: Optional[str]) -> List[str]:
    params = read_params()
    dbpath = params['dbpath']

    log_file = open(dbpath + 'backend.logs', "r")
    if filesystem is None:
        return [line[:-1] for line in log_file]
    else:
        return [line[:-1] for line in log_file if filesystem in line]
