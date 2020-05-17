"""This module contains all classes and functions for the controller app.

Classes:
    Controller: AMNES Controller application.
    RemoteControllerManager: Remote manager for AMNES Controller instance.
"""

import os
import signal
import sys
from contextlib import contextmanager
from pathlib import Path
from threading import Lock, Thread
from typing import Dict, Iterator, Optional

import Pyro5.api as Pyro5

from ...core.amnes_project import AmnesProject
from ...data.database.database_adapter import PostgresqlAdapter, SqliteDatabaseAdapter
from ...data.manager.storage_backend import StorageBackend
from ...data.manager.storage_backend_peewee import StorageBackendPeewee
from ..app import AmnesRemoteException, ExecutionApp
from .config import ControllerConfiguration
from .project_execution import ProjectExecutionManager
from .resultmanager import ExperimentReference, RemoteResultManager, ResultManager
from .storage import PostgresConfigTree


class Controller(
    ExecutionApp[ControllerConfiguration]
):  # pylint: disable=unsubscriptable-object
    """AMNES Controller application.

    Attributes:
        configuration (ControllerConfiguration): Initialized configuration for
                                                 the execution application.
        base (str): AMNES base directory for execution application.
    """

    APPID = "controller"

    def __init__(
        self, configuration: ControllerConfiguration, base: str, debug: bool
    ) -> None:
        """Constructor method for controller application.

        Args:
            configuration (ControllerConfiguration): Initialized configuration for
                                                     the execution application.
            base (str): AMNES base directory for execution application.
            debug (bool): If debug messages should be logged.
        """
        super().__init__(Controller.APPID, configuration, base, debug)
        self.__daemon: Optional[Pyro5.Daemon] = None
        self.__resultmanager: Optional[ResultManager] = None
        self.storage = None
        self.current_experiment = None

    @property
    def storage(self) -> Optional[StorageBackend]:
        """Optional[StorageBackend]: Storage backend used for persistent storage.

        Returns:
            Optional[StorageBackend]: Storage backend used for persistent storage.
        """
        return self.__storage

    @storage.setter
    def storage(self, storage: Optional[StorageBackend]) -> None:
        """Set storage backend used for persistent storage.

        Args:
            storage (Optional[StorageBackend]): Storage backend used for
                                                persistent storage.
        """
        self.__storage: Optional[StorageBackend] = storage

    @property
    def current_experiment(self) -> Optional[ExperimentReference]:
        """Optional[ExperimentReference]: Experiment which is currently running.

        May be None, if no experiment is currently executed.

        Returns:
            Optional[ExperimentReference]: Experiment which is currently running.
        """
        return self.__current_experiment

    @current_experiment.setter
    def current_experiment(
        self, current_experiment: Optional[ExperimentReference]
    ) -> None:
        """Sets currently running experiment.

        Args:
            current_experiment (Optional[ExperimentReference]): Experiment which is
                                                                currently running.
        """
        self.__current_experiment: Optional[ExperimentReference] = current_experiment

    def logic(self) -> None:
        """AMNES Controller application logic."""
        self.logger.info("Connecting to storage backend ...")
        self.__connect_storage_backend()
        self.logger.info("Connection to storage backend established.")
        self.logger.info("Initializing and starting Result Manager ...")
        self.__resultmanager = ResultManager(
            self.logger.getChild(ResultManager.LOGID), self
        )
        resultmanager_thread = Thread(
            name="ResultManager", target=self.__run_resultmanager
        )
        resultmanager_thread.daemon = False
        resultmanager_thread.start()
        self.logger.info("Result Manager successfully started.")
        self.logger.info("Initializing Pyro5 endpoint ...")
        self.__daemon = Pyro5.Daemon(
            host=self.configuration.execution.address,
            port=self.configuration.execution.port,
        )
        self.__daemon.register(
            RemoteControllerManager(self), RemoteControllerManager.PYROID
        )
        self.__daemon.register(
            RemoteResultManager(self.__resultmanager), RemoteResultManager.PYROID
        )
        self.logger.info("Pyro5 endpoint initialized.")
        self.logger.info(
            "AMNES Controller started successfully, accepting connections now."
        )
        self.__daemon.requestLoop()

    def __run_resultmanager(self) -> None:
        """Run result manager if available.

        Should be run in a seperate thread.

        Raises:
            ValueError: If result manager is not initialized.
        """
        if self.__resultmanager:
            self.__resultmanager.execute()
        else:
            self.logger.error("Result Manager is not initialized.")
            raise ValueError("Result Manager is not initialized.")

    def __connect_storage_backend(self) -> None:
        """Initialize connection to storage backend."""
        dataroot = f"{self.base}{os.path.sep}controller{os.path.sep}data"
        static_files_dir = f"{dataroot}{os.path.sep}static"
        Path(static_files_dir).mkdir(parents=True, exist_ok=True)
        storage_logger = self.logger.getChild("storage")
        if self.configuration.controller.backend == "sqlite":
            self.storage = StorageBackendPeewee(
                storage_logger,
                SqliteDatabaseAdapter(
                    f"{dataroot}{os.path.sep}db.sqlite",
                    pragmas={"foreign_keys": 1},
                    timeout=30,
                ),
                static_files_dir,
            )
            return
        if self.configuration.controller.backend == "postgres":
            postgres: Optional[
                PostgresConfigTree
            ] = self.configuration.controller.postgres
            if postgres is None:
                raise ValueError("Postgres configuration expected but not found.")
            self.storage = StorageBackendPeewee(
                storage_logger,
                PostgresqlAdapter(
                    postgres.database,
                    host=postgres.host,
                    port=postgres.port,
                    user=postgres.user,
                    password=postgres.password,
                ),
                static_files_dir,
            )
            return

    def shutdown(self) -> None:
        """AMNES Controller application shutdown handler."""
        self.logger.info(
            "Received shutdown signal for AMNES Controller, shutting down ..."
        )
        if self.__daemon:
            self.__daemon.shutdown()
        if self.__resultmanager:
            self.__resultmanager.shutdown()
        self.logger.info("AMNES Controller stopped gracefully, exiting now.")
        sys.exit(0)

    def import_project(self, yamlconfig: Dict) -> None:
        """Imports AMNES Project into persistent data backend.

        Args:
            yamlconfig (Dict): Configuration dictionary from YAML loading which
                               should be imported and set as current project.

        Raises:
            ValueError: If storage backend is not available or project with
                        given slug already exists.
        """
        self.logger.info("Loading AMNES Project configuration from CTL ...")
        project: AmnesProject = AmnesProject.create_amnes_project(yamlconfig)
        self.__feature_check_import(project)
        self.logger.info(
            f"AMNES Project '{project.slug}' successfully loaded from configuration."
        )
        self.logger.info("Inserting AMNES Project into storage backend ...")
        if self.storage:
            if self.storage.import_amnes_project(project) > 0:
                self.logger.info(
                    f"AMNES Project '{project.slug}' successfully imported."
                )
            else:
                self.logger.error(
                    f"AMNES Project with slug '{project.slug}' already exists."
                )
                raise ValueError(
                    f"AMNES Project with slug '{project.slug}' already exists."
                )
        else:
            self.logger.error("No storage backend available!")
            raise ValueError("No storage backend available!")

    def start_project(self, project: str) -> None:
        """Starts AMNES Project execution.

        Args:
            project (str): Slug of imported project which should be started.

        Raises:
            ValueError: If storage backend is not available or project with
                        given slug does not exist.
        """
        self.__check_project_slug(project)
        if self.storage:
            amnes_project = self.storage.get_amnes_project_by_slug(project)
            if amnes_project:
                execmanger = ProjectExecutionManager(
                    self.logger.getChild(ProjectExecutionManager.LOGID),
                    amnes_project,
                    self,
                )
                execmanger.run()
            else:
                self.logger.error(f"AMNES Project '{project}' does not exist.")
                raise ValueError(f"AMNES Project '{project}' does not exist.")
        else:
            self.logger.error("No Storage Backend available!")
            raise ValueError("No Storage Backend available!")

    def __feature_check_import(self, project: AmnesProject) -> None:
        """Check for used features which are not implemented yet.

        Args:
            project: Loaded AMNES Project which should be checked for
                     usage of not implemented features.
        """
        for node in project.template.nodes:
            for task in node.tasks:
                if len(task.files.keys) > 0:
                    self.logger.warning(
                        f"Task '{task.slug}' of node '{node.slug}' "
                        + "has files specified but feature is not implemented yet."
                    )

    @staticmethod
    def __check_project_slug(project: str) -> None:
        """Check if project slug is invalid.

        Args:
            project (str): Slug of project which should be checked.

        Raises:
            TypeError: If slug is not of type str.
            ValueError: If slug string is empty or only consists of whitespace.
        """
        if not isinstance(project, str):
            raise TypeError("Project slug is not of type string.")
        if (not project) or (project.isspace()):
            raise ValueError("The specified project slug must not be empty.")


