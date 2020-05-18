from strix.file_formats import kml_base
from strix import file_actions as fa

# Import remaining KML base functions
from strix.file_formats.kml_base import point_style, line_style, polygon_style, folder, kml


def from_gca_point(gca_obj, name_header, folder_name, folder_description='',
                   altitude_mode="ctg", style_to_use=None, pt_hidden=False, folder_collapsed=True):
    """
    Save features from GCA object into a kml folder

    Parameters
    ----------
    gca_obj : GCA
    name_header : str
        The header that will be used to label features
    folder_name : str
    folder_description : str
    altitude_mode : {'ctg', 'rtg', 'abs'}
    style_to_use : str
        name of style to use
    pt_hidden : bool
    folder_collapsed : bool

    Returns
    -------
    KML Folder

    """

    name_col = gca_obj.headers.index(name_header)

    pts = list()

    for feature in gca_obj.features:
        name = feature[0][name_col]
        coords = feature[1]
        attrs = feature[0]
        headers = gca_obj.headers
        pt = kml_base.point(coords, name, headers, attrs, altitude_mode, style_to_use, pt_hidden)
        pts.append(pt)

    pt_folder = kml_base.folder(folder_name, pts, folder_description, folder_collapsed)

    return pt_folder


def from_gca_linestring(gca_obj, name_header, folder_name, folder_description='',
                        altitude_mode="ctg", style_to_use=None, ls_hidden=False,
                        ls_follow_terrain=True, ls_extrude_to_ground=False, folder_collapsed=True):
    """
    Save features from GCA object into a kml folder

    Parameters
    ----------
    gca_obj : GCA
    name_header : str
        The header that will be used to label features
    folder_name : str
    folder_description : str
    altitude_mode : {'ctg', 'rtg', 'abs'}
    style_to_use : str
        name of style to use
    ls_hidden : bool
    ls_follow_terrain : bool
    ls_extrude_to_ground : bool
    folder_collapsed : bool

    Returns
    -------
    KML Folder

    """

    name_col = gca_obj.headers.index(name_header)

    lss = list()

    for feature in gca_obj.features:
        name = feature[0][name_col]
        coords = feature[1]
        attrs = feature[0]
        headers = gca_obj.headers

        ls = kml_base.line(coords, name, headers, attrs, altitude_mode, style_to_use, ls_hidden, ls_follow_terrain, ls_extrude_to_ground)
        lss.append(ls)

    ls_folder = kml_base.folder(folder_name, lss, folder_description, folder_collapsed)

    return ls_folder


def from_gca_polygon(gca_obj, name_header, folder_name, folder_description='',
                     altitude_mode="ctg", style_to_use=None, poly_hidden=False,
                     poly_follow_terrain=True, poly_extrude_to_ground=False, folder_collapsed=True):
    """
    Save features from GCA object into a kml folder

    Parameters
    ----------
    gca_obj : GCA
    name_header : str
        The header that will be used to label features
    folder_name : str
    folder_description : str
    altitude_mode : {'ctg', 'rtg', 'abs'}
    style_to_use : str
        name of style to use
    poly_hidden : bool
    poly_follow_terrain : bool
    poly_extrude_to_ground : bool
    folder_collapsed : bool

    Returns
    -------

    """

    name_col = gca_obj.headers.index(name_header)

    polygons = list()

    for feature in gca_obj.features:
        name = feature[0][name_col]
        coords = feature[1]
        attrs = feature[0]
        headers = gca_obj.headers

        poly = kml_base.polygon(coords, name, headers, attrs, altitude_mode, style_to_use, poly_hidden, poly_follow_terrain, poly_extrude_to_ground)
        polygons.append(poly)

    poly_folder = kml_base.folder(folder_name, polygons, folder_description, folder_collapsed)

    return poly_folder


def write(file_path, kml_str):
    """
    writes KML to file

    Parameters
    ----------
    file_path : str
        include file name and extension in path (e.g. docs/my_map.kml)
    kml_str : str

    Returns
    -------
    None

    """

    fa.text_writer(file_path, kml_str)
