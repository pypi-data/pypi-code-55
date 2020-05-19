import csv

import numpy as np
import pandas as pd
import pytest

from geospin.utilities.feature import addition

PROBE_TABLE_NAME = 'probe_table'


@pytest.fixture
def probe_db(postgresql_db):
    with postgresql_db.engine.connect() as conn:
        sql = f"""
        CREATE TABLE {PROBE_TABLE_NAME} (
            hex_id varchar(80),
            feature_1 float,
            feature_2 float
        );
        INSERT INTO {PROBE_TABLE_NAME} VALUES ('b', 1., 0.);
        INSERT INTO {PROBE_TABLE_NAME} VALUES ('c', 3., 2.);
        """
        conn.execute(sql)

    return postgresql_db


@pytest.fixture
def probe_db_with_unique_constraint(postgresql_db):
    with postgresql_db.engine.connect() as conn:
        sql = f"""
        CREATE TABLE {PROBE_TABLE_NAME} (
            hex_id varchar(80),
            feature_1 float,
            feature_2 float
        );
        INSERT INTO {PROBE_TABLE_NAME} VALUES ('b', 1., 0.);
        INSERT INTO {PROBE_TABLE_NAME} VALUES ('c', 3., 2.);

        ALTER TABLE {PROBE_TABLE_NAME}
            ADD CONSTRAINT hex_id_unique UNIQUE (hex_id);
        """
        conn.execute(sql)

    return postgresql_db


@pytest.fixture
def probe_db_with_primary_key(postgresql_db):
    with postgresql_db.engine.connect() as conn:
        sql = f"""
        CREATE TABLE {PROBE_TABLE_NAME} (
            hex_id varchar(80) PRIMARY KEY,
            feature_1 float,
            feature_2 float
        );
        INSERT INTO {PROBE_TABLE_NAME} VALUES ('b', 1., 0.);
        INSERT INTO {PROBE_TABLE_NAME} VALUES ('c', 3., 2.);
        """
        conn.execute(sql)

    return postgresql_db


@pytest.fixture
def path_empty(tmpdir):
    data_dir = tmpdir.mkdir('data')
    path = data_dir.join('file.csv')
    return str(path)


@pytest.fixture
def path_more_columns(path_empty):
    path = path_empty
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow([
            'hex_id', 'feature_1', 'feature_2', 'feature_3'])
        writer.writerow(['d', 5., 6., 8.])

    return str(path)


@pytest.fixture
def path_semicolon_delimiter(path_empty):
    path = path_empty
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['hex_id', 'feature_1', 'feature_2'])
        writer.writerow(['d', 5., 4.])

    return str(path)


@pytest.fixture
def path_less_columns(path_empty):
    path = path_empty
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(['hex_id', 'feature_1'])
        writer.writerow(['d', 5.])

    return str(path)


@pytest.fixture
def path_valid(path_empty):
    path = path_empty
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(['hex_id', 'feature_1', 'feature_2'])
        writer.writerow(['d', 5., 4.])
        writer.writerow(['a', -1., -2.])

    return str(path)


@pytest.fixture
def path_overwrite(path_empty):
    path = path_empty
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(['hex_id', 'feature_1', 'feature_2'])
        writer.writerow(['d', 5., 4.])
        writer.writerow(['b', 13., 12.])

    return str(path)


@pytest.fixture
def path_different_column_order(path_empty):
    path = path_empty
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(['feature_2', 'hex_id', 'feature_1'])
        writer.writerow([4., 'd', 5.])
        writer.writerow([12., 'b', 13.])
        writer.writerow([-2., 'a', -1.])

    return str(path)


@pytest.fixture
def path_duplicates(path_empty):
    path = path_empty
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(['hex_id', 'feature_1', 'feature_2'])
        writer.writerow(['d', 7., 6.])
        writer.writerow(['a', -1., -2.])
        writer.writerow(['a', -1., -2.])
        writer.writerow(['d', 5., 4.])

    return str(path)


def test_get_column_names_in_file(path_more_columns):
    file_copier = addition.FileCopier(db_backend=None, path=path_more_columns)
    columns = file_copier._get_column_names_in_file()
    assert columns == ['hex_id', 'feature_1', 'feature_2', 'feature_3']


def test_append_rows_from_file_to_table_raise_if_file_contains_more_columns(
        probe_db, db_backend, path_more_columns):
    with pytest.raises(ValueError,
                       match='File contains columns that are not in table'):
        file_copier = addition.FileCopier(db_backend=db_backend,
                                          path=path_more_columns)
        file_copier.append_rows_from_file_to_existing_table(
            table=PROBE_TABLE_NAME)


def test_append_rows_from_file_to_table_raise_if_file_contains_less_columns(
        probe_db, db_backend,
        path_less_columns):
    with pytest.raises(ValueError,
                       match='Table contains columns that are not in file!'):
        file_copier = addition.FileCopier(db_backend=db_backend,
                                          path=path_less_columns)
        file_copier.append_rows_from_file_to_existing_table(
            table=PROBE_TABLE_NAME)


