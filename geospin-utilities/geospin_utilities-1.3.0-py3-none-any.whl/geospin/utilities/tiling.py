"""Create hexagonal tilings"""

import itertools
import warnings
from dataclasses import dataclass

import numpy as np
from shapely.geometry import Point, Polygon

SQRT_3 = np.sqrt(3)


@dataclass
class Hexagon:
    """
    Hexagon with corner on top and bottom, i.e. `pointy` hexagons.
    Flat hexagons are not yet supported.

    Parameters:
        :param int q:
            First axial coordinate of hexagon, i.e., the 'column' value.
            See http://www.redblobgames.com/grids/hexagons/#basics for an
            illustration of the axial coordinate system.
        :param int r:
            Second axial coordinate of hexagon, i.e., the 'row' value.
        :param float edge_length:
            Edge length of hexagon.
        :param str orientation:
            Orientation of the hexagon. Currently only 'pointy' is supported.

    Attributes:
        :param float x:
            x position of hexagon center
        :param float y:
            y position of hexagon center
        :param str id:
            Identifier of hexagon. The identifier is comprised of the `q`
            and `r` coordinate. E.g., for q=3 and r=-4, the `self.id = '3,-4'`.
    """

    q: int = 0
    r: int = 0
    edge_length: float = 1.0
    orientation: str = 'pointy'

    def __post_init__(self):
        self.x, self.y = hex2cart(self.q, self.r, self.edge_length)
        self.id = f'{self.q},{self.r}'

        if self.orientation != 'pointy':
            raise NotImplementedError(f"Orientation {self.orientation} not yet "
                                      f"supported!")

    @property
    def center(self):
        """Shapely `Point` with center of hexagon in cartesian coordinates"""
        return Point(self.x, self.y)

    @property
    def boundary(self):
        """
        Shapely `Polygon` of hexagon boundaries in cartesian coordinates.
        """
        if self.orientation == 'pointy':
            degrees = [30, 90, 150, 210, 270, 330]
        elif self.orientation == 'flat':
            degrees = [0, 60, 120, 180, 240, 300]
        else:
            raise ValueError(f"Orientation {self.orientation} not known. "
                             f"Choose 'pointy' or 'flat'.")
        rads = np.deg2rad(degrees)
        xs = self.edge_length * np.cos(rads) + self.x
        ys = self.edge_length * np.sin(rads) + self.y
        polygon = Polygon(
            [(x, y) for x, y in zip(xs, ys)]
        )
        return polygon


