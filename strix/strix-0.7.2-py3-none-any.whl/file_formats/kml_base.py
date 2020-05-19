"""
Functions for creating KML placemarks.

"""

import xml.etree.ElementTree as ET


def altitude_modes(altitude_mode='ctg'):
    """Expands an abbreviated altitude mode to its full length name.

    Parameters
    ----------
    altitude_mode : {'ctg', 'rtg', 'abs'}
        Abbreviated altitude mode. (Default = 'ctg')

    Returns
    -------
    full_mode: str
        The full length name of the abbreviated altitude mode.

    Notes
    _____
    ctg = clampToGround
        Ignores any altitude value and places the feature on the surface of the ground.

    rtg = relativeToGround
        Measures the altitude from the ground level directly below the coordinates.

    abs = absolute
        Altitude relative to sea level.

    """

    # Abbreviation dictionary
    abbreviations = {'abs': 'absolute',
                     'ctg': 'clampToGround',
                     'rtg': 'relativeToGround'}

    if altitude_mode in abbreviations:
        full_mode = abbreviations[altitude_mode]
    else:
        full_mode = 'clampToGround'

    return full_mode


def kml_color(hex6_color, opacity=100):
    """Converts hex color to work with KML.

    When provided with an RGB hex color code, the function will return the KML equivalent of the provided color code.

    Parameters
    ----------
    hex6_color : str
        RGB hex color with "#".
    opacity : int, optional
        A value between 0 and 100 where 0 is transparent (Default = 100).

    Returns
    -------
    kml_color: str
        KML color code.

    Notes
    _____
    In a '.kml' file, color and opacity (alpha) values are expressed in hexadecimal notation. The range of values for
    any one color is 0 to 255 (00 to ff). For alpha, 00 is fully transparent and ff is fully opaque. The order of
    expression is aabbggrr, where aa=alpha (00 to ff); bb=blue (00 to ff); gg=green (00 to ff); rr=red (00 to ff).

    """

    r = hex6_color[1:3]
    g = hex6_color[3:5]
    b = hex6_color[5:]

    if 0 > opacity or opacity > 100:
        raise ValueError("Opacity value must be between 0 and 100")

    opacity_hex = format(int(round(opacity / 100 * 255, 0)), '02x')
    kml_color_code = str(opacity_hex + b + g + r).lower()

    return kml_color_code


def point(coords, name, headers, attributes, altitude_mode="ctg", style_to_use=None, hidden=False):
    """Creates a KML element of a point.

    Parameters
    ----------
    coords : list[float]
        A list of x, y, z coordinates as [x, y, z].
    name : str
        The name to be given to the point.
    headers : list[str]
        A list of headers to the attributes of the point.
    attributes : list[str]
        A list of the attributes of the point.
    altitude_mode : {'ctg', 'rtg', 'abs'}, optional
        An abbreviated altitude mode (Default = 'ctg').
    style_to_use : str, optional
        The name of the point style to be used (Default = None).
    hidden : bool, optional
        A value of 1 or 0 where 1 means the point will be visible (Default = 1).

    Returns
    -------
    object
        An element tree branch representing a KML point.

    Examples
    ________
    A point marking home plate at Fenway Park in Boston, MA.

    hp = point([-71.097769, 42.346249, 0], 'Home Plate', ['City', 'Park', 'Base'], ['Boston', 'Fenway', 'Home'], style_to_use='Bases Style')
    """

    # Create placemark
    placemark = ET.Element('Placemark')
    ET.SubElement(placemark, 'name').text = str(name)

    # Set 'visibility' value
    visibility = 1
    if hidden is True:
        visibility = 0
    else:
        pass
    ET.SubElement(placemark, 'visibility').text = str(visibility)

    # Assign style
    if style_to_use is not None:
        ET.SubElement(placemark, "styleUrl").text = str(style_to_use)

    # Format attributes for KML description balloon
    attribute_str = ''
    for cell in range(len(headers)):
        attribute_str += "<b>" + str(headers[cell]) + "</b>: " + str(attributes[cell]) + "<br>"
    ET.SubElement(placemark, "description").text = attribute_str

    # Create KML point as a child of placemark
    kml_point = ET.SubElement(placemark, 'Point')

    # Assign altitude mode to point
    ET.SubElement(kml_point, 'altitudeMode').text = altitude_modes(altitude_mode)

    # Create point's coordinate string.
    ET.SubElement(kml_point, 'coordinates').text = str(coords[0]) + "," + str(coords[1]) + "," + str(
        coords[2])

    # Create point's 'extended data' attribute table.
    extended_data = ET.SubElement(placemark, 'ExtendedData')
    for cell in range(len(headers)):
        data = ET.SubElement(extended_data, 'Data', {'name': headers[cell]})
        ET.SubElement(data, 'displayName').text = str(headers[cell])
        ET.SubElement(data, 'value').text = str(attributes[cell])

    return placemark