class RemoteControllerManager:
    """Remote manager for AMNES Controller instance."""

    PYROID = "rmtcontrollermngr"

    def __init__(self, controller: Controller) -> None:
        """Remote controller manager constructor method.

        Args:
            controller (Controller): Linked controller which should be managed.
        """
        self.__controller = controller
        self.__lock = Lock()

    @contextmanager
    def __exclusive(self) -> Iterator[None]:
        """Contextmanager for exclusive command execution in remote manager.

        Yields:
            None: No yield value available.

        Raises:
            ConnectionError: If exclusive command execution is blocked.
        """
        if self.__lock.acquire(blocking=True, timeout=2):
            try:
                yield
            finally:
                self.__lock.release()
        else:
            raise ConnectionError("Remote Manager currently blocked, try again later.")

    @Pyro5.expose  # type: ignore
    def import_project(self, yamlconfig: Dict) -> None:
        """Imports AMNES Project into persistent data backend.

        Args:
            yamlconfig (Dict): Configuration dictionary from YAML loading which
                               should be imported and set as current project.
        """
        with self.__exclusive():
            with AmnesRemoteException.exception_handling():
                self.__controller.import_project(yamlconfig)

    @Pyro5.expose  # type: ignore
    def start_project(self, project: str) -> None:
        """Starts AMNES Project execution.

        Args:
            project (str): Slug of imported project which should be started.
        """
        with self.__exclusive():
            with AmnesRemoteException.exception_handling():
                self.__controller.start_project(project)

    @Pyro5.expose  # type: ignore
    def stop_project(self) -> None:
        """Stops AMNES Project execution."""
        with self.__exclusive():
            with AmnesRemoteException.exception_handling():
                pass

    @staticmethod
    @Pyro5.expose  # type: ignore
    @Pyro5.oneway  # type: ignore
    def shutdown() -> None:
        """Shutdowns linked controller by SIGINT signal.

        This does not return a result and will not block on execution.
        As it only sends SIGINT, it is not required to run it exclusively.
        """
        with AmnesRemoteException.exception_handling():
            os.kill(os.getpid(), signal.SIGINT)

    @staticmethod
    @Pyro5.expose  # type: ignore
    @Pyro5.oneway  # type: ignore
    def kill() -> None:
        """Immediately calls operating system exit for linked controller.

        This does not return a result and will not block on execution.
        As it directly calls `os._exit()?, it is not required to run it exclusively.
        """
        with AmnesRemoteException.exception_handling():
            os._exit(2)  # pylint: disable=protected-access
