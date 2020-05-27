""" Target PostgreSQL has a GPL3 license. Cannot be used in a commercial product.
"""

import psycopg2
from urllib.parse import urlparse, parse_qs

from target_postgres.postgres import PostgresTarget
from target_postgres import target_tools

from .base import AbstractSingerTarget

class PostgreSQLSingerTarget(AbstractSingerTarget):
    def __init__(self, uri, database_name, config={}):
        super().__init__()
        result = urlparse(uri)

        username = result.username
        password = result.password
        hostname = result.hostname
        port = result.port

        # Support host being passed as query param. This is used by sqlalchemy
        # to allow unix sockets:
        # postgres://user:password@/dbname?host=/path/to/db
        query = parse_qs(result.query)

        if 'host' in query and not hostname:
            # host in query is a list of hosts.
            # join with commas
            hostname = ','.join(query['host'])

        self.connection = psycopg2.connect(
            database = database_name,
            user = username,
            password = password,
            host = hostname,
            port = port
        )
    
        self.config = config

    def send_messages(self, messages_str):
        with self.connection:
            postgres_target = PostgresTarget(
                self.connection,
                postgres_schema=self.config.get('postgres_schema', 'public'),
                logging_level=self.config.get('logging_level'),
                persist_empty_tables=self.config.get('persist_empty_tables'),
                add_upsert_indexes=self.config.get('add_upsert_indexes', True),
                before_run_sql=self.config.get('before_run_sql'),
                after_run_sql=self.config.get('after_run_sql'),
            )
            target_tools.stream_to_target(messages_str, postgres_target, config=self.config)
            
    def __repr__(self):
        return repr_obj(self, ['connection'])