def line(coords, name, headers, attributes, altitude_mode="ctg",
         style_to_use=None, hidden=False, follow_terrain=True, extrude_to_ground=False):
    """Creates a KML element of a line.

    Parameters
    ----------
    coords : collection
        A list of the coordinate sets comprising the line.
    name : str
        The name to be given to the line.
    headers : list[str]
        A list of headers to the attributes of the point.
    attributes : list[str]
        A list of the attributes of the point.
    altitude_mode : {'ctg', 'rtg', 'abs'}, optional
        An abbreviated altitude mode (Default = 'ctg').
    style_to_use : str, optional
        The name of the point style to be used (Default = None).
    hidden : bool, optional
        A value of 1 or 0 where 1 means the point will be visible (Default = 1).
    follow_terrain : bool, optional
        True = Line will follow terrain and curve of the Earth. (Default = True).
    extrude_to_ground : bool, optional
        True = Vertices of the line are extruded toward the center of the Earth's center. (Default = False).

    Returns
    -------
    object
        An element tree branch representing a KML line.

    Notes
    -----
    `Follow Terrain` only works when `altitude_mode` is set to "ctg".

    Examples
    ________
    A line marking the warning track boundary at Fenway Park in Boston, MA.

   warning_track_boundary_coords = [[-71.097727, 42.346729, 0],
                                     [-71.097721, 42.347030, 0],
                                     [-71.097023, 42.347030, 0],
                                     [-71.096694, 42.346892, 0],
                                     [-71.096457, 42.346414, 0],
                                     [-71.096499, 42.346359, 0],
                                     [-71.096695, 42.346306, 0],
                                     [-71.096971, 42.346287, 0]]

    wt = line(warning_track_boundary_coords, 'Warning Track', ['City', 'Park', 'Line'], ['Boston', 'Fenway', 'Warning track'], style_to_use='Warning Track Style')

    """

    # Create placemark
    placemark = ET.Element('Placemark')
    ET.SubElement(placemark, 'name').text = str(name)

    # Set 'visibility' value
    visibility = 1
    if hidden is True:
        visibility = 0
    else:
        pass
    ET.SubElement(placemark, 'visibility').text = str(visibility)

    # Assign style
    if style_to_use is not None:
        ET.SubElement(placemark, "styleUrl").text = '#' + str(style_to_use)

    # Format attributes for KML description balloon
    attribute_str = ''
    for cell in range(len(headers)):
        attribute_str += "<b>" + str(headers[cell]) + "</b>: " + str(attributes[cell]) + "<br>"
    ET.SubElement(placemark, "description").text = attribute_str

    # Create KML line as a child of placemark
    linestring = ET.SubElement(placemark, 'LineString')

    # Assign altitude mode to line
    ET.SubElement(linestring, 'altitudeMode').text = altitude_modes(altitude_mode)

    # Set 'tessellate' value
    tessellate = 1
    if follow_terrain is False:
        tessellate = 0
    else:
        pass
    ET.SubElement(linestring, 'tessellate').text = str(tessellate)

    # Set 'extrude' value
    extrude = 1
    if extrude_to_ground is False:
        extrude = 0
    else:
        pass
    ET.SubElement(linestring, 'extrude').text = str(extrude)

    # Create line's coordinate string.
    coord_string = ''
    for coord_set in coords:
        coord_string += str(coord_set[0]) + "," + str(coord_set[1]) + "," + str(coord_set[2]) + ' '
    ET.SubElement(linestring, 'coordinates').text = coord_string

    # Create line's 'extended data' attribute table.
    extended_data = ET.SubElement(placemark, 'ExtendedData')
    for cell in range(len(headers)):
        data = ET.SubElement(extended_data, 'Data', {'name': headers[cell]})
        ET.SubElement(data, 'displayName').text = str(headers[cell])
        ET.SubElement(data, 'value').text = str(attributes[cell])

    return placemark


