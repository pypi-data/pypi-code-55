"""This module contains all classes and functions for the worker app.

Classes:
    TaskExecutionResult: Task Execution Results.
    Worker: AMNES Worker application.
    RemoteWorkerManager: Remote manager for AMNES Worker instance.
    TaskFunctionProvider: Provider for functions and methods bound to modules for
                          task execution.
"""

from __future__ import annotations

import ipaddress
import os
import shutil
import socket
import sys
import uuid
from contextlib import contextmanager
from enum import Enum
from importlib import import_module
from pathlib import Path
from threading import Lock
from typing import BinaryIO, Iterator, Optional, Type, TypeVar

import Pyro5.api as Pyro5
from Pyro5.errors import PyroError

from ...core.node_task import NodeTaskFiles, NodeTaskParams
from ..app import AmnesRemoteException, ExecutionApp
from ..controller.resultmanager import RemoteResultManager
from .config import WorkerConfiguration
from .node_module import NodeModule, NodeModuleError

_Module = TypeVar("_Module", bound=NodeModule)


class TaskExecutionResult(Enum):
    """Task Execution Results.

    This enumeration contains all valid results for a task execution.
    """

    def __new__(cls, value: int, doc: str) -> TaskExecutionResult:
        """Custom initializer supporting docstrings for enumeration members.

        Args:
            cls (TaskExecutionResult): TaskExecutionResult class.
            value (int): Internal integer value used for state enum member.
            doc (str): Docstring for state enum member.

        Returns:
            TaskExecutionResult: TaskExecutionResult instance.
        """
        self = object.__new__(cls)
        self._value_ = value
        self.__doc__ = doc
        return self

    SUCCESS = (0, "Task execution was successful.")
    PYTHON_MODULE_NOT_FOUND = (
        11,
        "Could not import python module containing module class.",
    )
    PYTHON_CLASS_NOT_FOUND = (
        12,
        "Could not find python class representing node module.",
    )
    MODULE_NOT_NODEMODULE = (13, "Module is not a subclass of NodeModule.")
    WORKDIR_INIT_FAILED = (14, "Working directory initialization failed.")
    FUNCTIONPROVIDER_INIT_FAILED = (15, "Function provider initialization failed.")
    FAILURE = (255, "Task execution failed.")

    def __str__(self) -> str:
        """Get string representation of enum member.

        Returns:
            str: String representation of enum member.
        """
        return super().__str__().rsplit(".", 1)[-1]


