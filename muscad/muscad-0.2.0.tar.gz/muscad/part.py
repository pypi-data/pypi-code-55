from itertools import chain

from muscad import (
    Composite,
    Hole,
    Misc,
    Object,
    back,
    bottom,
    front,
    left,
    render_comment,
    right,
    top,
    EE,
)


def walk_mro_until(cls, supercls):
    for c in cls.mro():
        if c == supercls:
            break
        yield c


class Part(Composite):
    """
    Helper class to build complex objects.
    A Part is made of 3 kind of objects:
    - instances of Object, which will form the "main" structure of this Part
    - instances of Misc, which are miscellaneous items that will not be taken into account when evaluating this Part dimensions
    - instances of Hole, which will be "unfillable" holes which will be substracted from that Part.

    Those objects can be added to that Part using add_child(), add_misc() or add_hole().
    All class attributes that are instances of Object, Misc or Hole will be added to all instances of this Part.
    """

    def __init_subclass__(cls, **kwargs):
        """
        When creating an inherited class, sort all class-level attributes and make lists of all Objects, Misc and Holes
        """
        super().__init_subclass__(**kwargs)
        cls.class_parts = []
        cls.class_misc = []
        cls.class_holes = []
        for class_ in walk_mro_until(cls, Part):
            for name, obj in class_.__dict__.items():
                if name.startswith("_"):
                    continue
                cls._init_element(name, obj)

    @classmethod
    def _init_element(cls, name, obj):
        """
        Given a class level attribute, add it to the class level lists of misc/holes/parts.
        :param name: the attribute name
        :param obj: the attribute value
        :return:
        """
        if isinstance(obj, Misc):
            obj = obj.object
            if obj.comment is None:
                obj.comment = name
            cls.class_misc.append(obj)
        elif isinstance(obj, Hole):
            obj = obj.object
            if obj.comment is None:
                obj.comment = name
            cls.class_holes.append(obj)
        elif isinstance(obj, Object):
            if obj.comment is None:
                obj.comment = name
            cls.class_parts.append(obj)

    def __init__(self, *args, **kwargs):
        """
        When instanciating a Part, add the class level misc/holes/parts to the instance.
        :param args:
        :param kwargs:
        """
        super().__init__()
        self.children = self.class_parts.copy()
        self.holes = self.class_holes.copy()
        self.miscellaneous = self.class_misc.copy()
        self.init(*args, **kwargs)

    def init(self, *args, **kwargs):
        """
        Override this to add parametric children to this Parts
        :param args:
        :param kwargs:
        :return:
        """
        pass

    def add_hole(self, obj):
        if isinstance(obj, Hole):
            self.holes.append(obj.object)
        else:
            self.holes.append(obj)

    def add_misc(self, obj):
        self.miscellaneous.append(obj.object)

    def revert(self):
        """
        Turns all holes to children, and all children to holes.
        Note that misc items are untouched, so it probably makes no sense to revert a part containing misc items.
        :return: the same part, with holes and children reverted
        """
        self.children, self.holes = self.holes, self.children

    def __setattr__(self, key, value):
        previous = getattr(self, key, None)
        super().__setattr__(key, value)
        if key.startswith("_"):
            return
        elif isinstance(value, Misc):
            if value.comment is None:
                value.comment = key
            # if previous:
            #     self.miscellaneous.remove(previous)
            self.add_misc(value)
        elif isinstance(value, Hole):
            if value.comment is None:
                value.comment = key
            #            if previous:
            #               self.holes.remove(previous)
            self.add_hole(value)
        elif isinstance(value, Object):
            if value.comment is None:
                value.comment = key
            if previous:
                self.children.remove(previous)
            self.add_child(value)

    @render_comment
    def render(self, postprocess=True):
        if not self.children and not self.miscellaneous:
            raise RuntimeError("This part has no children")
        # renders children and misc
        renderable = sum(chain(self.children, self.miscellaneous))
        # if this part has holes, render a diff of all children with all holes
        if self.holes:
            renderable -= self.holes
        # applies postprocessing
        if postprocess:
            renderable = self.postprocess(renderable)
        # applies the modifier
        return renderable.set_modifier(self.modifier).render()

    def postprocess(self, renderable):
        """
        Applies some postprocessing transformation to the part, at render time.
        Postprocessing will not be taken into account when calculating this part dimension or position.
        You use it for example to position the Part to make printing easier.
        Postprocessing can be disabled by passing `postprocess=False` to ` render()`.
        This method can be overridden in subclasses. By default, it does nothing.
        :param renderable: the part to postprocess for rendering
        :return: the postprocessed renderable
        """
        return renderable

    def walk(self):
        yield from super().walk()
        for misc in self.miscellaneous:
            yield from misc.walk()

    @property
    def left(self):
        return left(self.children)

    @property
    def right(self):
        return right(self.children)

    @property
    def back(self):
        return back(self.children)

    @property
    def front(self):
        return front(self.children)

    @property
    def bottom(self):
        return bottom(self.children)

    @property
    def top(self):
        return top(self.children)


class MirroredPart(Part):
    def __init_subclass__(cls, x=False, y=False, z=False, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.mirror_x = x
        cls.mirror_y = y
        cls.mirror_z = z
        return cls

    @render_comment
    def render(self):
        if not self.children:
            raise RuntimeError("This part has no children")
        children = sum(self.children)
        if self.holes:
            children = children - self.holes
        if self.mirror_x:
            children = children.x_mirror(keep=True)
        if self.mirror_y:
            children = children.y_mirror(keep=True)
        if self.mirror_z:
            children = children.z_mirror(keep=True)
        return (
            (children + sum(self.miscellaneous))
            .set_modifier(self.modifier)
            .render()
        )

    @property
    def left(self):
        if self.mirror_x:
            return max(left(self.children), right(self.children))
        return left(self.children)

    @property
    def right(self):
        if self.mirror_x:
            return max(left(self.children), right(self.children))
        return right(self.children)

    @property
    def back(self):
        if self.mirror_y:
            return max(back(self.children), front(self.children))
        return back(self.children)

    @property
    def front(self):
        if self.mirror_y:
            return max(back(self.children), front(self.children))
        return front(self.children)

    @property
    def bottom(self):
        if self.mirror_z:
            return max(bottom(self.children), top(self.children))
        return bottom(self.children)

    @property
    def top(self):
        if self.mirror_z:
            return max(bottom(self.children), top(self.children))
        return top(self.children)


from muscad.primitives import Square


class RotationalExtrudedPart(Part):
    """
    A part that will be transformed with a RotationalExtrusion as postprocessing.
    You must build your part flat along the Y axis and have the shape defined on the positive X axis.
    """

    def init(self):
        # mask will hide the shape on negative X axis.
        mask = Square(width=self.width + EE, depth=self.depth + EE).align(
            right=self.center_x, center_y=self.center_y
        )
        self.add_hole(mask)

    def postprocess(self, renderable):
        return renderable.rotational_extrude()
