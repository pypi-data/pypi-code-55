"""Database package with adapters and abstractions.

The database is used to persist data. Amnes uses an ORM which also is abstracted
for flexebility. Peewee's databases will be used by default. If a user chooses to
use another ORM, database adapter can be added or removed.
"""

from .database_adapter import PostgresqlAdapter  # noqa: F401
from .database_adapter import SqliteDatabaseAdapter  # noqa: F401