def polygon(coords, name, headers, attributes, altitude_mode="ctg",
         style_to_use=None, hidden=False, follow_terrain=True, extrude_to_ground=False):
    """Creates a KML element of a polygon.

    Parameters
    ----------
    coords : collection
        A list of linear rings containing coordinates that comprise the polygon.
    name : str
        The name to be given to the line.
    headers : list[str]
        A list of headers to the attributes of the point.
    attributes : list[str]
        A list of the attributes of the point.
    altitude_mode : {'ctg', 'rtg', 'abs'}, optional
        An abbreviated altitude mode (Default = 'ctg').
    style_to_use : str, optional
        The name of the point style to be used (Default = None).
    hidden : bool, optional
        A value of 1 or 0 where 1 means the point will be visible (Default = 1).
    follow_terrain : bool, optional
        True = Line will follow terrain and curve of the Earth. (Default = True).
    extrude_to_ground : bool, optional
        True = Vertices of the line are extruded toward the center of the Earth's center. (Default = False).

    Returns
    -------
    object
        An element tree branch representing a KML line.

    Notes
    _____
    To close polygon, last coordinate set is a duplicate of first coordinate set.

    Examples
    ________
    A polygon marking the area between the bases at Fenway Park in Boston, MA.

    Bases polygon
    bases = [[-71.097769, 42.346249, 0],
             [-71.097440, 42.346251, 0],
             [-71.097441, 42.346496, 0],
             [-71.097772, 42.346491, 0],
             [-71.097769, 42.346249, 0]]

    Pitcher's mound hole
    mound = [[-71.097656, 42.346331, 0],
             [-71.097580, 42.346331, 0],
             [-71.097580, 42.346387, 0],
             [-71.097656, 42.346387, 0],
             [-71.097656, 42.346331, 0]]

    coords = [bases, mound]

    base_area = polygon(coords, 'Bases Area', ['City', 'Park', 'Area'], ['Boston', 'Fenway', 'Inside of bases'], style_to_use='Bases Area Style')

    """

    # Create placemark
    placemark = ET.Element('Placemark')
    ET.SubElement(placemark, 'name').text = str(name)

    # Set 'visibility' value
    visibility = 1
    if hidden is True:
        visibility = 0
    else:
        pass
    ET.SubElement(placemark, 'visibility').text = str(visibility)

    # Assign style
    if style_to_use is not None:
        ET.SubElement(placemark, "styleUrl").text = '#' + str(style_to_use)

    # Format attributes for KML description balloon
    attribute_str = ''
    for cell in range(len(headers)):
        attribute_str += "<b>" + str(headers[cell]) + "</b>: " + str(attributes[cell]) + "<br>"
    ET.SubElement(placemark, "description").text = attribute_str

    # Create KML polygon as a child of placemark
    kml_polygon = ET.SubElement(placemark, 'Polygon')

    # Assign altitude mode to line
    ET.SubElement(kml_polygon, 'altitudeMode').text = altitude_modes(altitude_mode)

    # Set 'tessellate' value
    tessellate = 1
    if follow_terrain is False:
        tessellate = 0
    else:
        pass
    ET.SubElement(kml_polygon, 'tessellate').text = str(tessellate)

    # Set 'extrude' value
    extrude = 1
    if extrude_to_ground is False:
        extrude = 0
    else:
        pass
    ET.SubElement(kml_polygon, 'extrude').text = str(extrude)

    # Create outer boundary
    outer_boundary = ET.SubElement(kml_polygon, 'outerBoundaryIs')
    outer_boundary_lr = ET.SubElement(outer_boundary, 'LinearRing')

    # Outer boundary coordinate string.
    coord_string = ''
    for coord_set in coords[0]:
        coord_string += str(coord_set[0]) + "," + str(coord_set[1]) + "," + str(coord_set[2]) + ' '
    ET.SubElement(outer_boundary_lr, 'coordinates').text = coord_string

    # Create inner boundary/boundaries.
    for ring in coords[1:]:
        inner_boundary = ET.SubElement(kml_polygon, 'innerBoundaryIs')
        inner_boundary_lr = ET.SubElement(inner_boundary, 'LinearRing')

        # Inner boundary coordinate string.
        coord_string = ''
        for coord_set in ring:
            coord_string += str(coord_set[0]) + "," + str(coord_set[1]) + "," + str(coord_set[2]) + ' '
        ET.SubElement(inner_boundary_lr, 'coordinates').text = coord_string

    # Create polygon's 'extended data' attribute table.
    extended_data = ET.SubElement(placemark, 'ExtendedData')
    for cell in range(len(headers)):
        data = ET.SubElement(extended_data, 'Data', {'name': headers[cell]})
        ET.SubElement(data, 'displayName').text = str(headers[cell])
        ET.SubElement(data, 'value').text = str(attributes[cell])

    return placemark


