import os
import subprocess
from functools import wraps
from typing import List, Optional

from muscad.helpers import normalize_angle, camel_to_snake


class MuSCAD:
    """
    Base class for all MuSCAD objects
    """

    def render(self):
        """
        Returns the SCAD code to render this object
        :return: (str) the SCAD code for this object
        """
        raise NotImplementedError()  # pragma: no cover

    def __str__(self):
        return self.render()

    def _repr_pretty_(self, p, cycle):
        """
        Helper method for Jupyter Notebook to show the rendered code instead of __repr__
        """
        p.text(str(self))


class MuSCADError(Exception):
    """
    Base class for all MuSCAD exceptions
    """


def indent(s, token="  "):
    """
    Indents a given string, with characters from ``token``
    Each line will be prefixed by indent.
    :param s: the string to indent (may contain multiple lines, separated by '\n'
    :param indent: the string to use as indentation
    :return: the indented string
    """
    return token + s.replace("\n", f"\n{token}")


def render_comment(f):
    """
    A helper decorator to add comments to rendered code
    """

    @wraps(f)
    def wrapper(self, *args, with_comment=True, **kwargs):
        code = f(self, *args, **kwargs)
        if with_comment and self.comment:
            comment = "".join(
                f"// {line}\n" for line in self.comment.split("\n")
            )
            return f"{comment}{code}"
        return code

    return wrapper


