import logging
import platform

from conf import conf


class HostnameFilter(logging.Filter):
    hostname = platform.node()

    def filter(self, record):
        record.hostname = HostnameFilter.hostname
        return True

# child process logger ignores the formatter
# how to: https://stackoverflow.com/questions/52118794/python-logger-duplicates-messages-on-screen-when-logging-to-stdout-and-two-file




logger = logging.getLogger()
logger.setLevel(conf.log_level)
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.addFilter(HostnameFilter())
    handler.setFormatter(
        logging.Formatter('- %(levelname)-5s %(asctime)-15s %(hostname)33s %(module)15s:%(lineno)-3s - %(message)s'))
    logger.addHandler(handler)
    logger.propagate = 0

