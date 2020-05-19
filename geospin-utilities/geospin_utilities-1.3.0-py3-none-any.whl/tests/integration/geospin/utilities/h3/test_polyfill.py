try:
    import h3

    h3.k_ring('841e265ffffffff', 4)
except AttributeError:
    from h3 import h3

import geopandas as gpd
import geopandas.testing
import mock
import numpy as np
import pytest
import shapely.geometry
from pyproj import Proj, Transformer
from shapely import wkt
from shapely.geometry import box, Point, Polygon, mapping, MultiPolygon, shape
from shapely.ops import transform

import geospin.utilities.h3.polyfill as polyfill
import geospin.utilities.tiling as tiling

EDGE_LENGTH_IN_DEGREES = 1e-6
EARTH_RADIUS_IN_METERS = 6378137
CENTER = ['0,0']
FIRST_RING = ['1,0', '1,-1', '0,-1', '-1,0', '-1,1', '0,1']
SECOND_RING = ['2,0', '2,-1', '2,-2', '1,-2', '0,-2', '-1,-1', '-2,0',
               '-2,1', '-2,2', '-1,2', '0,2', '1,1']


def assert_geometries_almost_equal(geometry, other_geometry,
                                   tolerated_deviation=0.01):
    """ Compare two geometries for equality.

    Fails if the area of the symmetric difference between
    the given geometries exceeds the tolerated deviation. To this end,
    the area of the symmetric difference is compared to the smaller geometry.

    :param shapely.geometry.Base geometry: First geometry to compare.
    :param shapely.geometry.Base other_geometry: Second geometry to compare.
    :param tolerated_deviation: The tolerated area deviation as fraction.
    """
    area_symmetric_diff = geometry.symmetric_difference(other_geometry).area
    area_deviation = area_symmetric_diff / min(geometry.area,
                                               other_geometry.area)
    assert area_deviation < tolerated_deviation


def approximate_meters2degrees(x):
    radians = x / EARTH_RADIUS_IN_METERS
    return np.rad2deg(radians)


def approximate_degrees2meters(a):
    radians = np.deg2rad(a)
    return EARTH_RADIUS_IN_METERS * radians


@pytest.fixture
def db_backend(postgresql_db):
    from geospin.utilities.backend import DatabaseBackend

    with mock.patch(
            'geospin.utilities.backend.create_engine') as mock_engine, \
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
def osm_db(postgresql_db):
    with postgresql_db.engine.connect() as conn:
        sql = """
        CREATE EXTENSION IF NOT EXISTS postgis;
        CREATE EXTENSION IF NOT EXISTS hstore;
        CREATE TABLE planet_osm_line (
            access varchar,
            highway varchar,
            osm_id int,
            part_of_network boolean,
            tags hstore,
            way geometry
        );
        INSERT INTO planet_osm_line VALUES
            ('vehicle', 'primary', 0, TRUE, NULL,
                ST_Transform(
                    ST_GeomFromText(
                        'LINESTRING(10.0 40.0, 10.01 40.01, 10.02 40.02)',
                        4326),
                    3857)
            ),
            ('yes', 'any', 1, TRUE, NULL,
                ST_Transform(
                    ST_GeomFromText(
                        'LINESTRING(20.0 50.0, 20.01 50.01, 20.02 50.02)',
                        4326),
                    3857)
            ),
            ('no', 'any', 2, FALSE, NULL,
                ST_Transform(
                    ST_GeomFromText(
                        'LINESTRING(-10.0 40.0, -10.01 40.01, -10.02 40.02)',
                        4326),
                    3857)
            ),
            ('no', 'other', 3, FALSE, NULL,
                ST_Transform(
                    ST_GeomFromText(
                        'LINESTRING(-15.0 50.0, -15.01 50.01, -15.02 50.02)',
                        4326),
                    3857)
            );
        CREATE TABLE road_network_table (
            geom geometry
        );
        INSERT INTO road_network_table VALUES
            (ST_GeomFromText('LINESTRING(10.0 40.0, 10.01 40.01, 10.02 40.02)',
                            4326)
            ),
            (ST_GeomFromText('LINESTRING(20.0 50.0, 20.01 50.01, 20.02 50.02)',
                            4326)
            );
        CREATE VIEW road_network AS (
            SELECT * FROM road_network_table
        );
        """
        conn.execute(sql)

    return postgresql_db


@pytest.fixture()
def road_network_polyfiller(osm_db, db_backend):
    buffer_size = 100
    resolution = 6
    polyfiller = polyfill.RoadNetworkPolyFiller(
        db_backend, buffer_size, resolution, chunk_resolution=4)
    return polyfiller