class Object(MuSCAD):
    """
    Base class for all OpenSCAD geometry objects. Do not instantiate this class directly.
    """

    def __init_subclass__(cls, name=None, **kwargs):
        """
        Derive a name from the subclasses name, if not explicitly declared.
        :param name: a string (if explicitly declared)
        :param kwargs: remaining attributes (unused)
        :return: a subclass with a `name` attribute
        """
        super().__init_subclass__(**kwargs)
        if name is None:
            cls.object_name = camel_to_snake(cls.__name__)
        else:
            cls.object_name = name

    def __init__(self):
        """
        Base constructor for Objects.
        :param children:
        """
        self.modifier = ""
        self.comment = None

    def set_modifier(self, m):
        """
        Set or remove a modifier for this object.
        :param m: one of OpenSCAD's modifiers, as a single char str, or None to remove the modifier.
        :return: the same object, with modifier applied
        """
        if not m:
            self.modifier = ""
            return self
        self.modifier = m
        return self

    def disable(self):
        """
        Disables the object (modifer *)
        :return: the same object, disabled
        """
        return self.set_modifier("*")

    def debug(self):
        """
        Enables debug for the object (modifier #)
        :return: the same object, in debug mode
        """
        return self.set_modifier("#")

    def background(self):
        """
        Sets the object as background (modifier %)
        :return: the same object, as background
        """
        return self.set_modifier("%")

    def root(self):
        """
        Sets the object as root (modifier !)
        :return: the same object, as root
        """
        return self.set_modifier("!")

    def remove_modifier(self):
        """
        Remove any previously applied modifier.
        :return: the same object, with any modifier removed
        """
        return self.set_modifier(None)

    def transform(self, transformation):
        """
        Apply a transformation to this object
        :param transformation: a Transformation to apply
        :return: a transformed object
        """
        return transformation.apply(self)

    def __add__(self, other):
        """
        Adding two objects together creates a Union of those objects
        :param other: another object
        :return: a Union of both objects
        """
        return Union(self, other)

    def __radd__(self, other):
        """
        Makes sure sum(*[object, ...]) works
        :param other: another object, or 0
        :return: a Union of both objects
        """
        if other == 0:
            return self
        return other + self

    def __sub__(self, other):
        """
        Substracting an object from another creates a Difference of those objects
        :param other: another object
        :return: a Difference of self - other
        """
        return Difference(self, other)

    def __and__(self, other):
        """
        Logical and between two objects creates an Intersection between those objects
        :param other: another object
        :return: an Intersection of self and other
        """
        return Intersection(self, other)

    def translate(self, *, x: float = 0, y: float = 0, z: float = 0):
        """
        Applies a `Translation` to this object.
        :param x: x axis translation
        :param y: y axis translation
        :param z: z axis translation
        :return: a translated object
        """
        return Translation(x=x, y=y, z=z)(self)

    def rightward(self, dist):
        """
        Helper method to apply a Translation to the right on X axis on the current object
        :param dist: distance in mm
        :return: an object, translated to the right by `dist` mm
        """
        if dist == 0:
            return self
        return self.transform(Translation(x=dist))

    def leftward(self, dist):
        """
        Helper method to apply a Translation to the left on X axis on the current object
        :param dist: distance in mm
        :return: an object, translated to the left by `dist` mm
        """
        if dist == 0:
            return self
        return self.transform(Translation(x=-dist))

    def forward(self, dist):
        """
        Helper method to apply a forward Translation on Y axis on the current object
        :param dist: distance in mm
        :return: an object, translated forwards by `dist` mm
        """
        if dist == 0:
            return self
        return self.transform(Translation(y=dist))

    def backward(self, dist):
        """
        Helper method to apply a backward Translation on Y axis on the current object
        :param dist: distance in mm
        :return: an object, translated backwards by `dist` mm
        """
        if dist == 0:
            return self
        return self.transform(Translation(y=-dist))

    def up(self, dist):
        """
        Helper method to apply a upwards Translation on Z axis on the current object
        :param dist: distance in mm
        :return: an object, translated upwards by `dist` mm
        """
        if dist == 0:
            return self
        return self.transform(Translation(z=dist))

    def down(self, dist):
        """
        Helper method to apply a downwards Translation on Z axis on the current object
        :param dist: distance in mm
        :return: an object, translated downwards by `dist` mm
        """
        if dist == 0:
            return self
        return self.transform(Translation(z=-dist))

    def rotate(self, *, x: float = 0, y: float = 0, z: float = 0):
        """
        Applies a rotation to this object.
        :param x: x angle
        :param y: y angle
        :param z: z angle
        :return: a rotated object
        """
        x = normalize_angle(x)
        y = normalize_angle(y)
        z = normalize_angle(z)
        if x == y == z == 0.0:
            return self
        return Rotation(x=x, y=y, z=z)(self)

    def x_rotate(self, angle):
        """
        Helper method to apply a Rotation on X axis on the current object
        :param angle: angle in degrees
        :return: an object, rotated by `angle` degrees on X axis
        """
        return self.rotate(x=angle)

    def y_rotate(self, angle):
        """
        Helper method to apply a Rotation on Y axis on the current object
        :param angle: angle in degrees
        :return: an object, rotated by `angle` degrees on Y axis
        """
        return self.rotate(y=angle)

    def z_rotate(self, angle):
        """
        Helper method to apply a Rotation on Z axis on the current object
        :param angle: angle in degrees
        :return: an object, rotated by `angle` degrees on Z axis
        """
        return self.rotate(z=angle)

    def left_to_bottom(self):
        """
        Alias for self.y_rotate(-90)
        :return:
        """
        return self.y_rotate(-90)

    def left_to_top(self):
        """
        Alias for self.y_rotate(90)
        :return:
        """
        return self.y_rotate(90)

    def left_to_front(self):
        """
        Alias for self.z_rotate(-90)
        :return:
        """
        return self.z_rotate(-90)

    def left_to_back(self):
        """
        Alias for self.z_rotate(90)
        :return:
        """
        return self.z_rotate(90)

    def right_to_bottom(self):
        """
        Alias for self.y_rotate(90)
        :return:
        """
        return self.y_rotate(90)

    def right_to_top(self):
        """
        Alias for self.y_rotate(-90)
        :return:
        """
        return self.y_rotate(-90)

    def right_to_front(self):
        """
        Alias for self.z_rotate(90)
        :return:
        """
        return self.z_rotate(90)

    def right_to_back(self):
        """
        Alias for self.z_rotate(90)
        :return:
        """
        return self.z_rotate(90)

    def front_to_left(self):
        """
        Alias for self.z_rotate(90)
        :return:
        """
        return self.z_rotate(90)

    def front_to_right(self):
        """
        Alias for self.z_rotate(-90)
        :return:
        """
        return self.z_rotate(-90)

    def front_to_top(self):
        """
        Alias for self.x_rotate(90)
        :return:
        """
        return self.x_rotate(90)

    def front_to_bottom(self):
        """
        Alias for self.x_rotate(-90)
        :return:
        """
        return self.x_rotate(-90)

    def back_to_left(self):
        """
        Alias for self.z_rotate(-90)
        :return:
        """
        return self.z_rotate(-90)

    def back_to_right(self):
        """
        Alias for self.z_rotate(90)
        :return:
        """
        return self.z_rotate(90)

    def back_to_top(self):
        """
        Alias for self.x_rotate(-90)
        :return:
        """
        return self.x_rotate(-90)

    def back_to_bottom(self):
        """
        Alias for self.x_rotate(90)
        :return:
        """
        return self.x_rotate(90)

    def bottom_to_left(self):
        """
        Alias for self.y_rotate(90)
        :return:
        """
        return self.y_rotate(90)

    def bottom_to_right(self):
        """
        Alias for self.y_rotate(-90)
        :return:
        """
        return self.y_rotate(-90)

    def bottom_to_front(self):
        """
        Alias for self.x_rotate(90)
        :return:
        """
        return self.x_rotate(90)

    def bottom_to_back(self):
        """
        Alias for self.x_rotate(-90)
        :return:
        """
        return self.x_rotate(-90)

    def upside_down(self, y_axis=False):
        """
        Turns the object upside down on its x axis. Equivalent to self.x_rotate(180).
        If y_axis is True, rotate on y axis instead.
        :return: an object rotated 180° on X or Y axis
        """
        if not y_axis:
            return self.x_rotate(180)
        else:
            return self.y_rotate(180)

    def front_to_back(self):
        """
        Alias for self.z_rotate(180)
        :return: an object rotated 180° on Z axis
        """
        return self.z_rotate(180)

    def scale(self, *, x: float = 1.0, y: float = 1.0, z: float = 1.0):
        """
        Applies a scaling transformation to this object.
        :param x: x ratio
        :param y: y ratio
        :param z: z ratio
        :return: a scaled object
        """
        return Scaling(x=x, y=y, z=z)(self)

    def resize(self, *, x: float = 0, y: float = 0, z: float = 0):
        """
        Applies a resize transformation to this object.
        :param x: x size
        :param y: y size
        :param z: z size
        :return: a resized object
        """
        return Resizing(x=x, y=y, z=z)(self)

    def mirror(self, *, x: float = 0, y: float = 0, z: float = 0):
        """
        Applies a mirror transformation to this object.
        :param x: x mirror factor
        :param y: y mirror factor
        :param z: z mirror factor
        :return: a mirrored object
        """
        return Mirroring(x=x, y=y, z=z)(self)

    def x_mirror(self, center: float = 0.0, keep=False):
        """
        Helper method to mirror this object on the X axis or a parallel.
        :param center: the X coordinate of the axis to mirror on
        :param keep: if True, the initial object is kept in addition to its mirror
        :return: a mirrored object
        """
        if keep:
            return self.x_mirror(center, keep=False) + self
        return self.leftward(center).mirror(x=1).rightward(center)

    def y_mirror(self, center: float = 0.0, keep=False):
        """
        Helper method to mirror this object on the Y axis or a parallel.
        :param center: the Y coordinate of the axis to mirror on
        :param keep: if True, the initial object is kept in addition to its mirror
        :return: a mirrored object
        """
        if keep:
            return self.backward(center).mirror(y=1).forward(center) + self
        return self.backward(center).mirror(y=1).forward(center)

    def z_mirror(self, center: float = 0.0, keep=False):
        """
        Helper method to mirror this object on the Z axis or a parallel.
        :param center: the Y coordinate of the axis to mirror on
        :param keep: if True, the initial object is kept in addition to its mirror
        :return: a mirrored object
        """
        if keep:
            return self.down(center).mirror(z=1).up(center) + self
        return self.down(center).mirror(z=1).up(center)

    def linear_extrude(
        self,
        height: float,
        center: bool = False,
        convexity: int = 10,
        twist: float = 0.0,
        slices=None,
        scale: float = 1.0,
        segments="auto",
    ):
        """
        Applies a linear extrusion transformation to this object.
        :param height: height of the extrusion
        :param center: if true, center the extrusion
        :param convexity:
        :param twist:
        :param slices:
        :param scale:
        :param segments: number of segments. If set to "auto", automatically
        determines the number of segments to get a good-looking round result.
        """
        return LinearExtrusion(
            height=height,
            center=center,
            convexity=convexity,
            twist=twist,
            slices=slices,
            scale=scale,
            segments=segments,
        )(self)

    def z_linear_extrude(
        self,
        distance=None,
        *,
        bottom=None,
        center_z=None,
        top=None,
        convexity=10,
        twist=0.0,
        slices=None,
        scale=1.0,
        segments="auto",
    ):
        bottom, center_z, top, distance = calc(bottom, center_z, top, distance)
        return self.linear_extrude(
            distance,
            convexity=convexity,
            twist=twist,
            slices=slices,
            scale=scale,
            segments=segments,
        ).align(bottom=bottom)

    def y_linear_extrude(
        self,
        distance=None,
        *,
        back=None,
        center_y=None,
        front=None,
        convexity=10,
        twist=0.0,
        slices=None,
        scale=1.0,
        segments="auto",
    ):
        back, center_y, front, distance = calc(back, center_y, front, distance)
        return (
            self.linear_extrude(
                distance,
                convexity=convexity,
                twist=twist,
                slices=slices,
                scale=scale,
                segments=segments,
            )
            .front_to_top()
            .align(back=back)
        )

    def x_linear_extrude(
        self,
        distance=None,
        *,
        left=None,
        center_x=None,
        right=None,
        convexity=10,
        twist=0.0,
        slices=None,
        scale=1.0,
        segments="auto",
    ):
        left, center_x, right, distance = calc(left, center_x, right, distance)
        return (
            self.linear_extrude(
                distance,
                convexity=convexity,
                twist=twist,
                slices=slices,
                scale=scale,
                segments=segments,
            )
            .y_rotate(-90)
            .align(left=left)
        )

    def rotational_extrude(
        self, angle: float = 360, convexity=None, segments="auto",
    ):
        """
        Applies a rotational extrusion to this object.
        :param angle:
        :param convexity:
        :param segments: number of segments. If set to "auto", automatically
        determines the number of segments to get a good-looking round result.
        :return:
        """
        return RotationalExtrusion(
            angle=angle, convexity=convexity, segments=segments,
        )(self)

    def hull(self):
        return Hull(self)

    def color(self, name: str, alpha: float = None):
        """
        Applies a color to this object.
        :param name:
        :param alpha:
        :return:
        """
        return Color(name, alpha=alpha)(self)

    def hole(self):
        """
        Turns this object into a Hole.
        :return: a Hole
        """
        return Hole(self)

    def misc(self):
        """
        Turns this object into a Misc item.
        :return: a Misc
        """
        return Misc(self)

    def __invert__(self):
        """
        Operator alternative to .hole().
        :return: a Hole based on this object
        """
        return self.hole()

    @property
    def width(self):
        return self.right - self.left

    @property
    def depth(self):
        return self.front - self.back

    @property
    def height(self):
        return self.top - self.bottom

    @property
    def left(self):
        raise NotImplementedError("left", self.__class__)  # pragma: no cover

    @property
    def right(self):
        raise NotImplementedError("right", self.__class__)  # pragma: no cover

    @property
    def center_x(self):
        return (self.right + self.left) / 2

    @property
    def back(self):
        raise NotImplementedError("back", self.__class__)  # pragma: no cover

    @property
    def front(self):
        raise NotImplementedError("front", self.__class__)  # pragma: no cover

    @property
    def center_y(self):
        return (self.front + self.back) / 2

    @property
    def bottom(self):
        raise NotImplementedError("bottom", self.__class__)  # pragma: no cover

    @property
    def top(self):
        raise NotImplementedError("top", self.__class__)  # pragma: no cover

    @property
    def center_z(self):
        return (self.top + self.bottom) / 2

    def bounding_box(self):
        return Cube(self.width, self.depth, self.height).translate(
            x=self.left, y=self.back, z=self.bottom
        )

    def slide(self, *, x=0, y=0, z=0):
        return Slide(x=x, y=y, z=z)(self)

    def align(
        self,
        *,
        left=None,
        center_x=None,
        right=None,
        back=None,
        center_y=None,
        front=None,
        bottom=None,
        center_z=None,
        top=None,
    ):
        x = y = z = 0
        if left is not None:
            x = left - self.left
        elif center_x is not None:
            x = center_x - self.center_x
        elif right is not None:
            x = right - self.right
        if back is not None:
            y = back - self.back
        elif center_y is not None:
            y = center_y - self.center_y
        elif front is not None:
            y = front - self.front
        if bottom is not None:
            z = bottom - self.bottom
        elif center_z is not None:
            z = center_z - self.center_z
        elif top is not None:
            z = top - self.top

        return self.translate(x=x, y=y, z=z)

    def __stl__(self):
        return self

    @property
    def file_name(self):
        return camel_to_snake(self.__class__.__name__)

    def render_to_file(self, path=None, openscad=False):
        if path is None:
            path = self.file_name
        return render_to_file(self, path, openscad=openscad)

    def export_stl(self, path=None):
        obj = self.__stl__()
        if path is None:
            path = self.file_name
        scad_path = obj.render_to_file(path=path)
        export_stl(scad_path)


