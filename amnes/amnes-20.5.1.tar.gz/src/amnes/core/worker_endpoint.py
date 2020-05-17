"""This module contains all necessary definitions for the WorkerEndpoint class.

Classes:
    WorkerEndpoint: Worker endpoint class that defines an endpoint for the communication
                    between the controller and a specific worker.
"""

from __future__ import annotations

import ipaddress
from typing import Dict

from ..utils.parser import ParsingError, YamlParsable
from .amnes_object import AmnesObject


class WorkerEndpoint(AmnesObject, YamlParsable):
    """Worker endpoint class that defines a communication endpoint for a single worker.

    Attributes:
        address (str): Valid IPv4 or IPv6 address to be used for management
                       communication.
        port (int): Valid port number to be used for management communication.
    """

    def __init__(
        self, slug: str, name: str, description: str, address: str, port: int
    ) -> None:
        """Worker Endpoint class constructor method.

        Args:
            slug (str): Short identifier for the Worker Endpoint,
                        which must be a valid, non-empty string.
            name (str): Full name for the Worker Endpoint.
            description (str): Custom description for the Worker Endpoint.
            address (str): Valid IPv4 or IPv6 address to be used for
                           management communication.
            port (int): Valid port number to be used for management communication.
        """
        super().__init__(slug, name, description)
        self.address = address
        self.port = port

    def __eq__(self, other: object) -> bool:
        """Check equality between WorkerEndpoint instance and an arbitrary object.

        Args:
            other (object): Arbitrary object to be checked for equality
                            with this WorkerEndpoint instance.

        Returns:
            bool: True if `other` is equal to the current WorkerEndpoint instance,
                  otherwise returns false.

        Raises:
            TypeError: If `other` is not of type WorkerEndpoint.
        """
        if not isinstance(other, WorkerEndpoint):
            raise TypeError(
                "The object to be compared to is not of type WorkerEndpoint."
            )
        return (
            super().__eq__(other)
            and self.address == other.address
            and self.port == other.port
        )

    @staticmethod
    def parse(config: Dict) -> WorkerEndpoint:
        """Static method for parsing a WorkerEndpoint configuration.

        The overwritten parse method requires a dictionary with exactly
        one key which has a dictionary of all needed attributes as its value.
        The key is used as slug for the WorkerEndpoint instance that is created.

        Example YAML config:

        ```yaml
        endpoint:
          name: Worker Endpoint
          description: My worker endpoint.
          address: 123.123.123.123
          port: 789
        ```

        Example dictionary from YAML config:

        ```python
        {
          "endpoint": {
              "name": "Worker Endpoint",
              "description": "My worker endpoint.",
              "address": "123.123.123.123",
              "port": 789
          }
        }
        ```

        Args:
            config (Dict): Dictionary from which the WorkerEndpoint instance is created.

        Returns:
            WorkerEndpoint: The WorkerEndpoint instance created from `config`.

        Raises:
            ParsingError: If an exception occurs while parsing the `config`.
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
            address = values.get("address")
            if address is not None:
                del values["address"]
            port = values.get("port")
            if port is not None:
                del values["port"]

        if values:
            raise ParsingError(message="Config tree not empty after parsing.", key=key)

        with YamlParsable._parse_key_context(key):
            endpoint = WorkerEndpoint(key, name, description, address, port)

        return endpoint

    @property
    def address(self) -> str:
        """str: IPv4 or IPv6 address which is used for management communication.

        Returns:
            address (str): IPv4 or IPv6 address which is used for
                           management communication.
        """
        return self.__address

    @address.setter
    def address(self, address: str) -> None:
        """Worker Endpoint address Setter function.

        Args:
            address (str): Valid IPv4 or IPv6 address for the Worker Endpoint to be set.

        Raises:
            TypeError: If `address` is not of type string.
            ValueError: If `address`  string is not a valid IPv4 or IPv6 address.
        """
        if not isinstance(address, str):
            raise TypeError("Given address is not of type string.")
        if (not address) or (address.isspace()):
            raise ValueError(
                "Given address string is not a valid IPv4 or IPv6 address."
            )
        try:
            ipaddress.ip_address(address)
        except ValueError as exc:
            raise ValueError(
                "Given address string is not a valid IPv4 or IPv6 address."
            ) from exc
        self.__address = address

    @property
    def port(self) -> int:
        """int: Port number which is used for management communication.

        Returns:
            port (int): Port number which is used for management communication.
        """
        return self.__port

    @port.setter
    def port(self, port: int) -> None:
        """Worker Endpoint address Setter function.

        Args:
            port (int): Valid port number for the Worker Endpoint to be set.

        Raises:
            TypeError: If `port` is not of type integer.
            ValueError: If integer `port`  is outside the permitted value range.
        """
        if not isinstance(port, int):
            raise TypeError("Given port number is not of type integer.")
        if not 0 < port <= 65535:
            raise ValueError("Given port number is outside the permitted value range.")
        self.__port = port
