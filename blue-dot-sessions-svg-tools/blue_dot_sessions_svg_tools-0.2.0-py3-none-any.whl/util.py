import logging
import typing
import math

Dim1FloatType = typing.List[float]
Dim2FloatType = typing.List[Dim1FloatType]
Dim3FloatType = typing.List[Dim2FloatType]


module_logger = logging.getLogger(__name__)

__all__ = [
    "dist",
    "slope",
    "calc_sin_theta",
    "calc_cos_theta",
    "rotate",
    "calc_centroid"
]


def dist(xy1: Dim1FloatType, xy2: Dim1FloatType) -> float:
    return math.sqrt((xy2[1] - xy1[1])**2 +  (xy2[0] - xy1[0])**2)


def slope(xy1: Dim1FloatType, xy2: Dim1FloatType) -> float:
    return (xy2[1] - xy1[1])/(xy2[0] - xy1[0])


def calc_sin_theta(xy1: Dim1FloatType, xy2: Dim1FloatType) -> float:
    hyp = dist(xy1, xy2)
    return (xy2[1] - xy1[1]) / hyp


def calc_cos_theta(xy1: Dim1FloatType, xy2: Dim1FloatType) -> float:
    hyp = dist(xy1, xy2)
    return (xy2[0] - xy1[0]) / hyp


def rotate(xy: Dim1FloatType, sin_theta: float, cos_theta: float) -> Dim1FloatType:
    """
    cos(theta) -sin(theta)
    sin(theta) cos(theta)
    """
    return [xy[0]*cos_theta - xy[1]*sin_theta,
            xy[0]*sin_theta + xy[1]*cos_theta]


def calc_centroid(vertices: Dim2FloatType) -> Dim1FloatType:
    """
    Calculate the centroid of some polygon

    Using formula from https://en.wikipedia.org/wiki/Centroid#Of_a_polygon
    """
    vertices_copy = vertices.copy()
    vertices_copy.append(vertices[0])
    area = 0.0
    Cx = 0.0
    Cy = 0.0

    module_logger.debug(f"_calc_centroid: vertices={vertices}")

    for idx in range(len(vertices_copy) - 1):
        xi, yi = vertices_copy[idx]
        xpi, ypi = vertices_copy[idx + 1]

        intermediate = xi*ypi - xpi*yi
        Cx += (xi + xpi)*intermediate
        Cy += (yi + ypi)*intermediate
        area += intermediate

    # area /= 2.0
    Cx /= 3.0*area
    Cy /= 3.0*area
    return [Cx, Cy]
