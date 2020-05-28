from zepl_logging import logging

logger = logging.Logging()

logger.base_config('9d513bb6444bfba39822dd5b0e28c5500d6f7da0', notebook='test_NB', organization='OZX')
logger.info('this is  a info message')
logger.error('this is  a error message')
logger.warning('this is  a warning message')
logger.debug('this is  a debug message')
logger.critical('this is  a critical message')


