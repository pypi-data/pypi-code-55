import logging
import typing
import shutil
import math
import random
import logging
import xml.etree.ElementTree as ET

from .util import Dim1FloatType, Dim2FloatType, Dim3FloatType
from . import util

module_logger = logging.getLogger(__name__)

__all__ = [
    "added_vertices_polygon",
    "jagged_line_polygon",
    "rounded_corner_polygon",
    "curved_paths2svg",
    "straight_paths2svg",
    "added_vertices_polygon2svg",
    "jagged_line_polygon2svg",
    "rounded_corner_polygon2svg",
    "modify_svg",
    "polygon2svg_lookup"
]


def added_vertices_polygon(
    vertices_flat: Dim1FloatType,
    vertices_per_side: int,
    convex_concave_factor: float
) -> Dim2FloatType:
    module_logger.debug(f"added_vertices_polygon: vertices_per_side={vertices_per_side}")
    module_logger.debug(f"added_vertices_polygon: convex_concave_factor={convex_concave_factor}")

    vertices: Dim2FloatType = [vertices_flat[idx:idx+2] for idx
                              in range(0, len(vertices_flat), 2)]
    module_logger.debug(f"added_vertices_polygon: vertices={vertices}")
    n_vertices = len(vertices)
    vertices_overlap = vertices.copy()
    vertices_overlap.append(vertices[0])

    paths = []

    # centroid = _calc_centroid(vertices)
    # module_logger.debug(f"added_vertices_polygon: centroid={centroid}")

    # def _find_intersection(l0: Dim1FloatType, l1: Dim1FloatType) -> Dim1FloatType:
    #     m0 = util.slope(l1, l0)
    #     m1 = -1.0 / m0
    #
    #     x0, y0 = l0
    #     x1, y1 = centroid.copy()
    #
    #     xi = (m0*x0 - m1*x1 + y1 - y0)/(m0 - m1)
    #     yi = m1*(xi - x1) + y1
    #     intersect = [xi, yi]
    #     module_logger.debug(f"_find_intersection: translated intersection: [{(xi):.2f}, {(yi):.2f}]")
    #     return intersect, util.dist(l0, intersect), util.dist(intersect, l1)
    #
    # fig, axes = plt.subplots(2, 2)
    # axes = axes.flatten()
    for idx in range(n_vertices):
        sl = vertices_overlap[idx: idx + 2]
        dist = util.dist(sl[0], sl[1])
        cos_theta = util.calc_cos_theta(sl[0], sl[1])
        sin_theta = util.calc_sin_theta(sl[0], sl[1])

        # start, end = sl[0].copy(), sl[1].copy()
        # mid_point = dist/2.0
        # _, pre_midpoint_incre, post_midpoint_incre = _find_intersection(start, end, axes[idx])
        # module_logger.debug(f"added_vertices_polygon: idx={idx}, "
        #                     f"dist={dist}, "
        #                     f"pre_midpoint_incre={pre_midpoint_incre:.2f}, "
        #                     f"post_midpoint_incre={post_midpoint_incre:.2f}")

        pre_rotate = [[0.0, 0.0]]

        x_val = 0.0
        y_val = 0.0

        half = int(vertices_per_side + 1) / 2
        x_incre = dist / (vertices_per_side + 1)

        for idy in range(1, vertices_per_side + 1):
            if idy >= half:
                # x_val += pre_midpoint_incre
                y_val += convex_concave_factor / idy
            else:
                # x_val += post_midpoint_incre
                y_val -= convex_concave_factor / idy
            x_val += x_incre
            # module_logger.debug(f"added_vertices_polygon: idx={idx}, [{x_val:.2f}, {y_val:.2f}]")
            _rot = util.rotate([x_val, 0.0], sin_theta, cos_theta)
            module_logger.debug(f"added_vertices_polygon: idx={idx},<circle cx=\"{(_rot[0] + sl[0][0]):.2f}\" cy=\"{(_rot[1] + sl[0][1]):.2f}\" r=\"2\"/>")
            pre_rotate.append(
                [x_val, y_val])

        for pair in pre_rotate:
            post_rotate = util.rotate(pair, sin_theta, cos_theta)
            paths.append([post_rotate[0] + sl[0][0], post_rotate[1] + sl[0][1]])
        # paths.append(sl[0])
        # paths.append(centroid)

    # plt.show()
    return paths