class Worker(
    ExecutionApp[WorkerConfiguration]
):  # pylint: disable=unsubscriptable-object
    """AMNES Worker application.

    Attributes:
        configuration (WorkerConfiguration): Initialized configuration for
                                             the execution application.
        base (str): AMNES base directory for execution application.
    """

    APPID = "worker"

    def __init__(
        self, configuration: WorkerConfiguration, base: str, debug: bool
    ) -> None:
        """Constructor method for worker application.

        Args:
            configuration (WorkerConfiguration): Initialized configuration for
                                                 the worker application.
            base (str): AMNES base directory for worker application.
            debug (bool): If debug messages should be logged.
        """
        super().__init__(Worker.APPID, configuration, base, debug)
        self.__daemon: Optional[Pyro5.Daemon] = None

    def logic(self) -> None:
        """AMNES Worker application logic."""
        self.logger.info("Initializing Pyro5 endpoint ...")
        self.__daemon = Pyro5.Daemon(
            host=self.configuration.execution.address,
            port=self.configuration.execution.port,
        )
        self.__daemon.register(RemoteWorkerManager(self), RemoteWorkerManager.PYROID)
        self.logger.info("Pyro5 endpoint initialized.")
        self.logger.info(
            "AMNES Worker started successfully, accepting connections now."
        )
        self.__daemon.requestLoop()

    def shutdown(self) -> None:
        """AMNES Worker application shutdown handler."""
        self.logger.info("Received shutdown signal for AMNES Worker, shutting down ...")
        if self.__daemon:
            self.__daemon.shutdown()
        self.logger.info("AMNES Worker stopped gracefully, exiting now.")
        sys.exit(0)

    def __module_execute(self, execid: str, module_instance: NodeModule) -> bool:
        """Run `execute` function for given NodeModule instance.

        Args:
            execid (str): Module execution ID used by logging.
            module_instance (NodeModule): NodeModule instance for which `execute`
                                          should be called.

        Returns:
            bool: True, if the `execute` function call was successful,
                  else False.
        """
        success = True
        try:
            module_instance.execute()
        except Exception as exc:  # pylint: disable=broad-except
            success = False
            if isinstance(exc, NodeModuleError):
                module_instance.error = exc
                module_instance.corrupt = False
                self.logger.warning(
                    f"({execid}) Module error occured while running 'execute()': {exc}"
                )
            else:
                module_instance.error = None
                module_instance.corrupt = True
                self.logger.error(
                    f"({execid}) "
                    + f"Uncatched error occured while running 'execute()': {exc}"
                )
        else:
            module_instance.error = None
            module_instance.corrupt = False
        return success

    def __module_collect(self, execid: str, module_instance: NodeModule) -> bool:
        """Run `collect` function for given NodeModule instance.

        Args:
            execid (str): Module execution ID used by logging.
            module_instance (NodeModule): NodeModule instance for which `collect`
                                          should be called.

        Returns:
            bool: True, if the `collect` function call was successful,
                  else False.
        """
        success = True
        try:
            module_instance.collect()
        except Exception as exc:  # pylint: disable=broad-except
            success = False
            if isinstance(exc, NodeModuleError):
                module_instance.error = exc
                module_instance.corrupt = False
                self.logger.warning(
                    f"({execid}) Module error occured while running 'execute()': {exc}"
                )
            else:
                module_instance.error = None
                module_instance.corrupt = True
                self.logger.error(
                    f"({execid}) "
                    + f"Uncatched error occured while running 'execute()': {exc}"
                )
        else:
            module_instance.error = None
            module_instance.corrupt = False
        return success

    def __module_cleanup(self, execid: str, module_instance: NodeModule) -> bool:
        """Run `cleanup` function for given NodeModule instance.

        Args:
            execid (str): Module execution ID used by logging.
            module_instance (NodeModule): NodeModule instance for which `cleanup`
                                          should be called.

        Returns:
            bool: True, if the `cleanup` function call was successful,
                  else False.
        """
        success = True
        try:
            module_instance.cleanup()
        except Exception as exc:  # pylint: disable=broad-except
            success = False
            if isinstance(exc, NodeModuleError):
                module_instance.error = exc
                module_instance.corrupt = False
                self.logger.warning(
                    f"({execid}) Module error occured while running 'execute()': {exc}"
                )
            else:
                module_instance.error = None
                module_instance.corrupt = True
                self.logger.error(
                    f"({execid}) "
                    + f"Uncatched error occured while running 'execute()': {exc}"
                )
        return success

    def __module_init(
        self,
        execid: str,
        modulecls: Type[_Module],
        params: NodeTaskParams,
        files: NodeTaskFiles,
        workdir: str,
    ) -> Optional[NodeModule]:
        """Initializes an instance of the given module class.

        Args:
            execid (str): Module execution ID used by logging.
            modulecls (Type): Class from which an instance should be created.
            params (NodeTaskParams): Parameters used for module execution.
            files (NodeTaskFiles): Files used for module execution.
            workdir (str): Working directory for the node module instance.

        Returns:
            Optional[NodeModule]: Node modules instances created from the given module
                                  class or None if initialization failed.
        """
        try:
            return modulecls(params, files, workdir)
        except Exception as exc:  # pylint: disable=broad-except
            if isinstance(exc, NodeModuleError):
                self.logger.warning(
                    f"({execid}) Module error occured during instantiation: {exc}"
                )
            else:
                self.logger.error(
                    f"({execid}) "
                    + f"Uncatched error occured while during instantiation: {exc}"
                )
            return None

    def execute_module(  # pylint: disable=too-many-locals,too-many-return-statements
        self,
        execid: str,
        module: str,
        params: NodeTaskParams,
        files: NodeTaskFiles,
        controller_address: str,
        controller_port: int,
    ) -> TaskExecutionResult:
        """Executes module with given parameters and files.

        Args:
            execid (str): Module execution ID used by logging.
            module (str): Module which should be executed.
            params (NodeTaskParams): Parameters used for module execution.
            files (NodeTaskFiles): Files used for module execution.
            controller_address (str): Address of controller pyro5 endpoint.
            controller_port (int): Port of controller pyro5 endpoint.

        Returns:
            TaskExecutionResult: Task execution result after execution.
        """
        self.logger.info(f"Loading module '{module}' ...")
        (module_path, module_class) = tuple(module.rsplit(".", 1))
        try:
            modulecls: Type = getattr(import_module(module_path), module_class)
        except ModuleNotFoundError as merr:
            self.logger.error(f"Could not import python module '{module_path}': {merr}")
            return TaskExecutionResult.PYTHON_MODULE_NOT_FOUND
        except AttributeError as aerr:
            self.logger.error(
                "Could not import python class "
                + f"'{module_class}' from '{module_path}': {aerr}"
            )
            return TaskExecutionResult.PYTHON_CLASS_NOT_FOUND
        if not issubclass(modulecls, NodeModule):
            self.logger.error(f"Specified module '{module}' is not a NodeModule!")
            return TaskExecutionResult.MODULE_NOT_NODEMODULE
        self.logger.info(f"Successfully loaded node module '{module}'.")
        success: bool = True
        workdir = f"{self.base}{os.path.sep}worker{os.path.sep}{uuid.uuid4()}"
        self.logger.info(f"Preparing working directory '{workdir}' ...")
        try:
            Path(workdir).mkdir(parents=True)
        except OSError as oserr:
            self.logger.error(f"Could not prepare working directory: {oserr}")
            return TaskExecutionResult.WORKDIR_INIT_FAILED
        self.logger.info("Working directory prepared successfully.")
        self.logger.info("Initializing function provider ...")
        try:
            function_provider = TaskFunctionProvider(
                controller_address, controller_port
            )
        except PyroError as perr:
            self.logger.error(f"Function provider initialization failed: {perr}")
            return TaskExecutionResult.FUNCTIONPROVIDER_INIT_FAILED
        self.logger.info("Function provider initialized.")
        self.logger.info("Creating module instance ...")
        module_instance = self.__module_init(execid, modulecls, params, files, workdir)
        if module_instance is None:
            return TaskExecutionResult.FAILURE
        module_instance.store_io = function_provider.store_io  # type: ignore
        self.logger.info("Module instance created.")
        self.logger.info("Start execution of node module stages ...")
        success = self.__module_execute(execid, module_instance)
        success = self.__module_collect(execid, module_instance) & success
        success = self.__module_cleanup(execid, module_instance) & success
        result = TaskExecutionResult.SUCCESS if success else TaskExecutionResult.FAILURE
        self.logger.info(f"Execution finished with result '{result}'.")
        shutil.rmtree(workdir, ignore_errors=True)
        return result


