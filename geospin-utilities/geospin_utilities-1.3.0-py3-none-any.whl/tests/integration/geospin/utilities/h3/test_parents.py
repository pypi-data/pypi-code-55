import pandas as pd
import pytest

from geospin.utilities.h3 import parents

PROBE_TABLE_NAME = 'probe_table'


@pytest.fixture
def patch_h3_to_parent(monkeypatch):
    def h3_to_parent(h3_address, resolution):
        if resolution == 8:
            d = {
                'aaa': 'aaf',
                'aax': 'aaf',
                'bba': 'bbf',
                'cca': 'ccf',
                'ddc': 'ddf'
            }
        elif resolution == 7:
            d = {
                'aaa': 'aff',
                'aax': 'aff',
                'bba': 'bff',
                'cca': 'cff',
                'ddc': 'dff'
            }
        else:
            raise ValueError('Resolution not defined for h3_to_parent patch!')
        return d[h3_address]

    monkeypatch.setattr(parents.h3, 'h3_to_parent', h3_to_parent)


@pytest.fixture
def patch_h3_get_resolution(monkeypatch):
    def h3_get_resolution(hex_id):
        # The more trailing 'f', the lower the resolution in our simplified test
        if hex_id[-2] == 'ff':
            resolution = 7
        elif hex_id[-1] == 'f':
            resolution = 8
        else:
            resolution = 9
        return resolution

    monkeypatch.setattr(parents.h3, 'h3_get_resolution', h3_get_resolution)


def test_get_mapping_dataframe(patch_h3_to_parent, patch_h3_get_resolution):
    hex_ids_high_resolution = ['aaa', 'cca', 'ddc', 'aax']
    expected = pd.DataFrame(
        data=dict(
            hex_id_resolution_9=hex_ids_high_resolution,
            hex_id_resolution_8=['aaf', 'ccf', 'ddf', 'aaf'],
        )
    )

    h3_parents_ = parents.H3Parents(hex_ids_high_resolution,
                                    parent_resolution=8)
    result = h3_parents_.get_mapping_dataframe()
    pd.testing.assert_frame_equal(expected, result)


@pytest.fixture
def probe_db(postgresql_db):
    with postgresql_db.engine.connect() as conn:
        sql = f"""
        CREATE TABLE {PROBE_TABLE_NAME} (
            hex_id text,
            feature_1 float
        );
        INSERT INTO {PROBE_TABLE_NAME} VALUES ('aaa', 1.);
        INSERT INTO {PROBE_TABLE_NAME} VALUES ('bba', 3.);
        INSERT INTO {PROBE_TABLE_NAME} VALUES ('aax', 5.);

        """
        conn.execute(sql)

    return postgresql_db


@pytest.fixture
def probe_db_with_existing_h3_parents_table(probe_db):
    with probe_db.engine.connect() as conn:
        sql = f"""
        CREATE TABLE hex_id_parents_of_resolution_9 (
            hex_id_resolution_9 text PRIMARY KEY,
            hex_id_resolution_8 text
        );
        INSERT INTO hex_id_parents_of_resolution_9 VALUES ('aaa', 'aaf');
        INSERT INTO hex_id_parents_of_resolution_9 VALUES ('bba', 'bbf');
        INSERT INTO hex_id_parents_of_resolution_9 VALUES ('aax', 'aaf');

        """
        conn.execute(sql)

    return probe_db


def test_create_h3_parents_table(patch_h3_to_parent, patch_h3_get_resolution,
                                 db_backend, probe_db):
    expected = pd.DataFrame(
        data=dict(
            hex_id_resolution_9=['aaa', 'bba', 'aax'],
            hex_id_resolution_8=['aaf', 'bbf', 'aaf'],
        )
    )

    parents.create_h3_parents_table(
        db_backend=db_backend, parent_resolution=8,
        table_with_child_hex_ids=PROBE_TABLE_NAME
    )

    with db_backend.engine.connect() as connection:
        sql = """
        SELECT * FROM hex_id_parents_of_resolution_9;
        """
        result = pd.read_sql_query(sql, connection)

    pd.testing.assert_frame_equal(expected, result)


def test_create_h3_parents_table_if_exists(
        patch_h3_to_parent, patch_h3_get_resolution,
        db_backend, probe_db_with_existing_h3_parents_table):
    with pytest.raises(ValueError):
        parents.create_h3_parents_table(
            db_backend=db_backend, parent_resolution=8,
            table_with_child_hex_ids=PROBE_TABLE_NAME
        )


def test_append_to_h3_parents_table(
        patch_h3_to_parent, patch_h3_get_resolution,
        db_backend, probe_db_with_existing_h3_parents_table):
    expected = pd.DataFrame(
        pd.DataFrame(
            data=dict(
                hex_id_resolution_9=['aaa', 'bba', 'aax'],
                hex_id_resolution_8=['aaf', 'bbf', 'aaf'],
                hex_id_resolution_7=['aff', 'bff', 'aff'],
            )
        )
    )
    parents.append_to_h3_parents_table(
        db_backend,
        existing_table='hex_id_parents_of_resolution_9',
        child_resolution=9,
        parent_resolution=7)

    with db_backend.engine.connect() as connection:
        sql = """
        SELECT * FROM hex_id_parents_of_resolution_9;
        """
        result = pd.read_sql_query(sql, connection)

    pd.testing.assert_frame_equal(expected, result)
