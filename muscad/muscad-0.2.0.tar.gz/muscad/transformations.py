from muscad.base import Transformation
from muscad.helpers import normalize_angle


class Translation(Transformation, name="translate"):
    def __init__(self, *, x=0, y=0, z=0):
        super().__init__()
        self.x = x
        self.y = y
        self.z = z

    def _arguments(self):
        return {"v": [self.x, self.y, self.z]}

    def combine(self, other):
        if type(other) == self.__class__:
            self.x += other.x
            self.y += other.y
            self.z += other.z
            self.child = other.child
            return self
        return super().combine(other)

    def copy(self):
        return self.__class__(x=self.x, y=self.y, z=self.z)

    @property
    def left(self):
        return self.child.left + self.x

    @property
    def right(self):
        return self.child.right + self.x

    @property
    def back(self):
        return self.child.back + self.y

    @property
    def front(self):
        return self.child.front + self.y

    @property
    def bottom(self):
        return self.child.bottom + self.z

    @property
    def top(self):
        return self.child.top + self.z


class Rotation(Transformation, name="rotate"):
    """
    OpenSCAD rotate().
    """

    def __init__(self, *, x=0, y=0, z=0):
        super().__init__()
        self.x = normalize_angle(x)
        self.y = normalize_angle(y)
        self.z = normalize_angle(z)

    def _arguments(self):
        return {"a": [self.x, self.y, self.z]}

    def copy(self):
        return self.__class__(x=self.x, y=self.y, z=self.z)

    # TODO: make it work for all cases
    @property
    def center_x(self):
        if self.child.center_x == 0 and self.y == 0:  # and self.z == 0 ?
            return 0
        return super().center_x

    @property
    def center_y(self):
        if self.child.center_y == 0 and self.x == 0:  # and self.z == 0 ?
            return 0
        return super().center_y

    @property
    def center_z(self):
        if self.child.center_z == 0 and self.x == 0 and self.y == 0:
            return 0
        return super().center_z

    @property
    def left(self):
        if self.y == 0 and self.z == 0:  # rotation along X axis
            return self.child.left
        if self.x == 0 and self.z == 0:  # rotation along Y axis
            if self.y == 270:
                return -self.child.top
            elif self.y == 180:
                return -self.child.right
            elif self.y == 90:
                return self.child.bottom
        if self.x == 0 and self.y == 0:  # rotation along Z axis
            if self.z == 270:
                return self.child.back
            if self.z == 180:
                return -self.child.right
            if self.z == 90:
                return -self.child.front
        raise NotImplementedError(
            "Only simple 90° rotations along single axis are supported"
        )

    @property
    def right(self):
        if self.y == 0 and self.z == 0:  # rotation along X axis
            return self.child.right
        if self.x == 0 and self.z == 0:  # rotation along Y axis
            if self.y == 270:
                return -self.child.bottom
            elif self.y == 180:
                return -self.child.left
            elif self.y == 90:
                return self.child.top
        if self.x == 0 and self.y == 0:  # rotation along Z axis
            if self.z == 270:
                return self.child.front
            if self.z == 180:
                return -self.child.left
            if self.z == 90:
                return -self.child.back
        raise NotImplementedError(
            "Only simple 90° rotations along single axis are supported"
        )

    @property
    def back(self):
        if self.y == 0 and self.z == 0:  # rotation along X axis
            if self.x == 270:
                return self.child.bottom
            elif self.x == 180:
                return -self.child.front
            elif self.x == 90:
                return -self.child.top
        if self.x == 0 and self.z == 0:  # rotation along Y axis
            return self.child.back
        if self.x == 0 and self.y == 0:  # rotation along Z axis
            if self.z == 270:
                return -self.child.right
            if self.z == 180:
                return -self.child.front
            if self.z == 90:
                return self.child.left
        raise NotImplementedError(
            "Only simple 90° rotations along single axis are supported"
        )

    @property
    def front(self):
        if self.y == 0 and self.z == 0:  # rotation along X axis
            if self.x == 270:
                return self.child.top
            elif self.x == 180:
                return -self.child.back
            elif self.x == 90:
                return -self.child.bottom
        if self.x == 0 and self.z == 0:  # rotation along Y axis
            return self.child.front
        if self.x == 0 and self.y == 0:  # rotation along Z axis
            if self.z == 270:
                return -self.child.left
            if self.z == 180:
                return -self.child.back
            if self.z == 90:
                return self.child.right
        raise NotImplementedError(
            "Only simple 90° rotations along single axis are supported"
        )

    @property
    def bottom(self):
        if self.y == 0 and self.z == 0:  # rotation along X axis
            if self.x == 270:
                return -self.child.front
            elif self.x == 180:
                return -self.child.top
            elif self.x == 90:
                return self.child.back
        if self.x == 0 and self.z == 0:  # rotation along Y axis
            if self.y == 270:
                return self.child.left
            elif self.y == 180:
                return -self.child.top
            elif self.y == 90:
                return -self.child.right
        if self.x == 0 and self.y == 0:  # rotation along Z axis
            return self.child.bottom
        raise NotImplementedError(
            "Only simple 90° rotations along single axis are supported"
        )

    @property
    def top(self):
        if self.y == 0 and self.z == 0:  # rotation along X axis
            if self.x == 270:
                return -self.child.back
            elif self.x == 180:
                return -self.child.bottom
            elif self.x == 90:
                return self.child.front
        if self.x == 0 and self.z == 0:  # rotation along Y axis
            if self.y == 270:
                return self.child.right
            elif self.y == 180:
                return -self.child.bottom
            elif self.y == 90:
                return -self.child.left
        if self.x == 0 and self.y == 0:  # rotation along Z axis
            return self.child.top

        raise NotImplementedError(
            "Only simple 90° rotations along single axis are supported"
        )


