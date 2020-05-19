import numpy as np
import pytest
import shapely
from shapely.geometry import Point, Polygon

import geospin.utilities.tiling as tiling

EDGE_LENGTH_AT_SPACING_1 = tiling.spacing2edgelength(1)
SPACING_AT_EDGE_LENGTH_1 = tiling.edgelength2spacing(1)


def test_hexagon_initialization():
    hexagon = tiling.Hexagon(q=0, r=0, edge_length=2.)
    assert hexagon.edge_length == 2.


def test_hexagon_boundary():
    edge_length = 2.
    hexagon = tiling.Hexagon(q=1, r=-1, edge_length=edge_length)
    half_spacing = tiling.edgelength2spacing(edge_length) / 2.
    points_before_shift = np.array(
        [
            [half_spacing, 1],
            [0, 2],
            [-half_spacing, 1],
            [-half_spacing, -1],
            [0, -2],
            [half_spacing, -1]
        ]
    )
    expected = Polygon(
        points_before_shift +
        np.array([SPACING_AT_EDGE_LENGTH_1, 1.5 * edge_length]))
    result = hexagon.boundary
    assert expected.almost_equals(result)


def test_get_hexagonal_tiling():
    n_rings = 4
    expected = np.array(
        [
            # Center
            [0, 0],

            # First ring
            [1, 0], [0, 1], [-1, 1], [-1, 0], [0, -1], [1, -1],

            # Second ring
            [2, 0], [1, 1], [0, 2], [-1, 2], [-2, 2], [-2, 1], [-2, 0],
            [-1, -1], [0, -2], [1, -2], [2, -2], [2, -1],

            # Third ring
            [3, 0], [2, 1], [1, 2], [0, 3], [-1, 3], [-2, 3], [-3, 3],
            [-3, 2], [-3, 1], [-3, 0], [-2, -1], [-1, -2], [0, -3],
            [1, -3], [2, -3], [3, -3], [3, -2], [3, -1],
        ]
    )
    expected = np.sort(expected, axis=0)
    result = np.sort(tiling.get_hexagonal_tiling(n_rings), axis=0)
    np.testing.assert_array_equal(result, expected)


@pytest.mark.parametrize(
    'q, r, expected_x, expected_y',
    [
        # Center location
        (0, 0, 0, 0),
        # First ring
        (1, 0, SPACING_AT_EDGE_LENGTH_1, 0),
        (0, 1, 0.5 * SPACING_AT_EDGE_LENGTH_1, -1.5),
        (-1, 1, -0.5 * SPACING_AT_EDGE_LENGTH_1, -1.5),
        (-1, 0, -SPACING_AT_EDGE_LENGTH_1, 0),
        (0, -1, -0.5 * SPACING_AT_EDGE_LENGTH_1, 1.5),
        (1, -1, 0.5 * SPACING_AT_EDGE_LENGTH_1, 1.5),
    ]
)
def test_hex2cart(q, r, expected_x, expected_y):
    result_x, result_y = tiling.hex2cart(q, r, edge_length=1.)
    assert pytest.approx(expected_x) == result_x
    assert pytest.approx(expected_y) == result_y


@pytest.mark.parametrize(
    'x, y, expected_q, expected_r',
    [
        # Center location
        (0, 0, 0, 0),
        # First ring
        (SPACING_AT_EDGE_LENGTH_1, 0, 1, 0),
        (0.5 * SPACING_AT_EDGE_LENGTH_1, 1.5, 1, -1),
        (-0.5 * SPACING_AT_EDGE_LENGTH_1, 1.5, 0, -1),
        (-SPACING_AT_EDGE_LENGTH_1, 0, -1, 0),
        (-0.5 * SPACING_AT_EDGE_LENGTH_1, -1.5, -1, 1),
        (0.5 * SPACING_AT_EDGE_LENGTH_1, -1.5, 0, 1),
    ]
)
def test_cart2hex(x, y, expected_q, expected_r):
    result_q, result_r = tiling.cart2hex(x, y, edge_length=1.)
    assert pytest.approx(expected_q) == result_q
    assert pytest.approx(expected_r) == result_r


def test_tiling():
    tiling_ = tiling.Tiling(n_rings=4)
    assert len(tiling_.hexagons) == 37


def test_polyfill_center_only():
    geometry = Point(0, 0).buffer(0.5)
    tiling_ = tiling.Tiling(n_rings=10)

    expected = ['0,0']
    result = tiling_.get_ids_of_hexagons_with_center_inside_geometry(geometry)

    assert expected == result


def test_polyfill_first_ring():
    geometry = Point(0, 0).buffer(SPACING_AT_EDGE_LENGTH_1 + 0.1)
    tiling_ = tiling.Tiling(n_rings=10, edge_length=1.)

    expected = ['0,0', '1,0', '1,-1', '0,-1', '-1,0', '-1,1', '0,1']
    result = tiling_.get_ids_of_hexagons_with_center_inside_geometry(geometry)

    assert sorted(expected) == sorted(result)


def test_polyfill_bounding_box_right():
    geometry = shapely.geometry.box(
        -0.1, -0.1, 2 * SPACING_AT_EDGE_LENGTH_1 + 0.1, 4.1)

    tiling_ = tiling.Tiling(n_rings=10, edge_length=1.)
    expected = ['0,0', '1,0', '2,0', '1,-1', '2,-1', '1,-2', '2,-2', '3,-2']

    result = tiling_.get_ids_of_hexagons_with_center_inside_geometry(geometry)
    assert sorted(expected) == sorted(result)
