from strix.gca import valid_geom_types, GCA
from re import split
from strix.value_validation import decimal_degree_validate

__all__ = ["from_gca", "EGFValidate", "to_gca"]


def from_gca_point(gca_obj):
    """
    Converts Point GCA to an EGF string.

    Returns
    -------
    egf_str : str
        Point GCA as an EGF string

    """
    if gca_obj.geometry_type != "PT":
        raise ValueError(f"Expected geometry type to be 'PT' and got '{gca_obj.geometry_type}' instead")

    features = gca_obj.features

    egf_str = ""

    egf_str += str(gca_obj.geometry_type)
    egf_str += "\n" * 4
    egf_str += ', '.join(str(i) for i in gca_obj.headers)

    for ft in features:
        lng, lat, elev = ft[1][:3]
        egf_str += "\n" * 4
        egf_str += ', '.join(str(i) for i in ft[0])
        egf_str += "\n"
        egf_str += ', '.join(str(coord) for coord in [lat, lng, elev])
    egf_str += "\n"

    return egf_str


def from_gca_linestring(gca_obj):
    """
    Converts LineString GCA to an EGF string.

    Returns
    -------
    egf_str : str
        LineString GCA as an EGF string

    """

    if gca_obj.geometry_type != "LS":
        raise ValueError(f"Expected geometry type to be 'LS' and got '{gca_obj.geometry_type}' instead")

    features = gca_obj.features

    egf_str = ""

    egf_str += str(gca_obj.geometry_type)
    egf_str += "\n" * 4
    egf_str += ', '.join(str(i) for i in gca_obj.headers)

    for ft in features:
        egf_str += "\n" * 4
        egf_str += ', '.join(str(i) for i in ft[0])

        for coord_set in ft[1]:
            lng, lat, elev = coord_set[:3]
            egf_str += "\n"
            egf_str += ', '.join(str(coord) for coord in [lat, lng, elev])

    egf_str += "\n"

    return egf_str


def from_gca_polygon(gca_obj):
    """
    Converts Polygon CGA to an EGF string.

    Returns
    -------
    egf_str : str
        Polygon GCA as an EGF string

    """

    if gca_obj.geometry_type != "POLY":
        raise ValueError(f"Expected geometry type to be 'POLY' and got '{gca_obj.geometry_type} instead'")

    egf_str = ""

    egf_str += str(gca_obj.geometry_type)
    egf_str += "\n" * 4
    egf_str += ', '.join(str(i) for i in gca_obj.headers)

    for ft in gca_obj.features:
        egf_str += "\n" * 4
        egf_str += ', '.join(str(i) for i in ft[0])

        for rg_num, ring in enumerate(ft[1]):
            if rg_num > 0:
                egf_str += "\n"
            # In GCA Poly, each ring has matching first/last coordinate sets. EGF does not.
            for coord_set in ring[:-1]:
                lng, lat, elev = coord_set[:3]
                egf_str += "\n"
                egf_str += ', '.join(str(coord) for coord in [lat, lng, elev])

    egf_str += "\n"

    return egf_str


def from_gca(gca_obj):
    if gca_obj.geometry_type == "PT":
        return from_gca_point(gca_obj)
    elif gca_obj.geometry_type == "LS":
        return from_gca_linestring(gca_obj)
    elif gca_obj.geometry_type == "POLY":
        return from_gca_polygon(gca_obj)
    else:
        raise ValueError(f"'{gca_obj.geometry_type}' is not a valid geometry type")


class EGFValidate:
    """
    Checks that the general structure of an GEF file is correct.
        - That the EGF is of a valid geometry type
        - That there are the correct number of sections in the EGF
        - That sections are separated by 3 blank lines
        - That there are the minimum number of coordinate sets required for declared geometry type
        - That the header section is a single line
        - That last line of file is blank

    """
    def __init__(self, egf_str):
        self.egf_str = egf_str
        self.sections = self.split_sections()
        self.geometry_type = self.geom_type()

        self.last_line_blank()
        self.section_separators()
        self.headers_single_line()
        self.min_coord_sets()

    def section_separators(self):
        sections = split("\n\n\n\n\n", self.egf_str)
        assert len(sections) == 1, "EGF Sections cannot be separated by more than 3 blank lines"

        return True

    def split_sections(self):
        sections_split = split("\n\n\n\n", self.egf_str)
        assert len(sections_split) >= 3, f"EGF Should have at least 3 Sections, {len(sections_split)} found"

        return sections_split

    def geom_type(self):
        geom = self.sections[0]

        assert geom in valid_geom_types, f"'{geom}' is not a valid geometry type"

        return geom

    def last_line_blank(self):
        final_two_chars = self.egf_str[-2:]
        assert final_two_chars[0].isdigit() and final_two_chars[1] == '\n', "A single blank line is required after final digit of the last coordinate in an EGF file."

        return True

    def headers_single_line(self):
        header_section = self.sections[1]
        header_lines = split("\n", header_section)

        assert len(header_lines) == 1, f"Header section is invalid. Expected 1 line. Found {len(header_lines)}"

        return True

    def min_coord_sets(self):

        features = self.sections[2:]

        # Remove last line from EGF string (Should be blank)
        features[-1] = features[-1][:-1]

        geom_type = self.geom_type()

        if geom_type == 'PT':
            for ft_num, feature_string in enumerate(features, 1):
                ft = split("\n", feature_string)

                # Includes attribute row in count
                assert len(ft) == 2, f"Invalid POINT feature. Must have only 2 lines (attributes / coordinates) pr POINT feature. {len(ft)} lines detected in {ft}"

        elif geom_type == 'LS':
            for ft_num, feature_string in enumerate(features, 1):
                ft = split("\n", feature_string)

                # Includes attribute row in count
                assert len(ft) >= 3, f"Invalid LINESTRING feature. Must have a minimum of 2 coordinate sets. {len(ft) - 1} detected in {ft}"

                assert "" not in ft[1:], f"Invalid LINESTRING feature. Blank line detected in coordinate set section of {ft}"

        elif geom_type == 'POLY':
            for ft_num, feature_string in enumerate(features, 1):
                rings = split("\n\n", feature_string)

                for ring_num, ring in enumerate(rings, 1):
                    coord_sets = split("\n", ring)

                    # remove attribute row from outer ring section so rings have fair comparison of coordinate sets
                    if ring_num == 1:
                        coord_sets = coord_sets[1:]
                    assert len(coord_sets) >= 3, f"Invalid POLYGON feature. Polygon rings must have a minimum of 3 coordinate sets. {len(coord_sets)} coordinate sets detected in RING({ring_num}) of FEATURE({ft_num})"

        else:
            raise ValueError(f"'{geom_type}' in not a valid Geometry Type")

        return True