def point_style(name, icon="http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png", color=('#ffff00', 100), scale=1.2,
                label_color=('#ffffff', 100), label_size=1.0):
    """Creates a KML element of a point style.

    Parameters
    ----------
    name : str
    icon : str
    color : tuple[str, int]
    scale : float
    label_color : tuple[str, int]
    label_size : float

    Returns
    -------
    object
        An element tree branch representing a KML point style.

    Notes
    -----
    Icons: http://kml4earth.appspot.com/icons.html

    Examples
    ________
    Red square icon

    style for home plate
    hp_style = point_style('Bases Style', 'http://maps.google.com/mapfiles/kml/shapes/placemark_square.png', ('f2392c', 100))

    """
    style = ET.Element("Style", id=name)
    icon_style = ET.SubElement(style, "IconStyle")
    ET.SubElement(icon_style, "color").text = kml_color(*color)
    ET.SubElement(icon_style, "scale").text = str(scale)

    icon_icon = ET.SubElement(icon_style, "Icon")
    ET.SubElement(icon_icon, "href").text = str(icon)

    label_style = ET.SubElement(style, "LabelStyle")
    ET.SubElement(label_style, "scale").text = str(label_size)
    ET.SubElement(label_style, "color").text = kml_color(*label_color)

    return style


def line_style(name, color=('#ff0000', 100), width=3.0, extrude_color=('#34c9eb', 35)):
    """Creates a KML element of a line style.

    Parameters
    ----------
    name : str
    color : tuple[str, int]
    width : float
    extrude_color : tuple[str, int]

    Returns
    -------
    object
        An element tree branch representing a KML line style.

    Examples
    --------
    Green line

    warning track line style
    wt_style = line_style('Warning Track Style', ('0ff563', 100))

    """

    style = ET.Element("Style", id=name)
    styled_line = ET.SubElement(style, "LineStyle")

    ET.SubElement(styled_line, "color").text = kml_color(*color)
    ET.SubElement(styled_line, "width").text = str(width)

    styled_extrude = ET.SubElement(style, "PolyStyle")
    ET.SubElement(styled_extrude, "color").text = kml_color(*extrude_color)

    return style


def polygon_style(name, color=('#03cafc', 40), outline_width=1.0, outline_color=('#fcdf03', 100)):
    """Creates a KML element of a polygon style.

    Parameters
    ----------
    name : str
    color : tuple[str, int]
    outline_width : float
    outline_color : tuple[str, int]

    Returns
    -------
    object
        An element tree branch representing a KML polygon style.

    Examples
    ________
    Create a polygon style with default styling
    poly_style('Bases Area Style')

    """

    style = ET.Element("Style", id=name)

    poly_color = ET.SubElement(style, "PolyStyle")
    ET.SubElement(poly_color, "color").text = kml_color(*color)

    outline = ET.SubElement(style, "LineStyle")
    ET.SubElement(outline, "color").text = kml_color(*outline_color)
    ET.SubElement(outline, "width").text = str(outline_width)

    return style


def folder(name, loose_items, description='', folder_collapsed=True, hidden=True):
    """Creates a KML element of a folder and fills it with specified KML elements.

    Parameters
    ----------
    name : str
    loose_items : list
    description : str
    folder_collapsed : bool
    hidden : bool
        A folder's visibility is set by the visibility of the contents within. The default is to have folders hidden so
        that empty folders are not visible. If an item gets added to a folder and the item is set to be visible, the
        containing folder will become visible even if it set to not be.

    Returns
    -------
    object
        An element tree branch representing a folder.

    Examples
    --------
    f = folder('Placemarks', [hp, wt, base_area], 'Sample placemarks.')

    """

    new_folder = ET.Element("Folder")
    ET.SubElement(new_folder, "name").text = str(name)
    ET.SubElement(new_folder, "description").text = str(description)

    collapsed = 0
    if folder_collapsed is False:
        collapsed = 1
    else:
        pass

    ET.SubElement(new_folder, "open").text = str(collapsed)

    # Set 'visibility' value
    visibility = 0
    if hidden is False:
        visibility = 1
    else:
        pass

    ET.SubElement(new_folder, 'visibility').text = str(visibility)

    for item in loose_items:
        ET.Element.append(new_folder, item)

    return new_folder


def kml(name, styles, features, description='', folder_collapsed=True):
    """Creates a KML string.

    Parameters
    ----------
    name : str
    styles : list
    features : list
    description : str
    folder_collapsed : bool

    Returns
    -------
    str
        A string of a kml file contents.

    Examples
    --------
    k = kml('Fenway Park', [hp_style, wt_style, bases_area_style], [f])

    """

    kml_doc = ET.Element('kml', {'xmlns': 'http://www.opengis.net/kml/2.2'})
    body = ET.SubElement(kml_doc, "Document")
    ET.SubElement(body, "name").text = str(name)
    ET.SubElement(body, "description").text = str(description)

    collapsed = 0
    if folder_collapsed is False:
        collapsed = 1
    else:
        pass

    ET.SubElement(body, "open").text = str(collapsed)

    for style in styles:
        ET.Element.append(body, style)
    for item in features:
        ET.Element.append(body, item)

    kml_string = '<?xml version="1.0" encoding="UTF-8"?>'
    kml_string += ET.tostring(kml_doc, encoding='unicode', method='xml')

    return kml_string
