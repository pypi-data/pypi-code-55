"""This module contains classes and functions for AMNES project execution.

Classes:
    TaskExecutionManager: Manager class for executing one node task.
"""

import traceback
from logging import Logger
from typing import TYPE_CHECKING, Dict

import Pyro5.api as Pyro5
from Pyro5.errors import CommunicationError, PyroError

from ...core.node_task import NodeTask
from ...core.worker_endpoint import WorkerEndpoint
from ..logging import InstanceLogging
from ..worker.app import RemoteWorkerManager, TaskExecutionResult

if TYPE_CHECKING:
    from .app import Controller  # pylint: disable=cyclic-import


class TaskExecutionManager(InstanceLogging):
    """Manager class for executing one node task."""

    LOGID = "taskexecutionmanager"

    PYRO_CMD_TIMEOUT = 5
    PYRO_TASK_TIMEOUT = 3600

    def __init__(
        self,
        logger: Logger,
        controller: "Controller",
        endpoint: WorkerEndpoint,
        task: NodeTask,
        status: Dict[str, bool],
        identifier: str,
    ) -> None:
        """Experiment execution manager constructor method.

        Args:
            logger (Logger): Logger for object instance.
            controller (Controller): Controller which started the task execution.
            endpoint (WorkerEndpoint): Endpoint of node on which the task should
                                       be executed.
            task (NodeTask): Task which should be executed by the manager.
            status (Dict[str, bool]): Status dictionary for task's stage.
            identifier (str): Thread identifier for this task execution manager.
        """
        InstanceLogging.__init__(self, logger)
        self.__controller: "Controller" = controller
        self.__endpoint: WorkerEndpoint = endpoint
        self.__task: NodeTask = task
        self.__status: Dict[str, bool] = status
        self.__identifier: str = identifier

    def run(self) -> None:
        """Run task execution."""
        self.logger.info(
            "Initializing worker connection to "
            + f"'[{self.__endpoint.address}]:{self.__endpoint.port}' ..."
        )
        try:
            manager = self.__init_manager()
        except PyroError:
            self.logger.error(
                f"Could not initialize remote worker manager:\n"
                + f"{traceback.format_exc()}"
            )
        manager._pyroTimeout = (  # type: ignore # pylint: disable=protected-access
            TaskExecutionManager.PYRO_TASK_TIMEOUT
        )
        self.logger.info(
            "Worker connection to "
            + f"'[{self.__endpoint.address}]:{self.__endpoint.port}' initialized."
        )
        self.logger.info(
            f"Executing task '{self.__task.slug}' "
            + f"on worker '[{self.__endpoint.address}]:{self.__endpoint.port}' ..."
        )
        result = TaskExecutionResult(  # pylint: disable=no-value-for-parameter
            # type: ignore
            manager.execute_module(
                self.__task.slug,
                self.__task.module,
                self.__task.params,
                self.__task.files,
                self.__controller.configuration.execution.address,
                self.__controller.configuration.execution.port,
            )
        )
        self.logger.info(
            f"Finished task '{self.__task.slug}' "
            + f"on worker '[{self.__endpoint.address}]:{self.__endpoint.port}' "
            + f"with result '{result}'."
        )
        self.__status[self.__identifier] = result is TaskExecutionResult.SUCCESS

    def __init_manager(self) -> RemoteWorkerManager:
        """Initializes Pyro5 proxy for remote worker manager of node.

        Returns:
            RemoteWorkerManager: Pyro5 proxy for remote worker manager of node.

        Raises:
            CommunicationError: If remote worker manager test fails.
        """
        manager = Pyro5.Proxy(
            f"PYRO:{RemoteWorkerManager.PYROID}"
            + f"@{self.__endpoint.address}"
            + f":{self.__endpoint.port}"
        )
        manager._pyroTimeout = (  # pylint: disable=protected-access
            TaskExecutionManager.PYRO_CMD_TIMEOUT
        )
        if manager.ping() != RemoteWorkerManager.PINGMSG:
            raise CommunicationError(
                "Could not successfully test remote worker manager!"
            )
        return manager
