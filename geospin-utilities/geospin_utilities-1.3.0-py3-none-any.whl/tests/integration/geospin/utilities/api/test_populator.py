"""Tests for the prediction populator module."""

import os
import re

import geopandas as gpd
import mock
import pandas as pd
import pytest
import shapely.wkt
import sqlalchemy
from sqlalchemy.dialects import postgresql

from geospin.utilities.api.populator import Populator, \
    ZipCodePopulator, PredictionPopulator

WKT_FREIBURG_BBOX = ('POLYGON ((7.811232366023555 48.02055134850694, '
                     '7.86753729766418 48.02055134850694, '
                     '7.86753729766418 47.98115369099538, '
                     '7.811232366023555 47.98115369099538, '
                     '7.811232366023555 48.02055134850694))')
ZIP_CODE_FREIBURG = '79106'
PROBE_TABLE_NAME = 'probe_table'


class pytest_regex:
    """Assert that a given string meets some expectations."""

    def __init__(self, pattern, flags=0):
        self._regex = re.compile(pattern, flags)

    def __eq__(self, actual):
        return bool(self._regex.match(actual))

    def __repr__(self):
        return self._regex.pattern

    def contained_in(self, other):
        return bool(re.search(self._regex, other))


@pytest.fixture()
def target_db(postgresql_db):
    table_predictions = sqlalchemy.Table(
        'predictions',
        sqlalchemy.MetaData(postgresql_db.engine),
        sqlalchemy.Column('hex_id', postgresql.TEXT, primary_key=True),
        sqlalchemy.Column('prediction', postgresql.INTEGER)
    )

    table_zip_codes = sqlalchemy.Table(
        'zip_codes',
        sqlalchemy.MetaData(postgresql_db.engine),
        sqlalchemy.Column('zip_code', postgresql.TEXT, primary_key=True),
        sqlalchemy.Column('wkt', postgresql.TEXT),
        sqlalchemy.Column('geojson', postgresql.TEXT),
        sqlalchemy.Column('hex_ids', postgresql.ARRAY(postgresql.TEXT)),
    )

    postgresql_db.create_table(table_predictions, table_zip_codes)

    conn = postgresql_db.engine.connect()
    conn.execute(table_zip_codes.insert(), [
        {'zip_code': '79101', 'wkt': 'POLYGON((10, 10))', 'geojson': 'dummy',
         'hex_ids': ['row0', 'row1']},
    ])

    conn.execute(table_predictions.insert(), [
        {'hex_id': 'row0', 'prediction': 1},
        {'hex_id': 'row1', 'prediction': 3},
    ])

    return postgresql_db


@pytest.fixture()
def empty_target_db(postgresql_db):
    return postgresql_db


@pytest.fixture()
def probe_db(postgresql_db):
    table = sqlalchemy.Table(
        PROBE_TABLE_NAME,
        sqlalchemy.MetaData(postgresql_db.engine),
        sqlalchemy.Column('hex_id', sqlalchemy.Text, primary_key=True),
        sqlalchemy.Column('feature_1', sqlalchemy.Integer),
        sqlalchemy.Column('another_feature', sqlalchemy.Integer)
    )

    # Pass a variable amount of tables to create
    postgresql_db.create_table(table)

    conn = postgresql_db.engine.connect()
    conn.execute(table.insert(), [
        {'hex_id': 'row0', 'feature_1': 1, 'another_feature': 0},
        {'hex_id': 'row1', 'feature_1': 3, 'another_feature': 2},
        {'hex_id': 'row2', 'feature_1': 5, 'another_feature': 4},
        {'hex_id': 'row3', 'feature_1': 7, 'another_feature': 6},
        {'hex_id': 'row4', 'feature_1': 9, 'another_feature': 8},
    ])
    return postgresql_db


@pytest.fixture()
def non_consecutive_temp_folder(tmpdir):
    temp_folder = tmpdir.mkdir('test_folder')
    f = temp_folder.join('chunk_0000.csv')
    f.write('')
    f = temp_folder.join('chunk_0003.csv')
    f.write('')
    return str(temp_folder)


@pytest.fixture()
def consecutive_temp_folder(tmpdir):
    temp_folder = tmpdir.mkdir('test_folder')
    f = temp_folder.join('chunk_0000.csv')
    f.write('hex_id,prediction\nrow0,0\nrow1,10\n')
    f = temp_folder.join('chunk_0001.csv')
    f.write('hex_id,prediction\nrow2,20\nrow3,30\n')
    return str(temp_folder)


@pytest.fixture()
def empty_temp_folder(tmpdir):
    temp_folder = tmpdir.mkdir('test_folder')
    return str(temp_folder)


