"""This module contains all classes for controller configuration.

Classes:
    ControllerConfigTree: Configuration tree for an AMNES controller.
    ControllerConfiguration: Configuration for for an AMNES controller.
"""

from __future__ import annotations

import ipaddress
from typing import Dict, Optional

from ...utils import errors
from ...utils.config import BaseConfigTree, ConfigurationError
from ..config import ExecutionConfigTree, ExecutionConfiguration
from .storage import PostgresConfigTree


class ControllerConfigTree(BaseConfigTree):
    """Configuration tree for an AMNES controller.

    This configuration tree defines basic configuration values for an
    AMNES controller.
    """

    BACKENDS = ["sqlite", "postgres"]

    def __init__(
        self,
        *,
        backend: str,
        postgres: Optional[PostgresConfigTree],
        filetransfer_address: str,
        filetransfer_port: int
    ) -> None:
        """Controller configuration tree constructor method.

        Args:
            backend (str): Identifier for storage backend used by controller.
            postgres (Optional[PostgresConfigTree]): Postgres Database
                                                     Configuration used if postgres is
                                                     used as backend.
            filetransfer_address (str): Address for the file transfer endpoint of the
                                        AMNES Controller.
            filetransfer_port (int): Port for the file transfer endpoint of the
                                     AMNES Controller.

        """
        self.__set_backend(backend)
        self.__set_postgres(postgres)
        self.__set_filetransfer_address(filetransfer_address)
        self.__set_filetransfer_port(filetransfer_port)

    @property
    def backend(self) -> str:
        """str: Identifier for storage backend used by controller.

        Returns:
            str: Identifier for storage backend used by controller.
        """
        return self.__backend

    def __set_backend(self, backend: str) -> None:
        """Set identifier for storage backend used by controller.

        Args:
            backend (str): Identifier for storage backend used by controller.

        Raises:
            TypeError: If given backend is not of type string.
            ValueError: If given backend is invalid or unknown.
        """
        if not isinstance(backend, str):
            raise errors.noftc("backend", str)
        if backend not in ControllerConfigTree.BACKENDS:
            raise ValueError("Invalid backend specified.")
        self.__backend: str = backend

    @property
    def postgres(self) -> Optional[PostgresConfigTree]:
        """Optional[PostgresConfigTree]: Postgres Database Configuration.

        Returns:
            Optional[PostgresConfigTree]: Postgres Database Configuration.
        """
        return self.__postgres

    def __set_postgres(self, postgres: Optional[PostgresConfigTree]) -> None:
        """Set postgres Database Configuration.

        Args:
            postgres (PostgresConfigTree): Postgres Database Configuration.

        Raises:
            TypeError: If given postgres configuration is not of type
                       PostgresConfigTree (and not None).
        """
        if postgres is None:
            self.__postgres: Optional[PostgresConfigTree] = None
            return
        if not isinstance(postgres, PostgresConfigTree):
            raise errors.noftc("postgres", PostgresConfigTree)
        self.__postgres = postgres

    @property
    def filetransfer_address(self) -> str:
        """str: Address for the file transfer endpoint of the AMNES Controller.

        Returns:
            str: Address for the file transfer endpoint of the AMNES Controller.
        """
        return self.__filetransfer_address

    def __set_filetransfer_address(self, filetransfer_address: str) -> None:
        """Set address attribute for file transfer endpoint of the AMNES Controller.

        Args:
            filetransfer_address (str): Address for the file transfer endpoint of the
                                        AMNES Controller.

        Raises:
            TypeError: If given address is not of type string.
            ValueError: If given address is not a valid IPv4 or IPv6 address.
        """
        if not isinstance(filetransfer_address, str):
            raise errors.noftc("filetransfer_address", str)
        try:
            ipaddress.ip_address(filetransfer_address)
        except ValueError as exc:
            raise ValueError(
                "Given address is not a valid IPv4 or IPv6 address."
            ) from exc
        self.__filetransfer_address: str = filetransfer_address

    @property
    def filetransfer_port(self) -> int:
        """int: Port for the file transfer endpoint of the AMNES Controller.

        Returns:
            int: Port for the file transfer endpoint of the AMNES Controller.
        """
        return self.__filetransfer_port

    def __set_filetransfer_port(self, filetransfer_port: int) -> None:
        """Set port attribute for the file transfer endpoint of the AMNES Controller.

        Args:
            filetransfer_port (int): Port for the file transfer endpoint of the
                                     AMNES Controller.

        Raises:
            TypeError: If given port is not of type integer.
            ValueError: If given port is outside of permitted port range.
        """
        if not isinstance(filetransfer_port, int):
            raise errors.noftc("filetransfer_port", int)
        if not 0 < filetransfer_port <= 65535:
            raise ValueError("Given port is outside of permitted port range.")
        self.__filetransfer_port: int = filetransfer_port

    @classmethod
    def parse(cls, cfgdict: Dict) -> ControllerConfigTree:
        """Parse dictionary and create controller configuration tree.

        Args:
            cfgdict (Dict): Part of configuration dictionary which is located under the
                            controller configuration key of the configuration tree.

        Returns:
            Controller configuration tree created from the given dictionary.

        Raises:
            ConfigurationError: If an exception occurs while parsing the config
                                dictionary.
        """
        backend = cfgdict.get("backend")
        if backend is not None:
            del cfgdict["backend"]
        postgrestree: Optional[PostgresConfigTree] = None
        if backend == "postgres":
            postgres = cfgdict.get("postgres")
            if postgres is None:
                raise ConfigurationError(
                    message="Postgres backend specified but not configured."
                )
            del cfgdict["postgres"]
            if not isinstance(postgres, Dict):
                raise ConfigurationError(
                    message="Postgres configuration must be a tree."
                )
            postgrestree = PostgresConfigTree.parse(postgres)
        filetransfer_address = cfgdict.get("filetransfer_address")
        if filetransfer_address is not None:
            del cfgdict["filetransfer_address"]
        filetransfer_port = cfgdict.get("filetransfer_port")
        if filetransfer_port is not None:
            del cfgdict["filetransfer_port"]

        if cfgdict:
            raise ConfigurationError(
                message="Invalid configuration keys for controller config specified."
            )

        try:
            return ControllerConfigTree(
                backend=backend,
                postgres=postgrestree,
                filetransfer_address=filetransfer_address,
                filetransfer_port=filetransfer_port,
            )
        except Exception as exc:
            raise ConfigurationError(obj="controller config tree") from exc


