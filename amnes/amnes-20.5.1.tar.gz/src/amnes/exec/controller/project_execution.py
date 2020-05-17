"""This module contains classes and functions for AMNES project execution.

Classes:
    ProjectExecutionManager: Manager class for executing an entire AMNES Project.
"""

from logging import Logger
from typing import TYPE_CHECKING, Dict, Iterator, List, Tuple

import Pyro5.api as Pyro5
from Pyro5.errors import PyroError

from ...core.amnes_project import AmnesProject
from ...core.experiment import ConcreteExperiment, ExperimentState
from ...core.experiment_sequence import ExperimentSequence
from ...core.worker_endpoint import WorkerEndpoint
from ...data.manager.storage_backend import ConcreteExperimentReference
from ..logging import InstanceLogging
from ..worker.app import RemoteWorkerManager
from .experiment_execution import ExperimentExecutionManager
from .resultmanager import ExperimentReference

if TYPE_CHECKING:
    from .app import Controller  # pylint: disable=cyclic-import


class ProjectExecutionManager(InstanceLogging):
    """Manager class for executing an entire AMNES Project."""

    LOGID = "projectexecutionmanager"

    DEFAULT_TIMEOUT = 20

    def __init__(
        self, logger: Logger, project: AmnesProject, controller: "Controller"
    ) -> None:
        """Project execution manager constructor method.

        Args:
            logger (Logger): Logger for object instance.
            project (AmnesProject): Project to be executed.
            controller (Controller): Controller which started the project execution.
        """
        InstanceLogging.__init__(self, logger)
        self.__project: AmnesProject = project
        self.__controller: "Controller" = controller
        self.__workers: Dict[str, Tuple[WorkerEndpoint, RemoteWorkerManager]] = {}

    def run(self) -> None:
        """Run project execution."""
        self.logger.info(
            f"Execution of AMNES Project '{self.__project.slug}' started ..."
        )
        self.logger.info("Moving CREATED experiments to PENDING state ...")
        self.logger.info(
            f"{self.__schedule_experiments()} experiments were moved to PENDING state."
        )
        self.logger.info("Initializing remote worker managers for every node ...")
        self.logger.info(
            f"{self.__init_managers()} remote worker managers were initialized."
        )
        self.logger.info("Checking for availability of all workers ...")
        unavailable = self.__check_managers()
        if unavailable:
            errstr = "Following workers are not available:\n"
            for endpoint in unavailable:
                errstr = errstr + f"~ '{endpoint.address}:{endpoint.port}'\n"
            self.logger.error(errstr)
            return
        self.logger.info("All workers available.")
        self.logger.info("Starting experiment executions ...")
        for sequence, experiment, repetition in self.__pending_experiments():
            ref = ExperimentReference(
                concrete_experiment_reference=ConcreteExperimentReference(
                    concrete_experiment_slug=experiment.slug,
                    sequence_parameter_set_slug=sequence.pset.slug,
                    amnes_project_slug=self.__project.slug,
                ),
                repetition=repetition,
            )
            self.__controller.current_experiment = ref
            self.logger.info(
                f"Initiate execution of '"
                + f"{sequence.pset.slug}"
                + f"${experiment.slug}"
                + f"${repetition}"
                + "' ..."
            )
            self.__update_experiment_state(
                sequence, experiment, repetition, ExperimentState.RUNNING
            )
            result = ExperimentExecutionManager(
                self.__controller.logger.getChild(ExperimentExecutionManager.LOGID),
                self.__controller,
                experiment,
                repetition,
            ).run()
            self.__update_experiment_state(sequence, experiment, repetition, result)
            self.logger.info(
                f"Execution finished for '"
                + f"{sequence.pset.slug}"
                + f"${experiment.slug}"
                + f"${repetition}"
                + f"' with result {result}"
                + "."
            )
            self.__controller.current_experiment = None
        self.logger.info("All pending experiments were processed.")
        self.logger.info(
            f"Execution of AMNES Project '{self.__project.slug}' finished."
        )

    def __update_experiment_state(
        self,
        sequence: ExperimentSequence,
        experiment: ConcreteExperiment,
        repetition: int,
        state: ExperimentState,
    ) -> None:
        """Update experiment state of specific repetition.

        Args:
            sequence (ExperimentSequence): Sequences to which the experiment belongs to.
            experiment (ConcreteExperiment): Experiment reference to be updated.
            repetition (int): Repetition whoes state should be updated.
            state (ExperimentState): New state of the repetition which should be
                                     updated.

        Raises:
            ValueError: If storage backend is not available.
        """
        experiment.set_state(repetition, state)
        if self.__controller.storage:
            self.__controller.storage.update_experiment_states(
                {repetition: state}.items(),
                ConcreteExperimentReference(
                    concrete_experiment_slug=experiment.slug,
                    sequence_parameter_set_slug=sequence.pset.slug,
                    amnes_project_slug=self.__project.slug,
                ),
            )
        else:
            self.logger.error("No Storage Backend available!")
            raise ValueError("No Storage Backend available!")

    def __schedule_experiments(self) -> int:
        """Set all CREATED experiments of project to PENDING state.

        Returns:
            int: Number of experiments set to PENDING state.

        Raises:
            ValueError: If storage backend is not available.
        """
        counter: int = 0
        for sequence in self.__project.sequences:
            for experiment in sequence.experiments:
                for rep_key, rep_value in experiment.states:
                    if rep_value == ExperimentState.CREATED:
                        experiment.set_state(rep_key, ExperimentState.PENDING)
                        counter = counter + 1
                if self.__controller.storage:
                    self.__controller.storage.update_experiment_states(
                        experiment.states,
                        ConcreteExperimentReference(
                            concrete_experiment_slug=experiment.slug,
                            sequence_parameter_set_slug=sequence.pset.slug,
                            amnes_project_slug=self.__project.slug,
                        ),
                    )
                else:
                    self.logger.error("No Storage Backend available!")
                    raise ValueError("No Storage Backend available!")
        return counter

    def __init_managers(self) -> int:
        """Initialize remote worker manager for every node.

        Returns:
            int: Number of remote worker managers initialized.
        """
        counter: int = 0
        for node in self.__project.template.nodes:
            endpoint = node.endpoint
            manager = Pyro5.Proxy(
                f"PYRO:{RemoteWorkerManager.PYROID}@{endpoint.address}:{endpoint.port}"
            )
            manager._pyroTimeout = (  # pylint: disable=protected-access
                ProjectExecutionManager.DEFAULT_TIMEOUT
            )
            self.__workers[node.slug] = (endpoint, manager)
            counter = counter + 1
        return counter

    def __check_managers(self) -> List[WorkerEndpoint]:
        """Checks all remote managers for availability.

        Returns:
            List[WorkerEndpoint]: List of all WorkerEndpoints which did not respond.
        """
        unavailable: List[WorkerEndpoint] = []
        for _, (endpoint, manager) in self.__workers.items():
            try:
                if not manager.ping() == RemoteWorkerManager.PINGMSG:
                    unavailable.append(endpoint)
            except PyroError:
                unavailable.append(endpoint)
        return unavailable

    def __pending_experiments(
        self,
    ) -> Iterator[Tuple[ExperimentSequence, ConcreteExperiment, int]]:
        """Generator for all pending experiments of AMNES Project.

        Yields:
            ExperimentSequence: Sequence of next pending experiment.
            ConcreteExperiment: Instance of next pending experiment.
            int: Repetition of next pending experiment.
        """
        done: bool = False
        while not done:
            done = True
            for sequence in self.__project.sequences:
                for experiment in sequence.experiments:
                    for repetition, state in experiment.states:
                        if state == ExperimentState.PENDING:
                            done = False
                            yield (sequence, experiment, repetition)
