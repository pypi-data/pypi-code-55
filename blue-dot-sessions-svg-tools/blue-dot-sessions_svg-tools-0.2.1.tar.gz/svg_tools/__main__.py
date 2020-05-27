import typing
import argparse
import shutil
import math
import random
import os
import logging

from . import (
    jagged_line_polygon2svg,
    rounded_corner_polygon2svg,
    added_vertices_polygon2svg,
    modify_svg
)


def create_parser(modify_fn_names: typing.List[str]) -> argparse.ArgumentParser:

    modify_fn_names_str = ", ".join(modify_fn_names)

    parser = argparse.ArgumentParser(description="Modify primitive SVG polygons")
    parser.add_argument("file_paths", metavar="file-paths", type=str, nargs="+",
                        help="Files whose polygons to round")
    parser.add_argument("-r", "--radius", action="store", dest="radius", type=float, default=2.0,
                        help="Corner Radius for output SVG paths (default %(default)s.")

    parser.add_argument("--modify-fn", action="store", dest="modify_fn_name", type=str, default="rounded",
                        help=(f"Modification function to apply to SVG polygons. "
                              f"Available functions are {modify_fn_names_str} (default %(default)s.)"))
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Verbose output")

    return parser


def main():

    modify_fn_lookup = {
        "jagged": jagged_line_polygon2svg,
        "rounded": lambda points, *args: rounded_corner_polygon2svg(points, args[0]),
        "add_vertices": lambda points, *args: added_vertices_polygon2svg(
            points, 1, args[0])
    }

    parsed = create_parser(list(modify_fn_lookup.keys())).parse_args()

    level = logging.INFO
    if parsed.verbose:
        level = logging.DEBUG

    logging.basicConfig(level=level)
    logging.getLogger("matplotlib").setLevel(logging.ERROR)
    print(vars(parsed))
    file_paths = parsed.file_paths
    for file_path in file_paths:
        output_file_path = f"{os.path.splitext(file_path)[0]}.{parsed.modify_fn_name}.svg"
        shutil.copy(file_path, output_file_path)
        modify_svg(
            output_file_path,
            lambda points: modify_fn_lookup[parsed.modify_fn_name](points, parsed.radius))

main()
