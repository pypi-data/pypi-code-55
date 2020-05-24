import cx_Oracle

from trecord.database import Database
from trecord.error import TRecordError


class CxOracle(Database):
    """This class implements the database using cx_Oracle"""

    def __init__(self) -> None:
        super().__init__()

    def connect(self, database_url: str):
        super().connect(database_url)
        if self.database_url.database:
            dsn = cx_Oracle.makedsn(self.database_url.host, self.database_url.port, self.database_url.database)
        else:
            dsn = self.database_url.host
        self.connection = cx_Oracle.connect(user=self.database_url.username,
                                            password=self.database_url.password,
                                            dsn=dsn,
                                            encoding="UTF-8",
                                            nencoding="UTF-8"
                                            )

    def query(self, query: str, limit: int = None):
        try:
            result = super().query(query, limit)
            return result
        except cx_Oracle.Error as err:
            raise TRecordError(err)

    def add_row_limit_in_query(self, query, limit):
        query = query.strip(' ;')
        if limit and query.lower().startswith('select'):
            return f'SELECT * FROM ({query}) WHERE ROWNUM <= {limit}'
        else:
            return query

    def get_data_type(self, type_code: int) -> str:
        """
        Check the type code and return a string description
        :param type_code:
        :return:
        """
        mapping = {
            cx_Oracle.STRING: 'STRING',
            cx_Oracle.BLOB: 'BLOB',
            cx_Oracle.BOOLEAN: 'BOOLEAN',
            cx_Oracle.CLOB: 'CLOB',
            cx_Oracle.DATETIME: 'DATETIME',
            cx_Oracle.FIXED_CHAR: 'FIXED_CHAR',
            cx_Oracle.FIXED_NCHAR: 'FIXED_NCHAR',
            cx_Oracle.INTERVAL: 'INTERVAL',
            cx_Oracle.NATIVE_INT: 'NATIVE_INT',
            cx_Oracle.NCHAR: 'NCHAR',
            cx_Oracle.NCLOB: 'NCLOB',
            cx_Oracle.ROWID: 'ROWID',
            cx_Oracle.BINARY: 'BINARY',
            cx_Oracle.NUMBER: 'NUMBER',
            cx_Oracle.TIMESTAMP: 'TIMESTAMP'
        }
        for key in mapping.keys():
            if type_code is key:
                return mapping[key]

        return str(type_code)

    def get_version(self) -> str:
        return '\n'.join(self.query('SELECT * FROM V$VERSION').get_col(0)) + '\n'

    def get_current_db(self) -> str:
        return ''

    def check_dict_privs(self) -> bool:
        count = self.query(f"select count(*) from USER_SYS_PRIVS where PRIVILEGE like '%SELECT%DICTIONARY%'")[0][0]
        if count > 0:
            return True
        else:
            return False

    def get_tables(self, database=None) -> list:
        if not database:
            database = self.database_url.username

        return self.query(f"SELECT table_name FROM ALL_TABLES WHERE owner = '{database.upper()}'").get_col(0)

    def get_partitions(self, table, database) -> []:
        query = f"""
            SELECT
            c.COLUMN_NAME,
            t.PARTITIONING_TYPE
            FROM ALL_PART_TABLES t
            JOIN ALL_PART_KEY_COLUMNS c
            ON   t.OWNER = c.OWNER
            AND  t.TABLE_NAME = c.NAME
            WHERE t.TABLE_NAME = '{table.upper()}'
            AND   t.OWNER = '{database.upper()}'
            ORDER BY c.COLUMN_POSITION
            """
        return self.query(query).dict

    def get_ddl(self, table, database=None) -> str:
        if not database:
            database = self.database_url.username

        ddl = None
        partitions = self.get_partitions(table, database)

        if self.check_dict_privs() and not partitions:
            ddl = self.get_ddl_from_meta(table, database)
        else:
            ddl = self.create_ddl(table, database)
            if partitions:
                ddl += f'\nPartition Info:\n'
                for item in partitions:
                    ddl = ddl + \
                          f'PARTITION BY {item["PARTITIONING_TYPE(STRING)"]} ({item["COLUMN_NAME(STRING)"]})' + "\n"

        return ddl

    def create_ddl(self, table, database):
        ddl = f'CREATE TABLE {database}.{table} (\n'

        metadata = self.query(f"select column_name, data_type, data_length, data_precision, data_scale, nullable \
            from all_tab_columns where upper(table_name) = upper('{table}') and upper(owner) = upper('{database}') "
                              f"order by column_id;")

        for index, column in enumerate(self.column_list_for_ddl(metadata)):
            if index == 0:
                ddl += ('  {} {}\n'.format(column[0], column[1]))
            else:
                ddl += (', {} {}\n'.format(column[0], column[1]))

        ddl += ')\n;\n\n'

        for index_owner, index_name, unique in self.get_indexes(table, database):
            if unique == 'NONUNIQUE':
                ddl += f"CREATE INDEX {index_owner}.{index_name} ON {database}.{table} " \
                       f"({','.join(self.get_index_columns(index_name, index_owner))});\n\n"
            else:
                ddl += f"CREATE UNIQUE INDEX {index_owner}.{index_name} ON {database}.{table} " \
                       f"({','.join(self.get_index_columns(index_name, index_owner))});\n\n"

        return ddl

    def get_indexes(self, table, database):
        return self.query(
            f"select OWNER AS INDEX_OWNER, INDEX_NAME, UNIQUENESS "
            f"from all_indexes where upper(table_name) = upper('{table}')"
            f" and upper(owner) = upper('{database}')")

    def get_index_columns(self, index, owner):
        return self.query(
            f"select COLUMN_NAME from all_ind_columns"
            f" where index_owner = '{owner}' and INDEX_NAME = '{index}'").get_col(0)

    def column_list_for_ddl(self, metadata):
        column_ddl = []
        for column_name, data_type, length, precision, scale, nullable in metadata:
            if data_type == 'NUMBER':
                if not precision:
                    precision = 38
                    scale = 0
                column_ddl.append([column_name, 'DECIMAL({}, {})'.format(precision, scale)])
            elif data_type == 'VARCHAR2':
                column_ddl.append([column_name, 'VARCHAR2({})'.format(length)])
            elif data_type.startswith('TIMESTAMP'):
                column_ddl.append([column_name, 'TIMESTAMP'])
            elif data_type == 'DATE':
                column_ddl.append([column_name, 'DATE'])
            elif data_type == 'CHAR':
                column_ddl.append([column_name, 'CHAR({})'.format(length)])
            else:
                raise RuntimeError('New data type found: {}'.format(data_type))

            if nullable == 'N':
                column_ddl[-1][-1] += ' NOT NULL'

        return column_ddl

    def get_ddl_from_meta(self, table, database) -> str:
        ddl = str(
            self.query(f"SELECT dbms_metadata.get_ddl('TABLE', '{table.upper()}', '{database.upper()}') FROM dual")[0][
                0]) + '\n;\n'

        for row in self.query(
                f"SELECT distinct index_owner, index_name FROM all_ind_columns "
                f"where table_name = '{table.upper()}' and table_owner = '{database.upper()}'"):
            index_owner = row[0]
            index_name = row[1]
            if f'"{index_name}"' in ddl:
                continue
            ddl = ddl + '\n' + str(
                self.query(f"SELECT dbms_metadata.get_ddl('INDEX', '{index_name}', '{index_owner}') FROM dual")[0][
                    0]) + '\n;\n'

        return ddl


if __name__ == '__main__':
    import sys

    sql = CxOracle()
    sql.connect(sys.argv[1])
    print(sql.get_version())
    print(sql.get_current_db())
    print(sql.get_ddl('agg_cs_aps_interval', 'cs_orp'))
