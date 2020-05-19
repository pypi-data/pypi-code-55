try:
    import h3

    h3.k_ring('841e265ffffffff', 4)
except AttributeError:
    from h3 import h3

import logging
import time

import pyproj
import shapely
import shapely.ops
import shapely.wkt

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def buffer_polygon(polygon, buffer_size,
                   source_crs='epsg:4326',
                   buffering_crs='epsg:3035'):
    """
    Create a buffer around the given polygon and return it.

    :param shapely.geometry.Polygon polygon: A polygon
    :param int buffer_size: Size of the buffer in meters
    :param str source_crs: Source CRS of the polygon
    :param str buffering_crs: CRS used to calculate the buffer. Must
        be metric, measured in meter. Will not be checked!
    :return shapely.geometry.Polygon poly:
        The buffered polygon
    """
    # transform to metric crs
    # https://gis.stackexchange.com/questions/127427/transforming-shapely
    # -polygon-and-multipolygon-objects
    projection = pyproj.Transformer.from_proj(
        pyproj.Proj(init=source_crs),
        pyproj.Proj(init=buffering_crs)
    )
    polygon_metric = shapely.ops.transform(projection.transform, polygon)
    # add buffer
    # https://gis.stackexchange.com/questions/97963/how-to-surround-a-polygon
    # -object-with-a-corridor-of-specified-width/97964
    polygon_metric = polygon_metric.buffer(distance=buffer_size)
    # transform back to origin crs
    projection = pyproj.Transformer.from_proj(
        pyproj.Proj(init=buffering_crs),
        pyproj.Proj(init=source_crs)
    )
    poly = shapely.ops.transform(projection.transform, polygon_metric)
    return poly


class PolyFiller:
    """
    Fill polygons and multipolygons with H3 hexagons.

    This extends upon H3's ``polyfill`` function in the following ways:
    * Geometries can be specified in different formats
    * Multipolygons are supported
    * Whether or not hexagons at the geometry boundaries are included or
    excluded can be specified

    .. note::
        If geometry is a single polygon in GeoJSON format and no buffering is
        desired one can use `polyfill` from H3 directly (more efficient,
        because no shape transformation is required).
    """

    def __init__(self,
                 resolution=9,
                 add_hex_id_if='center_within_buffer',
                 source_crs='epsg:4326',
                 buffer_crs='epsg:3035'):
        """
        :param int resolution:
            Resolution of H3 hexagons that should fill the polygon
        :param str add_hex_id_if:
            Choose 'center_within_buffer' or 'center_contained'.

            For 'center_contained', only hex IDs whose centers are within the
            provided geometry are returned by `fill()`.

            For 'center_within_buffer', a buffer is added to the geometry that
            is to be filled. This buffer is slightly smaller than the average
            distance between two centers. Note that the distance between two
            centers is different at different locations because the sizes of
            H3 hexagons vary. If the distance were constant, it would
            suffice to choose the buffer size equal to the edge length. Here
            we make it `1.73 x edge length`. The rationale is this: Making it
            larger leads to less hex IDs that are missed. Making it smaller
            than `sqrt(3) x edge length` avoids adding too many hex IDs that
            are outside the given polygons. However, this does not guarantee
            that no hex IDs are missed if the edge length varies by more than
            1.73 in the area of the provided geometries. Neither does it
            guarantee that no unnecessary hexagons are added at the boundary
            (indeed, this is very likely to happen).

        :param str source_crs:
            Coordinate reference system of `geometry`. Not needed,
            if `geometry` is a GeoJson dictionary
        :param str buffering_crs:
            Coordinate reference system used for buffering. The default 3035 is
            accurate in Europe.
        """
        self.resolution = resolution
        self.add_hex_id_if = add_hex_id_if
        self.source_crs = source_crs
        self.buffer_crs = buffer_crs

    def fill(self, geometry):
        """
        Return list of hex IDs that are inside `geometry`.

        :param geometry:
            Representation of a polygon or a multipolygon. This can either be a
            GeoJson dictionary, a WKT string or a shapely geometry.
        :type geometry:
            dict or str or shapely.geometry.Polygon or
            shapely.geometry.MultiPolygon
        :return list: List of H3 hex IDs.
        """
        hex_ids = []
        polygons = self._get_list_of_polygons_in_geometry(geometry)
        for polygon in polygons:
            hex_ids.extend(self._fill_polygon(polygon))
        return list(set(hex_ids))

    def _fill_polygon(self, polygon):
        """
        :param shapely.geometry.Polygon polygon:
        :return list:
            List of hex IDs inside ``polygon``
        """
        # Convert shapely object to geojson
        geo_json = shapely.geometry.mapping(polygon)
        hex_ids = h3.polyfill(geo_json, res=self.resolution,
                              geo_json_conformant=True)
        return hex_ids

    def _buffer_polygon(self, polygon):
        """
        Apply different buffering schemes specified by `self.add_hex_id_if`.

        :param shapely.geometry.Polygon polygon:
        :return shapely.geometry.Polygon buffered_polygon:
            A buffered polygon
        """
        if self.add_hex_id_if == 'center_within_buffer':
            buffer_size = 1.73 * h3.edge_length(self.resolution, 'm')
            buffered_polygon = buffer_polygon(
                polygon, buffer_size, source_crs=self.source_crs,
                buffering_crs=self.buffer_crs)
        elif self.add_hex_id_if == 'contained':
            raise NotImplementedError
        else:
            raise ValueError('Buffering scheme not known.')

        return buffered_polygon

    @staticmethod
    def _convert_geometry_to_shape(geometry):
        """
        :return shape.geometry.base.BaseGeometry:
            Shapely geometry based on representation specified in `geometry`.
            See `fill()` for details.
        """
        if isinstance(geometry, str):
            shape = shapely.wkt.loads(geometry)
        elif isinstance(geometry, dict):
            shape = shapely.geometry.asShape(geometry)
        elif isinstance(geometry, shapely.geometry.base.BaseGeometry):
            # No conversion for shapely geometries
            shape = geometry
        else:
            raise ValueError('Geometry is in invalid format.')
        return shape

    def _get_list_of_polygons_in_geometry(self, geometry):
        """
        :return list: List of shapely Polygons that comprise `geometry`
        """
        shape = PolyFiller._convert_geometry_to_shape(geometry)

        # 'center-contained' does not require buffering
        if self.add_hex_id_if == 'center_contained':
            shape = shape
        elif self.add_hex_id_if == 'center_within_buffer':
            shape = self._buffer_polygon(shape)
        else:
            raise NotImplementedError(
                f"Method '{self.add_hex_id_if}' not implemented")

        if isinstance(shape, shapely.geometry.Polygon):
            polygons = [shape]
        elif isinstance(shape, shapely.geometry.MultiPolygon):
            polygons = shape
        else:
            raise ValueError('shape must be Polygon or MultiPolygon')
        return polygons


