import json
import webbrowser
import urllib.parse
from strix.gca import GCA

__all__ = ["from_gca", "to_gca"]


def from_gca(gca_obj, visualize=False):
    """
    Converts GCA object to GeoJSON Feature Class.

    Parameters
    ----------
    gca_obj : GCA
    visualize : bool
        True = Generate GeoJSON string + open with http://geojson.io

    Returns
    -------
    str

    """

    def geo_json_feature_collection():
        """
        Creates a GeoJSON dict from GCA object

        Returns
        -------
        str
        """

        geometry_type = gca_obj.geometry_type
        headers = gca_obj.headers
        features = gca_obj.features

        def feature_init(feature_type):
            """
            Initializes empty GeoJSON feature of a specific type.

            Parameters
            ----------
            feature_type : str
                PT = Point
                LS = LineString
                POLY = Polygon

            Returns
            -------
            dict

            """

            if feature_type == "PT":
                feature_type = "Point"
            elif feature_type == "LS":
                feature_type = "LineString"
            elif feature_type == "POLY":
                feature_type = "Polygon"
            else:
                raise ValueError(f"'{feature_type}' not recognized as a valid feature type")

            feature = dict()
            feature["type"] = "Feature"
            feature["geometry"] = {}
            feature["geometry"]["type"] = feature_type
            feature["geometry"]["coordinates"] = []
            feature["properties"] = {}

            return feature

        def populate():
            """
            Populates GeoJson Feature Collection with GCA object

            Returns
            -------
            dict

            """

            # initialize feature collection
            fc = dict()
            fc["type"] = "FeatureCollection"
            fc["features"] = list()

            for feature in features:
                ft_coords = feature[1]
                ft_attrs = feature[0]

                json_ft = feature_init(geometry_type)

                json_ft["geometry"]["coordinates"].extend(ft_coords)
                json_ft["properties"] = dict(zip(headers, ft_attrs))
                fc["features"].append(json_ft)

            return fc

        return populate()

    feature_class = geo_json_feature_collection()

    feature_class_string = json.dumps(geo_json_feature_collection())

    if visualize is True:
        url = r"http://geojson.io/#data=data:application/json,"
        url_json = urllib.parse.quote(json.dumps(feature_class, separators=(',', ':')))
        full_url = url + url_json
        webbrowser.open(full_url)

    return feature_class_string


def to_gca_point_components(json_str):
    json_dict = json.loads(json_str)

    gca_type = 'PT'
    gca_coords = list()
    gca_attrs = list()

    for ft_num, ft in enumerate(json_dict['features']):
        # Grab attribute headers
        if ft_num == 0:
            gca_attrs.append([*ft['properties']])
        else:
            pass

        gca_attrs.append(list(ft['properties'].values()))
        gca_coords.append(ft['geometry']['coordinates'])

    return gca_type, gca_coords, gca_attrs


def to_gca_linestring_components(json_str):
    json_dict = json.loads(json_str)

    gca_type = 'LS'
    gca_coords = list()
    gca_attrs = list()

    for ft_num, ft in enumerate(json_dict['features']):
        # Grab attribute headers
        if ft_num == 0:
            gca_attrs.append([*ft['properties']])
        else:
            pass

        gca_attrs.append(list(ft['properties'].values()))
        gca_coords.append(ft['geometry']['coordinates'])

    return gca_type, gca_coords, gca_attrs


def to_gca_polygon_components(json_str):
    json_dict = json.loads(json_str)

    gca_type = 'POLY'
    gca_coords = list()
    gca_attrs = list()

    for ft_num, ft in enumerate(json_dict['features']):
        # Grab attribute headers
        if ft_num == 0:
            gca_attrs.append([*ft['properties']])
        else:
            pass

        gca_attrs.append(list(ft['properties'].values()))
        gca_coords.append(ft['geometry']['coordinates'])

    return gca_type, gca_coords, gca_attrs


def from_geo_json_validate(json_str):
    json_dict = json.loads(json_str)
    assert json_dict['type'] == 'FeatureCollection', "GeoJSON Type is not 'FeatureCollection'"

    types = list()
    for ft in json_dict['features']:
        if ft['geometry'] is None:
            raise ValueError("Null geometry detected in GeoJSON file. Fix or remove Null geometries to continue.")

        types.append(ft['geometry']['type'])

    types = set(types)
    assert len(types) == 1, "Multiple geometry types detected in GeoJSON FeatureCollection. Expected all features to be of single type"

    return json_str


def to_gca(json_str):
    json_str = from_geo_json_validate(json_str)
    json_dict = json.loads(json_str)

    json_type = json_dict['features'][0]['geometry']['type']

    if json_type == "Point":
        return GCA(*to_gca_point_components(json_str))
    elif json_type == "LineString":
        return GCA(*to_gca_linestring_components(json_str))
    elif json_type == "Polygon":
        return GCA(*to_gca_polygon_components(json_str))
    else:
        raise ValueError(f"'{json_type}' is not a recognized GeoJSON geometry type")