class Tiling:
    """
    Ring-wise tiling of space with hexagons

    Hexagonal tilings can be used to patch `h3` functions:

    Say we want to test a function `fill_rectangle` that gets all H3 IDs of
    hexagons that are inside a rectangle. With `h3`, we fill a geometry using
    `h3.polyfill`. But we want to test `fill_rectangle` without requiring `h3`.
    `Tiling` can be used to path H3 functions.

    Here's the definition of fill rectangle:
    >>> from h3 import h3
    >>> import shapely.geometry
    >>> def fill_rectangle(minx, miny, maxx, maxy, resolution=9):
    ...     box = shapely.geometry.box(minx=minx, miny=miny, maxx=maxx,
    ...                                maxy=maxy)
    ...     geo_json = shapely.geometry.mapping(box)
    ...     hex_ids = h3.polyfill(geo_json, res=resolution,
    ...                           geo_json_conformant=True)
    ...     return hex_ids
    >>> sorted(fill_rectangle(minx=0, miny=0, maxx=0.005, maxy=0.005))
    ['89754e64d23ffff', '89754e64d27ffff', '89754e64d2bffff', '89754e64d2fffff']

    For testing, it is difficult to know what H3 hex IDs will be returned and
    this might change when `h3` changes. So let's patch `h3.polyfill` using a
    `pytest` fixture with `monkepatch`.
    >>> import pytest
    >>> @pytest.fixture
    ... def patch_h3_polyfill(monkeypatch):
    ...     tiling_ = Tiling(n_rings=10,
    ...                            edge_length=EDGE_LENGTH)
    ...     def mock_polyfill(geo_json, res, geo_json_conformant):
    ...         geometry = shapely.geometry.asShape(geo_json)
    ...         return tiling_.get_ids_of_hexagons_with_center_inside_geometry(
    ...                  geometry)
    ...     monkeypatch.setattr(h3, 'polyfill', mock_polyfill)

    Now we can write a test function that does not use `h3` at all and thus
    allows for systematic testing. Note that we use a small edge length,
    because we typically work in WGS 84 projection (so LAT, LON). Our
    approach is to use a hexagonal tiling so small that angles can be
    converted to distances by simple multiplication with the earth radius.
    This way we don't need to bother about projections in the test. So here
    all coordinates are angles, but it doesn't really matter.
    >>> EDGE_LENGTH = 1e-6
    >>> def test_fill_rectangle(patch_h3_polyfill):
    ...     # Note that we don't expect the center ID to be part of it,
    ...     # because it only touches the lower left corner but is not
    ...     # contained.
    ...     expected = ['1,-1']
    ...     result = fill_rectangle(
    ...         minx=0, miny=0, maxx=1.8*EDGE_LENGTH, maxy=1.8*EDGE_LENGTH)
    ...     assert sorted(expected) == sorted(result)
    """

    def __init__(self, n_rings=1, edge_length=1.):
        """
        :param int n_rings:
            Number of rings around `q = 0, r = 0`.
            `n_ring=0` returns only the center hexagon.
            See `get_hexagonal_tiling` for details.
        :param float edge_length:
            Edge length of each hexagon in the hexagonal tiling.
        """
        self.n_rings = n_rings
        self.edge_length = edge_length
        self.hexagons = [
            Hexagon(q=q, r=r, edge_length=edge_length)
            for (q, r) in get_hexagonal_tiling(n_rings)
        ]

    def get_ids_of_hexagons_with_center_inside_geometry(self, geometry):
        """
        Get IDs of all hexagons whose centers are within provided geometry.

        Useful to patch `h3.polyfill`.

        :param shapely.geometry.Polygon or shapely.geometry.MultiPolygon:
            Geometry to fill.
        :return List[str] hex_ids:
            List of hexagon IDs
        """
        hex_ids = [
            hexagon.id for hexagon in self.hexagons if
            hexagon.center.within(geometry)
        ]
        return hex_ids

    def get_ids_of_hexagons_with_boundaries_inside_geometry(self, geometry):
        warnings.warn(
            "get_ids_of_hexagons_with_boundaries_inside_geometry is an "
            "experimental untested method!")
        hex_ids = [
            hexagon.id for hexagon in self.hexagons if
            hexagon.boundary.within(geometry)
        ]
        return hex_ids

    def get_ids_of_hexagons_intersected_by_geometry(self, geometry):
        warnings.warn(
            "get_ids_of_hexagons_intersected_by_geometry is an "
            "experimental untested method!")
        hex_ids = [
            hexagon.id for hexagon in self.hexagons if
            hexagon.boundary.intersects(geometry)
        ]
        return hex_ids


def get_hexagonal_tiling(n_rings):
    """
    Return axial coordinates of hexagons arranged in rings.

    See http://www.redblobgames.com/grids/hexagons/#basics for
    an illustration of the axial coordinate system.

    :param int n_rings:
        Number of rings around the center. `n_rings=0` contains only the center.
    :return ndarray axial_coordinates:
        Axial coordinates of shape
        `(N, 2)` where `N = 1 + 3 n_rings (n_rings - 1)`.
    """
    a = np.arange(-n_rings + 1, n_rings)
    axial_coordinates = []
    for x, y, z in itertools.product(a, repeat=3):
        if x + y + z == 0:
            axial_coordinates.append([x, y])
    axial_coordinates = np.array(axial_coordinates)
    return axial_coordinates


def spacing2edgelength(spacing):
    """
    :param float spacing:
        Distance between two hexagon centers in a hexagonal grid.
    :return float:
        Edge length of hexagons in a grid of spacing `spacing`.
    """
    return spacing / SQRT_3


def edgelength2spacing(edge_length):
    """
    :param float edge_length:
        Edge length of hexagon.
    :return float:
        Distance between two hexagon centers (i.e., spacing) in a grid of
        hexagons of edge length `edgelength`.
    """
    return SQRT_3 * edge_length


def hex2cart(q, r, edge_length):
    """
    Convert hexagonal coordinate in axial representation to cartesian coordinate

    :param float q: 'Column' value of hexagonal coordinate.
    :param float r: 'Row' value of hexagonal coordinate.
    :param float edge_length: Edge length of hexagon.
    :return tuple (x, y): Tuple of cartesian coordinates.
    """
    x = SQRT_3 * edge_length * (q + r / 2.)
    y = - edge_length * r * 3 / 2.
    return x, y


def cart2hex(x, y, edge_length):
    """
    Convert cartesian coordinate to hexagonal coordinate in axial representation

    Inverse of `hex2cart`.

    :param float x: x coordinate
    :param float y: y coordinate
    :param float edge_length: Edge length of hexagon
    :return tuple (q, r): Tuple of hexagonal coordinates
    """
    q = (SQRT_3 * x + y) / (3 * edge_length)
    r = - 2 * y / (3 * edge_length)
    return q, r