@pytest.fixture()
def messy_temp_folder(tmpdir):
    temp_folder = tmpdir.mkdir('test_folder')
    f = temp_folder.join('chunk_0000.csv')
    f.write('a')
    f = temp_folder.join('chunk_0001.csv')
    f.write('a')
    f = temp_folder.join('other_file.csv')
    f.write('a')
    return str(temp_folder)


@pytest.fixture()
def db_backend(postgresql_db):
    from geospin.utilities.backend import DatabaseBackend

    with mock.patch('geospin.utilities.backend.create_engine') as mock_engine, \
            mock.patch(
                'geospin.utilities.backend.sessionmaker') as mock_factory, \
            mock.patch(
                'geospin.utilities.backend.scoped_session') as mock_session:
        mock_factory.return_value = '<FACTORY>'
        mock_session.return_value = '<SESSION>'
        mock_engine.return_value = postgresql_db.engine

        db = DatabaseBackend(
            user='user', password='pw', host='my.db.host', port=5432,
            database='database')

        db.conn_url = postgresql_db.engine.url
    return db


@pytest.fixture()
def populator(db_backend):
    populator_ = Populator(db_backend)
    return populator_


@pytest.fixture()
def zip_code_populator(db_backend, mock_fetch_latest_zip_code_areas):
    zip_code_populator_ = ZipCodePopulator(db_backend=db_backend)
    return zip_code_populator_


@pytest.fixture()
def prediction_populator(db_backend):
    prediction_populator = PredictionPopulator(predict_function=None,
                                               probe_db_backend=db_backend,
                                               db_backend=db_backend)
    prediction_populator.probe_db_table_name = PROBE_TABLE_NAME
    return prediction_populator


@pytest.fixture()
def mock_fetch_latest_zip_code_areas(monkeypatch):
    gdf = gpd.GeoDataFrame(
        [
            {
                "wkt": shapely.wkt.loads(WKT_FREIBURG_BBOX),
                "zip_code": ZIP_CODE_FREIBURG,
            }
        ],
        crs='epsg:4326',
        geometry='wkt'
    )

    m_zip_codes = mock.MagicMock()
    m_zip_codes.return_value = gdf

    monkeypatch.setattr('geospin.utilities.api.populator.'
                        'fetch_latest_zip_code_areas', m_zip_codes)

    return m_zip_codes


@pytest.fixture()
def mock_safe_make_temp_folder(prediction_populator):
    safe_make_temp_folder_mock = mock.MagicMock()
    safe_make_temp_folder_mock.return_value = (False, -1)
    prediction_populator._safe_make_temp_folder = \
        safe_make_temp_folder_mock
    return safe_make_temp_folder_mock


# TESTS


class TestPopulator:

    def test_dump_db(self, target_db, populator, tmpdir):
        temp_folder = tmpdir.mkdir('dump')
        dump_filename = os.path.join(str(temp_folder), 'test_dump.sql')
        populator.dump_db(dump_filename)

        # Check that the dump file exists
        assert os.path.isfile(dump_filename)

        with open(dump_filename) as file:
            dump_content = file.read()

        # Check that the copy statement for predictions is there
        copy_predictions = ('COPY public.predictions (hex_id, prediction) '
                            'FROM stdin;\n'
                            'row0	1\n'
                            'row1	3')
        assert copy_predictions in dump_content

        # Check that the copy statement for zip_codes is there
        copy_zip_codes = ('COPY public.zip_codes '
                          '(zip_code, wkt, geojson, hex_ids) FROM stdin;\n'
                          '79101	POLYGON((10, 10))	dummy	{row0,row1}')
        assert copy_zip_codes in dump_content


