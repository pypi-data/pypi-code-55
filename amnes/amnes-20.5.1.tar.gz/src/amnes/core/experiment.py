"""This module contains all necessary definitions for all experiment classes.

Classes:
    ExperimentState: Enumeration containing all valid states for an experiment instance.
    ExperimentAbstract: Defines an abstract experiment to which an ordered list
                        of ExperimentStage instances and a list of ExperimentNodes
                        is assigned.
    ExperimentTemplate: Defines a template for an experiment node to which an
                        ordered list of ExperimentStage instances and a list of
                        ExperimentNodeTemplate instances is assigned.
    ConcreteExperiment: Defines a ConcreteExperiment to which an ordered list of
                        ExperimentStage instances and a list of ConcreteExperimentNode
                        instances is assigned.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, Generic, ItemsView, List, TypeVar

from ..utils.parser import ParsingError, YamlParsable
from .amnes_object import AmnesObject
from .experiment_node import ConcreteExperimentNode, ExperimentNodeTemplate
from .experiment_stage import ExperimentStage

NodeType = TypeVar("NodeType", ExperimentNodeTemplate, ConcreteExperimentNode)


class ExperimentState(Enum):
    """AMNES Experiment States.

    This enumeration contains all valid states for an experiment.
    """

    def __new__(cls, value: int, doc: str) -> ExperimentState:
        """Custom initializer supporting docstrings for enumeration members.

        Args:
            cls (ExperimentState): ExperimentState class.
            value (int): Internal integer value used for state enum member.
            doc (str): Docstring for state enum member.

        Returns:
            ExperimentState: ExperimentState instance.
        """
        self = object.__new__(cls)
        self._value_ = value
        self.__doc__ = doc
        return self

    CREATED = (11, "The CREATED state is set for newly created ConcreteExperiments.")

    PENDING = (
        21,
        "The PENDING state is set for ConcreteExperiments waiting for their execution.",
    )
    RUNNING = (
        22,
        "The RUNNING state is set for ConcreteExperiments currently being executed.",
    )

    FINISHED = (
        31,
        "The FINISHED state is set for ConcreteExperiments that were executed "
        + "successfully.",
    )
    FAILED = (
        32,
        "The FAILED state is set for ConcreteExperiments that could not be executed "
        + "successfully.",
    )
    ABORTED = (
        33,
        "The ABORTED state is set for ConcreteExperiments whose execution was aborted "
        + "by the controller.",
    )

    def __str__(self) -> str:
        """Get string representation of enum member.

        Returns:
            str: String representation of enum member.
        """
        return super().__str__().rsplit(".", 1)[-1]


class ExperimentAbstract(ABC, AmnesObject, Generic[NodeType]):
    """Abstract experiment class containing all necessary stages and experiment nodes.

    Defines an abstract experiment to which an ordered list of ExperimentStage instances
    and a list of ExperimentNodes is assigned.

    Attributes:
        stages (List[ExperimentStage]): Ordered list of all ExperimentStage instances
                                        defined for this experiment.
        nodes (List[NodeType]): List of all ExperimentNodes for this experiment.
    """

    def __init__(
        self, slug: str, name: str, description: str, stages: List[ExperimentStage]
    ) -> None:
        """Abstract experiment class constructor method.

        Args:
            slug (str): Short identifier for the experiment,
                        which must be a valid, non-empty string.
            name (str): Full name for the experiment.
            description (str): Custom description for the experiment.
            stages (List[ExperimentStage]): List of all ExperimentStage instances
                                            for this experiment.

        Raises:
            TypeError: If `stages` is not of type List or a stage is not
                       of type ExperimentStage.
            ValueError: If a stage in `stages` has an ambiguous slug
                        that is already in use.
        """
        super().__init__(slug, name, description)
        self.__nodes: Dict[str, NodeType] = {}
        if not isinstance(stages, List):
            raise TypeError("Given stages are not of type List.")
        slugs: List[str] = []
        for stage in stages:
            if not isinstance(stage, ExperimentStage):
                raise TypeError("Stage is not of type ExperimentStage.")
            if stage.slug in slugs:
                raise ValueError("Found slug duplicate in given stage list.")
            slugs.append(stage.slug)
        self.__stages = stages.copy()

    @abstractmethod
    def __eq__(self, other: object) -> bool:
        """Check equality between this Experiment instance and an arbitrary object.

        Args:
            other (object): Arbitrary object to be checked for equality
                            with this Experiment instance.

        Returns:
            bool: True if `other` is equal to the current ExperimentNode instance,
                  otherwise returns false.

        Raises:
            TypeError: If `other` is not of type ExperimentNodeAbstract.
        """
        if not isinstance(other, ExperimentAbstract):
            raise TypeError(
                "The object to be compared to is not of type ExperimentAbstract."
            )
        return (
            super().__eq__(other)
            and self.stages == other.stages
            and self._nodes_view() == other._nodes_view()
        )

    @property
    def stages(self) -> List[ExperimentStage]:
        """List[ExperimentStage]: ExperimentStages of this Experiment instance.

        Returns:
            stages (List[ExperimentStage]): ExperimentStages of this Experiment
                                            instance.
        """
        return self.__stages.copy()

    @property
    def nodes(self) -> List[NodeType]:
        """List[NodeType]: ExperimentNodes of this Experiment instance.

        Returns:
            nodes (List[NodeType]): ExperimentNodes of this Experiment instance.
        """
        return list(self.__nodes.values())

    @abstractmethod
    def add_nodes(self, nodes: List[NodeType]) -> None:
        """Add new nodes to the node list of this Experiment instance.

        Subclasses must check the types for the list and its elements before calling
        this abstract method.

        Args:
            nodes (List[NodeType]): List of nodes to be added.

        Raises:
            ValueError: If a node in `nodes` has an ambiguous slug
                        that is already in use.
        """
        slugs: List[str] = []
        for node in nodes:
            if node.slug in self.__nodes:
                raise ValueError("Used slug of node already in use.")
            if node.slug in slugs:
                raise ValueError("Found slug duplicate in given node list.")
            slugs.append(node.slug)

        for node in nodes:
            self.__nodes[node.slug] = node

    def remove_nodes(self, slugs: List[str]) -> None:
        """Remove nodes from the node list of this Experiment instance.

        Args:
            slugs (List[str]): List of all slugs which identify the nodes
                               which should be removed.

        Raises:
            TypeError: If `slugs` is not of type List or a slug is not of type String.
            ValueError: If a slug cannot be resolved to any node.
        """
        if not isinstance(slugs, List):
            raise TypeError("Given slugs are not of type List.")

        delslugs: List[str] = []
        for slug in slugs:
            if not isinstance(slug, str):
                raise TypeError("Slug is not of type String.")
            if slug not in self.__nodes:
                raise ValueError("Used slug cannot be resolved to any node.")
            if slug in delslugs:
                raise ValueError("Found slug duplicate in given slug list.")
            delslugs.append(slug)

        for slug in delslugs:
            del self.__nodes[slug]

    def _nodes_view(self) -> ItemsView[str, NodeType]:
        return self.__nodes.items()


class ExperimentTemplate(ExperimentAbstract, YamlParsable):
    """Experiment template class containing all necessary stages and experiment nodes.

    Defines a template for an experiment node to which an ordered list of
    ExperimentStage instances and a list of ExperimentNodeTemplate instances
    is assigned.

    Attributes:
        stages (List[ExperimentStage]): List of all ExperimentStage instances
                                        defined for this experiment.
        nodes (List[ExperimentNodeTemplate]): List of all ExperimentNodeTemplate
                                              instances for this experiment.
    """

    def __eq__(self, other: object) -> bool:
        """Check equality between this ExperimentTemplate and an arbitrary object.

        Extends the superclass equality method to check for correct types.

        Args:
            other (object): Arbitrary object to be checked for equality
                            with this ExperimentTemplate instance.

        Returns:
            bool: True if `other` is equal to the current ExperimentTemplate
                  instance, otherwise returns false.

        Raises:
            TypeError: If `other` is not of type ExperimentTemplate.
        """
        if not isinstance(other, ExperimentTemplate):
            raise TypeError(
                "The object to be compared to is not of type ExperimentTemplate."
            )
        return super().__eq__(other)

    @staticmethod
    def _parse_stages(key: str, values: Dict) -> List[ExperimentStage]:
        """Internal method for parsing the ExperimentStage List.

        Args:
            key (str): Key of the ExperimentTemplate dictionary that is parsed.
            values (Dict): Values of the ExperimentTemplate dictionary that is parsed.

        Returns:
            stages_list (List[ExperimentStage]): The parsed list of ExperimentStage
                                                 instances.

        Raises:
            ParsingError: If no stages key is defined or the list of stages is empty.
        """
        if "stages" in values:
            with YamlParsable._parse_key_context(key):
                stages = values.get("stages")
            if stages is None:
                raise ParsingError(
                    message="The specified list of stages is empty.", key=key
                )
            stages_list = []
            with YamlParsable._parse_key_context(key):
                for stage in stages:
                    if isinstance(stage, str):
                        exp_stage = ExperimentStage.parse({stage: None})
                    else:
                        stage_key = list(stage.keys())[0]
                        stage_values = list(stage.values())[0]
                        exp_stage = ExperimentStage.parse({stage_key: stage_values})
                    stages_list.append(exp_stage)
                del values["stages"]
        else:
            raise ParsingError(
                message="No stages were defined for the experiment template.", key=key
            )
        return stages_list

    @staticmethod
    def _parse_nodes(key: str, values: Dict) -> List[ExperimentNodeTemplate]:
        """Internal method for parsing the ExperimentNodeTemplate List.

        Args:
            key (str): Key of the ExperimentTemplate dictionary that is parsed.
            values (Dict): Values of the ExperimentTemplate dictionary that is parsed.

        Returns:
            nodes_list (List[ExperimentNodeTemplate]): The parsed list of
                                                       ExperimentNodeTemplate instances.

        Raises:
            ParsingError: If no nodes key is defined or the list of nodes is empty.
        """
        if "nodes" in values:
            with YamlParsable._parse_key_context(key):
                nodes = values.get("nodes")
            if nodes is None:
                raise ParsingError(
                    message="The specified list of nodes is empty.", key=key
                )
            nodes_list = []
            with YamlParsable._parse_key_context(key):
                for node in nodes:
                    exp_node = ExperimentNodeTemplate.parse({node: nodes.get(node)})
                    nodes_list.append(exp_node)
                del values["nodes"]
        else:
            raise ParsingError(
                message="No experiment node templates were defined "
                + "for the experiment template."
            )
        return nodes_list

    @staticmethod
    def parse(config: Dict) -> ExperimentTemplate:
        """Static method for parsing an ExperimentTemplate configuration.

        The overwritten parse method requires a dictionary with exactly
        one key value pair as parameter.
        The key is used as slug for the ExperimentTemplate instance
        that is created.

        Example YAML config:

        ```yaml
        template:
          name: Template 1
          description: My experiment template.
          stages:
            - Ping:
                name: Ping Stage
                description: My ping stage.
            - Collect

          nodes:
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
            node_2:
              name: My Node 2
              description: My second node.
              endpoint:
                address: 234.234.234.234
                port: 12345
              tasks:
                collect_stat:
                  module: CollectStatistics
                  stage: Collect
                  params:
                    level: "1"
        ```

        Dictionary, which is passed for this ExperimentTemplate:

        ```python
        {
            "template": {
                "name": "Template 1",
                "description": "My experiment template.",
                "stages": [
                    {
                        "Ping": None,
                        "name": "Ping Stage",
                        "description": "My ping stage."
                    },
                    "Collect"],
                "nodes": {
                    "node_1": {
                        "name": "My Node 1",
                        "description": "My first node.",
                        "endpoint": {"address": "123.123.123.123", "port": 12345},
                        "tasks": {
                            "my_ping": {
                                "module": "PingModule",
                                "stage": "Ping",
                                "params": {"count": "[[1]]", "dest": "node_2"},
                            }
                        },
                    },
                    "node_2": {
                        "name": "My Node 2",
                        "description": "My second node.",
                        "endpoint": {"address": "234.234.234.234", "port": 12345},
                        "tasks": {
                            "collect_stat": {
                                "module": "CollectStatistics",
                                "stage": "Collect",
                                "params": {"level": "1"},
                            }
                        },
                    },
                },
            }
        }
        ```

        Args:
            config (Dict): Dictionary from which the ExperimentTemplate
                           instance is created.

        Returns:
            experiment (ExperimentTemplate): The ExperimentTemplate instance
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

        stages = ExperimentTemplate._parse_stages(key, values)
        nodes = ExperimentTemplate._parse_nodes(key, values)

        if values:
            raise ParsingError(message="Config tree not empty after parsing.", key=key)

        with YamlParsable._parse_key_context(key):
            experiment = ExperimentTemplate(key, name, description, stages)
            experiment.add_nodes(nodes)

        return experiment

    def add_nodes(self, nodes: List[ExperimentNodeTemplate]) -> None:
        """Add new nodes to the node list of this Experiment instance.

        Extends the abstract superclass method to check for correct types.

        Args:
            nodes (List[ExperimentNodeTemplate]): List of nodes to be added.

        Raises:
            TypeError: If `nodes` is not of type List or a node in `nodes`
                       is not of type ExperimentNodeTemplate.
        """
        if not isinstance(nodes, List):
            raise TypeError("Given nodes are not of type List.")
        for node in nodes:
            if not isinstance(node, ExperimentNodeTemplate):
                raise TypeError("Given node is not of type ExperimentNodeTemplate.")
        super().add_nodes(nodes)