def jagged_line_polygon(
    vertices_flat: Dim1FloatType,
    noise: float
) -> Dim2FloatType:
    """
    Rotation Matrix:

    cos(theta) -sin(theta)
    sin(theta) cos(theta)

    """
    vertices: Dim2FloatType = [vertices_flat[idx:idx+2] for idx
                              in range(0, len(vertices_flat), 2)]
    n_vertices = len(vertices)
    vertices_overlap = vertices.copy()
    vertices_overlap.append(vertices[0])

    paths = []

    for idx in range(n_vertices):

        sl = vertices_overlap[idx: idx + 2]
        pre_rotate = [[0.0, 0.0]]
        dist = util.dist(sl[0], sl[1])
        cos_theta = util.calc_cos_theta(sl[0], sl[1])
        sin_theta = util.calc_sin_theta(sl[0], sl[1])

        x_dist = 0.0

        while dist - x_dist > noise:
            if x_dist < noise:
                ru_y = random.uniform(0, noise)
            else:
                ru_y = random.uniform(-noise, noise)
            x_dist += random.uniform(0.5*noise, noise)
            pre_rotate.append([x_dist, ru_y])

        pre_rotate.append([dist, 0.0])
        post_rotate_translate = [
            [sl[0][0] + pair[0]*cos_theta - pair[1]*sin_theta,
             sl[0][1] + pair[0]*sin_theta + pair[1]*cos_theta] for pair in pre_rotate
        ]
        paths.extend(post_rotate_translate)

    return paths


def rounded_corner_polygon(
    vertices_flat: Dim1FloatType,
    radius: float
) -> Dim3FloatType:

    vertices: Dim2FloatType = [vertices_flat[idx:idx+2] for idx
                              in range(0, len(vertices_flat), 2)]

    n_vertices = len(vertices)
    vertices_overlap = vertices.copy()
    vertices_overlap.insert(0, vertices[-1])
    vertices_overlap.append(vertices[0])


    paths = []
    for idx in range(1, n_vertices + 1):
        sl = vertices_overlap[idx - 1:idx + 2]
        sin_theta = util.calc_sin_theta(sl[0], sl[1])
        cos_theta = util.calc_cos_theta(sl[0], sl[1])
        x0 = sl[1][0] - cos_theta * radius
        y0 = sl[1][1] - sin_theta * radius

        sin_theta = util.calc_sin_theta(sl[1], sl[2])
        cos_theta = util.calc_cos_theta(sl[1], sl[2])
        x2 = sl[1][0] + cos_theta * radius
        y2 = sl[1][1] + sin_theta * radius
        paths.append(
            [[x0, y0], sl[1], [x2, y2]]
        )

    return paths


def curved_paths2svg(paths: Dim3FloatType) -> str:

    svg_str = []
    end_point = paths[0][0]
    control = "M"
    for idx in range(len(paths)):
        [x0, y0], [x1, y1], [x2, y2] = paths[idx]
        if idx > 0:
            control = "L"
        svg_str.append(
            f'{control} {x0} {y0} Q {x1} {y1}, {x2} {y2} '
        )
    svg_str.append(f"L {end_point[0]} {end_point[1]}")

    return "".join(svg_str)


def straight_paths2svg(paths: Dim2FloatType) -> str:

    svg_str = [f"M {paths[0][0]} {paths[0][1]} "]
    for idx in range(1, len(paths)):
        x0, y0 = paths[idx]
        svg_str.append(f'L {x0} {y0} ')
    return "".join(svg_str)


def added_vertices_polygon2svg(paths: Dim1FloatType, *args) -> str:
    return straight_paths2svg(
        added_vertices_polygon(paths, *args)
    )


def jagged_line_polygon2svg(paths: Dim1FloatType, *args) -> str:
    return straight_paths2svg(
        jagged_line_polygon(paths, *args)
    )

def rounded_corner_polygon2svg(paths: Dim1FloatType, *args) -> str:
    return curved_paths2svg(
        rounded_corner_polygon(paths, *args)
    )


def polygon_iter(file_path: str):
    """
    """
    ET.register_namespace("", "http://www.w3.org/2000/svg")
    tree = ET.parse(file_path)
    root = tree.getroot()

    prefix = "{http://www.w3.org/2000/svg}"
    g = root.find(f"{prefix}g")
    if g is None:
        raise ValueError("Cannot find group element!")

    for child in g.iter(f"{prefix}polygon"):
        yield child

    tree.write(file_path)


def modify_svg(file_path: str, polygon_modify_fn: typing.Callable):
    """
    Round all the corners in an SVG of the type generated by primitive
    """
    ET.register_namespace("", "http://www.w3.org/2000/svg")
    tree = ET.parse(file_path)
    root = tree.getroot()

    prefix = "{http://www.w3.org/2000/svg}"
    g = root.find(f"{prefix}g")
    if g is None:
        raise ValueError("Cannot find group element!")

    for child in g.iter(f"{prefix}polygon"):
        points = [float(val) for val in child.attrib["points"].split(",")]
        paths_str = polygon_modify_fn(points)
        child.tag = f"{prefix}path"
        child.attrib["d"] = paths_str
        del child.attrib["points"]

    tree.write(file_path)


polygon2svg_lookup = {
    "added_vertices": added_vertices_polygon2svg,
    "jagged_line": jagged_line_polygon2svg,
    "rounded_corner": rounded_corner_polygon2svg
}
