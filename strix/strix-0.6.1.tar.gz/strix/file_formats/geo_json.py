import json
import webbrowser
import urllib.parse


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