class ControllerConfiguration(ExecutionConfiguration):
    """Configuration for for an AMNES controller.

    This configuration consists of the following configuration trees:
      - `ExecutionConfigTree`: Configuration tree for AMNES execution components.
      - `ControllerConfigTree`: Configuration tree for an AMNES controller.

    Example YAML configuration:

    ```yaml
    exec:
        name: "Example Component"
        address: "123.123.123.123"
        port: 789
    controller:
        backend: "postgres" (or "sqlite")
        postgres:
            host: "dbhost"
            port: 5432
            user: "postgres"
            password: "sergtsop"
            database: "amnes"
        filetransfer_address: "123.123.123.123"
        filetransfer_port: 987
    ```

    Attributes:
        execution (ExecutionConfigTree): Configuration tree for AMNES execution
                                         components.
        controller (ControllerConfigTree): Configuration tree for an AMNES controller.
    """

    def __init__(
        self, *, execution: ExecutionConfigTree, controller: ControllerConfigTree
    ) -> None:
        """Controller configuration constructor method.

        Args:
            execution (ExecutionConfigTree): Configuration tree for AMNES execution
                                             components.
            controller (ControllerConfigTree): Configuration tree for an AMNES
                                               controller.
        """
        super().__init__(execution=execution)
        self.__set_controller(controller)

    @classmethod
    def create_from(
        cls, execution_config: ExecutionConfiguration, controller: ControllerConfigTree
    ) -> ControllerConfiguration:
        """Create controller configuration from existing execution configuration.

        Args:
            execution_config (ExecutionConfiguration): Existing execution configuration
                                                       which should be used as base.
            controller (ControllerConfigTree): Configuration tree for an AMNES
                                               controller.

        Returns:
            Controller configuration created on existing execution configuration.
        """
        return ControllerConfiguration(
            execution=execution_config.execution, controller=controller
        )

    @classmethod
    def from_yamldict(cls, yamlconfig: Dict) -> ControllerConfiguration:
        """Create controller configuration from YAML dictionary.

        This function will read and delete the key 'controller' of the YAML dictionary.
        It calls functions which will read and delete the following keys: 'exec'.

        Args:
            yamlconfig (Dict): Dictionary representation of an YAML file from which the
                               controller configuration should be created.

        Returns:
            Controller configuration created from the given YAML dictionary.

        Raises:
            ConfigurationError: If an exception occurs while creating the
                                controller configuration.
        """
        execconfig = super().from_yamldict(yamlconfig)
        controllertree = yamlconfig.get("controller")
        if controllertree is None:
            raise ConfigurationError(
                message="First level key 'controller' is missing"
                + "for controller configuration tree."
            )
        if not isinstance(controllertree, Dict):
            raise ConfigurationError(obj="controller config") from errors.noft(
                "controller config tree", "Dict"
            )
        controller = ControllerConfigTree.parse(controllertree)
        del yamlconfig["controller"]
        return ControllerConfiguration.create_from(execconfig, controller=controller)

    @property
    def controller(self) -> ControllerConfigTree:
        """ControllerConfigTree: Configuration tree for an AMNES controller.

        Returns:
            ControllerConfigTree: Configuration tree for an AMNES controller.
        """
        return self.__controller

    def __set_controller(self, controller: ControllerConfigTree) -> None:
        """Set controller config tree.

        Args:
            controller (ControllerConfigTree): Configuration tree for an AMNES
                                               controller.

        Raises:
            TypeError: If given controller config tree is not of type
                       ControllerConfigTree.
        """
        if not isinstance(controller, ControllerConfigTree):
            raise errors.noftc("controller config tree", ControllerConfigTree)
        self.__controller: ControllerConfigTree = controller
