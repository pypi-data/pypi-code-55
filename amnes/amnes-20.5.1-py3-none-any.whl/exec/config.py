"""This module contains all classes for execution configuration.

Classes:
    ExecutionConfigTree: Configuration tree for AMNES execution components.
    ExecutionConfiguration: Configuration for AMNES execution components.
"""

from __future__ import annotations

import ipaddress
from copy import deepcopy
from typing import Any, Dict, List

from ..utils import errors
from ..utils.config import BaseConfigTree, BaseConfiguration, ConfigurationError

LogDestination = Dict[str, Dict[str, Any]]


class ExecutionConfigTree(BaseConfigTree):
    """Configuration tree for AMNES execution components.

    This configuration tree defines basic configuration values for AMNES
    execution components, which are needed for IPC and Pyro5 communication.

    Example YAML tree:

    ```yaml
    name: "Example Component"
    address: "123.123.123.123"
    port: 789
    ```

    Attributes:
        name (str): Name of the AMNES execution component.
        address (str): Address for the main Pyro5 endpoint of the AMNES execution
                       component.
        port (int): Port for the main Pyro5 endpoint of the AMNES execution component.
        logging (List[LogDestination]): List of destinations for AMNES Execution
                                         logging.
    """

    def __init__(
        self, *, name: str, address: str, port: int, logging: List[LogDestination]
    ) -> None:
        """Execution configuration tree constructor method.

        Args:
            name (str): Name of the AMNES execution component.
            address (str): Address for the main Pyro5 endpoint of the AMNES execution
                           component.
            port (int): Port for the main Pyro5 endpoint of the AMNES execution
                        component.
            logging (List[LogDestination]): List of destinations for AMNES Execution
                                             logging.
        """
        self.__set_name(name)
        self.__set_address(address)
        self.__set_port(port)
        self.__set_logging(logging)

    @classmethod
    def parse(cls, cfgdict: Dict) -> ExecutionConfigTree:
        """Parse dictionary and create execution configuration tree.

        Args:
            cfgdict (Dict): Part of configuration dictionary which is located under the
                            execution configuration key of the configuration tree.

        Returns:
            Execution configuration tree created from the given dictionary.

        Raises:
            ConfigurationError: If an exception occurs while parsing the config
                                dictionary.
        """
        name = cfgdict.get("name")
        if name is not None:
            del cfgdict["name"]
        address = cfgdict.get("address")
        if address is not None:
            del cfgdict["address"]
        port = cfgdict.get("port")
        if port is not None:
            del cfgdict["port"]
        logging = cfgdict.get("logging")
        if logging is not None:
            del cfgdict["logging"]

        if cfgdict:
            raise ConfigurationError(
                message="Invalid configuration keys for execution config specified."
            )

        try:
            return ExecutionConfigTree(
                name=name, address=address, port=port, logging=logging
            )
        except Exception as exc:
            raise ConfigurationError(obj="execution config tree") from exc

    @property
    def name(self) -> str:
        """str: Name of the AMNES execution component.

        Returns:
            str: Name of the AMNES execution component.
        """
        return self.__name

    def __set_name(self, name: str) -> None:
        """Set name attribute for AMNES execution component.

        Args:
            name (str): Name of the AMNES execution component.

        Raises:
            TypeError: If given name is not of type string.
            ValueError: If given namen is empty or only consists of spaces.
        """
        if not isinstance(name, str):
            raise errors.noftc("name", str)
        if (not name) or (name.isspace()):
            raise ValueError("Given name is empty or only consists of spaces.")
        self.__name: str = name

    @property
    def address(self) -> str:
        """str: Address for the main Pyro5 endpoint of the AMNES execution component.

        Returns:
            str: Address for the main Pyro5 endpoint of the AMNES execution component.
        """
        return self.__address

    def __set_address(self, address: str) -> None:
        """Set address attribute for AMNES execution component.

        Args:
            address (str): Address for the main Pyro5 endpoint of the AMNES execution
                           component.

        Raises:
            TypeError: If given address is not of type string.
            ValueError: If given address is not a valid IPv4 or IPv6 address.
        """
        if not isinstance(address, str):
            raise errors.noftc("address", str)
        try:
            ipaddress.ip_address(address)
        except ValueError as exc:
            raise ValueError(
                "Given address is not a valid IPv4 or IPv6 address."
            ) from exc
        self.__address: str = address

    @property
    def port(self) -> int:
        """int: Port for the main Pyro5 endpoint of the AMNES execution component.

        Returns:
            int: Port for the main Pyro5 endpoint of the AMNES execution component.
        """
        return self.__port

    def __set_port(self, port: int) -> None:
        """Set port attribute for AMNES execution component.

        Args:
            port (int): Port for the main Pyro5 endpoint of the AMNES execution
                        component.

        Raises:
            TypeError: If given port is not of type integer.
            ValueError: If given port is outside of permitted port range.
        """
        if not isinstance(port, int):
            raise errors.noftc("port", int)
        if not 0 < port <= 65535:
            raise ValueError("Given port is outside of permitted port range.")
        self.__port: int = port

    @property
    def logging(self) -> List[LogDestination]:
        """List[LogDestination]: List of destinations for AMNES Execution logging.

        Returns:
            List[LogDestination]: List of destinations for AMNES Execution logging.
        """
        return self.__logging

    def __set_logging(self, logging: List[LogDestination]) -> None:  # noqa: C901
        """Set list of destinations for AMNES Execution logging.

        Args:
            logging (List[LogDestination]): List of destinations for AMNES Execution
                                             logging.

        Raises:
            TypeError: If invalid types were used for configuration parameters.
            ValueError: If invalid value were used for configuration parameters.
        """
        # pylint: disable=too-many-branches
        if not isinstance(logging, List):
            raise errors.noftc("logging", list)
        for dest in logging:
            if not isinstance(dest, Dict):
                raise errors.noftc("logging destination", dict)
            if len(dest.keys()) != 1:
                raise ValueError(
                    "Logging destination dictionary must have exactly "
                    + "one parent key identifying the backend."
                )
            backend = list(dest.keys())[0]
            if not isinstance(dest[backend], Dict):
                raise errors.noftc(f"logging.'{backend}'", dict)
            if backend == "syslog":
                host = dest[backend].get("host")
                if not isinstance(host, str):
                    raise errors.noftc("host", str)
                if (not host) or (host.isspace()):
                    raise ValueError("Given host is empty or only consists of spaces.")
                port = dest[backend].get("port")
                if not isinstance(port, int):
                    raise errors.noftc("port", int)
                if not 0 < port <= 65535:
                    raise ValueError("Given port is outside of permitted port range.")
                socktype = dest[backend].get("socktype")
                if not isinstance(socktype, str):
                    raise errors.noftc("socktype", str)
                if socktype not in ["tcp", "udp"]:
                    raise ValueError("Given socket type unknown.")
                if len(dest[backend].keys()) != 3:
                    raise ValueError(
                        "Unknown additional configuration parameters for "
                        + "syslog specified."
                    )
            elif backend == "tty":
                stream = dest[backend].get("stream")
                if not isinstance(stream, str):
                    raise errors.noftc("stream", str)
                if stream not in ["stdout", "stderr"]:
                    raise ValueError("Stream destination unknown.")
                if len(dest[backend].keys()) != 1:
                    raise ValueError(
                        "Unknown additional configuration parameters for "
                        + "tty specified."
                    )
            else:
                raise ValueError(f"Invalid backend '{backend}' specified.'")
        self.__logging: List[LogDestination] = deepcopy(logging)


