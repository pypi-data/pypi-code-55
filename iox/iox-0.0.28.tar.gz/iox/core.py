"""
core.py
written in Python3
author: C. Lockhart <chris@lockhartlab.org>
"""

from iox._config import defaults as config
import iox

database = None
if config['database'] == 'bigquery':
    database = iox.BigQuery()


def query(sql):
    if database is None:
        raise AttributeError('database default not set')
    return database.query(sql)
