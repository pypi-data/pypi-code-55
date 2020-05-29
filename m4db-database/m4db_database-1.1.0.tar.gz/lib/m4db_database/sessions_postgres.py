r"""
A set of utilities to create/open postgres databases for SQLAlchemy. Note, prior to running this script, an empty
database should be available. This may be created with the following instructions:

    postgres=# create database <db_name> owner=<user>;

@file sessions_postgres.py
@author L. Nagy, W. Williams
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import m4db_database.orm

from m4db_database.configuration import read_config_from_environ
from m4db_database.decorators import static

POSTGRES_URL_STRING = "postgresql://{user:}@{host:}/{database:}"


def setup_database(user, database, host, echo=False):
    r"""
    Create tables, indexes and relationships under a new database.
    Args:
        user: the database user.
        database: the name of the database under which to create database objects.
        host: the host on which the database lives.
        echo: boolean (default False) set to True if verbose SQLAlchemy output is required.

    Returns:
        The url string to connect to the databse.
    """
    db_url = POSTGRES_URL_STRING.format(
        user=user, host=host, database=database
    )

    # Connect to the database
    engine = create_engine(db_url, echo=echo)

    if hasattr(m4db_database.orm.Base, "metadata"):
        metadata = getattr(m4db_database.orm.Base, "metadata")
        metadata.create_all(engine)
    else:
        raise AssertionError("Fatal, m4db_database.orm.Base has no attribute 'metadata'")

    return db_url


@static(engine=None, Session=None)
def get_session(user=None, database=None, host=None, echo=False):
    r"""
    Retrieve an open database connection session, if user, database and host are None then attempt to use data
    stored in M4DB_CONFIG environment variable.

    Args:
        user: the database user.
        database: the name of the database under which to create database objects.
        host: the host on which the database lives.
        echo: boolean (default False) set to True if verbose SQLAlchemy output is required.

    Returns:
        A session connection to the database.

    """
    if get_session.engine is None:
        if user is None and database is None and host is None:
            config = read_config_from_environ()
            db_url = config["db_url"]
        else:
            db_url = POSTGRES_URL_STRING.format(
                user=user, host=host, database=database
            )
        get_session.engine = create_engine(db_url, echo=echo)

    if get_session.Session is None:
        get_session.Session = sessionmaker(bind=get_session.engine)

    return get_session.Session()
