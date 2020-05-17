"""This module contains all classes for CLI configurations.

Classes:
    ControlCommandConfigTree: Configuration tree for AMNES control command.
    ControlCommandConfiguration: Configuration for AMNES control command.
"""

from __future__ import annotations

import ipaddress
from typing import Dict

from ..utils import errors
from ..utils.config import BaseConfigTree, BaseConfiguration, ConfigurationError


class ControlCommandConfigTree(BaseConfigTree):
    """Configuration tree for AMNES control command.

    This configuration tree defines basic configuration values for AMNES
    control command, which are needed to control the AMNES Controller.

    Example YAML tree:

    ```yaml
    controller_address: "123.123.123.123"
    controller_port: 789
    ```

    Attributes:
        controller_address (str): Address of the AMNES Controller
                                  which should be controlled.
        controller_port (int): Port of the AMNES Controller
                               which should be controlled.
    """

    def __init__(self, *, controller_address: str, controller_port: int) -> None:
        """Control command configuration tree constructor method.

        Args:
            controller_address (str): Address of the AMNES Controller
                                      which should be controlled.
            controller_port (int): Port of the AMNES Controller
                                   which should be controlled.
        """
        self.__set_controller_address(controller_address)
        self.__set_controller_port(controller_port)

    @classmethod
    def parse(cls, cfgdict: Dict) -> ControlCommandConfigTree:
        """Parse dictionary and create control command configuration tree.

        Args:
            cfgdict (Dict): Part of configuration dictionary which is located under the
                            control command configuration key of the configuration tree.

        Returns:
            Control command configuration tree created from the given dictionary.

        Raises:
            ConfigurationError: If an exception occurs while parsing the config
                                dictionary.
        """
        controller_address = cfgdict.get("controller_address")
        if controller_address is not None:
            del cfgdict["controller_address"]
        controller_port = cfgdict.get("controller_port")
        if controller_port is not None:
            del cfgdict["controller_port"]

        if cfgdict:
            raise ConfigurationError(
                message="Invalid configuration keys "
                + "for control command config specified."
            )

        try:
            return ControlCommandConfigTree(
                controller_address=controller_address, controller_port=controller_port
            )
        except Exception as exc:
            raise ConfigurationError(obj="control command config tree") from exc

    @property
    def controller_address(self) -> str:
        """str: Address of the AMNES Controller which should be controlled.

        Returns:
            str: Address of the AMNES Controller which should be controlled.
        """
        return self.__controller_address

    def __set_controller_address(self, controller_address: str) -> None:
        """Set address of the AMNES Controller which should be controlled.

        Args:
            controller_address (str): Address of the AMNES Controller
                                      which should be controlled.

        Raises:
            TypeError: If given controller address is not of type string.
            ValueError: If given controller address is not a valid IPv4 or IPv6 address.
        """
        if not isinstance(controller_address, str):
            raise errors.noftc("controller address", str)
        try:
            ipaddress.ip_address(controller_address)
        except ValueError as exc:
            raise ValueError(
                "Given controller address is not a valid IPv4 or IPv6 address."
            ) from exc
        self.__controller_address: str = controller_address

    @property
    def controller_port(self) -> int:
        """int: Port of the AMNES Controller which should be controlled.

        Returns:
            int: Port of the AMNES Controller which should be controlled.
        """
        return self.__controller_port

    def __set_controller_port(self, controller_port: int) -> None:
        """Set port of the AMNES Controller which should be controlled.

        Args:
            controller_port (int): Port of the AMNES Controller
                                   which should be controlled.

        Raises:
            TypeError: If given controller port is not of type integer.
            ValueError: If given controller port is outside of permitted port range.
        """
        if not isinstance(controller_port, int):
            raise errors.noftc("controller port", int)
        if not 0 < controller_port <= 65535:
            raise ValueError("Given controllerport is outside of permitted port range.")
        self.__controller_port: int = controller_port


class ControlCommandConfiguration(BaseConfiguration):
    """Configuration for AMNES control command.

    This configuration consists of the following configuration trees:
      - `ControlCommandConfigTree`: Configuration tree for AMNES control command.

    Example YAML configuration:

    ```yaml
    ctl:
      controller_address: "123.123.123.123"
      controller_port: 789
    ```

    Attributes:
        ctl (ControlCommandConfigTree): Configuration tree for AMNES control command.
    """

    def __init__(self, *, ctl: ControlCommandConfigTree) -> None:
        """Control command configuration constructor method.

        Args:
            ctl (ControlCommandConfigTree): Configuration tree for AMNES
                                            control command.
        """
        self.__set_ctl(ctl)

    @classmethod
    def from_yamldict(cls, yamlconfig: Dict) -> ControlCommandConfiguration:
        """Create control command configuration from YAML dictionary.

        This function will read and delete the key 'ctl' of the YAML dictionary.

        Args:
            yamlconfig (Dict): Dictionary representation of an YAML file from which the
                               control command configuration should be created.

        Returns:
            Control command configuration created from the given YAML dictionary.

        Raises:
            ConfigurationError: If an exception occurs while creating the
                                control command configuration.
        """
        ctltree = yamlconfig.get("ctl")
        if ctltree is None:
            raise ConfigurationError(
                message="First level key 'ctl' is missing"
                + "for control command configuration tree."
            )
        if not isinstance(ctltree, Dict):
            raise ConfigurationError(obj="control command config") from errors.noft(
                "control command config tree", "Dict"
            )
        ctl = ControlCommandConfigTree.parse(ctltree)
        del yamlconfig["ctl"]
        return ControlCommandConfiguration(ctl=ctl)

    @property
    def ctl(self) -> ControlCommandConfigTree:
        """ControlCommandConfigTree: Configuration tree for AMNES control command.

        Returns:
            ControlCommandConfigTree: Configuration tree for AMNES control command.
        """
        return self.__ctl

    def __set_ctl(self, ctl: ControlCommandConfigTree) -> None:
        """Set control command config tree.

        Args:
            ctl (ControlCommandConfigTree): Configuration tree for AMNES
                                            control command.

        Raises:
            TypeError: If given control command config tree is not of type
                       ControlCommandConfigTree.
        """
        if not isinstance(ctl, ControlCommandConfigTree):
            raise errors.noftc("control command config tree", ControlCommandConfigTree)
        self.__ctl: ControlCommandConfigTree = ctl
