"""This module contains all necessary definitions for the ParameterSet class.

Classes:
    ParameterSet: Parameter Set class for organizing parameters and assignments
                  for experiments.
    ParameterSetError: Error raised for invalid operations on parameter sets.
"""

from __future__ import annotations

from typing import Dict, ItemsView, KeysView, List

from ..utils.parser import ParsingError, YamlParsable
from .amnes_object import AmnesObject


class ParameterSet(AmnesObject, YamlParsable):
    """Parameter Set class for organizing parameters and assignments for experiments.

    Attributes:
        parameters (KeysView[str]): View of all registered parameters for this set.
        assignments (ItemsView[str, List[str]]): View of all parameters and their
                                                 assignments.
    """

    def __init__(self, slug: str, name: str, description: str) -> None:
        """Parameter Set class constructor method.

        Parameters and their assignments cannot be set on object initialization
        and must be added by `add_parameter` and `add_assignments` afterwards.

        Args:
            slug (str): Short identifier for the Parameter Set,
                        which must be a valid, non-empty string.
            name (str): Full name for the Parameter Set.
            description (str): Custom description for the Parameter Set.
        """
        super().__init__(slug, name, description)
        self.__assignments: Dict[str, List[str]] = {}

    def __eq__(self, other: object) -> bool:
        """Check equality between current ParameterSet instance and arbitrary object.

        Args:
            other (object): Arbitrary object to be checked for equality
                            with this ParameterSet instance.

        Returns:
            bool: True if `other` is equal to the current ParameterSet instance,
                  otherwise returns false.

        Raises:
            TypeError: If `other` is not of type ParameterSet.
        """
        if not isinstance(other, ParameterSet):
            raise TypeError("The object to be compared to is not of type ParameterSet.")
        if (not super().__eq__(other)) or (not self.parameters == other.parameters):
            return False
        self_dict = dict(self.assignments)
        other_dict = dict(other.assignments)
        for parameter in self.parameters:
            if set(self_dict[parameter]) != set(other_dict[parameter]):
                return False
        return True

    @staticmethod
    def parse(config: Dict) -> ParameterSet:
        """Static method for parsing a ParameterSet configuration.

        The overwritten parse method requires a dictionary with exactly
        one key value pair as parameter.
        The key is used as slug for the ParameterSet instance
        that is created.

        Example YAML config:

        ```yaml
        first_exp:
          name: First Experiment Sequence
          description: My first experiment sequence.
          assignments:
            "1": ["5000", "3000"]
            "2": ["5000"]
        ```

        Dictionary, which is passed for this NodeTask:

        ```python
        {
        "first_exp": {
            "name": "First Experiment Sequence",
            "description": "My first experiment sequence.",
            "assignments": {"1": ["5000", "3000"], "2": ["5000"]},
        }
        ```

        Args:
            config (Dict): Dictionary from which the ParameterSet instance is created.

        Returns:
            pset (ParameterSet): The ParameterSet instance created from `config`.

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
            assignments = values.get("assignments")

        if assignments is None:
            raise ParsingError(
                message="No assignments were found in the ParameterSet.", key=key
            )
        del values["assignments"]

        if values:
            raise ParsingError(
                message="Config tree not empty after parsing.", key=key,
            )

        with YamlParsable._parse_key_context(key):
            pset = ParameterSet(key, name, description)

        for param in assignments:
            with YamlParsable._parse_key_context(key):
                pset.add_parameter(param)
            with YamlParsable._parse_key_context(key):
                pset.add_assignments(param, assignments[param])

        return pset

    @property
    def assignments(self) -> ItemsView[str, List[str]]:
        """ItemsView[str, List[str]]: View of all parameters and their assignments.

        Returns:
            ItemsView[str, List[str]]: View of all parameters and their assignments.
        """
        return self.__assignments.items()

    @property
    def parameters(self) -> KeysView[str]:
        """KeysView[str]: View of all registered parameters for this set.

        Returns:
            KeysView[str]: View of all registered parameters for this set.
        """
        return self.__assignments.keys()

    def add_parameter(self, parameter: str) -> None:
        """Add new parameter to parameter set.

        The given parameter must not already be a parameter of the parameter set
        and the parameter must be a valid parameter string.

        Args:
            parameter (str): The parameter which should be added.

        Raises:
            ParameterSetError: If parameter is already present in set.
        """
        self._check_parameter_validity(parameter)
        if self._isparameter(parameter):
            raise ParameterSetError("Given parameter already present in set.")
        self.__assignments.update({parameter: []})

    def remove_parameter(self, parameter: str) -> None:
        """Remove existing parameter from parameter set.

        The given parameter must already be a parameter of the parameter set
        and the parameter must be a valid parameter string.

        This will also remove all assignments of the parameter.

        Args:
            parameter (str): The parameter which should be removed.

        Raises:
            ParameterSetError: If parameter is not already present in set.
        """
        self._check_parameter_validity(parameter)
        if not self._isparameter(parameter):
            raise ParameterSetError("Given parameter not present in set.")
        del self.__assignments[parameter]

    def add_assignments(self, parameter: str, values: List[str]) -> None:
        """Add assignments to existing parameter in parameter set.

        The given parameter must already be a parameter of the parameter set
        and the parameter must be a valid parameter string.
        The list of values must be a list of valid value strings.

        It is possible to add the same value for a parameter more than once.

        Args:
            parameter (str): The parameter to which the values should be added
                             as assignments.
            values (List[str]): The values which should be added as assignments.

        Raises:
            ParameterSetError: If parameter is not already present in set.
        """
        self._check_parameter_validity(parameter)
        if not self._isparameter(parameter):
            raise ParameterSetError("Given parameter not present in set.")
        self._check_values_validity(values)
        self.__assignments[parameter].extend(values)

    def remove_assignments(self, parameter: str, values: List[str]) -> None:
        """Remove assignments from existing parameter in parameter set.

        The given parameter must already be a parameter of the parameter set
        and the parameter must be a valid parameter string.
        The given values must be a list of valid value strings and be set as
        assignments for the parameter at least once.

        If one of the given values are not assignments for the parameter,
        none of the values are removed.
        If a given value is an assignment for the parameter mutiple times,
        only one occurrence is removed.

        Args:
            parameter (str): The parameter from which the assignment values
                             should be removed.
            values (List[str]): The assignments values which should be removed.

        Raises:
            ParameterSetError: If parameter is not already present in set or
                               not all values are assignments for the given
                               parameter.
        """
        self._check_parameter_validity(parameter)
        if not self._isparameter(parameter):
            raise ParameterSetError("Given parameter not present in set.")
        self._check_values_validity(values)
        if not all(val in self.__assignments[parameter] for val in values):
            raise ParameterSetError(
                "Given values are not all assignments for given parameter."
            )
        for val in values:
            self.__assignments[parameter].remove(val)

    def _isparameter(self, parameter: str) -> bool:
        """Check if the parameter is already in parameter set.

        Args:
            parameter (str): Parameter which should be checked.

        Returns:
            bool: True if parameter is already in parameter set, False otherwise.
        """
        return parameter in self.parameters

    @staticmethod
    def _check_parameter_validity(parameter: str) -> None:
        """Check if the parameter meets the string requirements.

        This check does not return anything but will instead raise
        an error if the given parameter does not meet the string
        requirements.

        This internal methods must be used by all public methods
        which accept parameters.

        Args:
            parameter (str): Parameter which should be checked.

        Raises:
            TypeError: If parameter is not of type string.
            ValueError: If parameter is an invalid parameter string.
        """
        if not isinstance(parameter, str):
            raise TypeError("Given parameter string is not of type string.")
        if (not parameter) or (parameter.isspace()):
            raise ValueError("Given parameter string is not a valid parameter string.")

    @staticmethod
    def _check_values_validity(values: List[str]) -> None:
        """Check if the value list meets the requirements.

        This check does not return anything but will instead raise
        an error if the given list of values does not meet the requirements.

        This internal methods must be used by all public methods
        which accept lists of values.

        Args:
            values (List[str]): List of values which should be checked.

        Raises:
            TypeError: If list is not of type List or if any value from the list
                       is not of type string.
        """
        if not isinstance(values, List):
            raise TypeError("Values are not a list.")
        for val in values:
            if not isinstance(val, str):
                raise TypeError("Value is not of type string.")


class ParameterSetError(Exception):
    """Error raised for invalid operations on parameter sets.

    This error is raised by ParameterSet class for invalid operations and states.
    """
