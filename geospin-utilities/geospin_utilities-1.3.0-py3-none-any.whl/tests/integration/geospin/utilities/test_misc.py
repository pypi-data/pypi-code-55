import os
import zipfile

import mock
import pytest

from shapely.geometry import Point, Polygon, mapping
import fiona


_PLZ_GEBIETE_FILES = [
    'plz-gebiete.shp', 'plz-gebiete.shx', 'plz-gebiete.dbf', 'plz-gebiete.cpg']
POLYGON_1 = Polygon([[0, 0], [1, 0], [1, 1], [0, 1]])
ZIP_CODE_1 = '01234'
POLYGON_2 = Polygon([[5, 5], [10, 5], [10, 10], [5, 10]])
ZIP_CODE_2 = '01010'


@pytest.fixture()
def tmp_data_dir(tmpdir):
    """Creates a temporal data dir."""
    data_dir = tmpdir.mkdir('test_tmp')

    return data_dir


@pytest.fixture()
def tmp_shapefile(tmp_data_dir):
    """Creates a shapefile including the POLYGON_1 + _2

    There will be two elements in the shapefile with
        geometry: POLYGON_1, POLYGON_2
        properties: {'plz': ZIP_CODE_1, 'note': 'dummy note'},
            {'plz': ZIP_CODE_2, 'note': 'dummy note'}
    """
    # Define a polygon feature geometry with one attribute
    schema = {
        'geometry': 'Polygon',
        'properties': {'plz': 'str', 'note': 'str'},
    }
    shp_file = tmp_data_dir.join("plz-gebiete.shp")
    # Write a new Shapefile
    with fiona.open(str(shp_file), 'w', 'ESRI Shapefile', schema=schema) as c:
        c.write({
            'geometry': mapping(POLYGON_1),
            'properties': {'plz': ZIP_CODE_1, 'note': 'dummy note'},
        })
        c.write({
            'geometry': mapping(POLYGON_2),
            'properties': {'plz': ZIP_CODE_2, 'note': 'dummy note'},
        })

    return shp_file


@pytest.fixture()
def tmp_zipped_shapefile(tmp_data_dir, tmp_shapefile):
    """Creates a zipped shapefile from the tmp_shapefile

    """
    zip_file = tmp_data_dir.join("plz-gebiete.shp.zip")

    with zipfile.ZipFile(str(zip_file), 'w') as z:
        for filename in _PLZ_GEBIETE_FILES:
            z.write(os.path.join(str(tmp_data_dir), filename), filename)

    return zip_file


@pytest.fixture()
def mock_requests(monkeypatch):
    m_requests = mock.MagicMock()

    monkeypatch.setattr(
        'geospin.utilities.misc.requests',
        m_requests)
    return m_requests


def test_rectangular_cells():
    bounds = 7.64, 47.95, 7.66, 47.97
    from geospin.utilities.misc import rectangular_cells
    result = list(rectangular_cells(bounds, 3, 3))
    assert len(result) == 9


def test_create_grid():
    polygon = 'POLYGON ((7.66 47.96, 7.65 47.95, 7.64 47.97, 7.66 47.96))'
    from geospin.utilities.misc import create_grid
    result = create_grid(polygon, wkt=False)
    assert isinstance(list(result)[0], Point)
    result = create_grid(polygon, wkt=True)
    assert isinstance(list(result)[0], str)


def test_fetch_latest_zip_code_areas(mock_requests, tmp_zipped_shapefile,
                                     tmp_shapefile):
    from geospin.utilities.misc import fetch_latest_zip_code_areas
    content = open(str(tmp_zipped_shapefile), 'rb').read()

    response = mock.MagicMock()
    response.content = content
    mock_requests.get.return_value = response

    result = fetch_latest_zip_code_areas()

    # Check number of rows
    assert len(result) == 2

    # Check number of columns
    assert len(result.columns) == 2

    # Check the column names
    column_names = list(result.columns)
    assert sorted(column_names) == sorted(['zip_code', 'wkt'])

    # Check the zip code values
    assert ZIP_CODE_1 in result['zip_code'].values
    assert ZIP_CODE_2 in result['zip_code'].values

    # Check the wkts for the zip codes
    mask_zip_code_1 = result['zip_code'] == ZIP_CODE_1
    mask_zip_code_2 = result['zip_code'] == ZIP_CODE_2
    assert result.loc[mask_zip_code_1, 'wkt'].values[0].equals(POLYGON_1)
    assert result.loc[mask_zip_code_2, 'wkt'].values[0].equals(POLYGON_2)