class Primitive(Object):
    """
    Base class for simple objects with no children.
    Those are the primitive types such as Cube, Sphere, etc.
    Do not instantiate this class directly.
    """

    def __init__(self, **kwargs):
        super().__init__()
        self.arguments = kwargs

    def _arguments(self):
        """
        Get a argument dict for this object. This must be implemented by subclasses
        :return: a dict of arguments as {"param_name": arg_value}
        """
        return self.arguments

    def _iter_arguments(self):
        """
        Iterates over arguments.
        :return: a iterator of (key, val) tuples
        """
        for key, val in self._arguments().items():
            if val is None:
                continue
            if isinstance(val, str):
                yield key, f'"{val}"'
            elif val is True:
                yield key, "true"
            elif val is False:
                yield key, "false"
            elif isinstance(val, (tuple, list)):
                yield key, f"[{', '.join(str(item) for item in val)}]"
            else:
                yield key, val

    @classmethod
    def _render_arguments(cls, params):
        """
        Render the parameters for this object as OpenSCAD code. (anything between the parenthesis)
        :return: a str
        """
        return ", ".join(
            f"{key}={val}" if key else f"{val}" for key, val in params
        )

    @render_comment
    def render(self):
        """
        Render this object as OpenSCAD code.
        :return: a str of OpenSCAD code
        """
        return f"{self.modifier}{self.object_name}({self._render_arguments(self._iter_arguments())});"

    def walk(self):
        yield self


