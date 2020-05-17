"""This module contains all classes, functions and decorators for AMNES Logging.

Classes:
    InstanceLogging: Class for adding logger attribute for instances.
    AmnesLogger: Singleton Root Logger for AMNES.
    TraceLogger: Singleton Logger for logging traces of function calls.

Decorators:
    tracelog: Enables trace logging for decorated function.
"""

import logging
import socket
import sys
from functools import wraps
from logging import Formatter, Handler, Logger, NullHandler, StreamHandler
from logging.handlers import SysLogHandler
from typing import Any, Callable, Dict, List, Mapping, Sequence, TypeVar, cast

from ..exec.config import LogDestination
from ..utils.metaclasses import SingletonMeta


class InstanceLogging:  # pylint: disable=too-few-public-methods
    """Class for adding logger attribute for instances.

    Attributes:
        logger (Logger): Logger for object instance.
    """

    def __init__(self, logger: Logger) -> None:
        """Instance logging constructor method.

        Args:
            logger (Logger): Logger for object instance.
        """
        self.__logger: Logger = logger

    @property
    def logger(self) -> Logger:
        """Logger: Logger for object instance.

        Returns:
            Logger: Logger for object instance.
        """
        return self.__logger


class AmnesLogger(
    InstanceLogging, metaclass=SingletonMeta
):  # pylint: disable=too-few-public-methods
    """Singleton Root Logger for AMNES.

    This class uses the Singleton pattern.
    """

    def __init__(self) -> None:
        """Amnes logger constructor method."""
        self.__disable_default_root()
        InstanceLogging.__init__(self, logging.getLogger("amnes"))
        self.logger.setLevel(logging.INFO)

    @staticmethod
    def __disable_default_root() -> None:
        """Disable default root logger."""
        for handler in logging.root.handlers:
            logging.root.removeHandler(handler)
        logging.root.addHandler(NullHandler())


class TraceLogger(InstanceLogging, metaclass=SingletonMeta):
    """Singleton Logger for logging traces of function calls.

    This class uses the Singleton pattern.
    """

    def __init__(self) -> None:
        """Trace logger constructor method."""
        InstanceLogging.__init__(self, AmnesLogger().logger.getChild("trace"))

    def enter(self, cal: Callable) -> None:
        """Log entering event for callable.

        Args:
            cal (Callable): Callable which is entered.
        """
        self.logger.debug(f"Entering: {cal.__qualname__}")

    def leave(self, cal: Callable) -> None:
        """Log leaving event for callable.

        Args:
            cal (Callable): Callable which is left.
        """
        self.logger.debug(f"Leaving: {cal.__qualname__}")


_Function = TypeVar("_Function", bound=Callable[..., Any])


def tracelog(func: _Function) -> _Function:
    """Enables trace logging for decorated function.

    Args:
        func (_Function): Function which should be decorated.

    Returns:
        _Function: Given function decorated with trace logging calls.
    """

    @wraps(func)
    def wrapper(*args: Sequence[Any], **kwargs: Mapping[Any, Any]) -> Any:
        TraceLogger().enter(func)
        value = func(*args, **kwargs)
        TraceLogger().leave(func)
        return value

    return cast(_Function, wrapper)


def create_handlers(destinations: List[LogDestination]) -> List[Handler]:
    """Create list of already configured handlers from logging destination list.

    Args:
        destinations (List[LogDestination]): List of logging destinations from which
                                             handlers should be created.

    Returns:
        List[Handlers]: List of already configured handlers from
                        logging destination list.

    Raises:
        ValueError: If unsupported handler is specified.
    """
    handlers: List[Handler] = []
    for destination in destinations:
        backend = list(destination.keys())[0]
        config = destination[backend]
        if backend == "syslog":
            handlers.append(__create_syslog_handler(config))
        elif backend == "tty":
            handlers.append(__create_stream_handler(config))
        else:
            raise ValueError("Unsupported handler specified.")
    return handlers


LOG_FORMAT: str = "%(levelname)s ~ %(name)s[%(threadName)s]: %(message)s"


def __create_syslog_handler(config: Dict[str, Any]) -> SysLogHandler:
    """Create syslog logging handler from configuration.

    Args:
        config (Dict[str, Any]): Configuration from which the handler should be created.

    Returns:
        Syslog logging handler from configuration.
    """
    socktype = socket.SOCK_STREAM if config["socktype"] == "tcp" else socket.SOCK_DGRAM
    handler = SysLogHandler(
        address=(config["host"], config["port"]), socktype=socktype,
    )
    handler.setFormatter(Formatter(LOG_FORMAT))
    return handler


def __create_stream_handler(config: Dict[str, Any]) -> StreamHandler:
    """Create stream logging handler from configuration.

    Args:
        config (Dict[str, Any]): Configuration from which the handler should be created.

    Returns:
        Stream logging handler from configuration.
    """
    stream = sys.stdout if config["stream"] == "stdout" else sys.stderr
    handler = StreamHandler(stream=stream)
    handler.setFormatter(
        Formatter("%(asctime)s.%(msecs)03d " + LOG_FORMAT, datefmt="%Y-%m-%dT%H:%M:%S")
    )
    return handler
