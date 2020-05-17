"""This module contains all classes for storage backend configuration.

Classes:
    PostgresConfigTree: Configuration tree for Postgres Database Connection.
    PostgresConfiguration: Configuration for Postgres Database Connection.
"""

from __future__ import annotations

from typing import Dict

from ...utils import errors
from ...utils.config import BaseConfigTree, ConfigurationError


class PostgresConfigTree(BaseConfigTree):
    """Configuration tree for Postgres Database Connection.

    This configuration tree defines basic configuration values for Postgres
    Database Connection used by controller for persistent storage.

    Example YAML tree:

    ```yaml
    host: "dbhost"
    port: 5432
    user: "postgres"
    password: "sergtsop"
    database: "amnes"
    ```

    Attributes:
        host (str): Hostname or address of the postgres database server.
        port (int): Port used by the postgres database server.
        user (str): Username used for authentication.
        password (str): Password used for authentication.
        database (str): Postgres database name for AMNES peristent storage.
    """

    def __init__(
        self, *, host: str, port: int, user: str, password: str, database: str
    ) -> None:
        """Execution configuration tree constructor method.

        Args:
            host (str): Hostname or address of the postgres database server.
            port (int): Port used by the postgres database server.
            user (str): Username used for authentication.
            password (str): Password used for authentication.
            database (str): Postgres database name for AMNES peristent storage.
        """
        self.__set_host(host)
        self.__set_port(port)
        self.__set_user(user)
        self.__set_password(password)
        self.__set_database(database)

    @classmethod
    def parse(cls, cfgdict: Dict) -> PostgresConfigTree:
        """Parse dictionary and create postgres configuration tree.

        Args:
            cfgdict (Dict): Part of configuration dictionary which is located under the
                            postgres configuration key of the
                            configuration tree.

        Returns:
            Postgres database configuration tree created from the given dictionary.

        Raises:
            ConfigurationError: If an exception occurs while parsing the config
                                dictionary.
        """
        host = cfgdict.get("host")
        if host is not None:
            del cfgdict["host"]
        port = cfgdict.get("port")
        if port is not None:
            del cfgdict["port"]
        user = cfgdict.get("user")
        if user is not None:
            del cfgdict["user"]
        password = cfgdict.get("password")
        if password is not None:
            del cfgdict["password"]
        database = cfgdict.get("database")
        if database is not None:
            del cfgdict["database"]

        if cfgdict:
            raise ConfigurationError(
                message="Invalid configuration keys for postgres config specified."
            )

        try:
            return PostgresConfigTree(
                host=host, port=port, user=user, password=password, database=database
            )
        except Exception as exc:
            raise ConfigurationError(obj="postgres config tree") from exc

    @property
    def host(self) -> str:
        """str: Hostname or address of the postgres database server.

        Returns:
            str: Hostname or address of the postgres database server.
        """
        return self.__host

    def __set_host(self, host: str) -> None:
        """Set host or address of the postgres database server.

        Args:
            host (str): Hostname or address of the postgres database server.

        Raises:
            TypeError: If given host is not of type string.
            ValueError: If given host is empty or only consists of spaces.
        """
        if not isinstance(host, str):
            raise errors.noftc("host", str)
        if (not host) or (host.isspace()):
            raise ValueError("Given host is empty or only consists of spaces.")
        self.__host: str = host

    @property
    def port(self) -> int:
        """int: Port used by the postgres database server.

        Returns:
            int: Port used by the postgres database server.
        """
        return self.__port

    def __set_port(self, port: int) -> None:
        """Set port used by the postgres database server.

        Args:
            port (int): Port used by the postgres database server.

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
    def user(self) -> str:
        """str: Username used for authentication.

        Returns:
            str: Username used for authentication.
        """
        return self.__user

    def __set_user(self, user: str) -> None:
        """Set username used for authentication.

        Args:
            user (str): Username used for authentication.

        Raises:
            TypeError: If given user is not of type string.
            ValueError: If given user is empty or only consists of spaces.
        """
        if not isinstance(user, str):
            raise errors.noftc("user", str)
        if (not user) or (user.isspace()):
            raise ValueError("Given user is empty or only consists of spaces.")
        self.__user: str = user

    @property
    def password(self) -> str:
        """str: Password used for authentication.

        Returns:
            str: Password used for authentication.
        """
        return self.__password

    def __set_password(self, password: str) -> None:
        """Set password used for authentication.

        Args:
            password (str): Password used for authentication.

        Raises:
            TypeError: If given password is not of type string.
            ValueError: If given password is empty or only consists of spaces.
        """
        if not isinstance(password, str):
            raise errors.noftc("password", str)
        if (not password) or (password.isspace()):
            raise ValueError("Given user is empty or only consists of spaces.")
        self.__password: str = password

    @property
    def database(self) -> str:
        """str: Postgres database name for AMNES peristent storage.

        Returns:
            str: Postgres database name for AMNES peristent storage.
        """
        return self.__database

    def __set_database(self, database: str) -> None:
        """Set postgres database name for AMNES peristent storage.

        Args:
            database (str): Postgres database name for AMNES peristent storage.

        Raises:
            TypeError: If given database is not of type string.
            ValueError: If given datbase is empty or only consists of spaces.
        """
        if not isinstance(database, str):
            raise errors.noftc("database", str)
        if (not database) or (database.isspace()):
            raise ValueError("Given database is empty or only consists of spaces.")
        self.__database: str = database
