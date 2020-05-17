"""This module contains all necessary definitions for the NodeTask class.

Classes:
    NodeTask: NodeTask class for specifying tasks executed on a node in a stage.
    NodeTaskConfig: Simple key-value configuration for a NodeTask.
    NodeTaskParams: Simple key-value configuration for parameters of a NodeTask.
    NodeTaskFiles: Simple key-value configuration for linked files of a NodeTask.
"""

from __future__ import annotations

import re
from typing import Dict, ItemsView, KeysView, Optional

from ..utils.parser import ParsingError, YamlParsable
from .amnes_object import AmnesObject
from .experiment_stage import ExperimentStage


class NodeTaskConfig:
    """Simple key-value configuration for a NodeTask.

    Attributes:
        keys (KeysView[str]): View of all registered keys for this configuration.
        pairs (ItemsView[str, str]): View of all keys and their values.
    """

    def __init__(self, indict: Optional[Dict[str, str]] = None) -> None:
        """Node Task Configuration class constructor method.

        It is possible to initialize the key-value configuration with an
        existing set of key-value pairs.
        These pairs must meet the requirements for key and value strings.
        If any key or value fails the requirements check, nothing will be imported
        and the initialization will fail.

        Args:
            indict (Dict[str, str]): Key-Value pairs which must meet the requirements
                                     for key and value strings and are imported on
                                     configuration creation.

        Raises:
            TypeError: If input dictionary is not of type Dict.
        """
        self.__kvdic: Dict[str, str] = {}
        if indict is not None:
            if not isinstance(indict, Dict):
                raise TypeError("Given input dictinary is not of type Dict.")
            # Only add any pair if all pairs meet the requirements
            for key in indict:
                self._check_key(key)
                self._check_value(indict[key])
            for key in indict:
                self.add_pair(key, indict[key])

    def __eq__(self, other: object) -> bool:
        """Check equality between current NodeTaskConfig instance and arbitrary object.

        Args:
            other (object): Arbitrary object to be checked for equality
                            with this NodeTaskConfig instance.

        Returns:
            bool: True if `other` is equal to the current NodeTaskConfig instance,
                  otherwise returns false.

        Raises:
            TypeError: If `other` is not of type NodeTaskConfig.
        """
        if not isinstance(other, NodeTaskConfig):
            raise TypeError(
                "The object to be compared to is not of type NodeTaskConfig."
            )
        return self.pairs == other.pairs

    @property
    def keys(self) -> KeysView[str]:
        """KeysView[str]: View of all registered keys for this configuration.

        Returns:
            KeysView[str]: View of all registered keys for this configuration.
        """
        return self.__kvdic.keys()

    @property
    def pairs(self) -> ItemsView[str, str]:
        """ItemsView[str, str]: View of all keys and their values.

        Returns:
            ItemsView[str, str]: View of all keys and their values.
        """
        return self.__kvdic.items()

    def add_pair(self, key: str, value: str) -> None:
        """Add new key-value pair to configuration.

        The given key must not already be in use and the key and value strings
        must meet the requirements.

        Args:
            key (str): The key of the pair which should be added.
            value (str): The value of the pair which should be added.

        Raises:
            NodeTaskError: If key is already present in configuration.
        """
        self._check_key(key)
        self._check_value(value)
        if key in self.__kvdic:
            raise NodeTaskError("Given key already in use for this configuration.")
        self.__kvdic[key] = value

    def remove_pair(self, key: str) -> None:
        """Remove key-value pair from configuration.

        The given key must be in use for the configuration.

        Args:
            key (str): The key of the pair which shoule be removed.

        Raises:
            NodeTaskError: If key is not present in configuration.
        """
        self._check_key(key)
        if key not in self.__kvdic:
            raise NodeTaskError("Given key not in use for this configuration.")
        del self.__kvdic[key]

    def update_pair(self, key: str, value: str) -> None:
        """Update key-value pair of configuration.

        The given key must be in use for the configuration and the value string
        must meet the requirements.

        Args:
            key (str): The key of the pair which should be updated.
            value (str): The new value for the pair which should be updated.

        Raises:
            NodeTaskError: If key is not present in configuration.
        """
        self._check_key(key)
        self._check_value(value)
        if key not in self.__kvdic:
            raise NodeTaskError("Given key not in use for this configuration.")
        self.__kvdic[key] = value

    @staticmethod
    def _check_key(key: str) -> None:
        """Check if the key is a valid configuration key.

        This check does not return anything but will instead raise
        an error if the given key does not meet the string requirements.

        Args:
            key (str): Key which should be checked.

        Raises:
            TypeError: If key is not of type string.
            ValueError: If key is an invalid key string.
        """
        if not isinstance(key, str):
            raise TypeError("Given key string is not of type string.")
        if (not key) or (key.isspace()):
            raise ValueError("Given key string is not a valid config key string.")

    @staticmethod
    def _check_value(value: str) -> None:
        """Check if the value is a valid configuration value.

        This check does not return anything but will instead raise
        an error if the given value does not meet the string requirements.

        Args:
            value (str): Value which should be checked.

        Raises:
            TypeError: If value is not of type string.
            ValueError: If value is an invalid value string.
        """
        if not isinstance(value, str):
            raise TypeError("Given value string is not of type string.")
        if (not value) or (value.isspace()):
            raise ValueError("Given value string is not a valid config value string.")


