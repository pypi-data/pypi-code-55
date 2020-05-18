from pathlib import Path
from strix import file_actions as fa
from strix.file_formats import egf
from strix.file_formats import csv
from strix.file_formats import geo_json
from strix.file_formats import kml_gca as kml

__all__ = ["read_egf", "write_egf", "read_geojson", "write_geojson", "read_csv", "write_csv", "visualize", "write_kml"]


def read_egf(file_path):
    egf_as_str = fa.str_file_read(file_path)
    egf_as_gca = egf.to_gca(egf_as_str)

    return egf_as_gca


def write_egf(file_path, gca_obj):
    gca_as_egf = egf.from_gca(gca_obj)
    fa.text_writer(file_path, gca_as_egf)


def visualize(gca_obj):
    geo_json.from_gca(gca_obj, visualize=True)


def read_geojson(file_path):
    json_as_str = fa.str_file_read(file_path)
    json_as_gca = geo_json.to_gca(json_as_str)

    return json_as_gca


def write_geojson(file_path, gca_obj):
    gca_as_json_str = geo_json.from_gca(gca_obj)
    fa.text_writer(file_path, gca_as_json_str)


def read_csv(file_path):
    csv_as_list = fa.read_csv(file_path)
    csv_as_gca = csv.to_gca(csv_as_list)

    return csv_as_gca


def write_csv(file_path, gca_obj):
    gca_as_csv = csv.from_gca(gca_obj)
    fa.write_csv(file_path, gca_as_csv)


def write_kml(file_pth, gca_obj, name_header, folder_name, folder_description='', altitude_mode='ctg'):
    """
    Creates a KML from GCA object using default styling

    Parameters
    ----------
    file_pth : str
        include file name and extension in path (e.g. docs/my_map.kml)
    gca_obj : GCA
    name_header : str
        The header that will be used to label features
    folder_name : str
    folder_description : str
    altitude_mode : {'ctg', 'rtg', 'abs'}

    Returns
    -------
    None

    """

    file_path = Path(file_pth)
    file_name = file_path.stem
    if gca_obj.geometry_type == "PT":
        point = kml.from_gca_point(gca_obj, name_header, folder_name, folder_description, altitude_mode=altitude_mode, style_to_use='pt_style')
        style = kml.point_style('pt_style')
        kml_str = kml.kml(file_name, [style], [point], 'KML from GCA')
        fa.text_writer(file_path, kml_str)

    elif gca_obj.geometry_type == "LS":
        line = kml.from_gca_linestring(gca_obj, name_header, folder_name, folder_description, altitude_mode=altitude_mode, style_to_use='ls_style')
        style = kml.line_style('ls_style')
        kml_str = kml.kml(file_name, [style], [line], 'KML from GCA')
        fa.text_writer(file_path, kml_str)
    elif gca_obj.geometry_type == "POLY":
        poly = kml.from_gca_polygon(gca_obj, name_header, folder_name, folder_description, altitude_mode=altitude_mode, style_to_use='poly_style')
        style = kml.polygon_style('poly_style')
        kml_str = kml.kml(file_name, [style], [poly], 'KML from GCA')
        fa.text_writer(file_path, kml_str)
    else:
        raise ValueError(f"'{gca_obj.geometry_type}' is not a valid geometry type")
