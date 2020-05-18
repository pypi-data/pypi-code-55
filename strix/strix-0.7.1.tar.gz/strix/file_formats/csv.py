from strix.gca import valid_geom_types, GCA
from re import search
import json

__all__ = ["from_gca", "to_gca"]


def from_gca_point(gca_obj, xyz_data=False, geometry=True):
    """
    Converts gca object to CSV in GCA format

    Parameters
    ----------
    gca_obj : GCA
    xyz_data : Bool
        include LAT, LNG, ELEV columns in exported CSV
    geometry : Bool
        Include GCA Geometry column in exported CSV

    Returns
    -------
    collection
        2D table for CSV

    """

    csv_table = [list(gca_obj.headers)]

    if xyz_data is True:
        csv_table[0] += ["LAT", "LNG", "ELEV"]
    if geometry is True:
        csv_table[0] += [f"GEOMETRY_{gca_obj.geometry_type}"]
    else:
        pass

    for pt in gca_obj.features:
        row = list()
        row.extend(pt[0])

        if xyz_data is True:
            lng, lat, z = pt[1]
            row.extend([lat, lng, z])
        if geometry is True:
            row.append(pt[1])
        else:
            pass

        csv_table.append(row)

    return csv_table


def from_gca_linestring(gca_obj, geometry=True):
    """
    Converts gca object to CSV in GCA format

    Parameters
    ----------
    gca_obj : GCA
    geometry : Bool
        Include GCA Geometry column in exported CSV

    Returns
    -------
    collection
        2D table for CSV

    """

    if geometry is True:
        csv_table = [list(gca_obj.headers) + [f"GEOMETRY_{gca_obj.geometry_type}"]]
    else:
        csv_table = [list(gca_obj.headers)]

    for ls in gca_obj.features:
        row = list()
        row.extend(ls[0])

        if geometry is True:
            row.append(ls[1])

        csv_table.append(row)

    return csv_table


def from_gca_polygon(gca_obj, geometry=True):
    """
    Converts gca object to CSV in GCA format

    Parameters
    ----------
    gca_obj : GCA
    geometry : Bool
        Include GCA Geometry column in exported CSV

    Returns
    -------
    collection
        2D table for CSV

    """

    if geometry is True:
        csv_table = [list(gca_obj.headers) + [f"GEOMETRY_{gca_obj.geometry_type}"]]
    else:
        csv_table = [list(gca_obj.headers)]

    for poly in gca_obj.features:
        row = list()
        row.extend(poly[0])

        if geometry is True:
            row.append(poly[1])

        csv_table.append(row)

    return csv_table


def from_gca(gca_obj, geometry=True):
    if gca_obj.geometry_type == "PT":
        return from_gca_point(gca_obj, geometry=geometry)
    elif gca_obj.geometry_type == "LS":
        return from_gca_linestring(gca_obj, geometry=geometry)
    elif gca_obj.geometry_type == "POLY":
        return from_gca_polygon(gca_obj, geometry=geometry)
    else:
        raise ValueError(f"'{gca_obj.geometry_type}' is not a valid geometry type")


def to_gca_point_components(csv_list):
    """
    Converts CSV in GCA format to GCA components

    Parameters
    ----------
    csv_list : collection

    Returns
    -------
    collection
        GCA components

    """

    gca_type = 'PT'
    gca_coordinates = list()
    gca_attributes = list()

    csv_original_headers = csv_list[0]

    coords_index = csv_original_headers.index(f"GEOMETRY_{gca_type}")

    for line_num, line in enumerate(csv_list):
        if line_num != 0:
            line_coordinates = json.loads(line[coords_index])
            gca_coordinates.append(line_coordinates)

        del line[coords_index]

        gca_attributes.append(line)

    return gca_type, gca_coordinates, gca_attributes


def to_gca_linestring_components(csv_list):
    """
    Converts CSV in GCA format to GCA components

    Parameters
    ----------
    csv_list : collection

    Returns
    -------
    collection
        GCA components

    """

    gca_type = 'LS'
    gca_coordinates = list()
    gca_attributes = list()

    csv_original_headers = csv_list[0]

    coords_index = csv_original_headers.index(f"GEOMETRY_{gca_type}")

    for line_num, line in enumerate(csv_list):
        if line_num != 0:
            line_coordinates = json.loads(line[coords_index])
            gca_coordinates.append(line_coordinates)

        del line[coords_index]

        gca_attributes.append(line)

        # print(gca_coordinates)

    return gca_type, gca_coordinates, gca_attributes


def to_gca_polygon_components(csv_list):
    """
    Converts CSV in GCA format to GCA components

    Parameters
    ----------
    csv_list : collection

    Returns
    -------
    collection
        GCA components

    """

    gca_type = 'POLY'
    gca_coordinates = list()
    gca_attributes = list()

    csv_original_headers = csv_list[0]

    coords_index = csv_original_headers.index(f"GEOMETRY_{gca_type}")

    for line_num, line in enumerate(csv_list):
        if line_num != 0:
            line_coordinates = json.loads(line[coords_index])
            gca_coordinates.append(line_coordinates)

        del line[coords_index]

        gca_attributes.append(line)

    return gca_type, gca_coordinates, gca_attributes


def csv_geom_detect(csv_headers):
    """
    Detects geometry type from a CSV in GCA format

    Parameters
    ----------
    csv_headers : collection
        first row of csv list

    Returns
    -------
    str
        valid geometry type

    """

    headers = csv_headers
    coord_headers = [f"GEOMETRY_{gca_type}" for gca_type in valid_geom_types]

    csv_type = list()

    # Detect valid headers. If present, append
    for geom_type in coord_headers:
        if geom_type in headers:
            csv_type.append(geom_type)
    assert len(csv_type) == 1, f"Expected 1 valid geometry header. {len(csv_type)} different geometry types were found: {csv_type}"

    count = csv_headers.count(csv_type[0])
    assert count == 1, f"Expected 1 valid geometry header. Found {count} instances of '{csv_type[0]}'."

    geom_type = search(r"GEOMETRY_([A-Z]{2,4})", csv_type[0]).group(1)

    return geom_type


def to_gca(csv_str):
    geom_type = csv_geom_detect(csv_str[0])

    if geom_type == "PT":
        return GCA(*to_gca_point_components(csv_str))
    elif geom_type == "LS":
        return GCA(*to_gca_linestring_components(csv_str))
    elif geom_type == "POLY":
        return GCA(*to_gca_polygon_components(csv_str))
    else:
        raise ValueError(f"'{geom_type}' is not a valid geometry type")