class NodeTaskParams(NodeTaskConfig):
    """Simple key-value configuration for parameters of a NodeTask.

    Attributes:
        keys (KeysView[str]): View of all registered keys for this configuration.
        pairs (ItemsView[str, str]): View of all keys and their values.
    """

    @staticmethod
    def _check_value(value: str) -> None:
        """Check if the value is a valid configuration value.

        This check does not return anything but will instead raise
        an error if the given value does not meet the string requirements.

        In contrast to NodeTaskConfig, NodeTaskParams explicitly allows
        empty or space-only strings as values.

        Args:
            value (str): Value which should be checked.

        Raises:
            TypeError: If value is not of type string.
        """
        if not isinstance(value, str):
            raise TypeError("Given value string is not of type string.")
        # Parameter values can be empty or space-only strings

    @staticmethod
    def serialize(obj: NodeTaskParams) -> Dict:
        """Serialize NodeTaskParams instance for Pyro communication.

        Args:
            obj (NodeTaskParams): Instance to be serialized.

        Returns:
            Dict: Serialized representation of instance as dictionary.
        """
        return {
            "__class__": f"{NodeTaskParams.__module__}.{NodeTaskParams.__name__}",
            "data": dict(obj.pairs),
        }

    @staticmethod
    def deserialize(
        classname: str, indict: Dict  # pylint: disable=unused-argument
    ) -> NodeTaskParams:
        """Deserialize NodeTaskParams dictionary from Pyro communication.

        Args:
            classname (str): Name of class which was serialized.
            indict (Dict): Serialized representation of instance as dictionary.

        Returns:
            NodeTaskParams: Instance deserialized from dictionary representation.
        """
        return NodeTaskParams(indict["data"])


class NodeTaskFiles(NodeTaskConfig):
    """Simple key-value configuration for linked files of a NodeTask.

    The values only contain a unqiue identifier which can be passed to
    the DataManager to get the corresponding file.

    Attributes:
        keys (KeysView[str]): View of all registered keys for this configuration.
        pairs (ItemsView[str, str]): View of all keys and their values.
    """

    @staticmethod
    def serialize(obj: NodeTaskFiles) -> Dict:
        """Serialize NodeTaskFiles instance for Pyro communication.

        Args:
            obj (NodeTaskFiles): Instance to be serialized.

        Returns:
            Dict: Serialized representation of instance as dictionary.
        """
        return {
            "__class__": f"{NodeTaskFiles.__module__}.{NodeTaskFiles.__name__}",
            "data": dict(obj.pairs),
        }

    @staticmethod
    def deserialize(
        classname: str, indict: Dict  # pylint: disable=unused-argument
    ) -> NodeTaskFiles:
        """Deserialize NodeTaskFiles dictionary from Pyro communication.

        Args:
            classname (str): Name of class which was serialized.
            indict (Dict): Serialized representation of instance as dictionary.

        Returns:
            NodeTaskFiles: Instance deserialized from dictionary representation.
        """
        return NodeTaskFiles(indict["data"])


