from urllib import parse
from traceback import format_exc
from .log_helper import LogHelper
from typing import Any, Dict, List
from contextlib import contextmanager
from sqlalchemy import text, create_engine, exc


class DatabaseHelper:
    """This class allows to manage database queries."""

    def __init__(self, db_credentials, log_dir_path) -> None:
        self.db_credentials = db_credentials
        self.logger = LogHelper(log_dir_path, logger_name='db_helper', log_level='INFO')

    def select(self, required_columns, filter_parameters={}, fetchsize=1000, query_string='', table_name='') -> Any:
        """Makes SELECT queries to get data from the database.

        @:param self:
        @:param required_columns: columns to get from db
        @:param filter_parameters: filters for WHERE query
        @:param fetchsize: max amount of records which returns from the database
        @:param query_string: custom query string
        @:param table_name: destination table name
        @:type self: DatabaseHelper
        @:type required_columns: list
        @:type filter_parameters: dict
        @:type fetchsize: int
        @:type query_string: str
        @:type table_name: str

        Makes SELECT queries, gets max 1k records from fetchmany in a loop.

        @:returns: dictionaries list if exists, else empty list, exception - False
        @:rtype: list or bool
        """

        with self.db_connection() as connection:
            try:
                if not query_string:
                    if not required_columns:
                        required_columns = '*'
                    else:
                        required_columns = ','.join([required_column for required_column in required_columns])

                    query_string = 'SELECT {} FROM {}'.format(required_columns, table_name)

                    if filter_parameters:
                        query_string += ' WHERE'

                        filter_parameters_counter = 1
                        filters_len = len(filter_parameters)

                        for filter_name, filter_parameter in filter_parameters.items():
                            if isinstance(filter_parameter, list):
                                filter_params = '(' + ','.join(["N'" + str(value).replace("'", "''") + "'" for value in
                                                                filter_parameter]) + ')'
                                column_match = ' {} IN {}'.format(filter_name, filter_params)
                            else:
                                column_match = ' {}={}'.format(filter_name,
                                                               "N'" + str(filter_parameter).replace("'", "''") + "'")
                            if filter_parameters_counter != filters_len:
                                column_match += ' AND'
                            query_string += column_match
                            filter_parameters_counter += 1

                attempts = 3
                while attempts:
                    try:
                        query_result = connection.execute(text(query_string))
                        break
                    except exc.OperationalError:
                        attempts -= 1

                columns = [column[0] for column in query_result.cursor.description]

                result_data = []
                for batch_result in self.gen_batch_result(query_result, columns, fetchsize):
                    result_data.extend(batch_result)
                return result_data
            except:
                self.logger.write(40, 'Can\'t read data from the table. - \n\n{}'.format(format_exc()))
                return False

    def insert(self, data, check_dup=False, col_to_check: str = '', query_string: str = '',
               table_name: str = '') -> bool:
        """Makes INSERT query to put data to the database.

        @:param self:
        @:param data: dict of dicts or list of dicts
        @:param check_dup: check or not for duplicates in db (PRIMARY KEY)
        @:param col_to_check: column to check for duplicate
        @:param query_string: custom query string
        @:param table_name: destination table name
        @:type self: DatabaseHelper
        @:type data: dict or list
        @:type check_dup: bool
        @:type col_to_check: str
        @:type query_string: str
        @:type table_name: str

        Makes SELECT query for each col_to_check from data parameter to detect duplicate col_to_check in the database ->
        makes INSERT query for unique col_to_check data.

        @:returns: True or False
        @:rtype: bool
        """

        with self.db_connection() as connection:
            try:
                if not query_string:
                    if check_dup:
                        data_to_write = []
                        for key, value in data.items():
                            result = self.select([col_to_check], {col_to_check: key})
                            if not result:
                                data_to_write.append(value)
                    else:
                        if isinstance(data, list):
                            data_to_write = data
                        else:
                            data_to_write = list(data.values())

                    if data_to_write:
                        joined_keys = '({})'.format(','.join([key.replace("'",
                                                                          "''") for key in data_to_write[0].keys()]))

                        values_joined_list = []
                        items_values = (item_data.values() for item_data in data_to_write)
                        for item_values in items_values:
                            joined_item_values = '({})'.format(','.join(["N'" + str(value).replace("'", "''") + "'"
                                                                         for value in item_values]))
                            values_joined_list.append(joined_item_values)

                        if 'date' in data_to_write[0]:
                            if not data_to_write[0].get('date'):
                                query = text("INSERT INTO {} {} VALUES {}".format(table_name,
                                                                                  '(id)', "('{}')".format(
                                                                                   data_to_write[0].get('id'))))
                            else:
                                joined_values = ','.join(values_joined_list)
                                query = text("INSERT INTO {} {} VALUES {}".format(table_name, joined_keys,
                                                                                  joined_values))
                        else:
                            joined_values = ','.join(values_joined_list)
                            query = text("INSERT INTO {} {} VALUES {}".format(table_name, joined_keys, joined_values))
                connection.execute(query)
                return True
            except:
                self.logger.write(40, 'Can\'t write data to the table. - \n\n{}'.format(format_exc()))
                return False

    def update(self, data, filter_parameters: Dict = {}, query_string: str = '', table_name: str = '') -> bool:
        """Makes UPDATE query to update data in database.

        @:param self:
        @:param data: data to update
        @:param filter_parameters: filters for WHERE query
        @:param query_string: custom query string
        @:param table_name: destination table name
        @:type self: DatabaseHelper
        @:type data: dict
        @:type filter_parameters: dict
        @:type query_string: str
        @:type table_name: str

        Makes UPDATE query.

        @:returns: True or False
        @:rtype: bool
        """

        with self.db_connection() as connection:
            try:
                if not query_string:
                    set_string = ','.join(['{}=\'{}\''.format(key.replace("'", "''"), str(value).replace("'", "''"))
                                           for key, value in data.items()])
                    query_string = 'UPDATE {} SET {}'.format(table_name, set_string)

                    if filter_parameters:
                        query_string += ' WHERE'

                        filter_parameters_counter = 1
                        filters_len = len(filter_parameters)

                        for filter_name, filter_parameter in filter_parameters.items():
                            if isinstance(filter_parameter, list):
                                filter_params = '(' + ','.join(
                                    ["N'" + str(value).replace("'", "''") + "'" for value in filter_parameter]) + ')'
                                column_match = ' {} IN {}'.format(filter_name, filter_params)
                            else:
                                column_match = ' {}={}'.format(filter_name,
                                                               "N'" + str(filter_parameter).replace("'", "''") + "'")
                            if filter_parameters_counter != filters_len:
                                column_match += ' AND'
                            query_string += column_match
                            filter_parameters_counter += 1

                connection.execute(text(query_string))
                return True
            except:
                self.logger.write(40, 'Can\'t update data in db. - \n\n{}'.format(format_exc()))
                return False

    def delete(self, filter_parameters: Dict = {}, query_string: str = '', table_name: str = '') -> bool:
        """Makes DELETE query.

        @:param self:
        @:param filter_parameters: filters for WHERE query
        @:param query_string: custom query string
        @:param table_name: destination table name
        @:type self: DatabaseHelper
        @:type filter_parameters: dict
        @:type query_string: str
        @:type table_name: str

        Makes DELETE query to delete data from database.

        @:returns: True or False
        @:rtype: bool
        """

        with self.db_connection() as connection:
            try:
                if not query_string:
                    query_string = 'DELETE FROM {}'.format(table_name)

                    if filter_parameters:
                        query_string += ' WHERE'

                        filter_parameters_counter = 1
                        filters_len = len(filter_parameters)

                        for filter_name, filter_parameter in filter_parameters.items():
                            if isinstance(filter_parameter, list):
                                filter_params = '(' + ','.join(
                                    ["N'" + str(value).replace("'", "''") + "'" for value in filter_parameter]) + ')'
                                column_match = ' {} IN {}'.format(filter_name, filter_params)
                            else:
                                column_match = ' {}={}'.format(filter_name,
                                                               "N'" + str(filter_parameter).replace("'", "''") + "'")
                            if filter_parameters_counter != filters_len:
                                column_match += ' AND'
                            query_string += column_match
                            filter_parameters_counter += 1

                connection.execute(text(query_string))
                return True
            except:
                self.logger.write(40, 'Can\'t update data in db. - \n\n{}'.format(format_exc()))
                return False

    @staticmethod
    def gen_batch_result(cursor, columns: List[str], fetchsize: int) -> List[Dict[str, Any]]:
        """Makes fetchmany from cursor to get results from query.

        @:param cursor: database cursor
        @:param columns: columns to zip with values
        @:param fetchsize: max amount of records which returns from request at once
        @:type cursor: Cursor
        @:type columns: list
        @:type fetchsize: int

        Makes fetchmany from cursor to get results -> if not results - break -> yields fetchmany results.

        @:returns: ASINs list
        @:rtype: list
        """

        while True:
            results = cursor.fetchmany(fetchsize)
            if not results:
                break
            else:
                modify_results = [dict(zip(columns, row)) for row in results]
                yield modify_results

    @contextmanager
    def db_connection(self):
        """Yields connection.

        Gets db credentials from config file -> creates connection -> yields engine.
        """

        server = self.db_credentials.get('server')
        database = self.db_credentials.get('database')
        username = self.db_credentials.get('username')
        password = self.db_credentials.get('password')

        # Setup connection parameters
        driver = '{/opt/microsoft/msodbcsql17/lib64/libmsodbcsql-17.5.so.2.1}'
        connection_string = 'DRIVER={};SERVER={};PORT=1433;DATABASE={};UID={};PWD={}'.format(driver, server, database,
                                                                                             username, password)

        params = parse.quote_plus(connection_string)
        engine = create_engine('mssql+pyodbc:///?odbc_connect=%s' % params, fast_executemany=True)

        connection = engine.connect()
        try:
            yield connection
        except exc.DatabaseError as err:
            self.logger.write(40, 'DatabaseError. - {}'.format(format_exc()))
            connection.execute('ROLLBACK')
            raise err
        finally:
            connection.close()
