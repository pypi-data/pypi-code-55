import logging


def setup_logger(level=logging.DEBUG):
    """
    Setup the logger for a single module. This setup formats the log-messages. The root logger logs only to the
    console, according to the azure standard specifications.

    :param level: The Log-level of the messages, which shall be printed to the console
    """
    logging.basicConfig(format='%(asctime)s %(name)-10s %(levelname)-5s: %(message)s', datefmt='%d.%m.%Y %H:%M:%S %z',
                        level=level)
