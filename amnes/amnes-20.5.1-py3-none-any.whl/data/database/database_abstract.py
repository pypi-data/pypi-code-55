"""This module contains an abstraction for databases of an ORM.

Classes:
    AmnesDatabaseAbstract: An abstraction for databases for database adapters,
                           which all will be inherit from AmnesDatabaseAbstract.
"""
from abc import ABCMeta
from typing import List, Type

from ..models.base import BaseModel


# pylint: disable=too-few-public-methods
class AmnesDatabaseAbstract(metaclass=ABCMeta):
    """The AmnesDatabaseAbstract class abstracts the database from the ORM.

    Its usage is limited to implementations of database adapters and type-hints.
    """

    def create_tables(self, tables: List[Type[BaseModel]]) -> None:
        """Imports a list of Models into the database.

        Args:
            tables (List[Type[BaseModel]]): A list of Models where each will be mapped
                                            to its own table.
        """
