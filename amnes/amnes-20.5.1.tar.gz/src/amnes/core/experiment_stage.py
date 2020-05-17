"""This module contains all necessary definitions for the ExperimentStage class.

Classes:
    ExperimentStage: Experiment stage class for structuring
                     the experiment execution order.
"""

from __future__ import annotations

from typing import Dict

from ..utils.parser import ParsingError, YamlParsable
from .amnes_object import AmnesObject


class ExperimentStage(AmnesObject, YamlParsable):
    """Experiment stage class for structuring the experiment execution order.

    This class defines an experiment stage, that can be used in the experiment
    configuration by users to structure the order of experiment execution.
    """

    def __eq__(self, other: object) -> bool:
        """Check equality between ExperimentStage instance and an arbitrary object.

        Args:
            other (object): Arbitrary object to be checked for equality
                            with this ExperimentStage instance.

        Returns:
            bool: True if `other` is equal to the current ExperimentStage instance,
                  otherwise returns false.

        Raises:
            TypeError: If `other` is not of type ExperimentStage.
        """
        if not isinstance(other, ExperimentStage):
            raise TypeError(
                "The object to be compared to is not of type ExperimentStage."
            )
        return super().__eq__(other)

    @staticmethod
    def parse(config: Dict) -> ExperimentStage:
        """Static method for parsing an ExperimentStage configuration.

        The overwritten parse method requires a dictionary with exactly
        one key value pair as parameter.
        The key is used as slug for the ExperimentStage instance
        that is created.

        Example YAML config:

        ```yaml
        stages:
          - Ping:
              name: Ping Stage
              description: My ping stage.
          - Collect
        ```

        Dictionary, which is passed for each stage:

        ```python
        - {"Ping": {"name": "Ping Stage", "description": "My ping stage."}}
        - {'Collect': None}
        ```

        Args:
            config (Dict): Dictionary from which the ExperimentStage
                           instance is created.

        Returns:
            stage (ExperimentStage): The ExperimentStage instance created
                                     from `config`.

        Raises:
            ParsingError: If an exception occurs while parsing the `config`
                          dictionary or `config` is not empty after parsing.
        """
        YamlParsable._parse_check(config)

        key = list(config.keys())[0]
        values = list(config.values())[0]

        if values is None:
            with YamlParsable._parse_key_context(key):
                stage = ExperimentStage(key, "", "")
            return stage

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
            stage = ExperimentStage(key, name, description)

        if values:
            raise ParsingError(message="Config tree not empty after parsing.", key=key)

        return stage
