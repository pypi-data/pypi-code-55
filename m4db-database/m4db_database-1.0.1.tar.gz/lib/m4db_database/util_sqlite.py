r"""
A set of utilities to create/open sqlite databases for SQLAlchemy.

@file util.sqlite.py
@author L. Nagy, W. Williams
"""
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import m4db_database.orm

from m4db_database.configuration import read_config_from_environ

SQLITE_URL_STRING = "sqlite:///{file:}"


def setup_database(file, echo=False):
    r"""
    Create tables, indexes, relationships etc. for an SQLight database.

    Args:
        file: the file that will contain the database objects.
        echo: boolean (default False) set to True if verbose SQLAlchemy output is required.

    Returns:
        The url string to connect to the databse.
    """

    db_url = SQLITE_URL_STRING.format(file=os.path.abspath(file))

    engine = create_engine(db_url, echo=echo)

    if hasattr(m4db_database.orm.Base, "metadata"):
        metadata = getattr(m4db_database.orm.Base, "metadata")
        metadata.create_all(engine)
    else:
        raise AssertionError("Fatal, m4db_database.orm.Base has no attribute 'metadata'")

    return db_url


def get_session(file=None, echo=False):
    r"""
    Retrieve an open database connection session, if file is None, then attempt to use config
    data stored in the file pointed to by the M4DB_CONFIG environment variable.

    Args:
        file: the file that will contain the database objects.
        echo: boolean (default False) set to True if verbose SQLAlchemy output is required.

    Returns:
        A session connection to the database.
    """
    if file is None:
        config = read_config_from_environ()
        sql_url = config["db_url"]
    else:
        sql_url = SQLITE_URL_STRING.format(file=file)
    engine = create_engine(sql_url, echo=echo)

    Session = sessionmaker(bind=engine)
    return Session()