class Composite(Object):
    """
    Base class for Boolean operations (Union, Difference, Intersection)
    """

    def __init__(self, *children: Object):
        super().__init__()
        self.children: List[Object] = []
        if children:
            self.apply(*children)

    def add_child(self, child):
        """
        Add a children object to this Composite
        :param child:
        :return:
        """
        if child is None or child == 0:  # for sum(*Objects)
            return self
        elif isinstance(child, MuSCAD):
            self.children.append(child)
        else:
            self.children.extend(child)
        return self

    def apply(self, *children):
        for child in children:
            self.add_child(child)
        return self

    def __call__(self, *children):
        """
        Alias for self.apply(*children)
        :param children:
        :return:
        """
        return self.apply(*children)

    def _iter_children(self):
        """
        Iterate over children
        :return: an iterable
        """
        children = self.children

        # If the only children is a Union, return that union children directly
        if len(children) == 1:
            child = children[0]
            if isinstance(child, Union):
                children = child.children

        return children

    @classmethod
    def _render_children(cls, children):
        """
        Renders the children of this object as OpenSCAD code (anything between the brackets).
        :return: a str
        """
        # if len(children) == 1:
        #    child = children[0]
        #    return indent(child.render(with_comment=False))
        return (
            "{"
            + "".join(f"\n{indent(child.render())}" for child in children)
            + "\n}"
        )

    @render_comment
    def render(self):
        """
        Render this composite as valid OpenSCAD code.
        :return: a str
        """
        return (
            f"{self.modifier}{self.object_name}() "
            f"{self._render_children(self._iter_children())}"
        )

    def walk(self):
        for child in self.children:
            yield from child.walk()


