"""This module contains classes and functions for experiment execution.

Classes:
    ExperimentExecutionManager: Manager class for executing one concrete
                                experiment repetition.
"""

from copy import deepcopy
from logging import Logger
from threading import Thread
from typing import TYPE_CHECKING, Dict, List, Tuple

from ...core.experiment import ConcreteExperiment, ExperimentState
from ...core.experiment_node import ConcreteExperimentNode
from ...core.experiment_stage import ExperimentStage
from ...core.node_task import NodeTask
from ..logging import InstanceLogging
from .task_execution import TaskExecutionManager

if TYPE_CHECKING:
    from .app import Controller  # pylint: disable=cyclic-import


class ExperimentExecutionManager(InstanceLogging):
    """Manager class for executing one concrete experiment repetition."""

    LOGID = "experimentexecutionmanager"

    def __init__(
        self,
        logger: Logger,
        controller: "Controller",
        experiment: ConcreteExperiment,
        repetition: int,
    ) -> None:
        """Experiment execution manager constructor method.

        Args:
            logger (Logger): Logger for object instance.
            controller (Controller): Controller which started the experiment execution.
            experiment (ConcreteExperiment): Experiment of which one repetition
                                             should be executed.
            repetition (int): Repetition of concrete experiment, which should
                              be executed.
        """
        InstanceLogging.__init__(self, logger)
        self.__controller: "Controller" = controller
        self.__experiment: ConcreteExperiment = experiment
        self.__repetition: int = repetition

    def run(self) -> ExperimentState:
        """Run experiment repetition execution.

        Returns:
            ExperimentState: Result of executing the experiment.
        """
        self.logger.info(
            "Following stages need to be executed: "
            + f"{', '.join(stage.slug for stage in self.__experiment.stages)}"
        )
        for stage in self.__experiment.stages:
            self.logger.info(f"Start processing stage '{stage.slug}' ...")
            tasks = self.__tasks_per_stage(stage)
            if tasks:
                threads: List[Thread] = []
                stage_success: Dict[str, bool] = {}
                for node, task in tasks:
                    thread_name = f"TaskExecution-{node.slug}${task.slug}"
                    stage_success[thread_name] = False
                    thread = Thread(
                        target=TaskExecutionManager(
                            self.__controller.logger.getChild(
                                TaskExecutionManager.LOGID
                            ),
                            self.__controller,
                            deepcopy(node.endpoint),
                            deepcopy(task),
                            stage_success,
                            thread_name,
                        ).run,
                        name=thread_name,
                    )
                    self.logger.info(
                        f"Impose execution of task '{node.slug}' on node '{task.slug}'."
                    )
                    threads.append(thread)
                    self.logger.debug(f"Thread '{thread.name}': created.")
                for thread in threads:
                    thread.start()
                    self.logger.debug(f"Thread '{thread.name}': started.")
                for thread in threads:
                    thread.join()
                    self.logger.debug(f"Thread '{thread.name}': joined.")
                if False in stage_success.values():
                    self.logger.info(
                        f"Stage '{stage.slug}' failed because of the following tasks: "
                        + ", ".join(
                            [key[14:] for key, val in stage_success.items() if not val]
                        )
                    )
                    self.logger.info("Further stages were canceled.")
                    return ExperimentState.FAILED
            else:
                self.logger.info("Skipped empty stage.")

        self.logger.info("All stages processed.")
        return ExperimentState.FINISHED

    def __set_experiment_state(self, state: ExperimentState) -> None:
        """Sets state for internal experiment reference.

        Args:
            state (ExperimentState): State which should be set for internal experiment
                                     reference.
        """
        self.__experiment.set_state(self.__repetition, state)

    def __tasks_per_stage(
        self, stage: ExperimentStage
    ) -> List[Tuple[ConcreteExperimentNode, NodeTask]]:
        """Returns list of tasks with their node references for given stage.

        Args:
            stage (ExperimentStage): Stage for which a list of tasks with
                                     their node references should be returned.

        Returns:
            List[Tuple[ConcreteExperimentNode, NodeTask]]: List of tasks with their
                                                           node references for given
                                                           stage.
        """
        tasks: List[Tuple[ConcreteExperimentNode, NodeTask]] = []
        for node in self.__experiment.nodes:
            for task in node.tasks:
                if task.stage == stage:
                    tasks.append((node, task))
        return tasks
