"""This module contains all classes for worker configuration.

Classes:
    WorkerConfigTree: Configuration tree for an AMNES worker.
    WorkerConfiguration: Configuration for for an AMNES worker.
"""

from __future__ import annotations

from typing import Dict

from ...utils import errors
from ...utils.config import BaseConfigTree, ConfigurationError
from ..config import ExecutionConfigTree, ExecutionConfiguration


class WorkerConfigTree(BaseConfigTree):  # pylint: disable=too-few-public-methods
    """Configuration tree for an AMNES worker.

    This configuration tree defines basic configuration values for an
    AMNES worker.
    """

    @classmethod
    def parse(cls, cfgdict: Dict) -> WorkerConfigTree:
        """Parse dictionary and create worker configuration tree.

        Args:
            cfgdict (Dict): Part of configuration dictionary which is located under the
                            worker configuration key of the configuration tree.

        Returns:
            Worker configuration tree created from the given dictionary.
        """
        return WorkerConfigTree()


class WorkerConfiguration(ExecutionConfiguration):
    """Configuration for for an AMNES worker.

    This configuration consists of the following configuration trees:
      - `ExecutionConfigTree`: Configuration tree for AMNES execution components.
      - `WorkerConfigTree`: Configuration tree for an AMNES worker.

    Example YAML configuration:

    ```yaml
    exec:
        name: "Example Component"
        address: "123.123.123.123"
        port: 789
    worker: {}
    ```

    Attributes:
        execution (ExecutionConfigTree): Configuration tree for AMNES execution
                                         components.
        worker (WorkerConfigTree): Configuration tree for an AMNES worker.
    """

    def __init__(
        self, *, execution: ExecutionConfigTree, worker: WorkerConfigTree
    ) -> None:
        """Worker configuration constructor method.

        Args:
            execution (ExecutionConfigTree): Configuration tree for AMNES execution
                                             components.
            worker (WorkerConfigTree): Configuration tree for an AMNES worker.
        """
        super().__init__(execution=execution)
        self.__set_worker(worker)

    @classmethod
    def create_from(
        cls, execution_config: ExecutionConfiguration, worker: WorkerConfigTree
    ) -> WorkerConfiguration:
        """Create worker configuration from existing execution configuration.

        Args:
            execution_config (ExecutionConfiguration): Existing execution configuration
                                                       which should be used as base.
            worker (WorkerConfigTree): Configuration tree for an AMNES worker.

        Returns:
            Worker configuration created on existing execution configuration.
        """
        return WorkerConfiguration(execution=execution_config.execution, worker=worker)

    @classmethod
    def from_yamldict(cls, yamlconfig: Dict) -> WorkerConfiguration:
        """Create worker configuration from YAML dictionary.

        This function will read and delete the key 'worker' of the YAML dictionary.
        It calls functions which will read and delete the following keys: 'exec'.

        Args:
            yamlconfig (Dict): Dictionary representation of an YAML file from which the
                               worker configuration should be created.

        Returns:
            Worker configuration created from the given YAML dictionary.

        Raises:
            ConfigurationError: If an exception occurs while creating the
                                worker configuration.
        """
        execconfig = super().from_yamldict(yamlconfig)
        workertree = yamlconfig.get("worker")
        if workertree is None:
            raise ConfigurationError(
                message="First level key 'worker' is missing"
                + "for worker configuration tree."
            )
        if not isinstance(workertree, Dict):
            raise ConfigurationError(obj="worker config") from errors.noft(
                "worker config tree", "Dict"
            )
        worker = WorkerConfigTree.parse(workertree)
        del yamlconfig["worker"]
        return WorkerConfiguration.create_from(execconfig, worker=worker)

    @property
    def worker(self) -> WorkerConfigTree:
        """WorkerConfigTree: Configuration tree for an AMNES worker.

        Returns:
            WorkerConfigTree: Configuration tree for an AMNES worker.
        """
        return self.__worker

    def __set_worker(self, worker: WorkerConfigTree) -> None:
        """Set worker config tree.

        Args:
            worker (WorkerConfigTree): Configuration tree for an AMNES worker.

        Raises:
            TypeError: If given worker config tree is not of type WorkerConfigTree.
        """
        if not isinstance(worker, WorkerConfigTree):
            raise errors.noftc("worker config tree", WorkerConfigTree)
        self.__worker: WorkerConfigTree = worker
