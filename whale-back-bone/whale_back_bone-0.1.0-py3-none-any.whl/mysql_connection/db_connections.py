# @ 4th Whale Marketing 2020

import logging

import sqlite3
import pymysql
import pandas as pd

from dataclasses import dataclass
from sqlalchemy import create_engine
from sqlite3 import Error as sql3Error
from pymysql import Error as mysqlError

@dataclass
class db_connections:

    """
    Class that manages either local or external connections to MySQL databases

    In addition to create_local_connection and create_external_connection,
    you have also the query_to_db pandas sql query that returns a pd.DataFrame

    """

    logger = logging.getLogger(__name__)

    def create_local_connection(self, db_file_path:str) -> object:
        """ Create the connection into the DB you
        are after using SQLite
        :param db_file_path : path towards the database file
        :returns: Connection object or None
        """
        connection = None

        try:
            connection = sqlite3.connect(db_file_path)
        except sql3Error as e:
            self.logger.error(e)
            raise

        return connection


    def create_external_connection(
        self,
        host:str,
        port:int,
        dbname:str,
        user:str,
        password:str
    ) -> object:
        """ Connector to external MySQL server
        :param: host: full path ending by .com
        :param: port: an integer of the port to connect to
        :param: dbname: reference towards a specific database
        :param: user: the user name necessary to connect to the db
        :param: password: pwd necessary to connect to the db
        """

        connection = None

        try:
            connection = create_engine(f'mysql+pymysql://{user}:{password}@{host}:{port}/{dbname}')
        except mysqlError as err:
            self.logger.error(err)
            raise

        return connection.connect()


    def query_to_db(self, connection:object, query:str) -> pd.DataFrame:
        """ Use the previous connection and pass it a
        sql querry
        :param connection: the connection object
        :param querry: string sql querry
        :returns: the result of the querry
        """

        poke_db = pd.read_sql_query(sql=query, con=connection)

        return poke_db