class TestZipCodePopulator:

    def test_fetch_zip_codes(self, zip_code_populator, tmpdir):
        zip_codes_filename = os.path.join(tmpdir.mkdir('data'), 'test.csv')
        zip_code_populator.zip_codes_filename = zip_codes_filename
        zip_codes_df = zip_code_populator._fetch_zip_codes_from_url()
        zip_codes_reloaded_df = zip_code_populator._fetch_zip_codes_from_file()

        # Check that reload delivers the same result
        pd.testing.assert_frame_equal(zip_codes_df, zip_codes_reloaded_df)

        # check dtypes
        assert pd.api.types.is_string_dtype(zip_codes_df['zip_code'])
        assert pd.api.types.is_string_dtype(zip_codes_df['geojson'])
        assert pd.api.types.is_string_dtype(zip_codes_df['wkt'])
        assert pd.api.types.is_array_like(zip_codes_df['hex_ids'])

        # check that there is at least one hex_id
        assert len(zip_codes_df['hex_ids'].iloc[0]) >= 1

    def test_execute_empty_db(self, empty_target_db, zip_code_populator):
        zip_code_populator.execute()

        # Check that a table was created
        assert empty_target_db.has_table('zip_codes')

        with empty_target_db.engine.connect() as conn:
            # Check that the found WKT is the expected one
            result_wkt = conn.execute(
                'SELECT wkt FROM zip_codes').fetchall()
            expected_wkt = WKT_FREIBURG_BBOX
            assert result_wkt[0][0] == expected_wkt

            # Check the number of rows is exactly one
            assert len(result_wkt) == 1

            # Check that the found zip code is the expected one
            result_zip_code = conn.execute(
                'SELECT zip_code FROM zip_codes').fetchall()
            expected_zip_code = ZIP_CODE_FREIBURG
            assert result_zip_code[0][0] == expected_zip_code

    def test_execute_existing_db(self, target_db, zip_code_populator):
        zip_code_populator.execute()

        # Check there is still a table
        assert target_db.has_table('zip_codes')

        with target_db.engine.connect() as conn:
            # Check that the found WKT was overwritten
            result_wkt = conn.execute(
                'SELECT wkt FROM zip_codes').fetchall()
            expected_wkt = WKT_FREIBURG_BBOX
            assert result_wkt[0][0] == expected_wkt

            # Check the number of rows is exactly one
            assert len(result_wkt) == 1

            # Check that the found zip code was overwritten
            result_zip_code = conn.execute(
                'SELECT zip_code FROM zip_codes').fetchall()
            expected_zip_code = ZIP_CODE_FREIBURG
            assert result_zip_code[0][0] == expected_zip_code


