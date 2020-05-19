"""A place to keep standard geometries an associated functions."""

import os
from urllib.parse import urlparse
from urllib.parse import uses_netloc, uses_params, uses_relative

import geopandas as gpd
import shapely.geometry
import shapely.wkt

from geospin.utilities.data.wkt import germany_coarse, germany_fine

_VALID_URLS = set(uses_relative + uses_netloc + uses_params)
_VALID_URLS.discard("")

NAMES_TO_AGS = dict(
    germany='00000000',
    stuttgart='08111000',
    cologne='05315000',
    munich='09162000',
    berlin='11000000',
    frankfurt='06412000',
    hamburg='02000000',
    hannover='03241001',
    duesseldorf='05111000',
    bremen='04011000',
    freiburg='08311000',
)


def _is_url(url):
    """Check to see if *url* has a valid protocol.

    Copied from geopandas.io.file
    """
    try:
        return urlparse(url).scheme in _VALID_URLS
    except Exception:
        return False


class Germany(object):
    """
    Contains methods to determine if a point is located within Germany.

    Coarse and fine boundaries were generated according to:
    https://gis.stackexchange.com/questions/183248/getting-polygon-boundaries-
    of-city-in-json-from-google-maps-api/192298#192298
    """

    def __init__(self, coarse=True):
        """
        Initialize the boundary of Germany.

        :param bool coarse: Whether to use the coarse boundary of Germany.
        """
        if coarse:
            self.boundary = shapely.wkt.loads(germany_coarse)
        else:
            self.boundary = shapely.wkt.loads(germany_fine)

    def contains(self, lat, lon):
        """
        Determine if a point is located within Germany.

        :param float lat: Latitude of the location.
        :param float lon: Longitude of the location.
        :return: Whether the point is contained within Germany or not.
        :rtype: bool
        """
        point = shapely.geometry.Point(lon, lat)

        for polygon in self.boundary:
            if polygon.contains(point):
                return True
        return False


class VG250GeometryParser:
    """
    Obtain geometries in Germany from the Federal Agency for Cartography.

    The data by the Federal Agency for Cartography is refered to as VG250.

    Example usages:
    >>> import os
    >>> from shapely.geometry import Point
    >>> from geospin.utilities.geometry import VG250GeometryParser
    >>> # Define data location
    >>> data_location = os.path.expanduser(
    ...     '~/geospin/data/vg250_2019-01-01.utm32s.shape.ebenen/vg250_ebenen')
    >>> # Get geometry of Germany
    >>> parser = VG250GeometryParser(data_location)
    >>> germany = parser.get_geometry(identifier='00000000')
    >>> point_in_freiburg = Point(7.844821, 47.988375)
    >>> germany.contains(point_in_freiburg)
    True
    >>> # Get geometry of the city of Stuttgart by AGS code
    >>> stuttgart = parser.get_geometry(identifier='08111000')
    >>> stuttgart.contains(point_in_freiburg)
    False
    >>> point_in_stuttgart = Point(9.180604, 48.777996)
    >>> stuttgart.contains(point_in_stuttgart)
    True
    >>> # Get geometry of the city of Stuttgart by name
    >>> stuttgart_2 = parser.get_geometry(identifier='stuttgart')
    >>> stuttgart.equals(stuttgart_2)
    True
    >>> # Names are in lower case English spelling
    >>> duesseldorf = parser.get_geometry(identifier='duesseldorf')
    >>> point_in_duesseldorf = Point(6.784500, 51.229493)
    >>> duesseldorf.contains(point_in_duesseldorf)
    True
    >>> # Use a URL instead of a local file
    >>> url = (
    ... 'https://sgx.geodatenzentrum.de/wfs_vg250?service=wfs&version=2.0.0')
    >>> parser = VG250GeometryParser(data_location=url)
    >>> duesseldorf = parser.get_geometry(identifier='duesseldorf')
    >>> duesseldorf.contains(point_in_duesseldorf)
    True
    """

    def __init__(self, data_location, names_to_ags=NAMES_TO_AGS):
        """
        :param str data_location:
             One of:
               - Path to location of folder `vg250_ebenen` that contains `shp`
              files.
              - The URL to a Web Feature Service (WFS). Pass e.g.
              https://sgx.geodatenzentrum.de/wfs_vg250?service=wfs&version=2.0.0
              for the WFS of the Federal Agency for Cartography.
        :param dict names_to_ags:
            Dictionary with region names (e.g., 'duesseldorf') as keys and
            AGS codes as values.
        """
        self.data_location = data_location
        self.names_to_ags = names_to_ags

    def _identifier_to_ags_code(self, identifier):
        """Transform identifier to AGS code"""
        if identifier in self.names_to_ags.keys():
            ags_code = self.names_to_ags[identifier]
        elif len(identifier) == 8:
            ags_code = identifier
        else:
            raise ValueError('Given region identifier is neither a known '
                             'region name nor a valid AGS.')

        return ags_code

    def get_geometry(self, identifier='00000000'):
        """
        Get geometry of region specified by identifier

        :param str identifier:
            String of 8 digit AGS code or region name. See
            www.wikipedia.org/wiki/Community_Identification_Number#Germany
            for AGS codes.
            For convenience, some regions can be referred to by name in
            lowercase English spelling. The name has to exist in
            `self.names_to_ags`.
            Use
            https://www.statistikportal.de/de/produkte/gemeindeverzeichnis
            to find AGS for regions.
        :return geometry:
            Geometry of region specified by `identifier`.
        :rtype:
            shapely.geometry.Polygon or shapely.geometry.MultiPolygon
        """
        ags_code = self._identifier_to_ags_code(identifier)

        admin_level_suffix = self._get_admin_level_suffix_from_ags_code(
            ags_code)

        if _is_url(self.data_location):
            filename = \
                self.data_location + \
                f'&request=GetFeature&TYPENAME=VG250_{admin_level_suffix}' \
                f'&SRSNAME=EPSG:4326'
        else:
            filename = os.path.join(self.data_location,
                                    f'VG250_{admin_level_suffix}.shp')

        gdf = gpd.read_file(filename)
        gdf['AGS_0'] = gdf['AGS_0'].map(lambda x: str(x).zfill(8))
        gdf_in_region = gdf[(gdf['AGS_0'] == ags_code) & (gdf['GF'] == 4)]
        gdf_in_region = gdf_in_region.to_crs('epsg:4326')
        if len(gdf_in_region['geometry']) == 1:
            geometry = (gdf_in_region['geometry']).iloc[0]
        else:
            raise ValueError(
                'Given AGS contains more than one geometry. Consider using '
                '`unary_union` to unite them.')
        return geometry

    @staticmethod
    def _get_admin_level_suffix_from_ags_code(ags_code):
        """
        Return the file suffix for different administrative levels

        :param str ags_code:
            A valid AGS (= Amtlicher Gemeindeschlüssel) code.
        :return str suffix:
            The suffix for the administrative level.
        """
        ags_code_as_integer = int(ags_code)
        if ags_code_as_integer == 0:
            suffix = 'STA'
        elif ags_code_as_integer % 1e6 == 0:
            suffix = 'LAN'
        elif ags_code_as_integer % 1e5 == 0:
            suffix = 'RBZ'
        elif ags_code_as_integer % 1e3 == 0:
            suffix = 'KRS'
        else:
            suffix = 'GEM'

        return suffix