class RoadNetworkPolyFiller():
    """
    Fill geometry with H3 hexagons that are close to roads.

    This is an extension of the h3 polyfill function that fills only areas
    which are within a buffer around the road network.

    Note: The road network is extracted from a PostgreSQL database which is
        created using `osm2pqsql`.

    :param geospin.utilities.backend.DatabaseBackend osm_db_backend: The backend
        to the OSM database containing the table `planet_osm_line`.
    :param int buffer_size: Buffer size to put around the road network (meters).
    :param int resolution: The H3 resolution.
    :param int chunk_resolution: The resolution of chunk hexagons.
    :param int buffer_epsg: Coordinate reference system code used for buffering.
        Must be metric. The default is accurate in Europe.
    """

    def __init__(self, osm_db_backend, buffer_size, resolution,
                 chunk_resolution=6,
                 buffer_epsg=3035):
        self.osm_db_backend = osm_db_backend
        self.buffer_size = buffer_size
        self.buffer_epsg = buffer_epsg
        self.resolution = resolution
        self.chunk_resolution = chunk_resolution

        self.road_network_view_name = 'road_network'
        self.buffered_road_network_view_name = 'buffered_road_network'

    def _create_road_network_view(self, bounding_polygon):
        """Create a view of the road network within a bounding polygon.

        The lines in the `planet_osm_lines` are filtered by comparing the
        highway and access values with a whitelist.

        :param shapely.geometry.Polygon bounding_polygon:
        """
        highway_whitelist = ['motorway', 'motorway_link', 'trunk',
                             'trunk_link', 'primary', 'primary_link',
                             'secondary', 'secondary_link', 'tertiary',
                             'tertiary_link', 'residential', 'living_street',
                             'unclassified', 'service', 'pedestrian']
        access_whitelist = ['yes', 'motorcar', 'motor_vehicle', 'vehicle',
                            'permissive', 'hov', 'delivery',
                            'destination', 'customers', 'private', 'psv',
                            'emergency']
        vehicle_whitelist = ['yes', 'private', 'permissive', 'destination']
        motor_vehicle_whitelist = ['yes', 'private', 'permissive',
                                   'destination']

        with self.osm_db_backend.engine.connect() as conn:
            sql = f"""CREATE OR REPLACE VIEW {self.road_network_view_name} AS
            (SELECT
                ol.way AS geom
            FROM
                STRING_TO_ARRAY('{';'.join(highway_whitelist)}', ';')
                    AS highway_whitelist,
                STRING_TO_ARRAY('{';'.join(access_whitelist)}', ';')
                    AS access_whitelist,
                STRING_TO_ARRAY('{';'.join(vehicle_whitelist)}', ';')
                    AS vehicle_whitelist,
                STRING_TO_ARRAY('{';'.join(motor_vehicle_whitelist)}', ';')
                    AS motor_vehicle_whitelist,
                ST_Transform(
                    ST_GeomFromText('{bounding_polygon.wkt}', 4326), 3857)
                    AS bounds
            INNER JOIN planet_osm_line AS ol
            ON ST_Intersects(bounds, ol.way)
            WHERE
                ol.highway = ANY(highway_whitelist)
                OR ol.access = ANY(access_whitelist)
                OR (exist(ol.tags, 'vehicle')
                    AND ol.tags->'vehicle' = ANY(vehicle_whitelist))
                OR (exist(ol.tags, 'motor_vehicle')
                    AND ol.tags->'motor_vehicle' = ANY(motor_vehicle_whitelist))
            )
            """
            logger.info(' Create road network view ...')
            conn.execute(sql)

    def _drop_road_network_view(self):
        logger.info(' Drop road network view ...')
        with self.osm_db_backend.engine.connect() as conn:
            sql = f"DROP VIEW {self.road_network_view_name};"
            conn.execute(sql)

    def _fetch_buffered_road_network(self):
        """Fetch geometry of buffered road network given a road network view.

        The buffer radius is given by the sum of (a) the user passed buffer
        size and (b) the H3 edge length at the given resolution times 1.73.
        The latter ensures that the whole buffered region will be covered
        with hexagons. At least in Europe a factor of 1.73 should be enough,
        see documentation of `PolyFiller` for details.

        :return str: Returns the WKT of the buffered road network geometry.
        """
        full_buffer_size = (
                self.buffer_size +
                1.73 * h3.edge_length(self.resolution, unit='m'))
        with self.osm_db_backend.engine.connect() as conn:
            sql = f"""
            SELECT
                ST_AsText(
                    ST_Transform(
                            ST_Buffer(
                                ST_Transform(
                                        ST_Union(rn.geom),
                                        {self.buffer_epsg}),
                                {full_buffer_size}),
                            4326))
            FROM
                {self.road_network_view_name} as rn
            """
            logger.info(' Fetch buffered road network ...')
            result = conn.execute(sql).first()

        return result[0]

    def fill(self, geometry):
        """
        Fill geometry with hexagons that are close to roads.

        The filling will be done in chunks: the geometry is sub-sampled into
        smaller areas by using H3 polyfill at a resolution that is lower than
        the fill resolution.

        Note: The area is fully covered but there will be hexagons extending
            beyond the bounds of the geometry.

        :param shapely.geometry.Polygon, shapely.geometry.MultiPolygon geometry:
            Geometry to fill.
        :return list(str) hex_ids: List of hex IDs.
        """
        chunk_geometries = self._get_chunk_geometries(geometry)
        n_chunks = len(chunk_geometries)
        logger.info(f'Found #{n_chunks} chunks.')

        poly_filler = PolyFiller(self.resolution,
                                 add_hex_id_if='center_contained')
        hex_ids = set()
        for index, chunk_geometry in enumerate(chunk_geometries, 1):
            logger.info(
                f'Start with ({index}/{n_chunks})...')
            start_time = time.time()

            self._create_road_network_view(chunk_geometry)
            road_network_geom = self._fetch_buffered_road_network()

            if road_network_geom:
                hex_ids_in_chunk = poly_filler.fill(road_network_geom)
                hex_ids.update(hex_ids_in_chunk)
                logger.info(
                    f'Found #{len(hex_ids_in_chunk)} matching hex IDs. Done '
                    f'in {time.time() - start_time} sec.')
            else:
                logger.info('Found no hex IDs in this chunk.')

        self._drop_road_network_view()
        return list(hex_ids)

    def _get_chunk_geometries(self, geometry):
        """
        Get geometries of each chunk hexagon that intersects with `geometry`

        :param geometry: See `fill` method
        :return List[shapely.geometry.Polygon]:
        """
        chunker = PolyFiller(self.chunk_resolution,
                             add_hex_id_if='center_within_buffer')
        chunk_hex_ids = chunker.fill(geometry)
        chunk_geometries = []
        for chunk_hex_id in chunk_hex_ids:
            chunk_boundaries = h3.h3_to_geo_boundary(chunk_hex_id, True)
            chunk_geometry = shapely.geometry.asPolygon(chunk_boundaries)
            chunk_geometries.append(chunk_geometry)
        return chunk_geometries
