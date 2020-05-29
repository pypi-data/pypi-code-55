r"""
Set of utilities to open databases.
"""

import re

from m4db_database.configuration import read_config_from_environ

REGEX_POSTGRES = re.compile(r"^postgresql.*$")
REGEX_SQLITE = re.compile(r"^sqlite.*$")


def get_session(echo=False):
    r"""
    Retrieve an open database connection session from the M4DB_CONFIG file.

    Returns:
        A session connection.
    """
    config = read_config_from_environ()

    if REGEX_POSTGRES.match(config["db_url"]):
        from m4db_database.sessions_postgres import get_session
        return get_session(echo=echo)
    if REGEX_SQLITE.match(config["db_url"]):
        from m4db_database.sessions_sqlite import get_session
        return get_session(echo=echo)

    raise ValueError("Unsupported RDBMS in M4DB_CONFIG url '{}'".format(config["db_url"]))