class ExecutionConfiguration(BaseConfiguration):
    """Configuration for AMNES execution components.

    This configuration consists of the following configuration trees:
      - `ExecutionConfigTree`: Configuration tree for AMNES execution components.

    Example YAML configuration:

    ```yaml
    exec:
        name: "Example Component"
        address: "123.123.123.123"
        port: 789
    ```

    Attributes:
        execution (ExecutionConfigTree): Configuration tree for AMNES execution
                                         components.
    """

    def __init__(self, *, execution: ExecutionConfigTree) -> None:
        """Execution configuration constructor method.

        Args:
            execution (ExecutionConfigTree): Configuration tree for AMNES execution
                                             components.
        """
        self.__set_execution(execution)

    @classmethod
    def from_yamldict(cls, yamlconfig: Dict) -> ExecutionConfiguration:
        """Create execution configuration from YAML dictionary.

        This function will read and delete the key 'exec' of the YAML dictionary.

        Args:
            yamlconfig (Dict): Dictionary representation of an YAML file from which the
                               execution configuration should be created.

        Returns:
            Execution configuration created from the given YAML dictionary.

        Raises:
            ConfigurationError: If an exception occurs while creating the
                                execution configuration.
        """
        exectree = yamlconfig.get("exec")
        if exectree is None:
            raise ConfigurationError(
                message="First level key 'exec' is missing"
                + "for execution configuration tree."
            )
        if not isinstance(exectree, Dict):
            raise ConfigurationError(obj="execution config") from errors.noft(
                "execution config tree", "Dict"
            )
        execution = ExecutionConfigTree.parse(exectree)
        del yamlconfig["exec"]
        return ExecutionConfiguration(execution=execution)

    @property
    def execution(self) -> ExecutionConfigTree:
        """ExecutionConfigTree: Configuration tree for AMNES execution components.

        Returns:
            ExecutionConfigTree: Configuration tree for AMNES execution components.
        """
        return self.__execution

    def __set_execution(self, execution: ExecutionConfigTree) -> None:
        """Set execution config tree.

        Args:
            execution (ExecutionConfigTree): Configuration tree for AMNES execution
                                             components.

        Raises:
            TypeError: If given execution config tree is not of type
                       ExecutionConfigTree.
        """
        if not isinstance(execution, ExecutionConfigTree):
            raise errors.noftc("execution config tree", ExecutionConfigTree)
        self.__execution: ExecutionConfigTree = execution