class Scaling(Transformation, name="scale"):
    def __init__(self, *, x=0, y=0, z=0):
        super().__init__()
        self.x = x
        self.y = y
        self.z = z

    def _arguments(self):
        return {"v": [self.x, self.y, self.z]}

    @property
    def left(self):
        return self.child.left * self.x

    @property
    def right(self):
        return self.child.right * self.x

    @property
    def back(self):
        return self.child.back * self.y

    @property
    def front(self):
        return self.child.front * self.y

    @property
    def bottom(self):
        return self.child.bottom * self.z

    @property
    def top(self):
        return self.child.top * self.z


class Resizing(Transformation, name="resize"):
    def __init__(self, *, x, y, z, auto=None):
        super().__init__()
        self.x = x
        self.y = y
        self.z = z
        self.auto = auto

    def _arguments(self):
        return {"newsize": [self.x, self.y, self.z], "auto": self.auto}


class Mirroring(Transformation, name="mirror"):
    def __init__(self, *, x=0, y=0, z=0):
        super().__init__()
        self.x = x
        self.y = y
        self.z = z

    def _arguments(self):
        return {"v": [self.x, self.y, self.z]}

    @property
    def left(self):
        if self.x:
            if not self.y and not self.z:
                return -self.child.right
            raise NotImplementedError(
                "Only single axis mirror vectors are supported"
            )
        return self.child.left

    @property
    def right(self):
        if self.x:
            if not self.y and not self.z:
                return -self.child.left
            raise NotImplementedError(
                "Only single axis mirror vectors are supported"
            )
        return self.child.right

    @property
    def front(self):
        if self.y:
            if not self.x and not self.z:
                return -self.child.back
            raise NotImplementedError(
                "Only single axis mirror vectors are supported"
            )
        return self.child.front

    @property
    def back(self):
        if self.y:
            if not self.x and not self.z:
                return -self.child.front
            raise NotImplementedError(
                "Only single axis mirror vectors are supported"
            )
        return self.child.back

    @property
    def top(self):
        if self.z:
            if not self.x and not self.y:
                return -self.child.bottom
            raise NotImplementedError(
                "Only single axis mirror vectors are supported"
            )
        return self.child.top

    @property
    def bottom(self):
        if self.z:
            if not self.x and not self.y:
                return -self.child.top
            raise NotImplementedError(
                "Only single axis mirror vectors are supported"
            )
        return self.child.bottom