def to_gca_point_components(egf_str):
    egf_pt = EGFValidate(egf_str)
    sections = egf_pt.sections
    features = sections[2:]
    headers = split(", ", sections[1])

    # Remove last line from EGF string
    features[-1] = features[-1][:-1]

    gca_type = egf_pt.geometry_type
    gca_coordinates = list()
    gca_attributes = [headers]

    for ft_num, ft in enumerate(features, 1):
        ft_lines = split("\n", ft)

        for line_num, line in enumerate(ft_lines, 1):
            line_values = split(", ", line)

            # Attributes line
            if line_num == 1:
                gca_attributes.append(line_values)

            # Coordinates line
            if line_num == 2:
                lat, lng, elev = line_values
                xyz_coords = [decimal_degree_validate(i) for i in [lng, lat, elev]]
                gca_coordinates.append(xyz_coords)
            else:
                continue

    return gca_type, gca_coordinates, gca_attributes


def to_gca_linestring_components(egf_str):
    egf_pt = EGFValidate(egf_str)
    sections = egf_pt.sections
    features = sections[2:]
    headers = split(", ", sections[1])

    # Remove last line from EGF string
    features[-1] = features[-1][:-1]

    gca_type = egf_pt.geometry_type
    gca_coordinates = list()
    gca_attributes = [headers]

    for ft_num, ft in enumerate(features, 1):
        ft_coords = list()
        ft_lines = split("\n", ft)

        for line_num, line in enumerate(ft_lines, 1):
            line_values = split(", ", line)

            # Attributes line
            if line_num == 1:
                gca_attributes.append(line_values)

            # Coordinates line
            if line_num > 1:
                lat, lng, elev = line_values
                xyz_coords = [decimal_degree_validate(i) for i in [lng, lat, elev]]
                ft_coords.append(xyz_coords)

        gca_coordinates.append(ft_coords)

    return gca_type, gca_coordinates, gca_attributes


def to_gca_polygon_components(egf_str):
    egf_pt = EGFValidate(egf_str)
    sections = egf_pt.sections
    features = sections[2:]
    headers = split(", ", sections[1])

    # Remove last line from EGF string
    features[-1] = features[-1][:-1]

    gca_type = egf_pt.geometry_type
    gca_coordinates = list()
    gca_attributes = [headers]

    for poly_num, poly in enumerate(features, 1):
        poly_coords = list()
        rings = split("\n\n", poly)

        for ring_num, ring in enumerate(rings, 1):
            ring_coords = list()
            ring_line = split("\n", ring)

            for line_num, line in enumerate(ring_line, 1):
                line_values = split(", ", line)

                if ring_num == 1 and line_num == 1:
                    gca_attributes.append(line_values)
                else:
                    lat, lng, elev = line_values
                    xyz_coords = [decimal_degree_validate(i) for i in [lng, lat, elev]]
                    ring_coords.append(xyz_coords)

            # Make first coordinate set match last coordinate set for each ring in  GCA POLY
            ring_coords.append(ring_coords[0])

            poly_coords.append(ring_coords)
        gca_coordinates.append(poly_coords)

    return gca_type, gca_coordinates, gca_attributes


def to_gca(egf_str):

    egf = EGFValidate(egf_str)

    if egf.geometry_type == "PT":
        return GCA(*to_gca_point_components(egf_str))
    elif egf.geometry_type == "LS":
        return GCA(*to_gca_linestring_components(egf_str))
    elif egf.geometry_type == "POLY":
        return GCA(*to_gca_polygon_components(egf_str))
    else:
        raise ValueError(f"'{egf.geometry_type}' is not a valid geometry type")
