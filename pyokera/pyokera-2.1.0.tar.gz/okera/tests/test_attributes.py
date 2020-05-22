# Copyright 2019 Okera Inc. All Rights Reserved.
#
# Some integration tests for managing attributes
#
# pylint: disable=bad-continuation
# pylint: disable=too-many-arguments

import unittest

from okera import context

class AttributesTest(unittest.TestCase):
    @staticmethod
    def _contains_attribute(namespace, key, attributes):
        for attr in attributes:
            if attr.attribute_namespace == namespace and attr.key == key:
                return True
        return False

    @staticmethod
    def _collect_column_attributes(ds):
        result = {}
        for col in ds.schema.cols:
            if not col.attribute_values:
                continue
            for v in col.attribute_values:
                key = v.database
                if v.table:
                    key += '.' + v.table
                    if v.column:
                        key += '.' + v.column
                if key not in result:
                    result[key] = []
                result[key].append(
                    v.attribute.attribute_namespace + '.' + v.attribute.key)
        for _, v in result.items():
            v.sort()
        return result

    def _verify_attr(self, val, namespace, key, db, tbl, col):
        self.assertTrue(val.attribute.attribute_namespace == namespace)
        self.assertTrue(val.attribute.key == key)
        self.assertTrue(val.database == db)
        self.assertTrue(val.table == tbl)
        self.assertTrue(val.column == col)

    def test_basic(self):
        with context().connect() as conn:
            conn.create_attribute('abac_test', 'v1')
            conn.create_attribute('abac_test', 'v2')
            attributes = conn.list_attributes('abac_test')
            self.assertTrue(len(attributes) >= 2, msg=str(attributes))
            self.assertTrue(self._contains_attribute('abac_test', 'v1', attributes),
                            msg=str(attributes))
            self.assertTrue(self._contains_attribute('abac_test', 'v2', attributes),
                            msg=str(attributes))
            old_len = len(attributes)
            namespaces = conn.list_attribute_namespaces()
            self.assertTrue('abac_test' in namespaces)

            # Delete the attribute and make sure it is gone
            self.assertTrue(conn.delete_attribute('abac_test', 'v2'))
            attributes = conn.list_attributes('abac_test')
            for a in attributes:
                self.assertTrue(a.id is not None)
            self.assertTrue(old_len == len(attributes) + 1)
            self.assertTrue(self._contains_attribute('abac_test', 'v1', attributes),
                            msg=str(attributes))
            self.assertFalse(self._contains_attribute('abac_test', 'v2', attributes),
                             msg=str(attributes))
            namespaces = conn.list_attribute_namespaces()
            self.assertTrue('abac_test' in namespaces)

    def test_multiple_namespaces(self):
        ctx = context()
        test_user = "ATTRIBUTE_TEST_USER"
        with ctx.connect() as conn:
            conn.create_attribute('abac_test1', 'v')
            conn.create_attribute('abac_test2', 'v')
            conn.create_attribute('abac_test3', 'v')
            conn.execute_ddl("DROP ROLE IF EXISTS attribute_test_role")

            namespaces = conn.list_attribute_namespaces()
            self.assertTrue('abac_test1' in namespaces)
            self.assertTrue('abac_test2' in namespaces)
            self.assertTrue('abac_test3' in namespaces)

            # Editable only is the same for admin
            for editable in [True, False]:
                namespaces = conn.list_attribute_namespaces(editable_only=editable)
                self.assertTrue('abac_test1' in namespaces)
                self.assertTrue('abac_test2' in namespaces)
                self.assertTrue('abac_test3' in namespaces)

                attributes = conn.list_attributes('abac_test1')
                self.assertTrue(self._contains_attribute('abac_test1', 'v', attributes))
                self.assertFalse(self._contains_attribute('abac_test2', 'v', attributes))

                # List in all namespaces
                attributes = conn.list_attributes(editable_only=editable)
                self.assertTrue(self._contains_attribute('abac_test1', 'v', attributes))
                self.assertTrue(self._contains_attribute('abac_test2', 'v', attributes))
                self.assertTrue(self._contains_attribute('abac_test3', 'v', attributes))

                attributes = conn.list_attributes(None, editable_only=editable)
                self.assertTrue(self._contains_attribute('abac_test1', 'v', attributes))
                self.assertTrue(self._contains_attribute('abac_test2', 'v', attributes))
                self.assertTrue(self._contains_attribute('abac_test3', 'v', attributes))

                attributes = conn.list_attributes('', editable_only=editable)
                self.assertTrue(self._contains_attribute('abac_test1', 'v', attributes))
                self.assertTrue(self._contains_attribute('abac_test2', 'v', attributes))
                self.assertTrue(self._contains_attribute('abac_test3', 'v', attributes))

            # Try as a test user, no edit access
            ctx.enable_token_auth(token_str=test_user)
            namespaces = conn.list_attribute_namespaces()
            self.assertTrue('abac_test1' in namespaces)
            self.assertTrue('abac_test2' in namespaces)
            self.assertTrue('abac_test3' in namespaces)
            namespaces = conn.list_attribute_namespaces(editable_only=True)
            self.assertTrue(len(namespaces) == 0)

            attributes = conn.list_attributes('abac_test1')
            self.assertTrue(self._contains_attribute('abac_test1', 'v', attributes))
            self.assertFalse(self._contains_attribute('abac_test2', 'v', attributes))
            attributes = conn.list_attributes('abac_test1', editable_only=True)
            self.assertTrue(len(attributes) == 0)

            attributes = conn.list_attributes(editable_only=False)
            self.assertTrue(self._contains_attribute('abac_test1', 'v', attributes))
            self.assertTrue(self._contains_attribute('abac_test2', 'v', attributes))
            self.assertTrue(self._contains_attribute('abac_test3', 'v', attributes))
            attributes = conn.list_attributes('', editable_only=True)
            self.assertTrue(len(attributes) == 0)

            # Grant this test user all on two namespaces
            ctx.disable_auth()
            conn.execute_ddl("CREATE ROLE attribute_test_role")
            conn.execute_ddl("GRANT ROLE attribute_test_role TO GROUP " + test_user)
            conn.execute_ddl(
                "GRANT ALL ON ATTRIBUTE NAMESPACE abac_test1 TO ROLE attribute_test_role")

            ctx.enable_token_auth(token_str=test_user)
            namespaces = conn.list_attribute_namespaces()
            self.assertTrue('abac_test1' in namespaces)
            self.assertTrue('abac_test2' in namespaces)
            self.assertTrue('abac_test3' in namespaces)
            namespaces = conn.list_attribute_namespaces(editable_only=True)
            self.assertTrue('abac_test1' in namespaces)
            self.assertTrue('abac_test2' not in namespaces)

            attributes = conn.list_attributes('abac_test1')
            self.assertTrue(self._contains_attribute('abac_test1', 'v', attributes))
            self.assertFalse(self._contains_attribute('abac_test2', 'v', attributes))
            attributes = conn.list_attributes('abac_test1', editable_only=True)
            self.assertTrue(self._contains_attribute('abac_test1', 'v', attributes))
            self.assertFalse(self._contains_attribute('abac_test2', 'v', attributes))

            attributes = conn.list_attributes(editable_only=False)
            self.assertTrue(self._contains_attribute('abac_test1', 'v', attributes))
            self.assertTrue(self._contains_attribute('abac_test2', 'v', attributes))
            self.assertTrue(self._contains_attribute('abac_test3', 'v', attributes))
            attributes = conn.list_attributes('', editable_only=True)
            self.assertTrue(self._contains_attribute('abac_test1', 'v', attributes))
            self.assertFalse(self._contains_attribute('abac_test2', 'v', attributes))

    def test_create_delete(self):
        with context().connect() as conn:
            conn.delete_attribute('abac_test', 'v1')
            conn.delete_attribute('abac_test', 'v2')

            # Try deleting again, should not exist
            self.assertFalse(conn.delete_attribute('abac_test', 'v1'))
            self.assertFalse(conn.delete_attribute('abac_test', 'v2'))

            conn.create_attribute('abac_test', 'v1')
            conn.create_attribute('abac_test', 'v2')
            attributes = conn.list_attributes('abac_test')
            self.assertTrue(len(attributes) >= 2, msg=str(attributes))
            self.assertTrue(self._contains_attribute('abac_test', 'v1', attributes),
                            msg=str(attributes))
            self.assertTrue(self._contains_attribute('abac_test', 'v2', attributes),
                            msg=str(attributes))

            # Try deleting should exist
            self.assertTrue(conn.delete_attribute('abac_test', 'v1'))
            self.assertTrue(conn.delete_attribute('ABAC_test', 'V2'))

    def test_assign_get_attributes(self):
        db = 'attributes_test_db'
        with context().connect() as conn:
            conn.create_attribute('abac_test', 'V1')
            conn.create_attribute('ABAC_test', 'v2')

            conn.execute_ddl('DROP DATABASE IF EXISTS %s CASCADE' % db)
            conn.execute_ddl('CREATE DATABASE %s' % db)
            self.assertTrue(len(conn.list_datasets(db)) == 0)

            # Create 2 tables and 2 views
            conn.execute_ddl('CREATE TABLE %s.t1(c1 int, c2 int, c3 int)' % db)
            conn.execute_ddl('CREATE TABLE %s.t2(c1 int, c2 int, c3 int)' % db)
            conn.execute_ddl('CREATE VIEW %s.v1 AS SELECT * from %s.t1' % (db, db))
            conn.execute_ddl('CREATE VIEW %s.v2 AS SELECT * from %s.t1' % (db, db))
            self.assertTrue(len(conn.list_datasets(db)) == 4)

            # Get the attributes on t1, should be empty
            ds = conn.list_datasets(db, name='t1')[0]
            self.assertTrue(ds.attribute_values is None)
            attrs_by_col = self._collect_column_attributes(ds)
            self.assertTrue(not attrs_by_col)

            # Ensure get_tags returns empty
            self.assertEqual('',
                conn.scan_as_json("select get_tags('%s.t1') as v" % db)[0]['v'])
            self.assertEqual('',
                conn.scan_as_json("select get_tags('%s.t1.c1') as v" % db)[0]['v'])
            self.assertEqual('',
                conn.scan_as_json("select get_tags('%s.t1.not_a_col') as v" % db)[0]['v'])

            # Assign abac_test.v1 to t1
            conn.assign_attribute('abac_TEST', 'v1', db, 't1', cascade=False)
            conn.assign_attribute('abac_test', 'v1', db, 't1', cascade=False)
            ds = conn.list_datasets(db, name='t1')[0]
            attrs = ds.attribute_values
            self.assertTrue(attrs is not None)
            self.assertTrue(len(attrs) == 1)
            self._verify_attr(attrs[0], 'abac_test', 'v1', db, 't1', None)
            self.assertTrue(not self._collect_column_attributes(ds))

            # Check get_tags
            self.assertEqual('abac_test.v1',
                conn.scan_as_json("select get_tags('%s.t1') as v" % db)[0]['v'])
            self.assertEqual('',
                conn.scan_as_json("select get_tags('%s.t1.c1') as v" % db)[0]['v'])

            # Assign abac_test.v2 to t1
            conn.assign_attribute('abac_test', 'v2', db, 't1', cascade=False)
            ds = conn.list_datasets(db, name='t1')[0]
            attrs = ds.attribute_values
            self.assertTrue(attrs is not None)
            self.assertTrue(len(attrs) == 2)
            if attrs[0].attribute.key == 'v1':
                self._verify_attr(attrs[0], 'abac_test', 'v1', db, 't1', None)
                self._verify_attr(attrs[1], 'abac_test', 'v2', db, 't1', None)
            else:
                self._verify_attr(attrs[1], 'abac_test', 'v1', db, 't1', None)
                self._verify_attr(attrs[0], 'abac_test', 'v2', db, 't1', None)

            # Check get_tags
            self.assertEqual('abac_test.v1,abac_test.v2',
                conn.scan_as_json("select get_tags('%s.t1') as v" % db)[0]['v'])

            # Assign abac_test.v1 to v1 and v2.c2
            conn.assign_attribute('abac_test', 'v1', db, 'v1')
            conn.assign_attribute('abac_test', 'v1', db, 'v2', 'c2')
            ds = conn.list_datasets(db, name='v1')[0]
            self._verify_attr(ds.attribute_values[0], 'abac_test', 'v1', db, 'v1', None)

            # Check get_tags
            self.assertEqual('abac_test.v1',
                conn.scan_as_json("select get_tags('%s.v1') as v" % db)[0]['v'])
            self.assertEqual('',
                conn.scan_as_json("select get_tags('%s.v2.c1') as v" % db)[0]['v'])
            self.assertEqual('abac_test.v1',
                conn.scan_as_json("select get_tags('%s.v2.c2') as v" % db)[0]['v'])

            # Test get_tags on the table. The tag is on a column in the table but
            # we want this to count.
            self.assertEqual('abac_test.v1',
                conn.scan_as_json("select get_tags('%s.v2') as v" % db)[0]['v'])
            self.assertTrue(conn.scan_as_json(
                "select has_tag('%s.v2', 'abac_test.v1') as v" % db)[0]['v'])

            # Check has_tag
            self.assertTrue(conn.scan_as_json(
                "select has_tag('%s.t1', 'abac_test.v1') as v" % db)[0]['v'])
            self.assertTrue(conn.scan_as_json(
                "select has_tag('%s.t1', 'abac_test.v2') as v" % db)[0]['v'])
            self.assertFalse(conn.scan_as_json(
                "select has_tag('%s.t1', 'abac_test.v3') as v" % db)[0]['v'])
            self.assertTrue(conn.scan_as_json(
                "select has_tag('%s.v1', 'abac_test.v1') as v" % db)[0]['v'])
            self.assertFalse(conn.scan_as_json(
                "select has_tag('%s.v2.c1', 'abac_test.v1') as v" % db)[0]['v'])
            self.assertTrue(conn.scan_as_json(
                "select has_tag('%s.v2.c2', 'abac_test.v1') as v" % db)[0]['v'])
            self.assertFalse(conn.scan_as_json(
                "select has_tag('%s.v2.c1', 'abac_test.*') as v" % db)[0]['v'])
            self.assertTrue(conn.scan_as_json(
                "select has_tag('%s.v2.c2', 'abac_test.*') as v" % db)[0]['v'])

            ds = conn.list_datasets(db, name='v2')[0]
            self.assertTrue(ds.attribute_values is None)
            attrs = self._collect_column_attributes(ds)
            self.assertTrue(('%s.v2.c2' % db) in attrs)
            self.assertTrue(('%s.v2.c1' % db) not in attrs)

            # Try again with upper case db
            ds = conn.list_datasets(db.upper(), name='V2')[0]
            self.assertTrue(ds.attribute_values is None)
            attrs = self._collect_column_attributes(ds)
            self.assertTrue(('%s.v2.c2' % db) in attrs)
            self.assertTrue(('%s.v2.c1' % db) not in attrs)

            # Unassign abac_test.v1 from v2.c2
            conn.unassign_attribute('ABAC_test', 'v1', db, 'v2', 'c2')
            ds = conn.list_datasets(db, name='v2')[0]
            self.assertTrue(ds.attribute_values is None)
            attrs = self._collect_column_attributes(ds)
            self.assertTrue(not attrs)
            # Verify the assignment to v1 is still there
            ds = conn.list_datasets(db, name='v1')[0]
            self._verify_attr(ds.attribute_values[0], 'abac_test', 'v1', db, 'v1', None)

            # Check get_tags
            self.assertEqual('',
                conn.scan_as_json("select get_tags('%s.v2') as v" % db)[0]['v'])
            self.assertEqual('',
                conn.scan_as_json("select get_tags('%s.v2.c1') as v" % db)[0]['v'])
            self.assertEqual('',
                conn.scan_as_json("select get_tags('%s.v2.c2') as v" % db)[0]['v'])
            self.assertEqual('abac_test.v1,abac_test.v2',
                conn.scan_as_json("select get_tags('%s.t1') as v" % db)[0]['v'])

            # Unassign abac_test.v1 from v1
            conn.unassign_attribute('abac_test', 'V1', db, 'v1')
            ds = conn.list_datasets(db, name='v1')[0]
            self.assertTrue(ds.attribute_values is None)

    def test_assign_invalid_attributes(self):
        db = 'attributes_test_db'
        with context().connect() as conn:
            conn.create_attribute('abac_test', 'V1')

            conn.execute_ddl('DROP DATABASE IF EXISTS %s CASCADE' % db)
            conn.execute_ddl('CREATE DATABASE %s' % db)

            conn.assign_attribute('abac_test', 'v1', db)
            with self.assertRaises(Exception) as ex_ctx:
                conn.assign_attribute('abac_test', 'not-there', db)
            self.assertTrue('Cannot assign attributes' in str(ex_ctx.exception),
                            msg=str(ex_ctx.exception))

    @unittest.skip("This requires autotagging to be configured.")
    def test_tag_table(self):
        db = 'attributes_test_db'
        with context().connect() as conn:
            conn.execute_ddl('DROP DATABASE IF EXISTS %s CASCADE' % db)
            conn.execute_ddl('CREATE DATABASE %s' % db)
            conn.execute_ddl(('CREATE EXTERNAL TABLE %s.test LIKE AVRO ' +\
                '"s3://cerebrodata-test/poc_chase/avrodata/" STORED AS AVRO ' +\
                'LOCATION "s3://cerebrodata-test/poc_chase/avrodata/"') % db)

            # Should have no tags
            ds = conn.list_datasets(db, name='test')[0]
            self.assertTrue(ds.attribute_values is None)
            attrs = self._collect_column_attributes(ds)
            self.assertTrue(len(attrs) == 0)

            # Execute tag command
            conn.execute_ddl('ALTER TABLE %s.test EXECUTE AUTOTAG' % db)

            # Should have tags
            ds = conn.list_datasets(db, name='test')[0]
            self.assertTrue(ds.attribute_values is None)
            attrs = self._collect_column_attributes(ds)
            self.assertTrue('%s.test.email' % db in attrs)

    def test_cascade(self):
        db = 'attributes_test_db'
        with context().connect() as conn:
            conn.create_attribute('abac_test', 'v')
            conn.execute_ddl('DROP DATABASE IF EXISTS %s CASCADE' % db)
            conn.execute_ddl('CREATE DATABASE %s' % db)
            conn.execute_ddl('CREATE TABLE %s.tbl(i int)' % db)
            conn.execute_ddl('CREATE TABLE %s.tbl2(i int)' % db)
            conn.execute_ddl('CREATE VIEW %s.v1 AS SELECT * FROM %s.tbl' % (db, db))
            conn.execute_ddl('CREATE VIEW %s.v2 AS SELECT * FROM %s.tbl' % (db, db))
            conn.execute_ddl('CREATE VIEW %s.v1_1 AS SELECT * FROM %s.v1' % (db, db))
            tag = 'abac_test.v'

            for ddl, explicit in \
                    [(True, True), (True, False), (False, True), (False, False)]:
                # Should have no tags
                for v in ['tbl', 'tbl2', 'v1', 'v2', 'v1_1']:
                    ds = conn.list_datasets(db, name=v)[0]
                    self.assertTrue(ds.attribute_values is None)

                # Assign tag and cascade. Everything based on tbl should have tags
                if ddl:
                    if explicit:
                        conn.execute_ddl('ALTER TABLE %s.tbl ADD ATTRIBUTE %s CASCADE' % \
                            (db, tag))
                    else:
                        conn.execute_ddl('ALTER TABLE %s.tbl ADD ATTRIBUTE %s ' % \
                            (db, tag))
                else:
                    if explicit:
                        conn.assign_attribute('abac_test', 'v', db, 'tbl', cascade=True)
                    else:
                        conn.assign_attribute('abac_test', 'v', db, 'tbl')

                for v in ['tbl', 'v1', 'v2', 'v1_1']:
                    print("Running it on " + v)
                    ds = conn.list_datasets(db, name=v)[0]
                    self.assertTrue(ds.attribute_values is not None)
                for v in ['tbl2']:
                    ds = conn.list_datasets(db, name=v)[0]
                    self.assertTrue(ds.attribute_values is None)

                ## Unassign from v1, should cascade to v1_1
                conn.execute_ddl('ALTER VIEW %s.v1 DROP ATTRIBUTE %s CASCADE' % (db, tag))
                ## These should have tags
                for v in ['tbl', 'v2']:
                    print("Running it on " + v)
                    ds = conn.list_datasets(db, name=v)[0]
                    self.assertTrue(ds.attribute_values is not None)
                ## These should not have tags
                for v in ['v1', 'v1_1']:
                    print("Running it on " + v)
                    ds = conn.list_datasets(db, name=v)[0]
                    self.assertTrue(ds.attribute_values is None)

                # Unassign from root, nothing should have tags now
                if ddl:
                    if explicit:
                        conn.execute_ddl('ALTER TABLE %s.tbl DROP ATTRIBUTE %s CASCADE' %\
                            (db, tag))
                    else:
                        conn.execute_ddl('ALTER TABLE %s.tbl DROP ATTRIBUTE %s ' % \
                            (db, tag))
                else:
                    if explicit:
                        conn.unassign_attribute('abac_test', 'v', db, 'tbl', cascade=True)
                    else:
                        conn.unassign_attribute('abac_test', 'v', db, 'tbl')

                for v in ['tbl', 'tbl2', 'v1', 'v2', 'v1_1']:
                    print("Running it on " + v)
                    ds = conn.list_datasets(db, name=v)[0]
                    self.assertTrue(ds.attribute_values is None)

                # Assign without cascading, should only be on table
                if ddl:
                    conn.execute_ddl(
                        'ALTER TABLE %s.tbl ADD ATTRIBUTE %s DO NOT CASCADE' %
                        (db, tag))
                else:
                    conn.assign_attribute('abac_test', 'v', db, 'tbl', cascade=False)

                for v in ['tbl']:
                    print("Running it on " + v)
                    ds = conn.list_datasets(db, name=v)[0]
                    self.assertTrue(ds.attribute_values is not None)
                for v in ['tbl2', 'v1', 'v2', 'v1_1']:
                    ds = conn.list_datasets(db, name=v)[0]
                    self.assertTrue(ds.attribute_values is None)

                if ddl:
                    conn.execute_ddl(
                        'ALTER TABLE %s.tbl DROP ATTRIBUTE %s DO NOT CASCADE' %
                        (db, tag))
                else:
                    conn.unassign_attribute('abac_test', 'v', db, 'tbl', cascade=False)

    def _test_cascade_case(self, conn, db, view_def, c1, c2, no_c1=False, no_c2=False):
        conn.execute_ddl('DROP VIEW IF EXISTS %s.v' % db)

        # Create the view and verify inheritance
        conn.execute_ddl(view_def)
        ds = conn.list_datasets(db, name='v')[0]
        attrs = self._collect_column_attributes(ds)
        if no_c1:
            self.assertTrue('attr_test_db.v.' + c1 not in attrs)
        else:
            self.assertEqual(attrs['attr_test_db.v.' + c1], ['attr_test_db.a1'])
        if no_c2:
            self.assertTrue('attr_test_db.v.' + c2 not in attrs)
        else:
            self.assertEqual(attrs['attr_test_db.v.' + c2], ['attr_test_db.a2'])

        # Assign a tag to verify cascade
        conn.execute_ddl("alter table %s.base_table add column attribute c1 %s.a3"\
              % (db, db))
        ds = conn.list_datasets(db, name='v')[0]
        attrs = self._collect_column_attributes(ds)
        if no_c1:
            self.assertTrue('attr_test_db.v.' + c1 not in attrs)
        else:
            self.assertEqual(attrs['attr_test_db.v.' + c1],
                             ['attr_test_db.a1', 'attr_test_db.a3'])
        if no_c2:
            self.assertTrue('attr_test_db.v.' + c2 not in attrs)
        else:
            self.assertEqual(attrs['attr_test_db.v.' + c2], ['attr_test_db.a2'])

        conn.execute_ddl("alter table %s.base_table drop column attribute c1 %s.a3"\
              % (db, db))

    def test_cascade_cases(self):
        db = 'attr_test_db'
        with context().connect() as conn:
            conn.execute_ddl("create attribute if not exists %s.a1" % db)
            conn.execute_ddl("create attribute if not exists %s.a2" % db)
            conn.execute_ddl("create attribute if not exists %s.a3" % db)

            conn.execute_ddl("drop database if exists %s cascade" % db)
            conn.execute_ddl("create database if not exists %s" % db)

            # Create base table and intermediate view
            conn.execute_ddl(("create table %s.base_table " +
                "(c1 int attribute %s.a1, c2 int attribute %s.a2)") % (db, db, db))
            conn.execute_ddl(
                "create view %s.base_view as select * from %s.base_table" % (db, db))

            ds = conn.list_datasets(db, name='base_table')[0]
            attrs = self._collect_column_attributes(ds)
            self.assertEqual(attrs['attr_test_db.base_table.c1'], ['attr_test_db.a1'])
            self.assertEqual(attrs['attr_test_db.base_table.c2'], ['attr_test_db.a2'])

            self._test_cascade_case(conn, db,
                "create view %s.v as select * from %s.base_table" % (db, db),
                'c1', 'c2')
            self._test_cascade_case(conn, db,
                "create view %s.v as select c1 as c3, c2 as c4 from %s.base_table" % \
                    (db, db),
                'c3', 'c4')
            self._test_cascade_case(conn, db,
                "create view %s.v as select c1 as c2, c2 as c1 from %s.base_table" % \
                    (db, db),
                'c2', 'c1')
            self._test_cascade_case(conn, db,
                ("create view %s.v as select a.c1, b.c2 " +\
                "from %s.base_view a join %s.base_view b") % (db, db, db),
                'c1', 'c2')
            self._test_cascade_case(conn, db,
                "create view %s.v as select c1 + 1 as c1, c2 from %s.base_table" % \
                    (db, db),
                'c1', 'c2', True)
            self._test_cascade_case(conn, db,
                ("create view %s.v as select count(c1) as c1, c2 " +\
                "from %s.base_table group by 2") % (db, db),
                'c1', 'c2', True, True)

if __name__ == "__main__":
    unittest.main()
