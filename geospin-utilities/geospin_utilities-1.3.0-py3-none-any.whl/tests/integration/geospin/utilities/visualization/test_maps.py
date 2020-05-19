"""Test functions from visualization.maps.py."""
import folium
import geojson

from geospin.utilities.visualization import maps


def test_geospin_map_init():
    from geospin.utilities.visualization.maps import GeospinMap

    m = GeospinMap()

    layer_name = 'Geospin Basemap'
    tiles_url = 'http://maps.geospin.de/geospin-light-gray/{z}/{x}/{y}.png'
    attribution = 'Geospin'

    assert layer_name in m._children
    assert m._children[layer_name].tiles == tiles_url
    assert m._children[layer_name].options['attribution'] == attribution


def test_osm_map_init():
    from geospin.utilities.visualization.maps import OSMMap

    m = OSMMap()

    layer_name = 'OpenStreetMap'
    attribution = (
        'Data by &copy; <a href="http://openstreetmap.org">OpenStreetMap</a>, '
        'under <a href="http://www.openstreetmap.org/copyright">ODbL</a>.'
    )

    assert m._children[layer_name.lower()].options['attribution'] == attribution


def test_get_marker_factory():
    import folium.map
    from geospin.utilities.visualization.maps import get_marker_factory

    icon_args = {'color': 'blue', 'icon': 'info-sign'}
    marker_args = {'tooltip': 'test tool tip'}
    marker_factory = get_marker_factory(
        icon_args=icon_args,
        marker_args=marker_args,
    )

    location = [1, 2]

    marker_1 = marker_factory(location)
    marker_2 = marker_factory(location)

    assert type(marker_1) is folium.map.Marker
    assert type(marker_2) is folium.map.Marker
    assert not (marker_1 is marker_2)


def test_h3_choropleth_is_instance_of_layer():
    hex_ids = [
        '841f12dffffffff',
        '841f131ffffffff',
        '841f133ffffffff',
        '841f135ffffffff',
        '841f197ffffffff',
    ]
    values = [1., 2., 3., 4., 5.]
    h3_choropleth = maps.H3Choropleth(hex_ids, values)
    assert isinstance(h3_choropleth, folium.map.Layer)


def test_h3_boundary_feature(monkeypatch):
    geometry = {
        "type": "Polygon",
        "coordinates":
            [1, 2, 3]
    }

    def mock_get_geometry(x):
        return geometry

    monkeypatch.setattr(
        maps.H3BoundaryFeature,
        '_get_geometry',
        mock_get_geometry
    )
    hex_id = '871faec4dffffff'
    value = 4.
    expected = geojson.Feature(
        geometry=geometry,
        id=hex_id,
        properties={'value': value},
        hex_id=hex_id,
    )
    result = maps.H3BoundaryFeature(hex_id, value)
    assert expected == result


def test_h3_boundary_feature_collection():
    hex_ids = [
        '841f135ffffffff',
        '841f197ffffffff',
    ]
    values = [4., 5.]
    expected = geojson.FeatureCollection(
        [
            maps.H3BoundaryFeature(hex_ids[0], values[0]),
            maps.H3BoundaryFeature(hex_ids[1], values[1]),
        ]
    )
    result = maps.H3BoundaryFeatureCollection(hex_ids, values)
    assert expected == result
