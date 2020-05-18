#! python3  # noqa: E265

"""
    Matching table between FME and Isogeo geometry names.

    Copied from: https://github.com/isogeo/isogeo-worker-server/blob/520791363f3a8216947e573851e9e22829a11446/lib/sync/utils.js#L9-L20
"""

MATCHER_GEOMETRY = {
    "fme_point": "Point",
    "fme_area": "Polygon",
    "fme_line": "LineString",
    "fme_arc": "Curve",
    "fme_collection": "GeometryCollection",
    "fme_ellipse": "Curve",
    "fme_surface": "Surface",
    "fme_point_cloud": "Point",
}


# #############################################################################
# ##### Main #######################
# ##################################
if __name__ == "__main__":
    pass
