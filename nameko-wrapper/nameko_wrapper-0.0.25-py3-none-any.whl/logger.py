"""
Preset Logger

Config:
    LOGGER:
        filename:
        filemode:
        format:
        datefmt:
        style:
        level:
"""

import logging

from .config import config


# 读取Logger配置文件
LOGGER_CONFIG = config.get('LOGGER', {})
# LOGGER_CONFIG = {}

filename = LOGGER_CONFIG.get('filename', None)
filemode = LOGGER_CONFIG.get('filemode', 'w+')
format = LOGGER_CONFIG.get('format', '[%(levelname)s] %(asctime)s.%(msecs)03d %(module)s/%(funcName)s/%(lineno)d: %(message)s')
datefmt = LOGGER_CONFIG.get('datefmt', '%Y-%m-%d %H:%M:%S')
style = LOGGER_CONFIG.get('style', '%')
level = LOGGER_CONFIG.get('level', 'INFO')
# stream = LOGGER_CONFIG.get('stream', None)
# handler = LOGGER_CONFIG.get('handlers', None)
# force = LOGGER_CONFIG.get('force', None)

# 定义logger
logger = logging.getLogger()
logger.setLevel(level)

# 定义handler
if filename:
    handler = logging.FileHandler(filename=filename, mode=filemode)
else:
    handler = logging.StreamHandler()

formatter = logging.Formatter(
    fmt=format,
    datefmt=datefmt,
    style=style
)
handler.setFormatter(formatter)

logger.addHandler(handler)


if __name__ == '__main__':
    print(logger.info('Hello'))

