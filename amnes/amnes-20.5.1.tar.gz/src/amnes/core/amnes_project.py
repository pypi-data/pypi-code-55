"""This module contains all definitions for the AmnesProject class.

Classes:
    AmnesProject: Defines an AMNES project consisting of one ExperimentTemplate instance
                  and two lists for ParameterSets and their corresponding
                  ExperimentSequences. It also contains the number of repetitions for a
                  concrete experiment.
"""
from __future__ import annotations

from typing import Dict, ItemsView, List

from ..utils.parser import ParsingError, YamlParsable
from .amnes_object import AmnesObject
from .experiment import ExperimentTemplate
from .experiment_sequence import ExperimentSequence
from .parameter_set import ParameterSet


class AmnesProject(AmnesObject, YamlParsable):
    """AMNES project class representing the defined configuration and parameterisation.

    Defines an AMNES project consisting of one ExperimentTemplate instance
    and two lists for ParameterSets and their corresponding ExperimentSequences.
    It also contains the number of repetitions for a concrete experiment.

    Attributes:
        template (ExperimentTemplate): ExperimentTemplate instance defined
                                       for this AmnesProject.
        repetitions (int): Number of repetitions for a concrete experiment.
        psets (List[ParameterSet]): List of ParameterSet instances defined
                                    for this AmnesProject.
        sequences (List[ExperimentSequence]): List of ExperimentSequence instances
                                              defined for this AmnesProject.
    """

    def __init__(
        self,
        slug: str,
        name: str,
        description: str,
        template: ExperimentTemplate,
        repetitions: int,
    ) -> None:
        """AMNES project class constructor method.

        Args:
            slug (str): Short identifier for the AMNES project, which
                        must be a valid, non-empty string.
            name (str): Full name for the AMNES project.
            description (str): Custom description for the AMNES project.
            template (ExperimentTemplate): ExperimentTemplate instance for the
                                           AMNES project to be set.
            repetitions (int): Number of repetitions for a concrete experiment.
        """
        super().__init__(slug, name, description)
        self.template = template
        self.repetitions = repetitions
        self.__psets: Dict[str, ParameterSet] = {}
        self.__sequences: Dict[str, ExperimentSequence] = {}

    def __eq__(self, other: object) -> bool:
        """Check equality between this AmnesProject and an arbitrary object.

        Args:
            other (object): Arbitrary object to be checked for equality
                            with this AmnesProject instance.

        Returns:
            bool: True if `other` is equal to the current AmnesProject instance,
                  otherwise returns false.

        Raises:
            TypeError: If `other` is not of type AmnesProject.
        """
        if not isinstance(other, AmnesProject):
            raise TypeError("The object to be compared to is not of type AmnesProject.")
        return (
            super().__eq__(other)
            and self.template == other.template
            and self.repetitions == other.repetitions
            and self._psets_view() == other._psets_view()
            and self._sequences_view() == other._sequences_view()
        )

    @staticmethod
    def _parse_repetitions(key: str, values: Dict) -> int:
        """Internal method for parsing the number of ConcreteExperiment repetitions.

        Args:
            key (str): Key of the current AmnesProject dictionary that is parsed.
            values (Dict): Values of the current AmnesProject dictionary that is parsed.

        Returns:
            repetitions (int): Number of repetitions for one ConcreteExperiment.

        Raises:
            ParsingError: If no repetitions key in 'values' was found.
        """
        if "repetitions" in values:
            with YamlParsable._parse_key_context(key):
                repetitions = values.get("repetitions")
            if repetitions is not None:
                del values["repetitions"]
            else:
                raise ParsingError(
                    message="The defined repetitions value is empty.", key=key
                )
        else:
            raise ParsingError(
                message="No number of repetitions was defined for concrete experiments."
            )
        return repetitions

    @staticmethod
    def _parse_template(key: str, values: Dict) -> ExperimentTemplate:
        """Internal method for parsing the ExperimentTemplate.

        Args:
            key (str): Key of the current AmnesProject dictionary that is parsed.
            values (Dict): Values of the current AmnesProject dictionary that is parsed.

        Returns:
            template (ExperimentTemplate): The parsed ExperimentTemplate instance.

        Raises:
            ParsingError: If no template key in 'values' was found.
        """
        if "template" in values:
            with YamlParsable._parse_key_context(key):
                template_dict = values.get("template")
            if template_dict is not None:
                with YamlParsable._parse_key_context(key):
                    template = ExperimentTemplate.parse({"template": template_dict})
                del values["template"]
            else:
                raise ParsingError(message="The defined template is empty.", key=key)
        else:
            raise ParsingError(
                message="No template was defined for this project.", key=key
            )
        return template

    @staticmethod
    def _parse_parameter_sets(key: str, values: Dict) -> List[ParameterSet]:
        """Internal method for parsing the ParameterSet List.

        Args:
            key (str): Key of the current AmnesProject dictionary that is parsed.
            values (Dict): Values of the current AmnesProject dictionary that is parsed.

        Returns:
            psets (List[ParameterSet]): The parsed list of ParameterSet instances.

        Raises:
            ParsingError: If the defined parameters value is empty.
        """
        psets: List[ParameterSet] = []
        if "parameters" in values:
            with YamlParsable._parse_key_context(key):
                parameters_dict = values.get("parameters")
            if parameters_dict is not None:
                for pset in parameters_dict:
                    with YamlParsable._parse_key_context(key):
                        parameter_set = ParameterSet.parse(
                            {pset: parameters_dict.get(pset)}
                        )
                    psets.append(parameter_set)
                del values["parameters"]
            else:
                raise ParsingError(
                    message="The defined parameters value is empty.", key=key
                )
        return psets

    @staticmethod
    def parse(config: Dict) -> AmnesProject:
        """Static method for parsing an AmnesProject configuration.

        The overwritten parse method requires a dictionary with exactly
        one key value pair as parameter.
        The key is used as slug for the AmnesProject instance
        that is created.

        Example YAML config:

        ```yaml
        slug: myamnesproject
        name: My Test Amnes Project
        description: A basic configuration example for an Amnes Project.
        repetitions: 10
        template:
          stages:
            - Ping
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
        parameters:
          first_exp:
            name: First Experiment Sequence
            description: My first experiment sequence.
            assignments:
              "1": ["100", "200"]
        ```

        Dictionary, which is passed for this ExperimentTemplate:

        ```python
        {
            "myamnesproject": {
                "name": "My Test Amnes Project",
                "description": "A basic configuration example for an Amnes Project.",
                "repetitions": 10,
                "template": {
                    "stages": ["Ping"],
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
                                },
                            },
                        },
                    },
                },
                "parameters": {
                    "first_exp": {
                        "name": "First Experiment Sequence",
                        "description": "My first experiment sequence.",
                        "assignments": {"1": ["100", "200"]},
                    }
                }
            }
        }
        ```

        Args:
            config (Dict): Dictionary from which the AmnesProject
                           instance is created.

        Returns:
            project (AmnesProject): The AmnesProject instance
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

        repetitions = AmnesProject._parse_repetitions(key, values)
        template = AmnesProject._parse_template(key, values)
        psets = AmnesProject._parse_parameter_sets(key, values)

        if values:
            raise ParsingError(message="Config tree not empty after parsing.", key=key)

        with YamlParsable._parse_key_context(key):
            sequences = ExperimentSequence.create_sequences(
                template, psets, repetitions
            )
            project = AmnesProject(key, name, description, template, repetitions)
            project.add_psets(psets)
            project.add_sequences(sequences)

        return project

    @staticmethod
    def create_amnes_project(config: Dict) -> AmnesProject:
        """Method for creating an AmnesProject instance from a config dictionary.

        The controller can use this method to create an AmnesProject instance
        from a previously loaded YAML configuration file.
        All keys specified under the top-level key `.ignored` are ignored
        during parsing.

        Args:
            config (Dict): Configuration dictionary from which the AmnesProject
                           instance is to be generated.

        Returns:
            project (AmnesProject): The AmnesProject instance created from `config`.

        Raises:
            ParsingError: If an error occurred while creating the AmnesProject instance.
        """
        amnes_project_slug = str(config.get("slug"))
        with YamlParsable._parse_key_context(amnes_project_slug):
            del config["slug"]
        if ".ignored" in config:
            del config[".ignored"]
        with YamlParsable._parse_key_context(amnes_project_slug):
            project = AmnesProject.parse({amnes_project_slug: config})
        return project

    @property
    def template(self) -> ExperimentTemplate:
        """ExperimentTemplate: ExperimentTemplate of this AmnesProject instance.

        Returns:
            template (ExperimentTemplate): ExperimentTemplate of this AmnesProject
                                           instance.
        """
        return self.__template

    @template.setter
    def template(self, template: ExperimentTemplate) -> None:
        """Experiment template setter function.

        Args:
            template (ExperimentTemplate): ExperimentTemplate instance to be set
                                           for this AmnesProject instance.

        Raises:
            TypeError: If `template` is not of type ExperimentTemplate.
        """
        if not isinstance(template, ExperimentTemplate):
            raise TypeError("Template is not of type ExperimentTemplate.")
        self.__template = template

    @property
    def repetitions(self) -> int:
        """int: Number of repetitions of this AmnesProject instance.

        Returns:
            repetitions (int): Number of repetitions for a concrete experiment.
        """
        return self.__repetitions

    @repetitions.setter
    def repetitions(self, repetitions: int) -> None:
        """Repetitions setter function.

        Args:
            repetitions (int): Number of repetitions for a concrete experiment
                               to be set.

        Raises:
            TypeError: If `repetitions` is not of type integer.
            ValueError: If `repetitions` is not greater than or equal to one.
        """
        if not isinstance(repetitions, int):
            raise TypeError("Repetitions variable is not of type integer.")
        if repetitions <= 0:
            raise ValueError("Repetitions must be greater than or equal to one.")
        self.__repetitions = repetitions

    @property
    def psets(self) -> List[ParameterSet]:
        """List[ParameterSet]: ParameterSets of this AmnesProject instance.

        Returns:
            psets (List[ParameterSet]): ParameterSets of this AmnesProject instance.
        """
        return list(self.__psets.values())

    def _psets_view(self) -> ItemsView[str, ParameterSet]:
        return self.__psets.items()

    def add_psets(self, psets: List[ParameterSet]) -> None:
        """Add new parameter sets to the parameter set list of this AmnesProject.

        Args:
            psets (List[ParameterSet]): List of parameter sets to be added.

        Raises:
            TypeError: If `psets` is not of type List or a parameter set is not of
                       type ParameterSet.
            ValueError: If an parameter set in `psets` has an ambiguous slug that is
                        already in use.
        """
        if not isinstance(psets, List):
            raise TypeError("Given parameter sets are not of type List.")

        slugs: List[str] = []
        for pset in psets:
            if not isinstance(pset, ParameterSet):
                raise TypeError("Parameter set is not of type ParameterSet.")
            if pset.slug in self.__psets:
                raise ValueError("Used slug of parameter set already in use.")
            if pset.slug in slugs:
                raise ValueError("Found slug duplicate in given parameter set list.")
            slugs.append(pset.slug)

        for pset in psets:
            self.__psets[pset.slug] = pset

    def remove_psets(self, slugs: List[str]) -> None:
        """Remove parameter sets from the parameter set list of this AmnesProject.

        Args:
            slugs (List[str]): List of all slugs which identify the parameter sets
                               which should be removed.

        Raises:
            TypeError: If `slugs` is not of type List or a slug is not of type String.
            ValueError: If a slug cannot be resolved to any parameter set.
        """
        if not isinstance(slugs, List):
            raise TypeError("Given slugs are not of type List.")

        delslugs: List[str] = []
        for slug in slugs:
            if not isinstance(slug, str):
                raise TypeError("Slug is not of type String.")
            if slug not in self.__psets:
                raise ValueError("Used slug cannot be resolved to any parameter set.")
            if slug in delslugs:
                raise ValueError("Found slug duplicate in given slug list.")
            delslugs.append(slug)

        for slug in delslugs:
            del self.__psets[slug]

    @property
    def sequences(self) -> List[ExperimentSequence]:
        """List[ExperimentSequence]: ExperimentSequences of this AmnesProject instance.

        Returns:
            sequences (List[ExperimentSequence]): ExperimentSequences of this
                                                  AmnesProject instance.
        """
        return list(self.__sequences.values())

    def _sequences_view(self) -> ItemsView[str, ExperimentSequence]:
        return self.__sequences.items()

    def add_sequences(self, sequences: List[ExperimentSequence]) -> None:
        """Add new sequences to the sequence list of this AmnesProject.

        Args:
            sequences (List[ExperimentSequence]): List of sequences to be added.

        Raises:
            TypeError: If `sequences` is not of type List or an sequence is not of
                       type ExperimentSequence.
            ValueError: If an sequence in `sequences` has an ambiguous slug that is
                        already in use.
        """
        if not isinstance(sequences, List):
            raise TypeError("Given sequences are not of type List.")

        slugs: List[str] = []
        for seq in sequences:
            if not isinstance(seq, ExperimentSequence):
                raise TypeError("Sequence is not of type ExperimentSequence.")
            if seq.pset.slug in self.__sequences:
                raise ValueError(
                    "Used slug of corresponding parameter set for the "
                    + "experiment sequence is already in use."
                )
            if seq.pset.slug in slugs:
                raise ValueError(
                    "Found slug duplicate in given experiment sequence list."
                )
            slugs.append(seq.pset.slug)

        for seq in sequences:
            self.__sequences[seq.pset.slug] = seq

    def remove_sequences(self, slugs: List[str]) -> None:
        """Remove sequences from the sequence list of this AmnesProject.

        Args:
            slugs (List[str]): List of all slugs which identify the sequences
                               which should be removed.

        Raises:
            TypeError: If `slugs` is not of type List or a slug is not of type String.
            ValueError: If a slug cannot be resolved to any sequence.
        """
        if not isinstance(slugs, List):
            raise TypeError("Given slugs are not of type List.")

        delslugs: List[str] = []
        for slug in slugs:
            if not isinstance(slug, str):
                raise TypeError("Slug is not of type String.")
            if slug not in self.__sequences:
                raise ValueError(
                    "Used slug of corresponding ParameterSet cannot "
                    + "be resolved to any experiment sequence."
                )
            if slug in delslugs:
                raise ValueError("Found slug duplicate in given slug list.")
            delslugs.append(slug)

        for slug in delslugs:
            del self.__sequences[slug]