class ConcreteExperiment(ExperimentAbstract):
    """Experiment instance class containing necessary stages and experiment nodes.

    Defines an ConcreteExperiment to which an ordered list of ExperimentStage instances
    and a list of ConcreteExperimentNode instances is assigned.

    Attributes:
        stages (List[ExperimentStage]): List of all ExperimentStage instances
                                        defined for this experiment.
        nodes (List[ConcreteExperimentNode]): List of all ConcreteExperimentNode
                                              instances for this experiment.
        states (ItemsView[int, ExperimentState]): ExperimentStates for all repetitions
                                                  of this ConcreteExperiment.
    """

    def __init__(
        self,
        slug: str,
        name: str,
        description: str,
        stages: List[ExperimentStage],
        repetitions: int,
    ) -> None:
        """Experiment instance class constructor method.

        Extends ExperimentAbstract class constructor method
        by setting the ConcreteExperiment state.

        Args:
            slug (str): Short identifier for the experiment,
                        which must be a valid, non-empty string.
            name (str): Full name for the experiment.
            description (str): Custom description for the experiment.
            stages (List[ExperimentStage]): List of all ExperimentStage instances
                                            for this experiment to be set.
            repetitions (int): Positive number of repetitions, this ConcreteExperiment
                               should run.

        Raises:
            ValueError: If `repititions` is less than or equal to zero.
        """
        super().__init__(slug, name, description, stages)

        if repetitions <= 0:
            raise ValueError("Repetitions must be greater than or equal to one.")

        self.__states: Dict[int, ExperimentState] = {}
        for i in range(1, repetitions + 1):
            self.__states[i] = ExperimentState.CREATED

    def __eq__(self, other: object) -> bool:
        """Check equality between this ConcreteExperiment and an arbitrary object.

        Extends the superclass equality method to check for correct types.

        Args:
            other (object): Arbitrary object to be checked for equality
                            with this ConcreteExperiment instance.

        Returns:
            bool: True if `other` is equal to the current ConcreteExperiment
                  instance, otherwise returns false.

        Raises:
            TypeError: If `other` is not of type ConcreteExperiment.
        """
        if not isinstance(other, ConcreteExperiment):
            raise TypeError(
                "The object to be compared to is not of type ConcreteExperiment."
            )
        return super().__eq__(other) and self.states == other.states

    @property
    def states(self) -> ItemsView[int, ExperimentState]:
        # Property docstring line cannot be changed
        # pylint: disable=line-too-long
        """ItemsView[int, ExperimentState]: ExperimentStates for all repetitions of this ConcreteExperiment.

        Returns:
            state (ItemsView[int, ExperimentState]): ExperimentStates for all repetitions
                                                     of this ConcreteExperiment.
        """
        return self.__states.items()

    def set_state(self, repetition: int, state: ExperimentState) -> None:
        """Set state for specific repetition of this ConcreteExperiment.

        Args:
            repetition (int): Repetition number whose state should be set.
            state (ExperimentState): ExperimenState to be set for the specific
                                     repetition.

        Raises:
            TypeError: If `repetition` is not of type Integer
                       or `state` is not of type ExperimentState.
            ValueError: If `repetition` does not exists for this ConcreteExperiment.
        """
        if not isinstance(repetition, int):
            raise TypeError("Repetitions is not of type Integer.")
        if repetition not in self.__states:
            raise ValueError("Specified repetition number is invalid.")
        if not isinstance(state, ExperimentState):
            raise TypeError("State is not of type ExperimentState.")
        self.__states[repetition] = state

    def add_nodes(self, nodes: List[ConcreteExperimentNode]) -> None:
        """Add new nodes to the node list of this ConcreteExperiment.

        Extends the abstract superclass method to check for correct types.

        Args:
            nodes (List[ConcreteExperimentNode]): List of nodes to be added.

        Raises:
            TypeError: If `nodes` is not of type List or a node in `nodes`
                       is not of type ConcreteExperimentNode.
        """
        if not isinstance(nodes, List):
            raise TypeError("Given nodes are not of type List.")
        for node in nodes:
            if not isinstance(node, ConcreteExperimentNode):
                raise TypeError("Given node is not of type ConcreteExperimentNode.")
        super().add_nodes(nodes)