class RemoteWorkerManager:
    """Remote manager for AMNES Worker instance."""

    PYROID = "rmtworkermngr"
    PINGMSG = "pong"

    def __init__(self, worker: Worker) -> None:
        """Remote worker manager constructor method.

        Args:
            worker (Worker): Linked worker which should be managed.
        """
        self.__worker = worker
        self.__lock = Lock()

    @contextmanager
    def __exclusive(self) -> Iterator[None]:
        """Contextmanager for exclusive operation execution in remote manager.

        Yields:
            None: No yield value available.

        Raises:
            ConnectionError: If exclusive operation execution is blocked.
        """
        if self.__lock.acquire(blocking=True, timeout=2):
            try:
                yield
            finally:
                self.__lock.release()
        else:
            raise ConnectionError("Remote Manager currently blocked, try again later.")

    @staticmethod
    @Pyro5.expose  # type: ignore
    def ping() -> str:
        """Returns remote worker manager ping message.

        Returns:
            str: Remote worker manager ping message.
        """
        return RemoteWorkerManager.PINGMSG

    @Pyro5.expose  # type: ignore
    def execute_module(
        self,
        execid: str,
        module: str,
        params: NodeTaskParams,
        files: NodeTaskFiles,
        controller_address: str,
        controller_port: int,
    ) -> TaskExecutionResult:
        """Executes module with given parameters and files.

        Args:
            execid (str): Module execution ID used by logging.
            module (str): Module which should be executed.
            params (NodeTaskParams): Parameters used for module execution.
            files (NodeTaskFiles): Files used for module execution.
            controller_address (str): Address of controller pyro5 endpoint.
            controller_port (int): Port of controller pyro5 endpoint.

        Returns:
            TaskExecutionResult: Task execution result after execution.
        """
        with AmnesRemoteException.exception_handling():
            return self.__worker.execute_module(
                execid, module, params, files, controller_address, controller_port
            )


class TaskFunctionProvider:  # pylint: disable=too-few-public-methods
    """Provider for functions and methods bound to modules for task execution."""

    def __init__(self, controller_address: str, controller_port: int) -> None:
        """Task function provider constructor method.

        Args:
            controller_address (str): Address of controller pyro5 endpoint.
            controller_port (int): Port of controller pyro5 endpoint.
        """
        rmngr: RemoteResultManager = Pyro5.Proxy(
            f"PYRO:{RemoteResultManager.PYROID}@{controller_address}:{controller_port}"
        )
        rmngr._pyroTimeout = 10  # type: ignore
        rmngr.ping()
        self.__resultmanager = rmngr

    def store_io(self, stream: BinaryIO) -> None:
        """Method for storing content of an IO stream into a persistent object.

        This method can be bound to a node module instance.

        Args:
            stream (BinaryIO): IO stream which should be stored persistently.
        """
        token, (address, port) = self.__resultmanager.request_filetransfer()
        if isinstance(ipaddress.ip_address(address), ipaddress.IPv6Address):
            family = socket.AF_INET6
        else:
            family = socket.AF_INET
        with socket.socket(family, socket.SOCK_STREAM) as sock:
            sock.connect((address, port))
            sock.sendall(token.encode())
            sock.sendfile(stream)
