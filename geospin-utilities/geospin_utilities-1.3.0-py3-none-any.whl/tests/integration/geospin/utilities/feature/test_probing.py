"""Contains tests for the probing module."""

import mock
import pandas as pd
import pytest

from geospin.utilities.feature import probing

PROBE_TABLE_NAME = 'probe_table'


@pytest.fixture()
def probe_db(postgresql_db):
    with postgresql_db.engine.connect() as conn:
        sql = f"""
        CREATE TABLE {PROBE_TABLE_NAME} (
            hex_id varchar(80),
            feature_1 integer,
            another_feature integer
        );
        INSERT INTO {PROBE_TABLE_NAME} VALUES ('row0', 1, 0);
        INSERT INTO {PROBE_TABLE_NAME} VALUES ('row1', 3, 2);
        INSERT INTO {PROBE_TABLE_NAME} VALUES ('row2', 5, 4);
        INSERT INTO {PROBE_TABLE_NAME} VALUES ('row3', 7, 6);
        INSERT INTO {PROBE_TABLE_NAME} VALUES ('row4', 9, 8);
        """
        conn.execute(sql)


@pytest.fixture()
def mock_engine(monkeypatch, postgresql_db):
    m_engine = mock.MagicMock()
    m_engine.return_value = postgresql_db.engine

    monkeypatch.setattr(
        'geospin.utilities.backend.create_engine', m_engine)
    return m_engine


def test_get_probed_features_from_database(probe_db, mock_engine):
    hex_ids = ['row0', 'row1']
    probe_feature_df = probing.fetch_probed_features_for_hex_ids(
        hex_ids, 'user', 'password', db_table=PROBE_TABLE_NAME)

    expected_df = pd.DataFrame(
        index=['row0', 'row1'],
        data={'feature_1': [1, 3],
              'another_feature': [0, 2]}
    )
    expected_df.index.name = 'hex_id'
    pd.testing.assert_frame_equal(probe_feature_df, expected_df)


def test_transform_hex_id_list_to_sql_string_raises_when_empty():
    with pytest.raises(ValueError):
        probing.transform_hex_id_list_to_sql_string(hex_ids=[])


def test_transform_hex_id_list_to_sql_string_one_hex_id():
    result = probing.transform_hex_id_list_to_sql_string(hex_ids=['a'])
    assert "('a')" == result


def test_transform_hex_id_list_to_sql_string_many_hex_ids():
    result = probing.transform_hex_id_list_to_sql_string(
        hex_ids=['a', 'b', 'c'])
    assert "('a', 'b', 'c')" == result


def test_fetch_probed_features_for_hex_ids_duplicate_ids(probe_db, mock_engine):
    hex_ids = ['row0', 'row1', 'row0']
    probe_feature_df = probing.fetch_probed_features_for_hex_ids(
        hex_ids, 'user', 'password', db_table=PROBE_TABLE_NAME)

    expected_df = pd.DataFrame(
        index=['row0', 'row1'],
        data={'feature_1': [1, 3],
              'another_feature': [0, 2]}
    )
    expected_df.index.name = 'hex_id'
    pd.testing.assert_frame_equal(probe_feature_df, expected_df)