def test_append_rows_from_file_to_table(probe_db, db_backend, path_valid):
    sql = f"SELECT * FROM {PROBE_TABLE_NAME};"

    # ---- Before copy ----
    expected_before_copy = pd.DataFrame(
        index=['b', 'c'],
        data=dict(
            feature_1=[1., 3.],
            feature_2=[0., 2.],
        )
    )
    expected_before_copy.index.name = 'hex_id'

    with probe_db.engine.connect() as conn:
        result_before_copy = pd.read_sql_query(sql, conn, index_col='hex_id')

    pd.testing.assert_frame_equal(expected_before_copy, result_before_copy)

    # ---- Copy ----
    file_copier = addition.FileCopier(db_backend,
                                      path=path_valid)
    file_copier.append_rows_from_file_to_existing_table(table=PROBE_TABLE_NAME)

    # ---- After copy ----
    expected_after_copy = pd.DataFrame(
        index=['a', 'b', 'c', 'd'],
        data=dict(
            feature_1=[-1., 1., 3., 5.],
            feature_2=[-2., 0., 2., 4.],
        )
    )
    expected_after_copy.index.name = 'hex_id'

    with probe_db.engine.connect() as conn:
        result_after_copy = pd.read_sql_query(sql, conn, index_col='hex_id')

    pd.testing.assert_frame_equal(expected_after_copy, result_after_copy,
                                  check_like=True)


def test_append_rows_from_file_to_table_no_overwrite(probe_db, db_backend,
                                                     path_overwrite):
    sql = f"SELECT * FROM {PROBE_TABLE_NAME};"

    file_copier = addition.FileCopier(db_backend,
                                      path=path_overwrite)
    file_copier.append_rows_from_file_to_existing_table(table=PROBE_TABLE_NAME)

    expected = pd.DataFrame(
        index=['b', 'c', 'd'],
        data=dict(
            feature_1=[1., 3., 5.],
            feature_2=[0., 2., 4.],
        )
    )
    expected.index.name = 'hex_id'

    with probe_db.engine.connect() as conn:
        result = pd.read_sql_query(sql, conn, index_col='hex_id')

    pd.testing.assert_frame_equal(expected, result, check_like=True)


def test_append_rows_from_file_to_table_different_delimiter(
        probe_db, db_backend, path_semicolon_delimiter):
    sql = f"SELECT * FROM {PROBE_TABLE_NAME};"

    file_copier = addition.FileCopier(db_backend,
                                      path=path_semicolon_delimiter,
                                      delimiter=';')
    file_copier.append_rows_from_file_to_existing_table(table=PROBE_TABLE_NAME)

    expected = pd.DataFrame(
        index=['b', 'c', 'd'],
        data=dict(
            feature_1=[1., 3., 5.],
            feature_2=[0., 2., 4.],
        )
    )
    expected.index.name = 'hex_id'

    with probe_db.engine.connect() as conn:
        result = pd.read_sql_query(sql, conn, index_col='hex_id')

    pd.testing.assert_frame_equal(expected, result, check_like=True)


def test_append_rows_from_file_to_table_column_order(
        probe_db, db_backend, path_different_column_order):
    sql = f"SELECT * FROM {PROBE_TABLE_NAME};"

    file_copier = addition.FileCopier(db_backend,
                                      path=path_different_column_order)
    file_copier.append_rows_from_file_to_existing_table(table=PROBE_TABLE_NAME)

    expected = pd.DataFrame(
        index=['a', 'b', 'c', 'd'],
        data=dict(
            feature_1=[-1., 1., 3., 5.],
            feature_2=[-2., 0., 2., 4.],
        )
    )
    expected.index.name = 'hex_id'

    with probe_db.engine.connect() as conn:
        result = pd.read_sql_query(sql, conn, index_col='hex_id')

    pd.testing.assert_frame_equal(expected, result, check_like=True)


def test_append_rows_from_file_to_table_duplicates_in_file(
        probe_db, db_backend, path_duplicates):
    sql = f"SELECT * FROM {PROBE_TABLE_NAME};"

    file_copier = addition.FileCopier(db_backend,
                                      path=path_duplicates)
    file_copier.append_rows_from_file_to_existing_table(table=PROBE_TABLE_NAME)

    expected = pd.DataFrame(
        index=['a', 'b', 'c', 'd'],
        data=dict(
            feature_1=[-1., 1., 3., 7.],
            feature_2=[-2., 0., 2., 6.],
        )
    )
    expected.index.name = 'hex_id'

    with probe_db.engine.connect() as conn:
        result = pd.read_sql_query(sql, conn, index_col='hex_id')

    pd.testing.assert_frame_equal(expected, result, check_like=True)


