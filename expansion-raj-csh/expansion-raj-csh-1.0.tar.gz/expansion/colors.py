"""This is the colors module of the expansion package.
    Contains ColorInstruction abstract base class and predefined
    color classes for use in expansion.ColoredPoint().
"""

# pylint: disable=super-init-not-called

__version__ = '1.0'
__author__ = 'Rajarshi Mandal'
__all__ = ['ColorInstruction',
           'ColorA',
           'ColorB']

import abc


class ColorInstruction(metaclass=abc.ABCMeta):
    """Abstract Base Class for all color instructions to derive from."""
    def __init__(self, *args, **kwargs):
        pass

    def __call__(self, point, coords_diff):
        """Executes color instruction to obtain color.
            Not to be overriden by derived classes.

            Args:
                point (expansion.ColoredPoint): Parent point to calculate color from.
                coords_diff (iterable)(int): Difference in position in parent and child points.

            Returns:
                (iterable)(int): Color of child point.
        """
        if coords_diff == (1, 0):
            color = self.x_increasing(point)
        elif coords_diff == (0, 1):
            color = self.y_increasing(point)
        elif coords_diff == (-1, 0):
            color = self.x_decreasing(point)
        elif coords_diff == (0, -1):
            color = self.y_decreasing(point)

        return color

    @abc.abstractmethod
    def x_increasing(self, point):
        """Called when coords_diff == (1, 0),
            i.e. when x is increasing, but y is constant.

            Args:
                point (expansion.ColoredPoint): Parent point to calculate color from.

            Returns:
                (iterable)(int): Color of child point.
        """

    @abc.abstractmethod
    def y_increasing(self, point):
        """Called when coords_diff == (0, 1),
            i.e. when y is increasing, but x is constant.

            Args:
                point (expansion.ColoredPoint): Parent point to calculate color from.

            Returns:
                (iterable)(int): Color of child point.
        """

    @abc.abstractmethod
    def x_decreasing(self, point):
        """Called when coords_diff == (-1, 0),
            i.e. when x is decreasing, but y is constant.

            Args:
                point (expansion.ColoredPoint): Parent point to calculate color from.

            Returns:
                (iterable)(int): Color of child point.
        """

    @abc.abstractmethod
    def y_decreasing(self, point):
        """Called when coords_diff == (0, -1),
            i.e. when y is decreasing, but x is constant.

            Args:
                point (expansion.ColoredPoint): Parent point to calculate color from.

            Returns:
                (iterable)(int): Color of child point.
        """

class ColorA(ColorInstruction):
    """A builtin expansion color instruction, descriptively named 'A'."""
    def x_increasing(self, point):
        return (point.r+(1/point.length), point.g+(1/point.length), point.b-(1/point.length))

    def y_increasing(self, point):
        return (point.r-(1/point.length), point.g+(1/point.length), point.b+(1/point.length))

    def x_decreasing(self, point):
        return (point.r-(1/point.length), point.g-(1/point.length), point.b+(1/point.length))

    def y_decreasing(self, point):
        return (point.r+(1/point.length), point.g-(1/point.length), point.b-(1/point.length))

class ColorB(ColorInstruction):
    """A builtin expansion color instruction, descriptively named 'B'."""
    def x_increasing(self, point):
        return (point.r+(1/point.length), point.g+(1/point.length), point.b-(1/point.length))

    def y_increasing(self, point):
        return (point.r-(1/point.length), point.g+(1/point.length), point.b-(1/point.length))

    def x_decreasing(self, point):
        return (point.r-(1/point.length), point.g-(1/point.length), point.b+(1/point.length))

    def y_decreasing(self, point):
        return (point.r+(1/point.length), point.g-(1/point.length), point.b-(1/point.length))