def left(children):
    return min((child.left for child in children), default=0)


def right(children):
    return max((child.right for child in children), default=0)


def back(children):
    return min((child.back for child in children), default=0)


def front(children):
    return max((child.front for child in children), default=0)


def bottom(children):
    return min((child.bottom for child in children), default=0)


def top(children):
    return max((child.top for child in children), default=0)


class Union(Composite):
    """
    OpenSCAD union()
    """

    def __add__(self, other):
        """
        Adding to an Union adds a children instead of creating a new Union
        :param other: a children object
        :return: the same union with children appended
        """
        return self.add_child(other)

    @property
    def left(self):
        return left(self.children)

    @property
    def back(self):
        return back(self.children)

    @property
    def bottom(self):
        return bottom(self.children)

    @property
    def right(self):
        return right(self.children)

    @property
    def front(self):
        return front(self.children)

    @property
    def top(self):
        return top(self.children)


class ImplicitUnion(Union):
    def render(self):
        return f"{self.modifier}{self._render_children(self._iter_children())}"


class Difference(Composite):
    """
    OpenSCAD difference()
    """

    def __sub__(self, other):
        """
        Substracting from a Difference adds a children instead of creating a new Difference
        :param other: a children object
        :return: the same difference with children appended
        """
        return self.add_child(other)

    @property
    def left(self):
        return self.children[0].left

    @property
    def right(self):
        return self.children[0].right

    @property
    def back(self):
        return self.children[0].back

    @property
    def front(self):
        return self.children[0].front

    @property
    def bottom(self):
        return self.children[0].bottom

    @property
    def top(self):
        return self.children[0].top


