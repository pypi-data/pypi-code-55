"""This module contains all necessary definitions for all experiment node classes.

Classes:
    ExperimentNodeAbstract: Defines abstract experiment nodes to which a worker
                            endpoint and a list of tasks are assigned.
    ExperimentNodeTemplate: Defines a template for an ExperimentNode, to which a
                            WorkerEndpoint and a list of node tasks are assigned.
                            Within the NodeTasks, parameter values can contain
                            placeholders which will be used by parameter substitution.
    ConcreteExperimentNode: Defines a concrete experiment node, to which
                            a WorkerEndpoint and several node tasks are assigned.
                            Within the NodeTasks, parameters may only be assigned
                            exactly one value.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict, ItemsView, List

from ..utils.parser import ParsingError, YamlParsable
from .amnes_object import AmnesObject
from .node_task import NodeTask
from .worker_endpoint import WorkerEndpoint


class ExperimentNodeAbstract(ABC, AmnesObject):
    """Abstract experiment node class to summarize tasks to be executed by one node.

    Defines an abstract ExperimentNode class, from which the ExperimentNodeTemplate
    and ConreteExperimentNode classes inherit.
    One ExperimentNode consists of exactly one WorkerEndpoint instance
    and a list of NodeTasks.

    Attributes:
        endpoint (WorkerEndpoint): Management communication endpoint of the worker.
        tasks (List[NodeTask]): List of NodeTasks that an experiment node
                                should execute during an experiment.
    """

    def __init__(
        self, slug: str, name: str, description: str, endpoint: WorkerEndpoint
    ) -> None:
        """Experiment node class constructor method.

        Args:
            slug (str): Short identifier for the experiment node,
                        which must be a valid, non-empty string.
            name (str): Full name for the experiment node.
            description (str): Custom description for the experiment node.
            endpoint (WorkerEndpoint): Management communication endpoint of the worker.
        """
        super().__init__(slug, name, description)
        self.__endpoint: WorkerEndpoint = endpoint
        self.__tasks: Dict[str, NodeTask] = {}

    @abstractmethod
    def __eq__(self, other: object) -> bool:
        """Check equality between this ExperimentNode instance and an arbitrary object.

        Args:
            other (object): Arbitrary object to be checked for equality
                            with this ExperimentNode instance.

        Returns:
            bool: True if `other` is equal to the current ExperimentNode instance,
                  otherwise returns false.

        Raises:
            TypeError: If `other` is not of type ExperimentNodeAbstract.
        """
        if not isinstance(other, ExperimentNodeAbstract):
            raise TypeError(
                "The object to be compared to is not of type ExperimentNodeAbstract."
            )
        return (
            super().__eq__(other)
            and self.endpoint == other.endpoint
            and self._tasks_view() == other._tasks_view()
        )

    @property
    def endpoint(self) -> WorkerEndpoint:
        """WorkerEndpoint: Management communication endpoint of the worker.

        Returns:
            endpoint (WorkerEndpoint): Management communication endpoint of the worker.
        """
        return self.__endpoint

    @endpoint.setter
    def endpoint(self, endpoint: WorkerEndpoint) -> None:
        """Set the endpoint to be used for communication between worker and controller.

        Args:
            endpoint (WorkerEndpoint): Communication endpoint to be set.

        Raises:
            TypeError: If `endpoint` is not of type WorkerEndpoint.
        """
        if not isinstance(endpoint, WorkerEndpoint):
            raise TypeError("The endpoint to be set is not of type WorkerEndpoint.")
        self.__endpoint = endpoint

    @property
    def tasks(self) -> List[NodeTask]:
        """List[NodeTask]: NodeTasks of this ExperimentNode instance.

        Returns:
            tasks (List[NodeTask]): NodeTasks of this ExperimentNode instance.
        """
        return list(self.__tasks.values())

    def _tasks_view(self) -> ItemsView[str, NodeTask]:
        return self.__tasks.items()

    def add_tasks(self, tasks: List[NodeTask]) -> None:
        """Add new tasks to the task list of this ExperimentNode instance.

        Args:
            tasks (List[NodeTask]): List of tasks to be added.

        Raises:
            TypeError: If `tasks` is not of type List or a task is not of type NodeTask.
            ValueError: If a task in `tasks` has an ambiguous slug
                        that is already in use.
        """
        if not isinstance(tasks, List):
            raise TypeError("Given tasks are not of type List.")

        # Check all new tasks before altering dictionary
        slugs: List[str] = []
        for task in tasks:
            if not isinstance(task, NodeTask):
                raise TypeError("Task is not of type NodeTask.")
            if task.slug in self.__tasks:
                raise ValueError("Used slug of task already in use.")
            if task.slug in slugs:
                raise ValueError("Found slug duplicate in given task list.")
            slugs.append(task.slug)

        # Alter dictionary
        for task in tasks:
            self.__tasks[task.slug] = task

    def remove_tasks(self, slugs: List[str]) -> None:
        """Remove tasks from the task list of this ExperimentNode instance.

        Args:
            slugs (List[str]): List of all slugs which identify the tasks
                               which should be removed.

        Raises:
            TypeError: If `slugs` is not of type List or a slug is not of type String.
            ValueError: If a slug cannot be resolved to any task.
        """
        if not isinstance(slugs, List):
            raise TypeError("Given slugs are not of type List.")

        # Check all given slugs before altering dictionary
        delslugs: List[str] = []
        for slug in slugs:
            if not isinstance(slug, str):
                raise TypeError("Slug is not of type String.")
            if slug not in self.__tasks:
                raise ValueError("Used slug cannot be resolved to any task.")
            if slug in delslugs:
                raise ValueError("Found slug duplicate in given slug list.")
            delslugs.append(slug)

        # Alter dictionary
        for slug in delslugs:
            del self.__tasks[slug]


class ExperimentNodeTemplate(ExperimentNodeAbstract, YamlParsable):
    """Experiment node template class to summarize tasks to be executed by one node.

    Defines a template for an ExperimentNode, to which a WorkerEndpoint
    and a list of node tasks are assigned. Within the NodeTasks, parameter
    values can contain placeholders which will be used by parameter substitution.

    Attributes:
        endpoint (WorkerEndpoint): Management communication endpoint of the worker.
        tasks (List[NodeTask]): List of NodeTasks that an experiment node
                                    should execute during an experiment.
    """

    def __eq__(self, other: object) -> bool:
        """Check equality between this ExperimentNodeTemplate and an arbitrary object.

        Args:
            other (object): Arbitrary object to be checked for equality
                            with this ExperimentNodeTemplate instance.

        Returns:
            bool: True if `other` is equal to the current ExperimentNodeTemplate
                  instance, otherwise returns false.

        Raises:
            TypeError: If `other` is not of type ExperimentNodeAbstract.
        """
        if not isinstance(other, ExperimentNodeTemplate):
            raise TypeError(
                "The object to be compared to is not of type ExperimentNodeTemplate."
            )
        return super().__eq__(other)

    @staticmethod
    def parse(config: Dict) -> ExperimentNodeTemplate:
        """Static method for parsing an ExperimentNodeTemplate configuration.

        The overwritten parse method requires a dictionary with exactly
        one key value pair as parameter.
        The key is used as slug for the ExperimentNodeTemplate instance
        that is created.

        Example YAML config:

        ```yaml
        node_1:
          name: My Node 1
          description: My first node.
          endpoint:
            address: 123.123.123.123
            port: 12345
          tasks:
            my_ping:
              module: PingModule
              stage: Ping
              params:
                count: "[[1]]"
                dest: node_2
            collect_stat:
              module: CollectStatistics
              stage: Collect
              params:
                level: "1"
              files:
                appconfig: "/mydir/app.config"
        ```

        Dictionary, which is passed for this ExperimentNodeTemplate:

        ```python
        {
            "node_1": {
                "name": "My Node 1",
                "description": "My first node.",
                "endpoint": {"address": "123.123.123.123", "port": 12345},
                "tasks": {
                    "my_ping": {
                        "module": "PingModule",
                        "stage": "Ping",
                        "params": {"count": "[[1]]", "dest": "node_2"},
                    },
                    "collect_stat": {
                        "module": "CollectStatistics",
                        "stage": "Collect",
                        "params": {"level": "1"},
                        "files": {"appconfig": "/mydir/app.config"},
                    },
                },
            }
        }
        ```

        Args:
            config (Dict): Dictionary from which the ExperimentNodeTemplate
                           instance is created.

        Returns:
            node (ExperimentNodeTemplate): The ExperimentNodeTemplate instance
                                           created from `config`.

        Raises:
            ParsingError: If an exception occurs while parsing the `config`
                          dictionary.
        """
        YamlParsable._parse_check(config)

        key = list(config.keys())[0]
        values = list(config.values())[0]

        with YamlParsable._parse_key_context(key):
            name = values.get("name")
            if name is None:
                name = ""
            else:
                del values["name"]
            description = values.get("description")
            if description is None:
                description = ""
            else:
                del values["description"]
            endpoint = WorkerEndpoint.parse({"endpoint": values.get("endpoint")})
            del values["endpoint"]
            ntasks = values.get("tasks")
            if ntasks is not None:
                ntask_list = []
                for task in ntasks:
                    with YamlParsable._parse_key_context(key):
                        ntask = NodeTask.parse({task: ntasks.get(task)})
                    ntask_list.append(ntask)
            if "tasks" in values:
                del values["tasks"]

        if values:
            raise ParsingError(message="Config tree not empty after parsing.", key=key)

        with YamlParsable._parse_key_context(key):
            node = ExperimentNodeTemplate(key, name, description, endpoint)
            if ntasks is not None:
                node.add_tasks(ntask_list)

        return node


class ConcreteExperimentNode(ExperimentNodeAbstract):
    """Concrete experiment node class to summarize tasks to be executed by one node.

    Defines a concrete experiment node, to which a WorkerEndpoint
    and several node tasks are assigned.
    Within the NodeTasks, no placeholders should be present.

    Attributes:
        endpoint (WorkerEndpoint): Management communication endpoint of the worker.
        tasks (List[NodeTask]): List of NodeTasks that an experiment node
                                should execute during an experiment.
    """

    def __eq__(self, other: object) -> bool:
        """Check equality between this ConcreteExperimentNode and an arbitrary object.

        Args:
            other (object): Arbitrary object to be checked for equality
                            with this ConcreteExperimentNode instance.

        Returns:
            bool: True if `other` is equal to the current ConcreteExperimentNode
                  instance, otherwise returns false.

        Raises:
            TypeError: If `other` is not of type ConcreteExperimentNode.
        """
        if not isinstance(other, ConcreteExperimentNode):
            raise TypeError(
                "The object to be compared to is not of type ConcreteExperimentNode."
            )
        return super().__eq__(other)
