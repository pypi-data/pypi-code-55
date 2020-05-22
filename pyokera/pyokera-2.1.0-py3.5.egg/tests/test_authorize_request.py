# Copyright 2019 Okera Inc. All Rights Reserved.

#
# Tests for AuthorizeQuery() API
#
# pylint: disable=too-many-arguments

import unittest

from okera import context
from okera._thrift_api import TAuthorizeQueryParams
from okera._thrift_api import TRecordServiceException

from okera.tests import pycerebro_test_common as common

TEST_USER = 'testuser'

class AuthorizeQueryTest(common.TestBase):
    def authorize_query_audit_only(self, conn, query, user=None, db=None, dataset=None):
        request = TAuthorizeQueryParams()
        request.sql = query
        request.requesting_user = user
        request.use_session_local_tables = False
        request.audit_only = True
        if db:
            request.db = [db]
        if dataset:
            request.dataset = dataset
        result = conn.service.client.AuthorizeQuery(request)
        self.assertTrue(result is not None)
        return result

    def authorize_query(self, conn, query, user=None, use_tmp_tables=False):
        request = TAuthorizeQueryParams()
        request.sql = query
        request.requesting_user = user
        request.use_session_local_tables = use_tmp_tables
        result = conn.service.client.AuthorizeQuery(request)
        if result.requires_worker:
            return None
        self.assertTrue(result.result_schema is not None)
        return ' '.join(result.result_sql.split())

    # Returns * if the user can directly access the table, the rewritten query if
    # that's required or None if the user must go to ODAS.
    def authorize_table(self, conn, db, table, user=None, use_tmp_tables=False):
        request = TAuthorizeQueryParams()
        request.db = [db]
        request.dataset = table
        request.requesting_user = user
        request.use_session_local_tables = use_tmp_tables
        result = conn.service.client.AuthorizeQuery(request)
        if result.full_access:
            return '*'
        if result.requires_worker:
            return None
        self.assertTrue(result.result_schema is not None)
        return ' '.join(result.result_sql.split())

    def test_sql(self):
        ctx = context()
        with ctx.connect() as conn:
            self.assertEqual("SELECT 1", self.authorize_query(conn, "select 1"))
            self.assertEqual(
                "SELECT 1", self.authorize_query(conn, "select 1", None, True))

            self.assertEqual(
                "SELECT 'root' as user",
                self.authorize_query(conn, "select * from okera_sample.whoami"))
            self.assertEqual(
                "SELECT 'root' as user",
                self.authorize_query(
                    conn, "select * from okera_sample.whoami", None, True))

            self.assertEqual(
                "SELECT 'root' as user",
                self.authorize_query(conn, "select user from okera_sample.whoami"))
            self.assertEqual(
                "SELECT 'root' as user",
                self.authorize_query(
                    conn, "select user from okera_sample.whoami", None, True))

            self.assertEqual(
                None,
                self.authorize_query(conn, "select * from okera_sample.sample"))
            self.assertEqual(
                None,
                self.authorize_query(
                    conn, "select * from okera_sample.sample", None, True))

            self.assertEqual(
                "SELECT int_col FROM rs.alltypes_s3",
                self.authorize_query(conn, "select int_col from rs.alltypes_s3"))
            self.assertEqual(
                "SELECT int_col FROM rs.alltypes_s3_tmp",
                self.authorize_query(
                    conn, "select int_col from rs.alltypes_s3", None, True))

            self.assertEqual(
                "SELECT bool_col, tinyint_col, smallint_col, int_col, bigint_col, " +\
                "float_col, double_col, string_col, varchar_col, char_col, " +\
                "timestamp_col, decimal_col FROM all_table_types.s3",
                self.authorize_query(conn, "select * from all_table_types.s3"))
            self.assertEqual(
                "SELECT bool_col, tinyint_col, smallint_col, int_col, bigint_col, " +\
                "float_col, double_col, string_col, varchar_col, char_col, " +\
                "timestamp_col, decimal_col FROM all_table_types.s3_tmp",
                self.authorize_query(conn, "select * from all_table_types.s3",
                                     None, True))

            # Now run as testuser
            self.assertEqual(
                "SELECT 'testuser' as user",
                self.authorize_query(
                    conn, "select * from okera_sample.whoami", TEST_USER))
            self.assertEqual(
                "SELECT 'testuser' as user",
                self.authorize_query(
                    conn, "select * from okera_sample.whoami", TEST_USER, True))

            self.assertEqual(
                "SELECT int_col FROM rs.alltypes_s3",
                self.authorize_query(
                    conn, "select int_col from rs.alltypes_s3", TEST_USER))
            self.assertEqual(
                "SELECT int_col FROM rs.alltypes_s3_tmp",
                self.authorize_query(
                    conn, "select int_col from rs.alltypes_s3", TEST_USER, True))

            # * should expand to a subset of the columns
            self.assertEqual(
                "SELECT int_col, float_col, string_col FROM rs.alltypes_s3",
                self.authorize_query(conn, "select * from rs.alltypes_s3", TEST_USER))
            self.assertEqual(
                "SELECT int_col, float_col, string_col FROM rs.alltypes_s3_tmp",
                self.authorize_query(
                    conn, "select * from rs.alltypes_s3", TEST_USER, True))

            # Selecting a column wit no access should fail
            with self.assertRaises(TRecordServiceException) as ex_ctx:
                self.authorize_query(
                    conn, "select bool_col from rs.alltypes_s3", TEST_USER)
            self.assertTrue('does not have privileges' in str(ex_ctx.exception))
            with self.assertRaises(TRecordServiceException) as ex_ctx:
                self.authorize_query(
                    conn, "select bool_col from rs.alltypes_s3", TEST_USER, True)
            self.assertTrue('does not have privileges' in str(ex_ctx.exception))

    def test_audit_only(self):
        ctx = context()
        with ctx.connect() as conn:
            self.authorize_query_audit_only(conn, 'select * from bar1')
            self.authorize_query_audit_only(conn, 'select * from bar2', user='user1')
            self.authorize_query_audit_only(
                conn, 'select * from bar3',
                user='user2', db='xyz', dataset='abc.def')
            self.authorize_query_audit_only(
                conn, 'select * from bar4', user='user3',
                db='xyz,abc', dataset='abc.def,foo.bar')

    def test_table(self):
        ctx = context()
        with ctx.connect() as conn:
            self.assertEqual(None, self.authorize_table(conn, "okera_sample", "sample"))
            self.assertEqual(
                None, self.authorize_table(conn, "okera_sample", "sample", None, True))

            self.assertEqual(
                None, self.authorize_table(conn, "okera_sample", "sample", TEST_USER))
            self.assertEqual(
                None,
                self.authorize_table(conn, "okera_sample", "sample", TEST_USER, True))

            self.assertEqual('*', self.authorize_table(conn, "rs", "alltypes_s3"))
            self.assertEqual(
                '*',
                self.authorize_table(conn, "rs", "alltypes_s3", None, True))
            self.assertEqual(
                "SELECT int_col, float_col, string_col FROM rs.alltypes_s3",
                self.authorize_table(conn, "rs", "alltypes_s3", TEST_USER))
            self.assertEqual(
                "SELECT int_col, float_col, string_col FROM rs.alltypes_s3_tmp",
                self.authorize_table(conn, "rs", "alltypes_s3", TEST_USER, True))

            # This is a view, we want to "flatten"
            self.assertEqual(
                "SELECT 'root' as user",
                self.authorize_table(conn, "okera_sample", "whoami"))
            self.assertEqual(
                "SELECT 'root' as user",
                self.authorize_table(conn, "okera_sample", "whoami", None, True))
            self.assertEqual(
                "SELECT 'testuser' as user",
                self.authorize_table(conn, "okera_sample", "whoami", TEST_USER))
            self.assertEqual(
                "SELECT 'testuser' as user",
                self.authorize_table(conn, "okera_sample", "whoami", TEST_USER, True))

            # No access
            with self.assertRaises(TRecordServiceException) as ex_ctx:
                self.authorize_table(conn, "nytaxi", "parquet_data", TEST_USER)
            self.assertTrue('does not have privileges' in str(ex_ctx.exception))

            with self.assertRaises(TRecordServiceException) as ex_ctx:
                self.authorize_table(conn, "nytaxi", "parquet_data", TEST_USER, True)
            self.assertTrue('does not have privileges' in str(ex_ctx.exception))

    def test_tmp_views(self):
        ctx = context()
        with ctx.connect() as conn:
            # Get the full schema as root
            full_schema = conn.list_datasets("rs", name="alltypes_s3")[0].schema
            self.assertEqual(12, len(self._visible_cols(full_schema.cols)))

            # Get the schemas a testuser, this should be a subset
            ctx.enable_token_auth(token_str=TEST_USER)
            partial_schema = conn.list_datasets("rs", name="alltypes_s3")[0].schema
            self.assertEqual(3, len(self._visible_cols(partial_schema.cols)))

            # Reading the tmp version should have. It doesn't exist yet.
            with self.assertRaises(TRecordServiceException) as ex_ctx:
                conn.scan_as_json("rs.alltypes_s3_tmp")
            self.assertTrue('does not have privileges' in str(ex_ctx.exception))

            # Authorize this query, this will temporarily add the temp table and it
            # will have the full schema.
            self.authorize_table(conn, "rs", "alltypes_s3", TEST_USER, True)
            result = conn.list_datasets("rs", name="alltypes_s3_tmp")[0]

            # Note: this returns all the columns, which the user is not normally
            # able to see.
            self.assertEqual(12, len(self._visible_cols(result.schema.cols)))
            self.assertEqual(full_schema, result.schema)

            self.assertEqual("rs", result.db[0])
            self.assertEqual("alltypes_s3_tmp", result.name)

            self.assertEqual(
                '*',
                self.authorize_table(conn, "rs", "alltypes_s3_tmp", TEST_USER, True))

            # Do it again
            self.assertEqual(
                '*',
                self.authorize_table(conn, "rs", "alltypes_s3_tmp", TEST_USER, True))

        # Recreate the connection, the temp tables are gone
        with ctx.connect() as conn:
            with self.assertRaises(TRecordServiceException) as ex_ctx:
                self.authorize_table(conn, "rs", "alltypes_s3_tmp", TEST_USER, True)
            self.assertTrue('does not have privileges' in str(ex_ctx.exception))

    def test_require_worker(self):
        # Test tables are atypical and always require the worker to evaluate
        ctx = context()
        with ctx.connect() as conn:
            for user in [None, TEST_USER]:
                self.assertEqual(
                    None, self.authorize_table(conn, "all_table_types", "local_fs", user))
                self.assertEqual(
                    None,
                    self.authorize_table(
                        conn, "all_table_types", "external_view_only", user))
                self.assertEqual(
                    None,
                    self.authorize_table(
                        conn, "all_table_types", "external_view_only", user))
                self.assertEqual(
                    '*',
                    self.authorize_table(
                        conn, "all_table_types", "dbfs_table", user))
                if user is None:
                    self.assertEqual(
                        None,
                        self.authorize_table(
                            conn, "okera_system", "audit_logs", user))

                # FIXME: not working. We don't load enough metadata right now in this
                # RPC to do this.
                #self.assertEqual(
                #    None,
                #    self.authorize_table(
                #        conn, "all_table_types", "single_file_table", user))
                #self.assertEqual(
                #    None,
                #    self.authorize_table(
                #        conn, "all_table_types", "http_table", user))

if __name__ == "__main__":
    unittest.main()