class Intersection(Composite):
    """
    OpenSCAD intersection()
    """

    def __and__(self, other):
        """
        Intersecting with an Intersection adds a children instead of creating a new Intersection
        :param other: a children object
        :return: the same intersection with children appended
        """
        return self.add_child(other)

    @property
    def left(self):
        return max(child.left for child in self.children)

    @property
    def right(self):
        return min(child.right for child in self.children)

    @property
    def back(self):
        return max(child.back for child in self.children)

    @property
    def front(self):
        return min(child.front for child in self.children)

    @property
    def bottom(self):
        return max(child.bottom for child in self.children)

    @property
    def top(self):
        return min(child.top for child in self.children)


class Transformation(Primitive):
    """
    Base class for transformations.
    MuSCAD Transformations can have 1 single child (which can be a Union of multiple children)
    """

    def __init__(self, *children: Object):
        super().__init__()
        self.child: Optional[Object] = None
        self.apply(*children)

    def _arguments(self):
        return {}

    def apply(self, *children):
        if self.child:
            raise RuntimeError("Transformations cannot be applied twice")
        if children:
            if len(children) == 1:
                child = children[0]
                if isinstance(child, Union):
                    self.child = ImplicitUnion(*child.children)
                else:
                    self.child = child
            else:
                self.child = ImplicitUnion(*children)
        return self

    def __call__(self, *children):
        return self.apply(*children)

    @render_comment
    def render(self):
        return f"{self.modifier}{self.object_name}({self._render_arguments(self._iter_arguments())}) \n{self._render_child()}"

    def childattr(self, item):
        """
        Makes properties from the transformed object accessible through the Transformation
        :param item:
        :return:
        """
        return self.copy()(getattr(self.child, item, None))

    def __getattr__(self, item):
        return self.childattr(item)

    def copy(self):
        raise NotImplementedError()

    @property
    def file_name(self):
        return self.child.file_name

    def combine(self, child):
        """
        When applying multiple transformations of the same type, those may be combined
        :param child: another Composite
        :return: an object combining all transformations
        """
        raise NotImplementedError()

    def _render_child(self):
        return self.child.render()

    @property
    def left(self):
        return self.child.left

    @property
    def right(self):
        return self.child.right

    @property
    def width(self):
        return self.right - self.left

    @property
    def back(self):
        return self.child.back

    @property
    def front(self):
        return self.child.front

    @property
    def depth(self):
        return self.front - self.back

    @property
    def bottom(self):
        return self.child.bottom

    @property
    def top(self):
        return self.child.top

    @property
    def height(self):
        return self.top - self.bottom

    def walk(self):
        for child in self.child.walk():
            yield self.copy()(child)


# import basic transformations to make sure all helpers work
from .transformations import (
    Translation,
    Rotation,
    Scaling,
    Mirroring,
    Color,
    Resizing,
    LinearExtrusion,
    RotationalExtrusion,
    Slide,
    Hull,
)
from .primitives import Cube


