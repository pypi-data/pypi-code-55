import logging
import logging.config
import asyncio

try:
    # Python 3.7 and newer, fast reentrant implementation
    # witohut task tracking (not needed for that when logging)
    from queue import SimpleQueue as Queue
except ImportError:
    from queue import Queue
from typing import List

import yaml

from miniscule.base import read_config

log = logging.getLogger(__name__)


class LocalQueueHandler(logging.handlers.QueueHandler):
    def emit(self, record: logging.LogRecord) -> None:
        # Removed the call to self.prepare(), handle task cancellation
        try:
            self.enqueue(record)
        except asyncio.CancelledError:  # pylint: disable=try-except-raise
            raise
        except Exception:  # pylint: disable=broad-except
            self.handleError(record)


def setup_logging_queue() -> None:
    """Move log handlers to a separate thread.

    Replace handlers on the root logger with a LocalQueueHandler, and start a
    logging.QueueListener holding the original handlers.
    """

    queue = Queue()  # type: ignore
    root = logging.getLogger()
    root.setLevel(logging.INFO)

    handlers: List[logging.Handler] = []

    handler = LocalQueueHandler(queue)
    root.addHandler(handler)
    for h in root.handlers[:]:
        if h is not handler:
            root.removeHandler(h)
            handlers.append(h)

    listener = logging.handlers.QueueListener(
        queue, *handlers, respect_handler_level=True
    )
    listener.start()


def init_logging(config=None, key="log_config", asynchronous=False):
    """Initialize logging.

    :param config: The configuration dictionary
    :param key: The key under which the path of the logging configuration is
        stored.

    :returns: Nothing
    """
    path = None
    try:
        path = (config or read_config()).get(key)
    except FileNotFoundError:
        pass
    if path is None:
        log.debug("No logging configuration specified")
        return

    with open(path, "r") as handle:
        log_config = yaml.load(handle.read(), Loader=yaml.SafeLoader)
        logging.config.dictConfig(log_config)

    if asynchronous:
        setup_logging_queue()
