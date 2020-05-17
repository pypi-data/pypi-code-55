"""This module contains all necessary definitions for a Serializer class.

Classes:
    Serializer: Abstract Serializer class,
                from which all concrete Serializer classes inherit.
"""

from abc import abstractmethod
from typing import Any, List, Optional

from amnes.utils.metaclasses import SingletonABCMeta


class Serializer(metaclass=SingletonABCMeta):
    """Abstract Serializer class, from which all concrete Serializer classes inherit.

    This class defines the necessary definitions for a concrete Serializer.
    A Serializer is used to map data between Plain-Python-Objects and
    Database-Models. Data can be stored and queried via a Serializer.
    """

    @staticmethod
    @abstractmethod
    def exists_by_id(object_id: int) -> bool:
        """Check if correlating instance exists in the database.

        Args:
            object_id (int): Index of entry in database
        """

    @staticmethod
    @abstractmethod
    def insert(instance: Any, parent: Optional[Any]) -> int:
        """Insert Plain-Python-Object into the database.

        Args:
            instance (Any): Non-Empty instance of a Plain-Python-Object.
            parent (Optional[Any]): Optional parental reference fo model creation.
        """

    @staticmethod
    @abstractmethod
    def insert_bulk(instances: List[Any], parent: Optional[Any]) -> Optional[List[int]]:
        """Insert list of Plain-Python-Object into the database.

        Args:
            instances (List[Any]): Non-Empty instances of  Plain-Python-Objects.
            parent (Optional[Any]): Optional parental reference fo model creation.
        """

    @staticmethod
    def delete_by_id(object_id: int) -> None:
        """Delete an AmnesObject by id from the database.

        Args:
            object_id (int): Index of entry in database
        """

    @staticmethod
    @abstractmethod
    def update_by_id(instance: Any, object_id: int) -> None:
        """Update Plain-Python-Object inside the database.

        Args:
            instance (Any): Non-Empty instance of a Plain-Python-Object.
            object_id (int): Unique identification of data-entry
        """

    @staticmethod
    @abstractmethod
    def get_by_id(object_id: int) -> Any:
        """Insert Plain-Python-Object AmnesObject into the database.

        Args:
            object_id (int): Unique identifier, referencing to data-entry
                          inside the database.
        """
