"""This module contains concrete adapters for database types.

Classes:
    SqliteDatabaseAbstractAdapter: Implements the SqliteDatabase from Peewee.
"""

from peewee import PostgresqlDatabase, SqliteDatabase

from .database_abstract import AmnesDatabaseAbstract


class SqliteDatabaseAdapter(SqliteDatabase, AmnesDatabaseAbstract):
    """Implements the SqliteDatabase from Peewee.

    Read more on:
    http://docs.peewee-orm.com/en/latest/peewee/database.html#using-sqlite
    """

    def sequence_exists(self, seq: str) -> bool:
        """Inherited from Peewee's database.

        Is not implemented in Peewees's SqliteDatabase. This method
        is not intended to be used with SqliteDatabases.

        Args:
            seq (str): Name of the sequence.

        Raises:
            NotImplementedError: By default. This method is not implemented
        """
        raise NotImplementedError


class PostgresqlAdapter(PostgresqlDatabase, AmnesDatabaseAbstract):
    """Implements the PostgresqlDatabase from Peewee.

    Read more on:
    http://docs.peewee-orm.com/en/latest/peewee/database.html#using-postgresql
    """