class NodeTask(AmnesObject, YamlParsable):
    """NodeTask class for specifying tasks executed on a node in a stage.

    This class defines a specific task which has to be executed on a given node
    when AMNES is entering the specified stage.

    Attributes:
        slug (str): Short identifier for the Node Task,
                    which must be a valid, non-empty string.
        name (str): Full name for the Node Task.
        description (str): Custom description for the Node Task.
        module (str): Path of the module used as base for the Node Task.
        stage (ExperimentStage): Stage in which the Node Task should be executed.
        params (NodeTaskParams): Configuration parameters for the Node Task.
        files (NodeTaskFiles): Configuration files for the Node Task.
    """

    REGEX_MODULENAME = re.compile(r"^[a-zA-Z0-9_]+$")

    def __init__(
        self,
        slug: str,
        name: str,
        description: str,
        module: str,
        stage: ExperimentStage,
        params: Optional[NodeTaskParams],
        files: Optional[NodeTaskFiles],
    ) -> None:
        """Node task class constructor method.

        Configuration parameters and configuration files can be passed to
        the constructor.
        Otherwise an empty NodeTaskParams and NodeTaskFiles object is automatically
        created.

        Args:
            slug (str): Short identifier for the Node Task,
                        which must be a valid, non-empty string.
            name (str): Full name for the Node Task.
            description (str): Custom description for the Node Task.
            module (str): Path of the module used as base for the Node Task.
            stage (ExperimentStage): Stage in which the Node Task should be executed.
            params (:obj:`NodeTaskParams`, optional): Configuration parameters
                                                      for the Node Task.
            files (:obj:`NodeTaskFiles`, optional): Configuration files for
                                                    the Node Task.
        """
        super().__init__(slug, name, description)
        self.module = module
        self.stage = stage
        self.params = params if params is not None else NodeTaskParams()
        self.files = files if files is not None else NodeTaskFiles()

    def __eq__(self, other: object) -> bool:
        """Check equality between current NodeTask instance and arbitrary object.

        Args:
            other (object): Arbitrary object to be checked for equality
                            with this NodeTask instance.

        Returns:
            bool: True if `other` is equal to the current NodeTask instance,
                  otherwise returns false.

        Raises:
            TypeError: If `other` is not of type NodeTask.
        """
        if not isinstance(other, NodeTask):
            raise TypeError("The object to be compared to is not of type NodeTask.")
        return (
            super().__eq__(other)
            and (self.module == other.module)
            and (self.stage == other.stage)
            and (self.params == other.params)
            and (self.files == other.files)
        )

    @property
    def module(self) -> str:
        """str: Path of the module used as base for the Node Task.

        Returns:
            str: Path of the module used as base for the Node Task.
        """
        return self.__module

    @module.setter
    def module(self, module: str) -> None:
        """Node Task module path setter function.

        Args:
            module (str): Path of the module used as base for the Node Task.

        Raises:
            TypeError: If module path is not of type string.
            ValueError: If module path string does not match module path format.
        """
        if not isinstance(module, str):
            raise TypeError("Module path is not of type string.")
        module_parts = module.split(".")
        if (module_parts.__len__() < 2) or not all(
            NodeTask.REGEX_MODULENAME.match(mp) for mp in module_parts
        ):
            raise ValueError(
                "Given module path string does not match module path format."
            )
        self.__module = module

    @property
    def stage(self) -> ExperimentStage:
        """ExperimentStage: Stage in which the Node Task should be executed.

        Returns:
            ExperimentStage: Stage in which the Node Task should be executed.
        """
        return self.__stage

    @stage.setter
    def stage(self, stage: ExperimentStage) -> None:
        """Node Task stage setter function.

        Args:
            stage (ExperimentStage): Stage in which the Node Task should be executed.

        Raises:
            TypeError: If stage is not of type ExperimentStage.
        """
        if not isinstance(stage, ExperimentStage):
            raise TypeError("Stage is not of type ExperimentStage.")
        self.__stage = stage

    @property
    def params(self) -> NodeTaskParams:
        """NodeTaskParams: Configuration parameters for the Node Task.

        Returns:
            NodeTaskParams: Configuration parameters for the Node Task.
        """
        return self.__params

    @params.setter
    def params(self, params: NodeTaskParams) -> None:
        """Node Task configuration parameters setter function.

        Args:
            params (NodeTaskParams): Configuration parameters for the Node Task.

        Raises:
            TypeError: Configuration parameters object not of type NodeTaskParams.
        """
        if not isinstance(params, NodeTaskParams):
            raise TypeError(
                "Configuration parameters object not of type NodeTaskParams."
            )
        self.__params = params

    @property
    def files(self) -> NodeTaskFiles:
        """NodeTaskFiles: Configuration files for the Node Task.

        Returns:
            NodeTaskFiles: Configuration files for the Node Task.
        """
        return self.__files

    @files.setter
    def files(self, files: NodeTaskFiles) -> None:
        """Node Task configuration files setter function.

        Args:
            files (NodeTaskFiles): Configuration files for the Node Task.

        Raises:
            TypeError: Configuration files object not of type NodeTaskFiles.
        """
        if not isinstance(files, NodeTaskFiles):
            raise TypeError("Configuration files object not of type NodeTaskFiles.")
        self.__files = files

    @staticmethod
    def parse(config: Dict) -> NodeTask:
        """Static method for parsing a NodeTask configuration.

        The overwritten parse method requires a dictionary with exactly
        one key value pair as parameter.
        The key is used as slug for the NodeTask instance
        that is created.

        Example YAML config:

        ```yaml
        collect_stat:
          name: Collect Statistics
          description: My collect task.
          module: CollectStatistics
          stage: Collect
          params:
            level: "1"
          files:
            appconfig: "/mydir/app.config"
        ```

        Dictionary, which is passed for this NodeTask:

        ```python
        {
        "collect_stat": {
            "name": "Collect Statistics",
            "description": "My collect task.",
            "module": "CollectStatistics",
            "stage": "Collect",
            "params": {"level": "1"},
            "files": {"appconfig": "/mydir/app.config"},
        }
        ```

        Args:
            config (Dict): Dictionary from which the NodeTask instance is created.

        Returns:
            ntask (NodeTask): The NodeTask instance created from `config`.

        Raises:
            ParsingError: If an exception occurs while parsing the `config`
                          dictionary or `config` is not empty after parsing.
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
            module = values.get("module")
            if module is not None:
                del values["module"]
            stage = ExperimentStage.parse({values.get("stage"): None})
            del values["stage"]
            params = NodeTaskParams(values.get("params"))
            if values.get("params") is not None:
                del values["params"]
            files = NodeTaskFiles(values.get("files"))
            if values.get("files") is not None:
                del values["files"]

        if values:
            raise ParsingError(message="Config tree not empty after parsing.", key=key)

        with YamlParsable._parse_key_context(key):
            ntask = NodeTask(key, name, description, module, stage, params, files)

        return ntask


class NodeTaskError(Exception):
    """Error raised for invalid operations on node tasks and node task configs.

    This error is raised by NodeTask or NodeTaskConfig class (including subclasses)
    for invalid operations and states.
    """
