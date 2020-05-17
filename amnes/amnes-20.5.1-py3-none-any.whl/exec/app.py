"""This module contains all classes and functions for a basic execution app.

Classes:
    AmnesRemoteException: Exception raised by AMNES Components to pass errors
                          to remote destinations.
    ExecutionApp: Abstract generic execution application used as base for
                  AMNES components.
"""

from __future__ import annotations

import logging
import signal
import sys
import threading
import traceback as tb
from abc import ABCMeta, abstractmethod
from contextlib import contextmanager
from logging import Logger
from threading import Lock
from types import FrameType, TracebackType
from typing import Dict, Generic, Iterator, Optional, Type, TypeVar

from Pyro5.errors import get_pyro_traceback
from Pyro5.serializers import SerializerBase

from ..core.node_task import NodeTaskFiles, NodeTaskParams
from ..exec.config import ExecutionConfiguration
from ..exec.logging import AmnesLogger, InstanceLogging, create_handlers
from . import patcher

_Config = TypeVar("_Config", bound=ExecutionConfiguration)


class AmnesRemoteException(Exception):
    """Exception raised by AMNES Components to pass errors to remote destinations."""

    LOGGER: Optional[Logger] = None

    @staticmethod
    def deserialize(
        classname: str, indict: Dict  # pylint: disable=unused-argument
    ) -> AmnesRemoteException:
        """Deserialize AmnesRemoteException dictionary from Pyro communication.

        Args:
            classname (str): Name of class which was serialized.
            indict (Dict): Serialized representation of instance as dictionary.

        Returns:
            AmnesRemoteException: Instance deserialized from dictionary representation.
        """
        exc = AmnesRemoteException()
        # pylint: disable=protected-access
        exc._pyroTraceback = indict["attributes"]["_pyroTraceback"]  # type: ignore
        return exc

    @staticmethod
    @contextmanager
    def exception_handling() -> Iterator[None]:
        """Contextmanager for exception handling of worker remote exceptions.

        Yields:
            None: No yield value available.

        Raises:
            AmnesRemoteException: If any exception was raised in context.
        """
        try:
            yield
        except Exception as exc:
            type_, value, traceback = sys.exc_info()
            AmnesRemoteException.exception_hook_sys(type_, value, traceback)
            raise AmnesRemoteException() from exc

    @staticmethod
    def exception_hook_sys(
        type_: Optional[Type[BaseException]],
        value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        """Python exception hook for default system.

        Args:
            type_ (Type[BaseException]): Type of raised exception.
            value (BaseException): Raised exception.
            traceback (TracebackType): Traceback of raised exception.
        """
        if hasattr(value, "_pyroTraceback"):
            AmnesRemoteException.__log(
                logging.ERROR, "".join(get_pyro_traceback(type_, value, traceback))
            )
        else:
            AmnesRemoteException.__log(
                logging.ERROR, "".join(tb.format_exception(type_, value, traceback))
            )

    @staticmethod
    def exception_hook_threads(args) -> None:  # type: ignore
        """Python exception hook for threads.

        Args:
            args (ExceptionHookArgs): Exception hook arguments.
        """
        AmnesRemoteException.exception_hook_sys(
            args.exc_type, args.exc_value, args.exc_traceback
        )

    @staticmethod
    def __log(level: int, msg: str) -> None:
        """Logging function with STDERR fallback.

        Args:
            level (int): Log level used for logging.
            msg (str): Message which should be logged.
        """
        if AmnesRemoteException.LOGGER is None:
            print(
                "Logger for exceptions not configured, using fallback!", file=sys.stderr
            )
            print(msg, file=sys.stderr)
        else:
            AmnesRemoteException.LOGGER.log(level, msg)


class ExecutionApp(Generic[_Config], InstanceLogging, metaclass=ABCMeta):
    """Abstract generic execution application used as base for AMNES components.

    Every AMNES component which should be executed as a service must inherit
    from this class.

    Generic Types:
        _Config: Subclass of `ExecutionConfiguration`.

    Attributes:
        configuration (_Config): Initialized configuration for the execution
                                 application.
        base (str): AMNES base directory for execution application.
    """

    def __init__(self, appid: str, configuration: _Config, base: str, debug: bool):
        """Generic constructor method for execution application.

        Args:
            appid (str): Application ID used for logging.
            configuration (_Config): Initialized configuration for the execution
                                     application.
            base (str): AMNES base directory for execution application.
            debug (bool): If debug messages should be logged.
        """
        threading.current_thread().name = "App"
        patcher.patch()
        self.__set_configuration(configuration)
        self.__set_base(base)
        InstanceLogging.__init__(self, self.__configure_logging(appid, debug))
        self.__shutdown_lock = Lock()
        self.__register_serializer()

    def __configure_logging(self, appid: str, debug: bool) -> Logger:
        """Configure logging for execution application.

        Args:
            appid (str): Application ID used for logging.
            debug (bool): If debug messages should be logged.

        Returns:
            Logger: Logger instance for InstanceLogging constructor.
        """
        app_logger = AmnesLogger().logger.getChild(appid)
        app_logger.setLevel(logging.DEBUG if debug else logging.INFO)
        for handler in create_handlers(self.configuration.execution.logging):
            app_logger.addHandler(handler)
        AmnesRemoteException.LOGGER = app_logger
        if app_logger.level == logging.DEBUG:
            app_logger.debug("Debug Level for Logging enabled.")
        return app_logger

    def execute(self) -> None:
        """Execution method which is called to start the application.

        Before calling `self.logic()`, a signal hander is registered
        to catch `SIGINT` and call `self.shutdown()` if it is catched.
        """

        def signalhandler(
            sig: int, frame: FrameType  # pylint: disable=unused-argument
        ) -> None:
            if self.__shutdown_lock.acquire():
                self.shutdown()
                sys.exit(0)
            # Only one SIGINT handler should run.
            # This call will end with an exit, so lock is not released.

        signal.signal(signal.SIGINT, signalhandler)
        sys.excepthook = AmnesRemoteException.exception_hook_sys
        threading.excepthook = AmnesRemoteException.exception_hook_threads
        self.logic()

    @abstractmethod
    def logic(self) -> None:
        """Abstract method running the main logic of the execution application.

        This method must be implemented by all subclasses of `ExecutionApp` and
        is called by `self.execute()` on application execution.
        """

    @abstractmethod
    def shutdown(self) -> None:
        """Abstract method for shutting down the execution application.

        This method must be implemented by all subclasses of `ExecutionApp` and
        is called on `SIGINT` to shutdown the application.
        If no `sys.exit()` is called in the implementation of this method,
        the application will exit with exit code 0.
        """

    @property
    def configuration(self) -> _Config:
        """_Config: Initialized configuration for the execution application.

        Returns:
            _Config: Initialized configuration for the execution application.
        """
        return self.__configuration

    def __set_configuration(self, configuration: _Config) -> None:
        """Set configuration for the execution application.

        Args:
            configuration (_Config): Initialized configuration for the execution
                                     application.
        """
        self.__configuration: _Config = configuration

    @property
    def base(self) -> str:
        """str: AMNES base directory for execution application.

        Returns:
            str: AMNES base directory for execution application.
        """
        return self.__base

    def __set_base(self, base: str) -> None:
        """Set AMNES base directory for execution application.

        Args:
            base (str): AMNES base directory for execution application.
        """
        self.__base: str = base

    @staticmethod
    def __register_serializer() -> None:
        """Register serializers and deserializers for Pyro communication."""
        SerializerBase.register_dict_to_class(
            f"{AmnesRemoteException.__module__}.{AmnesRemoteException.__name__}",
            AmnesRemoteException.deserialize,
        )
        SerializerBase.register_class_to_dict(NodeTaskParams, NodeTaskParams.serialize)
        SerializerBase.register_dict_to_class(
            f"{NodeTaskParams.__module__}.{NodeTaskParams.__name__}",
            NodeTaskParams.deserialize,
        )
        SerializerBase.register_class_to_dict(NodeTaskFiles, NodeTaskFiles.serialize)
        SerializerBase.register_dict_to_class(
            f"{NodeTaskFiles.__module__}.{NodeTaskFiles.__name__}",
            NodeTaskFiles.deserialize,
        )
