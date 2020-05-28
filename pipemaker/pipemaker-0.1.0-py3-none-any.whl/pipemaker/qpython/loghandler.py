""" logging using shared objects
works across multiple machines
todo: add address when needed to use on multiple machines
"""
import os

import logging
from logging.handlers import QueueListener, QueueHandler
from ..utils.share import create_client


class SharedQueueHandler(QueueHandler):
    """ handler to put messages on shared queue """

    def __init__(self, **kwargs):
        logging.Handler.__init__(self)
        self.queue = create_client(port=logging.handlers.DEFAULT_TCP_LOGGING_PORT)


class FileHandler(logging.FileHandler):
    """ read messages from the log queue and write to file """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        log = logging.getLogger()
        if log.handlers:
            self.setFormatter(log.handlers[0].formatter)

        # listener
        q = create_client(port=logging.handlers.DEFAULT_TCP_LOGGING_PORT)
        self.listener = QueueListener(q, self)
        self.listener.start()