class TestPredictionPopulator:

    def test_get_sorted_chunk_idxs(self, consecutive_temp_folder,
                                   prediction_populator):
        prediction_populator.temp_folder = consecutive_temp_folder
        result = prediction_populator._get_sorted_chunk_idxs()
        expected = [0, 1]

        assert result == expected

    @pytest.mark.parametrize(
        "list_, expected",
        [([0, 1], True),
         ([0], True),
         ([0, 3], False),
         ([0, 0], False),
         ([1, 2], False),
         ([], False)]
    )
    def test_is_continuous_from_zero(self, prediction_populator, list_,
                                     expected):
        result = \
            prediction_populator._is_integer_list_continuous_from_zero(list_)
        assert result == expected

    def test_get_last_hex_id(self, prediction_populator,
                             consecutive_temp_folder):
        prediction_populator.temp_folder = consecutive_temp_folder
        result = prediction_populator._get_last_hex_id()
        assert result == 'row3'

    def test_safe_make_temp_folder_non_consecutive(self, prediction_populator,
                                                   non_consecutive_temp_folder):
        prediction_populator.temp_folder = non_consecutive_temp_folder
        with pytest.raises(IOError):
            prediction_populator._safe_make_temp_folder()

    def test_safe_make_temp_folder_messy(self, prediction_populator,
                                         messy_temp_folder):
        prediction_populator.temp_folder = messy_temp_folder
        with pytest.raises(IOError):
            prediction_populator._safe_make_temp_folder()

    @pytest.mark.parametrize(
        "chunk_size, chunk_offset, expected",
        [
            (10000, False, pytest_regex(
                r'SELECT [*] FROM \w+ ORDER BY hex_id ASC$')),
            (10000, 'row1', pytest_regex(
                (r"SELECT [*] FROM \w+ "
                 r"WHERE hex_id > 'row1' ORDER BY hex_id ASC$"))),
            (10000, 'row2', pytest_regex(
                (r"SELECT [*] FROM \w+ "
                 r"WHERE hex_id > 'row2' ORDER BY hex_id ASC$"))),
        ]
    )
    def test_get_probe_query_statement(self, prediction_populator, chunk_size,
                                       chunk_offset, expected):
        result = prediction_populator._get_probe_query_statement(chunk_size,
                                                                 chunk_offset)

        assert expected == result

    def test_make_temp_folder_non_consecutive(self,
                                              prediction_populator,
                                              non_consecutive_temp_folder):
        prediction_populator.temp_folder = non_consecutive_temp_folder
        with pytest.raises(IOError):
            prediction_populator._safe_make_temp_folder()

    def test_make_temp_folder_resume(self,
                                     prediction_populator,
                                     consecutive_temp_folder):
        prediction_populator.temp_folder = consecutive_temp_folder
        result_hex_id, result_chunk_id = \
            prediction_populator._safe_make_temp_folder()
        expected_hex_id = 'row3'
        expected_chunk_id = 1

        assert result_hex_id == expected_hex_id
        assert result_chunk_id == expected_chunk_id

    @mock.patch('os.makedirs', return_value=True)
    def test_make_temp_folder(self, mock_osmakedirs, prediction_populator):
        mkdir = mock.Mock()

        def update_status(name, mode=None, exist_ok=None):
            mkdir(name)

        mock_osmakedirs.side_effect = update_status

        result_hex_id, result_chunk_id = \
            prediction_populator._safe_make_temp_folder()
        expected_hex_id = False
        expected_chunk_id = -1

        assert result_chunk_id == expected_chunk_id
        assert result_hex_id == expected_hex_id
        mkdir.assert_called_with(prediction_populator.temp_folder)

    def test_get_chunk_files_consecutive(self, prediction_populator,
                                         consecutive_temp_folder):
        prediction_populator.temp_folder = consecutive_temp_folder
        chunk_filenames = prediction_populator._get_chunk_filenames()
        expected = ['chunk_0000.csv', 'chunk_0001.csv']

        assert sorted(chunk_filenames) == sorted(expected)

    def test_get_chunk_files_messy(self, prediction_populator,
                                   messy_temp_folder):
        prediction_populator.temp_folder = messy_temp_folder
        chunk_filenames = prediction_populator._get_chunk_filenames()
        expected = ['chunk_0000.csv', 'chunk_0001.csv']

        assert sorted(chunk_filenames) == sorted(expected)

    def test_contains_only_chunk_files_consecutive(self, prediction_populator,
                                                   consecutive_temp_folder):
        prediction_populator.temp_folder = consecutive_temp_folder
        result = prediction_populator._contains_only_chunk_files()

        assert result

    def test_contains_only_chunk_files_messy(self, prediction_populator,
                                             messy_temp_folder):
        prediction_populator.temp_folder = messy_temp_folder
        result = prediction_populator._contains_only_chunk_files()

        assert not result

    def test_contains_only_chunk_files_empty(self, prediction_populator,
                                             empty_temp_folder):
        prediction_populator.temp_folder = empty_temp_folder
        result = prediction_populator._contains_only_chunk_files()

        assert result

    @pytest.mark.parametrize(
        "filename, expected",
        [('chunk_0000.csv', 0),
         ('chunk_1000.csv', 1000)]
    )
    def test_chunk_filename_to_idx(self, prediction_populator, filename,
                                   expected):
        assert prediction_populator._chunk_filename_to_idx(filename) == expected

    @pytest.mark.parametrize(
        "filename",
        [(''),
         ('chunk_11000.csv'),
         ('chunk_110.csv')]
    )
    def test_chunk_filename_to_idx_wrong_format(self, prediction_populator,
                                                filename):
        with pytest.raises(ValueError):
            prediction_populator._chunk_filename_to_idx(filename)

    def test_process_chunk(self, prediction_populator, empty_temp_folder):
        chunk = [('row0', 1, 3), ('row1', 0, 2)]
        column_names = ['hex_id', 'feature_1', 'another_feature']
        chunk_idx = 0

        expected_filename = 'chunk_0000.csv'
        expected_content = 'hex_id,prediction\nrow0,1\nrow1,0\n'

        prediction_populator.temp_folder = empty_temp_folder
        prediction_populator.predict_function = lambda x: x.iloc[:, 0].values

        prediction_populator._process_chunk(chunk, chunk_idx, column_names)

        assert os.listdir(empty_temp_folder) == [expected_filename]

        with open(os.path.join(empty_temp_folder, expected_filename), 'r') as f:
            assert f.read() == expected_content

    def test_execute_in_chunks(self, probe_db, prediction_populator,
                               empty_temp_folder, postgresql_db,
                               mock_safe_make_temp_folder):
        expected_table_content = [('row0', 1),
                                  ('row1', 3),
                                  ('row2', 5),
                                  ('row3', 7),
                                  ('row4', 9)]

        prediction_populator.temp_folder = empty_temp_folder
        prediction_populator._load_model = mock.MagicMock()
        prediction_populator.predict_function = \
            lambda x: x.loc[:, 'feature_1'].values

        assert os.path.exists(empty_temp_folder)
        prediction_populator.execute_in_chunks(2)

        assert postgresql_db.has_table('predictions')
        # check that the temp folder was removed
        assert not os.path.exists(empty_temp_folder)

        with postgresql_db.engine.connect() as conn:
            result = conn.execute(
                'SELECT * FROM predictions LIMIT 10').fetchall()
            assert result == expected_table_content

    def test_execute_in_chunks_resume(self, probe_db, prediction_populator,
                                      consecutive_temp_folder, postgresql_db):
        expected_table_content = [('row0', 0),
                                  ('row1', 10),
                                  ('row2', 20),
                                  ('row3', 30),
                                  ('row4', 9)]

        prediction_populator.temp_folder = consecutive_temp_folder
        prediction_populator._load_model = mock.MagicMock()
        prediction_populator.predict_function = \
            lambda x: x.loc[:, 'feature_1'].values

        prediction_populator.execute_in_chunks(2)

        assert postgresql_db.has_table('predictions')
        with postgresql_db.engine.connect() as conn:
            result = conn.execute(
                'SELECT * FROM predictions LIMIT 10').fetchall()
            assert result == expected_table_content
