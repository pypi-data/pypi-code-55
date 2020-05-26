# 3D Primitives
import os
import sys

from muscad.base import Primitive


class Cube(Primitive):
    def __init__(self, width, depth, height):
        super().__init__()
        self._width = width
        self._depth = depth
        self._height = height

    @property
    def width(self):
        return self._width

    @property
    def depth(self):
        return self._depth

    @property
    def height(self):
        return self._height

    @property
    def left(self):
        return -self.width / 2

    @property
    def back(self):
        return -self.depth / 2

    @property
    def bottom(self):
        return -self.height / 2

    @property
    def right(self):
        return self.width / 2

    @property
    def front(self):
        return self.depth / 2

    @property
    def top(self):
        return self.height / 2

    def _arguments(self):
        return {
            "size": [self._width, self._depth, self._height],
            "center": True,
        }

    def half_left(self):
        return self.leftward(self.width / 2)

    def half_right(self):
        return self.rightward(self.width / 2)

    def half_back(self):
        return self.back(self.depth / 2)

    def half_forward(self):
        return self.forward(self.depth / 2)

    def half_down(self):
        return self.down(self.height / 2)

    def half_up(self):
        return self.up(self.height / 2)


class Cylinder(Primitive):
    def __init__(self, h, d, d2=None, segments="auto"):
        super().__init__()
        self._height = h
        self.diameter = d
        self.diameter2 = d2
        if segments == "auto":
            segments = int(d * 3.14 / 0.4)
        self.segments = segments

    def _arguments(self):
        if self.diameter2 is None:
            return {
                "h": self._height,
                "d": self.diameter,
                "$fn": self.segments,
                "center": True,
            }
        return {
            "h": self._height,
            "d1": self.diameter,
            "d2": self.diameter2,
            "$fn": self.segments,
            "center": True,
        }

    @property
    def width(self):
        return max(self.diameter, self.diameter2 or 0)

    @property
    def depth(self):
        return self.width

    @property
    def height(self):
        return self._height

    @property
    def left(self):
        return -self.width / 2

    @property
    def right(self):
        return self.width / 2

    @property
    def back(self):
        return -self.width / 2

    @property
    def front(self):
        return self.width / 2

    @property
    def bottom(self):
        return -self.height / 2

    @property
    def top(self):
        return self.height / 2

    def half_down(self):
        return self.down(self.height / 2)

    def half_up(self):
        return self.up(self.height / 2)


class Sphere(Primitive):
    def __init__(self, d, segments="auto"):
        super().__init__()
        self._diameter = d
        if segments == "auto":
            segments = int(d * 3.14 / 0.4)
        self._segments = segments

    def _arguments(self):
        return {"d": self._diameter, "$fn": self._segments}

    @property
    def width(self):
        return self._diameter

    @property
    def depth(self):
        return self._diameter

    @property
    def height(self):
        return self._diameter

    @property
    def left(self):
        return -self._diameter / 2

    @property
    def right(self):
        return self._diameter / 2

    @property
    def back(self):
        return -self._diameter / 2

    @property
    def front(self):
        return self._diameter / 2

    @property
    def bottom(self):
        return -self._diameter / 2

    @property
    def top(self):
        return self._diameter / 2


class Polyhedron(Primitive):
    def __init__(self, points, faces, convexity=1):
        super().__init__()
        self.points = points
        self.faces = faces
        self.convexity = convexity

    def _arguments(self):
        return {
            "points": self.points,
            "faces": self.faces,
            "convexity": self.convexity,
        }


# 2D Primitives
class Primitive2D(Primitive):
    @property
    def bottom(self):
        return 0

    @property
    def top(self):
        return 0

    @property
    def height(self):
        return 0


class Circle(Primitive2D):
    def __init__(self, d, segments="auto"):
        super().__init__()
        self._diameter = d
        if segments == "auto":
            segments = int(d * 3.14 / 0.4)
        self._segments = segments

    def _arguments(self):
        return {"d": self._diameter, "$fn": self._segments}

    @property
    def left(self):
        return -self._diameter / 2

    @property
    def right(self):
        return self._diameter / 2

    @property
    def back(self):
        return -self._diameter / 2

    @property
    def front(self):
        return self._diameter / 2


class Square(Primitive2D):
    def __init__(self, width, depth):
        super().__init__()
        self._width = width
        self._depth = depth

    def _arguments(self):
        return {"size": [self._width, self._depth], "center": True}

    @property
    def width(self):
        return self._width

    @property
    def depth(self):
        return self._depth

    @property
    def left(self):
        return -self.width / 2

    @property
    def right(self):
        return self.width / 2

    @property
    def back(self):
        return -self.depth / 2

    @property
    def front(self):
        return self.depth / 2


class Text(Primitive2D):
    def __init__(
        self,
        text,
        size=10,
        font=None,
        halign=None,
        valign=None,
        spacing=None,
        direction=None,
        language=None,
        script=None,
        segments=None,
    ):
        super().__init__()
        self.text = text
        self.size = size
        self.font = font
        self.halign = halign
        self.valign = valign
        self.spacing = spacing
        self.direction = direction
        self.language = language
        self.script = script
        self.segments = segments

    def _arguments(self):
        return {
            "text": self.text,
            "size": self.size,
            "font": self.font,
            "halign": self.halign,
            "valign": self.valign,
            "spacing": self.spacing,
            "direction": self.direction,
            "language": self.language,
            "script": self.script,
            "$fn": self.segments,
        }

    @property
    def left(self):
        if self.halign in (None, "left"):
            return 0
        raise NotImplementedError(
            "use halign='left' (default) to be able to align a Text to left"
        )

    @property
    def right(self):
        if self.halign == "right":
            return 0
        raise NotImplementedError(
            "use halign='right' to be able to align a Text to right"
        )

    @property
    def back(self):
        if self.valign in (None, "baseline", "bottom"):
            return 0
        raise NotImplementedError(
            "use valign='baseline' or 'bottom' to be able to align a Text to back"
        )

    @property
    def front(self):
        if self.valign == "top":
            return 0
        raise NotImplementedError(
            "use valign='top' to be able to align a Text to front"
        )


class Polygon(Primitive2D):
    def __init__(self, *points, path=None, convexity=None):
        super().__init__()
        self.points = list(points)
        self.path = path
        self.convexity = convexity

    def _arguments(self):
        return {
            "points": self.points,
            "path": self.path,
            "convexity": self.convexity,
        }

    @property
    def left(self):
        return min([point[0] for point in self.points])

    @property
    def right(self):
        return max([point[0] for point in self.points])

    @property
    def front(self):
        return max([point[1] for point in self.points])

    @property
    def back(self):
        return min([point[1] for point in self.points])


class Import(Primitive):
    def __init__(self, file, convexity=None, layer=None):
        if not os.path.isabs(file):
            file = os.path.join(os.path.dirname(sys.argv[0]), file)
        super().__init__(file=file, convexity=convexity, layer=layer)
