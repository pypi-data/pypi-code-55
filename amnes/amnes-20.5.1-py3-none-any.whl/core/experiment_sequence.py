"""This module contains all definitions for the ExperimentSequence class.

Classes:
    ExperimentSequence: Defines an experiment sequence that contains all
                        ConcreteExperiment instances created from exactly
                        one ParameterSet.
"""
from __future__ import annotations

from itertools import product
from typing import Dict, ItemsView, Iterator, List

from .experiment import ConcreteExperiment, ExperimentTemplate
from .experiment_node import ConcreteExperimentNode, ExperimentNodeTemplate
from .node_task import NodeTask, NodeTaskFiles, NodeTaskParams
from .parameter_set import ParameterSet


class ExperimentSequence:
    """Experiment sequence class containing all necessary ConcreteExperiment instances.

    Defines an experiment sequence that contains all ConcreteExperiment instances
    created from exactly one ParameterSet.

    Attributes:
        pset (ParameterSet): Corresponding ParameterSet instance.
        experiments (List[ConcreteExperiments]): List of ConcreteExperiment instances.
    """

    def __init__(self, pset: ParameterSet):
        """Experiment sequence class constructor method.

        Args:
            pset (ParameterSet): Corresponding ParameterSet instance.
        """
        self.pset = pset
        self.__experiments: Dict[str, ConcreteExperiment] = {}

    def __eq__(self, other: object) -> bool:
        """Check equality between this ExperimentSequence and an arbitrary object.

        Args:
            other (object): Arbitrary object to be checked for equality
                            with this ExperimentSequence instance.

        Returns:
            bool: True if `other` is equal to the current ExperimentSequence instance,
                  otherwise returns false.

        Raises:
            TypeError: If `other` is not of type ExperimentSequence.
        """
        if not isinstance(other, ExperimentSequence):
            raise TypeError(
                "The object to be compared to is not of type ExperimentSequence."
            )
        return (
            self.pset == other.pset
            and self._experiments_view() == other._experiments_view()
        )

    @property
    def pset(self) -> ParameterSet:
        """ParameterSet: ParameterSet instance of this ExperimentSequence.

        Returns:
            pset (ParameterSet): ParameterSet instance of this ExperimentSequence.
        """
        return self.__pset

    @pset.setter
    def pset(self, pset: ParameterSet) -> None:
        """Parameter set setter function.

        Args:
            pset (ParameterSet): Parameter set instance to be set for this
                                 ExperimentSequence instance.

        Raises:
            TypeError: If `pset` is not of type ParameterSet.
        """
        if not isinstance(pset, ParameterSet):
            raise TypeError("Parameter set is not of type ParameterSet.")
        self.__pset = pset

    @property
    def experiments(self) -> List[ConcreteExperiment]:
        """List[ConcreteExperiment]: ConcreteExperiments of this ExperimentSequence.

        Returns:
            experiments (List[ConcreteExperiment]): ConcreteExperiments of
                                                    this ExperimentSequence.
        """
        return list(self.__experiments.values())

    def _experiments_view(self) -> ItemsView[str, ConcreteExperiment]:
        return self.__experiments.items()

    def add_experiments(self, experiments: List[ConcreteExperiment]) -> None:
        """Add new experiments to the experiment list of this ExperimentSequence.

        Args:
            experiments (List[ConcreteExperiment]): List of experiments to be added.

        Raises:
            TypeError: If `experiments` is not of type List or an experiment is not of
                       type ConcreteExperiment.
            ValueError: If an experiment in `experiments` has an ambiguous slug that is
                        already in use.
        """
        if not isinstance(experiments, List):
            raise TypeError("Given experiments are not of type List.")

        slugs: List[str] = []
        for exp in experiments:
            if not isinstance(exp, ConcreteExperiment):
                raise TypeError("Experiment is not of type ConcreteExperiment.")
            if exp.slug in self.__experiments:
                raise ValueError("Used slug of experiment already in use.")
            if exp.slug in slugs:
                raise ValueError("Found slug duplicate in given experiment set list.")
            slugs.append(exp.slug)

        for exp in experiments:
            self.__experiments[exp.slug] = exp

    def remove_experiments(self, slugs: List[str]) -> None:
        """Remove experiments from the experiment list of this ExperimentSequence.

        Args:
            slugs (List[str]): List of all slugs which identify the experiments
                               which should be removed.

        Raises:
            TypeError: If `slugs` is not of type List or a slug is not of type String.
            ValueError: If a slug cannot be resolved to any experiment.
        """
        if not isinstance(slugs, List):
            raise TypeError("Given slugs are not of type List.")

        delslugs: List[str] = []
        for slug in slugs:
            if not isinstance(slug, str):
                raise TypeError("Slug is not of type String.")
            if slug not in self.__experiments:
                raise ValueError("Used slug cannot be resolved to any experiment.")
            if slug in delslugs:
                raise ValueError("Found slug duplicate in given slug list.")
            delslugs.append(slug)

        for slug in delslugs:
            del self.__experiments[slug]

    @staticmethod
    def _dict_product(input_dict: Dict) -> Iterator:
        """Creates a dictionary for all possible key-value combinations.

        Args:
            input_dict (Dict): Dictionary for which all key-value combinations
                               should be created.

        Returns:
            Iterator: All dictionaries that represent a concrete assignment.
        """
        return (dict(zip(input_dict, x)) for x in product(*input_dict.values()))

    @staticmethod
    def _replace_param(param_value: str, replace_dict: Dict) -> str:
        """Replaces a parameter value with the substitution given in 'replace_dict'.

        Args:
            param_value (str): Parameter assignment in which the placeholder
                               is to be replaced by a concrete value.
            replace_dict (Dict): Replacement Dictionary which contains all
                                 mappings from placeholders to concrete values.

        Returns:
            param_value (str): The passed 'param_value' in which possible
                               placeholders are replaced by concrete values.
        """
        for key in replace_dict:
            param_value = param_value.replace(f"[[{key}]]", replace_dict[key])
        return param_value

    @staticmethod
    def _create_concrete_ntasks(
        node: ExperimentNodeTemplate, assignments: Dict
    ) -> List[NodeTask]:
        """Internal method for creating NodeTask instances.

        Args:
            node (ExperimentNodeTemplate): The ExperimentNodeTemplate instance
                                           for which equivalent NodeTask instances
                                           with no placeholders in the task parameters
                                           should be created.
            assignments (Dict): Dictionary containing all placeholder replacements.

        Returns:
            node_tasks (List[NodeTask]): List of all created NodeTask instances.
        """
        node_tasks: List[NodeTask] = []
        for task in node.tasks:
            params_dict = dict(task.params.pairs)
            for key, value in params_dict.items():
                params_dict[key] = ExperimentSequence._replace_param(value, assignments)
            ntask = NodeTask(
                task.slug,
                task.name,
                task.description,
                task.module,
                task.stage,
                NodeTaskParams(params_dict),
                NodeTaskFiles(dict(task.files.pairs)),
            )
            node_tasks.append(ntask)
        return node_tasks

    @staticmethod
    def _create_concrete_nodes(
        template: ExperimentTemplate, assignments: Dict
    ) -> List[ConcreteExperimentNode]:
        """Internal method for creating ConcreteExperimentNode instances.

        Args:
            template (ExperimentTemplate): The ExperimentTemplate instance for which
                                           equivalent ConcreteExperimentNode instances
                                           with no placeholders in the task parameters
                                           should be created.
            assignments (Dict): Dictionary containing all placeholder replacements.

        Returns:
            nodes (List[ConcreteExperimentNode]): List of all created
                                                  ConcreteExperimentNode instances.
        """
        nodes: List[ConcreteExperimentNode] = []
        for node in template.nodes:
            node_tasks = ExperimentSequence._create_concrete_ntasks(node, assignments)
            exp_node = ConcreteExperimentNode(
                node.slug, node.name, node.description, node.endpoint
            )
            exp_node.add_tasks(node_tasks)
            nodes.append(exp_node)
        return nodes

    @staticmethod
    def _create_concrete_experiments(
        template: ExperimentTemplate, assignments: List[Dict], repetitions: int
    ) -> List[ConcreteExperiment]:
        """Internal method for creating ConcreteExperiment instances.

        Args:
            template (ExperimentTemplate): The ExperimentTemplate instance for which
                                           equivalent ConcreteExperiment instances
                                           with no placeholders in the task parameters
                                           should be created.
            assignments (List[Dict]): List of dictionaries each representing
                                      a replacement of placeholders for exactly
                                      one ConcreteExperimentInstance.
            repetitions (int): Number of repetitions to be set for one
                               ConcreteExperiment instance.

        Returns:
            experiments (List[ConcreteExperiment]): List of all created
                                                    ConcreteExperiment instances.
        """
        experiments: List[ConcreteExperiment] = []
        for i in range(0, len(assignments)):  # pylint: disable=consider-using-enumerate
            exp = ConcreteExperiment(
                "exp" + str(i + 1), "", "", template.stages, repetitions
            )
            nodes = ExperimentSequence._create_concrete_nodes(template, assignments[i])
            exp.add_nodes(nodes)
            experiments.append(exp)
        return experiments

    @staticmethod
    def create_sequences(
        template: ExperimentTemplate, psets: List[ParameterSet], repetitions: int
    ) -> List[ExperimentSequence]:
        """Create ExperimentSequences from an ExperimentTemplate and ParameterSets.

        Args:
            template (ExperimentTemplate): The ExperimentTemplate instance for which
                                           equivalent ConcreteExperiment instances
                                           with no placeholders in the task parameters
                                           should be created.
            psets (List[ParameterSet]): List of all ParameterSets for which an
                                        ExperimentSequence is created.
            repetitions (int): Number of repetitions to be set for one
                               ConcreteExperiment instance.

        Returns:
            sequences (List[ExperimentSequence]): List of all created
                                                  ExperimentSequence instances.
        """
        sequences: List[ExperimentSequence] = []
        if psets == []:
            sequence = ExperimentSequence(ParameterSet("empty_pset", "", ""))
            experiment = ConcreteExperiment("exp", "", "", template.stages, repetitions)
            for node in template.nodes:
                concrete_node = ConcreteExperimentNode(
                    node.slug, node.name, node.description, node.endpoint
                )
                for task in node.tasks:
                    concrete_node.add_tasks([task])
                experiment.add_nodes([concrete_node])
            sequence.add_experiments([experiment])
            sequences.append(sequence)

        for pset in psets:
            assignment_list = list(
                ExperimentSequence._dict_product(dict(pset.assignments))
            )
            experiments = ExperimentSequence._create_concrete_experiments(
                template, assignment_list, repetitions
            )

            sequence = ExperimentSequence(pset)
            sequence.add_experiments(experiments)
            sequences.append(sequence)

        return sequences
