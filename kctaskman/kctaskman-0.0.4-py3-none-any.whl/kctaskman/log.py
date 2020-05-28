import logging
import platform

logger = None


class HostnameFilter(logging.Filter):
    hostname = platform.node()

    def filter(self, record):
        record.hostname = HostnameFilter.hostname
        return True


def initLogger(level):
    global logger
    logger = logging.getLogger()
    logger.setLevel(level)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.addFilter(HostnameFilter())
        handler.setFormatter(
            logging.Formatter(
                '- %(levelname)-5s %(asctime)-15s %(hostname)33s %(module)15s:%(lineno)-3s - %(message)s'))
        logger.addHandler(handler)
        logger.propagate = 0


initLogger('DEBUG')

# child process logger ignores the formatter
# how to: https://stackoverflow.com/questions/52118794/python-logger-duplicates-messages-on-screen-when-logging-to-stdout-and-two-file