def test_append_rows_from_file_to_table_constraint_already_exists(
        probe_db_with_unique_constraint, db_backend, path_valid):
    sql = f"SELECT * FROM {PROBE_TABLE_NAME};"

    file_copier = addition.FileCopier(db_backend,
                                      path=path_valid)
    file_copier.append_rows_from_file_to_existing_table(table=PROBE_TABLE_NAME)

    expected = pd.DataFrame(
        index=['a', 'b', 'c', 'd'],
        data=dict(
            feature_1=[-1., 1., 3., 5.],
            feature_2=[-2., 0., 2., 4.],
        )
    )
    expected.index.name = 'hex_id'

    with probe_db_with_unique_constraint.engine.connect() as conn:
        result = pd.read_sql_query(sql, conn, index_col='hex_id')

    pd.testing.assert_frame_equal(expected, result, check_like=True)


def test_append_rows_from_file_to_table_with_primary_key(
        probe_db_with_primary_key, db_backend, path_valid):
    sql = f"SELECT * FROM {PROBE_TABLE_NAME};"

    file_copier = addition.FileCopier(db_backend,
                                      path=path_valid)
    file_copier.append_rows_from_file_to_existing_table(table=PROBE_TABLE_NAME)

    expected = pd.DataFrame(
        index=['a', 'b', 'c', 'd'],
        data=dict(
            feature_1=[-1., 1., 3., 5.],
            feature_2=[-2., 0., 2., 4.],
        )
    )
    expected.index.name = 'hex_id'

    with probe_db_with_primary_key.engine.connect() as conn:
        result = pd.read_sql_query(sql, conn, index_col='hex_id')

    pd.testing.assert_frame_equal(expected, result, check_like=True)


def test_copy_file_into_new_table(probe_db, db_backend, path_valid):
    new_table = 'my_new_table'

    expected = pd.DataFrame(
        data=dict(
            hex_id=['d', 'a'],
            feature_1=[5., -1.],
            feature_2=[4., -2.],
        )
    )

    copier = addition.FileCopier(db_backend, path=path_valid)
    copier.copy_file_into_new_table(table=new_table)

    sql = f"SELECT * FROM {new_table};"
    with probe_db.engine.connect() as conn:
        result = pd.read_sql_query(sql, conn)

    pd.testing.assert_frame_equal(expected, result)


def test_copy_file_into_new_table_column_subset(probe_db, db_backend,
                                                path_valid):
    new_table = 'my_new_table'

    expected = pd.DataFrame(
        data=dict(
            feature_1=[5., -1.],
        )
    )

    copier = addition.FileCopier(db_backend, path=path_valid)
    copier.copy_file_into_new_table(table=new_table, columns=['feature_1'])

    sql = f"SELECT * FROM {new_table};"
    with probe_db.engine.connect() as conn:
        result = pd.read_sql_query(sql, conn)

    pd.testing.assert_frame_equal(expected, result)


@pytest.fixture
def probe_db_to_test_view_creator(postgresql_db):
    with postgresql_db.engine.connect() as conn:
        sql = """
        CREATE TABLE imo0001_prices (
            hex_id varchar(80),
            imo0001_price float,
            imo0001_price_2014 float
        );
        INSERT INTO imo0001_prices
            VALUES ('af', 110.0, 100.0);
        INSERT INTO imo0001_prices
            VALUES ('bf', 220.0, 200.0);
        """
        conn.execute(sql)

        sql = """
        CREATE TABLE hex_id_parents (
            hex_id_resolution_9 varchar(80),
            hex_id_resolution_8 varchar(80)
        );
        INSERT INTO hex_id_parents VALUES ('aa', 'af');
        INSERT INTO hex_id_parents VALUES ('bb', 'bf');
        INSERT INTO hex_id_parents VALUES ('cc', 'cf');
        INSERT INTO hex_id_parents VALUES ('ab', 'af');
        """
        conn.execute(sql)

    return postgresql_db


def test_view_creator(db_backend, probe_db_to_test_view_creator):
    expected = pd.DataFrame(
        index=['aa', 'bb', 'cc', 'ab'],
        data=dict(
            imo0001_price=[110., 220., np.nan, 110.],
            imo0001_price_2014=[100., 200., np.nan, 100.]
        )
    )
    expected.index.name = 'hex_id'

    sql = """
    SELECT * FROM imo0001_prices_resolution_9
    """
    creator = addition.ViewCreator(
        db_backend,
        feature_table='imo0001_prices',
        hex_id_parents_table='hex_id_parents'
    )
    creator.create()

    with probe_db_to_test_view_creator.engine.connect() as connection:
        result = pd.read_sql(sql, connection, index_col='hex_id')

    pd.testing.assert_frame_equal(expected, result, check_like=True)


def test_list2string():
    my_list = ['col1', 'col2']
    expected = 'col1, col2'
    result = addition._list2string(my_list)
    assert expected == result
