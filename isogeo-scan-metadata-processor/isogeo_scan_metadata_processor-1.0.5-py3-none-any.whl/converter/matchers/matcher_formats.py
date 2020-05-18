#! python3  # noqa: E265

"""
    Matching table between FME short name and Isogeo formats names.

    See: https://github.com/isogeo/isogeo-worker-server/blob/520791363f3a8216947e573851e9e22829a11446/lib/sync/utils.js#L68-L87
"""

MATCHER_FORMAT = {
    "ECW": "ecw",
    "ESRISHAPE": "shp",
    "FILEGDB": "filegdb",
    "GEODATABASE_FILE": "filegdb",
    "GEODATABASE_SDE": "arcsde",
    "GEOTIFF": "geotiff",
    "GML": "gml",
    "INGR": "jpg",
    "POSTGIS": "postgis",
}


# #############################################################################
# ##### Main #######################
# ##################################
if __name__ == "__main__":
    pass