class Hole(MuSCAD):
    def __init__(self, obj):
        self.object = obj
        super().__init__()

    def __getattr__(self, key):
        return getattr(self.object, key)

    def __add__(self, other):
        if isinstance(other, Hole):
            return Hole(self.object + other.object)
        return super().__add__(other)

    def render(self):
        return self.object.render()

    @property
    def comment(self):
        return self.object.comment

    @comment.setter
    def comment(self, value):
        self.object.comment = value


class Misc(MuSCAD):
    def __init__(self, obj):
        self.object = obj
        super().__init__()

    def __getattr__(self, key):
        return getattr(self.object, key)

    def render(self):
        return self.object.render()

    @property
    def comment(self):
        return self.object.comment

    @comment.setter
    def comment(self, value):
        self.object.comment = value


def distance_between(one, other):
    return abs(one - other)


def middle_of(one, other):
    return one + (other - one) / 2


def render_to_file(obj, path, openscad=False):
    if not path.endswith(".scad"):
        path = path + ".scad"
    if not os.path.isabs(path):
        path = os.path.join(os.getcwd(), path)

    render = obj.render()
    with open(path, "wt") as foutput:
        foutput.write(render)
    if openscad and not os.environ.get("MUSCAD_NO_OPENSCAD"):
        try:
            os.startfile(path)
        except AttributeError:
            subprocess.call(["xdg-open", path])

    return path


def validate_calc(f):
    def wrapper(from_=None, center=None, to=None, distance=None):
        _from, _center, _to, _distance = f(from_, center, to, distance)
        if from_ is not None and _from != from_:
            raise ValueError(
                f"calculated from_ incompatible with specified from_ (difference={from_ - _from})"
            )
        if center is not None and _center != center:
            raise ValueError(
                f"calculated center incompatible with specified center (difference={center - _center})"
            )
        if from_ is not None and _from != from_:
            raise ValueError(
                f"calculated to incompatible with specified to (difference={to - _to})"
            )
        if from_ is not None and _from != from_:
            raise ValueError(
                f"calculated distance incompatible with specified from_ (difference={distance - _distance})"
            )
        return _from, _center, _to, _distance

    return wrapper


def calc(from_=None, center=None, to=None, distance=None):
    """
    Given at least 2 of from_, center, and distance, returns all 4.
    If only distance is given, default to center = 0
    """
    if (
        from_ is None
        and to is None
        and center is None
        and distance is not None
    ):
        center = 0

    if from_ is not None and center is not None:
        if from_ < center:
            distance = (center - from_) * 2
            to = from_ + distance
            return from_, center, to, distance
        else:
            distance = (from_ - center) * 2
            to = from_ - distance
            return to, center, from_, distance
    if from_ is not None and to is not None:
        if from_ < to:
            distance = to - from_
            center = from_ + distance / 2
            return from_, center, to, distance
        else:
            distance = from_ - to
            center = to + distance / 2
            return to, center, from_, distance
    if from_ is not None and distance is not None:
        to = from_ + distance
        distance = abs(distance)
        if from_ < to:
            center = from_ + distance / 2
            return from_, center, to, distance
        else:
            center = to + distance / 2
            return to, center, from_, distance
    if center is not None and to is not None:
        if center < to:
            distance = (to - center) * 2
            from_ = to - distance
            return from_, center, to, distance
        else:
            distance = (center - to) * 2
            from_ = to + distance
            return to, center, from_, distance
    if center is not None and distance is not None:
        distance = abs(distance)
        from_ = center - distance / 2
        to = center + distance / 2
        return from_, center, to, distance
    if to is not None and distance is not None:
        from_ = to - distance
        distance = abs(distance)
        if from_ < to:
            center = (to - from_) / 2
            return from_, center, to, distance
        else:
            center = (from_ - to) / 2
            return to, center, from_, distance
    raise ValueError("no sufficient input to calculate all params")


def export_stl(scad_path, stl_path=None):
    if not stl_path:
        stl_path = os.path.splitext(scad_path)[0] + ".stl"
    subprocess.call(["openscad", "-o", stl_path, scad_path])
    return stl_path


E = 0.02  # an EPSILON value. Use it when you want to make sure that 2 aligned planes do not overlap
EE: float = 0.04  # a double EPSILON value.

T = 0.1  # a small TOLERANCE value.
TT = 0.2  # a large TOLERANCE value.
TTT = 0.3  # a very large TOLERANCE value

INFINITY = 999_999_999
