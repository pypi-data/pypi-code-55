# Copyright 2020 Okera Inc. All Rights Reserved.
#
# Some integration tests for auth in PyOkera
#
# pylint: disable=global-statement
# pylint: disable=no-self-use
# pylint: disable=no-else-return

import unittest

#import datetime
import json
import warnings
import pytz

from okera import context
# from okera.tests import pycerebro_test_common as common

DEFAULT_PRESTO_PORT = 8049

## The all types check here will need to be verified against the JDBC data source,
## maybe by running query in DBeaver.
class JdbcScanTest(unittest.TestCase):

    def format(self, data):
        return json.dumps(data, sort_keys=True, indent=1)

    def assert_output(self, qry, expected, is_scan=True):
        warnings.filterwarnings("ignore", message="numpy.dtype size changed")
        ctx = context(dialect='presto', tz=pytz.timezone('UTC'))
        ctx.enable_token_auth(token_str='root')
        with ctx.connect(host='localhost', port=12050,
                         presto_port=DEFAULT_PRESTO_PORT) as conn:
            if is_scan:
                result = conn.scan_as_json(qry, strings_as_utf8=False)
            else:
                result = conn.execute_ddl(qry)
            print("Actual and expected: ")
            print(format(result))
            print(expected)
            print("Done printing.....")
            assert result == expected

    def test_jdbc_all_types(self):
        self.assert_output(
            'select * from jdbc_test_mysql.all_types_v2',
            [{'date': None, 'decimal': None, 'float': None, 'mediumint': None,
              'blob': None, 'tinyblob': None, 'bigint': None,
              'mediumtext': None, 'datetime': None, 'time': None,
              'longtext': None, 'mediumblob': None, 'smallint': None, 'enum': None,
              'varchar': None, 'tinytext': None, 'timestamp': None, 'binary': None,
              'longblob': None, 'int': None, 'set': None, 'tinyint': None, 'bool': None,
              'varbinary': None, 'text': None, 'char': None, 'double': None},
             {'date': '1990-01-01', 'decimal': '8.23', 'float': 7.099999904632568,
              'mediumint': 3, 'blob': 'blob', 'tinyblob': 'tinyblob', 'bigint': 5,
              'mediumtext': 'mediumtext', 'datetime': '2020-10-01 18:19:03.000',
              'time': '1970-01-01 00:20:20.000', 'longtext': 'longtext',
              'mediumblob': 'mediumblob', 'smallint': 2, 'enum': '1', 'varchar':
              'test', 'tinytext': 'tinytext', 'timestamp': '2017-06-01 18:19:03.000',
              'binary': 'binary\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
              'longblob': 'longblob', 'int': 4, 'set': '1,2  ', 'tinyint': 1,
              'bool': True, 'varbinary': 'varbinary', 'text': 'hello',
              'char': 'char      ', 'double': 6.0}])

        self.assert_output(
            'select * from jdbc_test_psql.all_types',
            [{'bigint': None, 'bigserial': 1, 'money': None, 'numeric': None,
              'text': None, 'timestamp': None, 'real': None, 'serial': 1, 'bool': None,
              'int': None, 'double': None, 'time': None, 'smallint': None, 'bit': None,
              'varchar': None, 'decimal': None, 'char': None},
             {'bigint': 3, 'bigserial': 2, 'money': 10.0, 'numeric': '7.10',
              'text': 'hello', 'timestamp': '2017-06-01 18:19:03.000', 'real': 2.13000011,
              'serial': 2, 'bool': True, 'int': 2, 'double': 6.0,
              'time': '1970-01-01 18:19:03.000', 'smallint': 1,
              'bit': 1010101010, 'varchar': 'test', 'decimal': '8.23',
              'char': 'char      '}])

        self.assert_output(
            'select * from jdbc_test_redshift.all_types',
            [{'int': None, 'decimal': None, 'text': None, 'smallint': None,
              'numeric': None, 'real': None, 'char': None, 'double': None, 'bool': None,
              'varchar': None, 'timestamp': None, 'bigint': None},
             {'int': 2, 'decimal': '8.23', 'text': 'hello', 'smallint': 1,
              'numeric': '7.10', 'real': 10.0, 'char': 'char      ',
              'double': 6.0, 'bool': True, 'varchar': 'test',
              'timestamp': '2017-06-01 18:19:03.000', 'bigint': 3}])

        ## TODO: FLOAT has precision loss, but this is know issue because
        ## Oracle DB treats float precision based on data.
        self.assert_output(
            'select * from jdbc_test_oracle.all_types',
            [{'int_col': 4, 'date_col': '2017-06-01 00:00:00.000',
              'timestamp_col': '2017-06-01 18:19:03.000', 'smallint_col': 3,
              'dec_col': '4000000.45', 'number_col': 1, 'numeric_col': 2,
              'bigint_col': '100000000000', 'decimal_col': '3000.45',
              'char_col': 'char      ', 'float_col': '0.000003',
              'varchar_col': 'varchar2', 'nvarchar_col': 'nvarchar2'},
             {'int_col': None, 'date_col': None, 'timestamp_col': None,
              'smallint_col': None, 'dec_col': None, 'number_col': None,
              'numeric_col': None, 'bigint_col': None, 'decimal_col': None,
              'char_col': None, 'float_col': None, 'varchar_col': None,
              'nvarchar_col': None}])

        ## TODO for snowflake, athena and sqlserver