class Multmatrix(Transformation):
    def __init__(self, matrix):
        super().__init__()
        self.matrix = matrix

    def _arguments(self):
        return {"m": self.matrix}


class Color(Transformation):
    def __init__(self, colorname, alpha=None):
        super().__init__()
        self.colorname = colorname
        self.alpha = alpha

    def _arguments(self):
        return {None: self.colorname, "alpha": self.alpha}

    def copy(self):
        return self.__class__(self.colorname, self.alpha)


class Offset(Transformation):
    def __init__(self, r=None, delta=None, chamfer=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if r and delta:
            raise ValueError("can't set both 'r' and 'delta'")
        if r is None and delta is None:
            raise ValueError("must set either 'r' or 'delta'")
        self.radius = r
        self.delta = delta
        self.chamfer = chamfer

    def _arguments(self):
        return {"r": self.radius, "delta": self.delta, "chamfer": self.chamfer}


class Minkowski(Transformation):
    pass


class Hull(Transformation):
    pass


class Projection(Transformation):
    def __init__(self, cut=False):
        super().__init__()
        self.cut = cut

    def _arguments(self):
        return {"cut": self.cut}


class Render(Transformation):
    def __init__(self, convexity=2):
        super().__init__()
        self._convexity = convexity

    def _arguments(self):
        return {"convexity": self._convexity}


class LinearExtrusion(Transformation, name="linear_extrude"):
    def __init__(
        self,
        height,
        center=False,
        convexity=10,
        twist=0,
        slices=None,
        scale=1.0,
        segments="auto",
    ):
        super().__init__()
        self._height = height
        self._center = center
        self._convexity = convexity
        self._twist = twist
        self._slices = slices
        self._scale = scale
        if segments == "auto":
            segments = int(twist * 3.14 / 0.4)
        self._segments = segments

    def _arguments(self):
        return {
            "height": self._height,
            "center": self._center,
            "convexity": self._convexity,
            "twist": self._twist,
            "slices": self._slices,
            "scale": self._scale,
        }

    @property
    def left(self):
        if self._twist == 0:
            return self.child.left
        raise NotImplementedError(
            "Linear extrusion with 'twist' is not supported"
        )

    @property
    def right(self):
        if self._twist == 0:
            return self.child.right
        raise NotImplementedError(
            "Linear extrusion with 'twist' is not supported"
        )

    @property
    def back(self):
        if self._twist == 0:
            return self.child.back
        raise NotImplementedError(
            "Linear extrusion with 'twist' is not supported"
        )

    @property
    def front(self):
        if self._twist == 0:
            return self.child.front
        raise NotImplementedError(
            "Linear extrusion with 'twist' is not supported"
        )

    @property
    def bottom(self):
        return self.child.bottom

    @property
    def top(self):
        return self.child.top + self._height


class RotationalExtrusion(Transformation, name="rotate_extrude"):
    def __init__(self, angle=360, convexity=None, segments="auto"):
        super().__init__()
        self.angle = angle
        self.convexity = convexity
        if segments == "auto":
            segments = int(angle * 3.14 / 0.4)
        self.segments = segments

    def _arguments(self):
        return {
            "angle": self.angle,
            "convexity": self.convexity,
            "$fn": self.segments,
        }


class Slide(Transformation):
    """
    Custom transformation that translate an object then Hulls the result to itself.
    If the object is a Composite, each part component is hulled to its translated self.
    This is useful for parts that must be slided into their final position, such as screws.
    Bounding box of the original object is untouched..
    """

    def __init__(self, *, x=0, y=0, z=0):
        super().__init__()
        self.x = x
        self.y = y
        self.z = z

    def render(self):
        return sum(
            Hull(child, child.translate(x=self.x, y=self.y, z=self.z))
            for child in self.child.walk()
        ).render()
