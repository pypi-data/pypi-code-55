try:
    import h3

    h3.k_ring('841e265ffffffff', 4)
except AttributeError:
    from h3 import h3

import shapely


def get_geojson_dict_of_hex_id_boundary(hex_id):
    """
    :param str hex_id:
        A hex ID
    :return dict:
        geoJSON-like dictionary
    """
    geojson_dict = {
        "type": "Polygon",
        "coordinates":
            [
                h3.h3_to_geo_boundary(
                    h3_address=str(hex_id),
                    geo_json=True)
            ]
    }
    return geojson_dict


def extract_bbox_polygon(polygon):
    """
    Return the bounding box of the provided polygon as new polygon object

    :param shapely.geometry.Polygon polygon: Shapely geometry polygon object
    :return: Shapely geometry Polygon object
    """
    min_lon, min_lat, max_lon, max_lat = polygon.bounds
    polygon_bbox_geom = shapely.geometry.box(min_lon, min_lat, max_lon, max_lat)
    return polygon_bbox_geom
