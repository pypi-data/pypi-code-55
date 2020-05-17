"""DataManager package with all necessary classes.

The DataManager creates an additional layer between the database,
it's ORM and the rest of the application. Queries will be made from client to
deliver persisted data and files.
"""
from ..serializer import *  # noqa: F401, F403
from .storage_backend_peewee import StorageBackendPeewee  # noqa: F401
