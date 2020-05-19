from enum import Enum


class OutputFormats:
    class Verbosity(Enum):
        GENERIC = "body"
        CONCISE = "skel"
        BRIEF = "ids"
        VERBOSE = "meta"

    class Geometry(Enum):
        FULL_GEOM = "geom"
        BOUNDING_BOX = "bb"
        CENTER_POINT = "center"

    class SortOrder(Enum):
        OBJECT_ID = "asc"
        QUADTILE = "qt"

    # Can set defaults and stuff here

opf = OutputFormats()

class OutputFormatter:
    def __init__(self,
                 verbosity=opf.Verbosity.GENERIC,
                 geometry=None,
                 sortorder=opf.SortOrder.OBJECT_ID):

        self._v = verbosity
        self._g = geometry
        self._s = sortorder

    @property
    def VERBOSITY(self):
        return self._v

    @VERBOSITY.setter
    def VERBOSITY(self, mode):
        self._v = mode

    @property
    def GEOMETRY(self):
        return self._g

    @GEOMETRY.setter
    def GEOMETRY(self, mode):
        self._g = mode

    @property
    def SORTORDER(self):
        return self._s

    @SORTORDER.setter
    def SORTORDER(self, mode):
        self._s = mode

    def __repr__(self):
        s = "out"
        modes = []
        if self._v != opf.Verbosity.GENERIC:
            modes.append(self._v.value)
        if self._g is not None:
            modes.append(self._g.value)
        if self._s == opf.SortOrder.QUADTILE:
            modes.append(self._s.value)
        if modes:
            s = f'''{s} {" ".join(m for m in modes)}'''
        return s + ";"