@pytest.fixture
def patch_h3_polyfill(monkeypatch):
    """Patch H3 polyfill, using custom idealized tiling"""
    tiling_ = tiling.Tiling(n_rings=10, edge_length=EDGE_LENGTH_IN_DEGREES)

    def mock_polyfill(geo_json, res, geo_json_conformant):
        geometry = shapely.geometry.asShape(geo_json)
        return tiling_.get_ids_of_hexagons_with_center_inside_geometry(geometry)

    monkeypatch.setattr(polyfill.h3, 'polyfill', mock_polyfill)


@pytest.fixture
def patch_h3_edge_length(monkeypatch):
    """Patch H3 edge_length using approximation at lat=0, lon=0."""

    def mock_edge_length(resolution, unit):
        if unit == 'm':
            return approximate_degrees2meters(EDGE_LENGTH_IN_DEGREES)
        else:
            raise ValueError('Mock requires unit in meters')

    monkeypatch.setattr(polyfill.h3, 'edge_length', mock_edge_length)


class TestPolyFiller:

    def test_fill_wkt(self):
        # Example extracted from the original h3 test set:
        # https://github.com/uber/h3-py/blob/master/tests/test_h3.py

        polygon_wkt = ('POLYGON ((-122.4089866999972145 37.813318999983238, '
                       '-122.3805436999997056 37.7866302000007224, '
                       '-122.3544736999993603 37.7198061999978478, '
                       '-122.5123436999983966 37.7076131999975672, '
                       '-122.5247187000021967 37.7835871999971715, '
                       '-122.4798767000009008 37.8151571999998453, '
                       '-122.4089866999972145 37.813318999983238))')

        poly_filler = polyfill.PolyFiller(resolution=9,
                                          add_hex_id_if='center_contained',
                                          source_crs='epsg:4326',
                                          buffer_crs='epsg:3395')
        result_unbuffered = poly_filler.fill(polygon_wkt)

        poly_filler = polyfill.PolyFiller(resolution=9,
                                          add_hex_id_if='center_within_buffer',
                                          source_crs='epsg:4326',
                                          buffer_crs='epsg:3395')
        result_buffered = poly_filler.fill(polygon_wkt)

        assert len(result_unbuffered) > 1000
        assert len(result_buffered) > len(result_unbuffered)

        polygon_wkt = (
            'MULTIPOLYGON (((-122.4089866999972145 37.813318999983238, '
            '-122.3805436999997056 37.7866302000007224, '
            '-122.3544736999993603 37.7198061999978478, '
            '-122.5123436999983966 37.7076131999975672, '
            '-122.5247187000021967 37.7835871999971715, '
            '-122.4798767000009008 37.8151571999998453, '
            '-122.4089866999972145 37.813318999983238)),'
            '((-122.48787523396457 37.70594418834231, '
            '-122.40238786824192 37.715450392685575, '
            '-122.39964128621067 37.6814940637173, '
            '-122.49130846150364 37.682852615477586, '
            '-122.48787523396457 37.70594418834231)))')

        poly_filler = polyfill.PolyFiller(resolution=9,
                                          add_hex_id_if='center_contained',
                                          source_crs='epsg:4326',
                                          buffer_crs='epsg:3395')
        result_unbuffered = poly_filler.fill(polygon_wkt)

        assert len(result_unbuffered) > 1000

    @pytest.mark.parametrize(
        "polygon", ['POLYGON ((7.854452133178711 47.991752635640694, '
                    '7.8544628620147705 47.991684424263916, 7.855846881866456 '
                    '47.99178135619341, 7.861538529396057 47.991580311988706, '
                    '7.861549258232116 47.99163775326998, 7.856115102767944 '
                    '47.9918387972509, 7.854452133178711 47.991752635640694))',
                    'POLYGON ((7.858609557151794 47.992248062934756, '
                    '7.858598828315734 47.9921403617537, 7.858781218528748 '
                    '47.99214395179668, 7.858781218528748 47.992248062934756, '
                    '7.858609557151794 47.992248062934756))'])
    def test_buffer(self, polygon):
        poly_filler = polyfill.PolyFiller(
            resolution=9, add_hex_id_if='center_within_buffer',
            source_crs='epsg:4326', buffer_crs='epsg:4839'
        )
        result = poly_filler.fill(polygon)
        assert len(result) > 0

    @pytest.mark.parametrize(
        "center_wkt", ['POINT (7.854452133178711 47.991752635640694)'])
    def test_buffer_center_point(self, center_wkt):
        center = wkt.loads(center_wkt)
        polygon = center.buffer(0.1)

        poly_filler = polyfill.PolyFiller(
            resolution=9, add_hex_id_if='center_within_buffer',
            source_crs='epsg:4326', buffer_crs='epsg:4839'
        )
        result = poly_filler.fill(polygon)
        hexagons_coordinates = h3.h3_set_to_multi_polygon(result, True)
        result_multipolygon = \
            shape({"type": "MultiPolygon", "coordinates": hexagons_coordinates})

        assert len(result) > 0
        assert result_multipolygon.contains(polygon)

    def test_point_reprojection(self):
        from geospin.utilities.h3.polyfill import h3
        source_projection = Proj(init='epsg:4326')
        target_projection = Proj(init='epsg:3035')
        project = Transformer.from_proj(
            source_projection,
            target_projection
        )
        project_inverse = Transformer.from_proj(
            target_projection,
            source_projection
        )

        resolution = 9
        h3_edge_length = h3.edge_length(resolution, unit='m')
        point = Point(7.85222, 47.9959)
        point_reprojected = transform(project.transform, point)

        polygon_reprojected = point_reprojected.buffer(h3_edge_length / 1000.0)
        polygon = transform(project_inverse.transform, polygon_reprojected)

        poly_filler = polyfill.PolyFiller(resolution,
                                          add_hex_id_if='center_within_buffer')
        result = poly_filler.fill(polygon)
        assert len(result) > 0

        poly_filler.add_hex_id_if = 'center_contained'
        result = poly_filler.fill(polygon)
        assert len(result) == 0

    @pytest.mark.parametrize(
        "geometry", [
            'POLYGON ((10. 50., 10. 51., 9. 51., 9. 50., 10. 50.))',
            ('MULTIPOLYGON (((10. 50., 10. 51., 9. 51., 9. 50., 10. 50.)), '
             '((11. 51., 11. 52., 10. 52., 10. 51., 11. 51.)))')
        ])
    def test_get_list_of_polygons_buffered_wkt(self, geometry):
        poly_filler = polyfill.PolyFiller(add_hex_id_if='center_within_buffer')
        result_polygons = poly_filler._get_list_of_polygons_in_geometry(
            geometry)
        expected = wkt.loads(geometry)

        result = shapely.ops.unary_union(result_polygons)
        assert expected.within(result)
        assert not (expected.contains(result))

    def test_get_list_of_polygons_from_wkt_single(self):
        poly_filler = polyfill.PolyFiller(add_hex_id_if='center_contained')
        wkt = 'POLYGON ((10. 50., 10. 51., 9. 51., 9. 50., 10. 50.))'

        expected_polygons = [
            Polygon([(10., 50.), (10., 51.), (9., 51.), (9., 50.), (10., 50.)])
        ]

        result_polygons = poly_filler._get_list_of_polygons_in_geometry(wkt)

        for expected, result in zip(expected_polygons, result_polygons):
            assert expected.equals(result)

    def test_get_list_of_polygons_from_wkt_multi(self):
        poly_filler = polyfill.PolyFiller(add_hex_id_if='center_contained')
        wkt = 'MULTIPOLYGON (((10. 50., 10. 51., 9. 51., 9. 50., 10. 50.)), ' \
              '((11. 51., 11. 52., 10. 52., 10. 51., 11. 51.)))'

        expected_polygons = [
            Polygon([(10., 50.), (10., 51.), (9., 51.), (9., 50.), (10., 50.)]),
            Polygon(
                [(11., 51.), (11., 52.), (10., 52.), (10., 51.), (11., 51.)])
        ]

        result_polygons = poly_filler._get_list_of_polygons_in_geometry(wkt)

        for expected, result in zip(expected_polygons, result_polygons):
            assert expected.equals(result)

    def test_get_list_of_polygons_from_shape_single(self):
        poly_filler = polyfill.PolyFiller(add_hex_id_if='center_contained')
        polygon = Polygon(
            [(1, 0), (1, 1), (0, 1), (0, 0), (1, 0)]
        )

        expected_polygons = [polygon]
        result_polygons = poly_filler._get_list_of_polygons_in_geometry(
            polygon)
        for expected, result in zip(expected_polygons, result_polygons):
            assert expected.equals(result)

    def test_get_list_of_polygons_from_shape_multi(self):
        poly_filler = polyfill.PolyFiller(add_hex_id_if='center_contained')
        poly_1 = Polygon([(1, 0), (1, 1), (0, 1), (0, 0), (1, 0)])
        poly_2 = Polygon([(6, 5), (6, 6), (5, 6), (5, 5), (6, 5)])
        polygon = MultiPolygon([poly_1, poly_2])

        expected_polygons = [poly_1, poly_2]
        result_polygons = poly_filler._get_list_of_polygons_in_geometry(
            polygon)
        for expected, result in zip(expected_polygons, result_polygons):
            assert expected.equals(result)

    def test_get_list_of_polygons_from_geo_json_single(self):
        poly_filler = polyfill.PolyFiller(add_hex_id_if='center_contained')
        geo_json = {'type': 'Polygon',
                    'coordinates': [
                        [
                            [1.0, 0.0], [1.0, 1.0], [0.0, 1.0],
                            [0.0, 0.0], [1.0, 0.0]
                        ],
                    ]}
        expected_polygons = [
            Polygon([(1, 0), (1, 1), (0, 1), (0, 0), (1, 0)])
        ]

        result_polygons = poly_filler._get_list_of_polygons_in_geometry(
            geo_json)

        for expected, result in zip(expected_polygons, result_polygons):
            assert expected.equals(result)

    def test_get_list_of_polygons_from_geo_json_multi(self):
        poly_filler = polyfill.PolyFiller(add_hex_id_if='center_contained')
        geo_json = {'type': 'MultiPolygon',
                    'coordinates': [
                        [[[1.0, 0.0], [1.0, 1.0], [0.0, 1.0],
                          [0.0, 0.0], [1.0, 0.0]]],
                        [[[6.0, 5.0], [6.0, 6.0], [5.0, 6.0],
                          [5.0, 5.0], [6.0, 5.0]]],
                    ]}
        expected_polygons = [
            Polygon([(1, 0), (1, 1), (0, 1), (0, 0), (1, 0)]),
            Polygon([(6, 5), (6, 6), (5, 6), (5, 5), (6, 5)])
        ]

        result_polygons = poly_filler._get_list_of_polygons_in_geometry(
            geo_json)

        for expected, result in zip(expected_polygons, result_polygons):
            assert expected.equals(result)

    def test_fill_returns_no_duplicate_hex_ids(self):
        # Two neighboring hexagons at resolution 9
        hex_id_1 = '891facb6037ffff'
        hex_id_1_boundary = h3.h3_to_geo_boundary(hex_id_1, geo_json=True)
        polygon_hex_id_1 = shapely.geometry.Polygon(hex_id_1_boundary)

        hex_id_2 = '891facb6023ffff'
        hex_id_2_boundary = h3.h3_to_geo_boundary(hex_id_2, geo_json=True)
        polygon_hex_id_2 = shapely.geometry.Polygon(hex_id_2_boundary)

        multipolygon_of_two_hexagons = shapely.geometry.MultiPolygon(
            [polygon_hex_id_1, polygon_hex_id_2])

        poly_filler = polyfill.PolyFiller()
        hex_ids = poly_filler.fill(multipolygon_of_two_hexagons)

        # No duplicates?
        number_of_duplicates = len(hex_ids) - len(set(hex_ids))
        assert number_of_duplicates == 0

    @pytest.mark.parametrize(
        'geometry, expected',
        [
            # Small circle around center
            (Point(0, 0).buffer(0.5 * EDGE_LENGTH_IN_DEGREES),
             CENTER),

            # Circle that contains first ring
            (Point(0, 0).buffer(1.1 * np.sqrt(3) * EDGE_LENGTH_IN_DEGREES),
             CENTER + FIRST_RING)
        ]
    )
    def test_without_buffer(self, patch_h3_polyfill, geometry,
                            expected):
        poly_filler = polyfill.PolyFiller(add_hex_id_if='center_contained')
        result = poly_filler.fill(geometry)

        assert sorted(expected) == sorted(result)

    @pytest.mark.parametrize(
        'geometry, expected',
        [
            # Circle slightly beyond center hexagon
            (Point(0, 0).buffer(1.1 * EDGE_LENGTH_IN_DEGREES),
             CENTER + FIRST_RING),

            # Circle so large that 1.73 factor leads to parts of the second ring
            # being added. Note that: 1.73 + 1.28 = 3.01, so just beyond 3 edge
            # lengths, which is the distance from center to every second hexagon
            # in the second ring.
            (Point(0, 0).buffer(1.28 * EDGE_LENGTH_IN_DEGREES),
             CENTER + FIRST_RING +
             ['2,-1', '1,-2', '-1,-1', '-2,1', '-1,2', '1,1']
             ),

            # Circle so large that 1.73 + 1.74 = 2 * 1.73 > 3.46
            (Point(0, 0).buffer(1.74 * EDGE_LENGTH_IN_DEGREES),
             CENTER + FIRST_RING + SECOND_RING
             ),
        ]

    )
    def test_with_buffer(self, patch_h3_polyfill,
                         patch_h3_edge_length,
                         geometry, expected):
        """
        Note that we use EPSG 3857 for the buffer CRS, because it's precise
        enough at lat=0, lon=0.
        """
        poly_filler = polyfill.PolyFiller(
            add_hex_id_if='center_within_buffer',
            buffer_crs='epsg:3857'
        )
        result = poly_filler.fill(geometry)

        assert sorted(expected) == sorted(result)


class TestRoadNetworkPolyFiller:

    def test_create_road_network_view(self, road_network_polyfiller, osm_db):
        global_bbox = box(-180, -85, 180, 85)  # limited to 3857 bounds
        road_network_polyfiller._create_road_network_view(global_bbox)

        # Fetch the result and the raw data
        with osm_db.engine.connect() as conn:
            gdf_result = gpd.GeoDataFrame.from_postgis(
                "SELECT * FROM road_network;", conn, geom_col='geom')
            gdf_raw = gpd.GeoDataFrame.from_postgis(
                "SELECT * FROM planet_osm_line;", conn, geom_col='way')

        # Check the view `road_network` was created
        assert osm_db.engine.has_table('road_network')

        # Check that the conditions are met (whitelist/blacklist is applied)
        gdf_raw = gdf_raw[gdf_raw['part_of_network']]
        gpd.testing.assert_geoseries_equal(gdf_result['geom'], gdf_raw['way'])

        # Check that the view is replaced
        global_bbox = box(9, 39, 11, 41)  # limited the bounds
        road_network_polyfiller._create_road_network_view(global_bbox)
        # Fetch the new result
        with osm_db.engine.connect() as conn:
            gdf_new_result = gpd.GeoDataFrame.from_postgis(
                "SELECT * FROM road_network;", conn, geom_col='geom')

        assert 0 < len(gdf_new_result) < len(gdf_result)

    def test_fetch_buffered_road_network(self, road_network_polyfiller, osm_db):
        result = road_network_polyfiller._fetch_buffered_road_network()
        result_geom = wkt.loads(result)

        resolution = road_network_polyfiller.resolution
        buffer_size = road_network_polyfiller.buffer_size
        full_buffer_size = buffer_size + 1.73 * h3.edge_length(resolution,
                                                               unit='m')

        # Fetch the raw data
        with osm_db.engine.connect() as conn:
            gdf_raw = gpd.GeoDataFrame.from_postgis(
                "SELECT * FROM road_network;", conn, geom_col='geom')

        # Check the resulting geometry
        gdf_raw = gdf_raw.to_crs(epsg='3035')
        gdf_raw['geom'] = gdf_raw['geom'].buffer(distance=full_buffer_size)
        gdf_raw = gdf_raw.to_crs(epsg='4326')
        raw_geom_union = gdf_raw['geom'].unary_union

        assert_geometries_almost_equal(result_geom, raw_geom_union)

    def test_fill(self, road_network_polyfiller, osm_db):
        bbox = box(9.9, 39.9, 10.1, 40.1)
        road_network_polyfiller.resolution = 9
        resulting_hex_ids = road_network_polyfiller.fill(bbox)

        resolution = road_network_polyfiller.resolution
        buffer_size = road_network_polyfiller.buffer_size
        full_buffer_size = buffer_size + 1.73 * h3.edge_length(resolution,
                                                               unit='m')

        with osm_db.engine.connect() as conn:
            gdf_raw = gpd.GeoDataFrame.from_postgis(
                f"""
                SELECT *
                FROM planet_osm_line as ol
                WHERE ST_Contains(
                        ST_Transform(ST_GeomFromText('{bbox.wkt}', 4326),
                                     3857),
                        ol.way);
                """, conn, geom_col='way')

        gdf_raw = gdf_raw.to_crs(epsg='3035')
        gdf_raw['way'] = gdf_raw['way'].buffer(full_buffer_size)
        gdf_raw = gdf_raw.to_crs(epsg='4326')

        geo_json = mapping(gdf_raw.unary_union)
        expected_hex_ids = list(h3.polyfill(geo_json, resolution, True))

        resulting_hex_ids.sort()
        expected_hex_ids.sort()
        assert resulting_hex_ids == expected_hex_ids
