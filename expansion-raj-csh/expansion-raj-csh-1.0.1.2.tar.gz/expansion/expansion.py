"""This is the main module in the expansion package.
    Contains the main classes and functions to be used when importing the expansion package.
    Classes and methods imported into namespace as
    expansion.name rather than expansion.expansion.name.
"""

from __future__ import annotations

__version__ = '1.0'
__author__ = 'Rajarshi Mandal'
__all__ = ['ColoredPoint',
           'ColoredPointHandler',
           'is_multiprocessing',
           'disable_multiprocessing',
           'enable_multiprocessing',
           'core_count']

import multiprocessing
import os
from typing import Iterable, List, Optional, Tuple, TYPE_CHECKING

from PIL import Image
import numpy as np

if TYPE_CHECKING:
    from expansion import callbacks as cb
    from expansion import colors

_M = [False, None, 1]

"""These are mutable flags to be passed between script and module.
    Not meant to be accessed directly, but rather through wrapper functions,
    such as enable_multiprocessing() or is_multiprocessing().

    _M[0] = multiprocessing
    _M[1] = pool
    _M[2] = core_count
"""

class ColoredPoint:
    """Reproductive point which stores its position and color.
        All attributes are read-only.
        Object instances do not define a __dict__, due to the
        use of __slots__ for decreased size and increased speed.

        Args:
            length (int): Side length of square numpy array of which this point belongs to.
            coords (tuple)(int): A tuple of integers, consisting of x, y
                                 coordinates in the range(0, length).
            rgb (tuple)(float): A tuple of 3 floats scaled between 0 and 1 to
                                represent the RGB color value of the point.
            color_instruction (expansion.colors.ColorInstruction): Instance of a subclass of
                                                                   expansion.colors.ColorInstruction
                                                                   that defines methods to determine
                                                                   color of reproduced point.
            environment_sensitive (bool): Boolean value, defaults to False,
                                          if True selects environment sensitive reproduce method.
    """
    __slots__ = ['_length', '_color_instruction', '_environment_sensitive', '_coords', '_rgb']

    def __init__(self, length: int, coords: Tuple[int, int], rgb: Tuple[float, float, float], # pylint: disable=too-many-arguments
                 color_instruction: colors.ColorInstruction,
                 environment_sensitive: bool = False) -> None:

        self._length = length
        self._color_instruction = color_instruction
        self._environment_sensitive = environment_sensitive
        self._coords = coords
        self._rgb = rgb

    @property
    def length(self) -> int:
        """(int): Side length of square numpy array of which this point belongs to."""
        return self._length

    @property
    def color_instruction(self) -> 'colors.ColorInstruction':
        """(expansion.colors.ColorInstruction): Color instruction of point."""
        return self._color_instruction

    @property
    def environment_sensitive(self) -> bool:
        """(bool): Selects reproduction method for point."""
        return self._environment_sensitive

    @property
    def x(self) -> int:
        """(int): X coordinate of point in range(0, ColoredPoint.length)."""
        return self._coords[0]

    @property
    def y(self) -> int:
        """(int): Y coordinate of point in range(0, ColoredPoint.length)."""
        return self._coords[1]

    @property
    def r(self) -> float:
        """(float): Red channel (RGB) of color of point scaled between 0 and 1."""
        return self._rgb[0]

    @property
    def g(self) -> float:
        """(float): Green channel (RGB) of color of point scaled between 0 and 1."""
        return self._rgb[1]

    @property
    def b(self) -> float:
        """(float): Blue channel (RGB) of color of point scaled between 0 and 1."""
        return self._rgb[2]

    def __repr__(self) -> str:
        """Representation of ColoredPoint instances.

            Returns:
                (str): Representation of ColoredPoint instance.
        """
        return (f'ColoredPoint(coords={self._coords}, rgb={self._rgb}, '
                f'color_instruction={self.color_instruction}, length={self.length}, '
                f'environment_sensitive={self.environment_sensitive})')

    def __eq__(self, value) -> bool:
        """Checks value equality based on underlying coordinates tuple,
            if both values compared are of type ColoredPoint,
            otherwise returns False.

            Args:
                value (object): The value to check equality against.

            Returns:
                (bool): Set to True if both values are of type ColoredPoint,
                        and coordinates are the same, otherwise is set to False.
        """
        return self._coords == value._coords if isinstance(value, ColoredPoint) else False

    def __hash__(self) -> int:
        """Returns hash of underlying coordinates tuple,
            as ColoredPoint instances are unhashable.
            Implemented for use in sets.

            Returns:
                (int): A unique integer that is the hash of the
                       coordinates tuple of the ColoredPoint instance.
        """
        return hash(self._coords)

    def reproduce(self, arr: Optional[np.ndarray] = None) -> List[ColoredPoint]:
        """Reproduces point with altered color and position
            by generating new instances of ColoredPoint.
            Checks to see whether 4 immediate directions of point are within bounds,
            before changing color by a small increment and instantiating a new ColoredPoint.
            If environment_sensitive is enabled then will check if an obstacle is in the way,
            colored in white(RGB = [1.0, 1.0, 1.0]),
            before instantiating new ColoredPoint.

            Args:
                arr (numpy.ndarray): An image, in the form of a numpy array with 3 ndimensions,
                                     and float values scaled between 0 and 1.
                                     Defaults to None, for when environment_sensitive is False,
                                     however should be passed an array
                                     when environment_sensitive is True.

            Returns:
                (list)(expansion.ColoredPoint): A list of the new ColoredPoint
                                                instances that have met the criteria.
        """
        return (_reproduce_environment_sensitive(self, arr) if self.environment_sensitive
                else _reproduce_environment_insensitive(self))

    def render(self, arr: np.ndarray) -> np.ndarray:
        """Draws point to specified array.

            Args:
                arr (numpy.ndarray): An image, in the form of a numpy array with 3 ndimensions,
                                     and float values scaled between 0 and 1.

            Returns:
                (numpy.ndarray): The initial array with the point now drawn onto it.
        """
        arr[self.x, self.y] = [self.r, self.g, self.b]
        return arr

class ColoredPointHandler:
    """Handles and contains ColoredPoint objects.

        Args:
            length (int): Side length of square numpy array, which handler renders to.
            initial_points (iterable)(expansion.ColoredPoint): Initial points for handler to use.
            initial_image (numpy.ndarray): Image, for handler to render to,
                                           in the form of a numpy with 3 ndimensions,
                                           and float values scaled between 0 and 1.
    """
    __slots__ = ['_length', '_arr', '_points', '_environment_sensitive']

    def __init__(self, length: int, initial_points: Iterable[ColoredPoint],
                 initial_image: Optional[np.ndarray] = None) -> None:
        self._length = length

        if initial_image is not None:
            self._arr = initial_image
        else:
            self._arr = np.zeros((length, length, 3), dtype=float)

        self._points = list(initial_points)
        self._environment_sensitive = self.points[0].environment_sensitive

    @property
    def length(self) -> int:
        """(int): Side length of square numpy array, which handler renders to. Read-only."""
        return self._length

    @property
    def arr(self) -> np.ndarray:
        """(numpy.ndarray): Image, for handler to render to, in the form of a numpy array
                            with 3 ndimensions, and float values scaled between 0 and 1.
        """
        return self._arr

    @arr.setter
    def arr(self, value: np.ndarray) -> None:
        """(numpy.ndarray): Image, for handler to render to, in the form of a numpy array
                            with 3 ndimensions, and float values scaled between 0 and 1.

            Raises:
                ValueError: If array given is of a different shape to original array.
        """
        if value.shape == self.arr.shape:
            self._arr = value
        else:
            raise ValueError('Expansion: value to set ColoredPointHandler.arr '
                             f'must be of same shape {self.arr.shape}')

    @property
    def points(self) -> List[ColoredPoint]:
        """(list)(expansion.ColoredPoint): Points for handler to use."""
        return self._points

    @points.setter
    def points(self, value: List[ColoredPoint]) -> None:
        """(list)(expansion.ColoredPoint): Points for handler to use.

            Raises:
                ValueError: If list passed is empty.
        """
        if len(value) > 0:
            self._points = value
        else:
            raise ValueError(f'Expansion: value {value} to set ColoredPointHandler.points'
                             'must be a non-empty list!')

    @property
    def environment_sensitive(self) -> bool:
        """(bool): Boolean value to select points' reproduction method."""
        return self._environment_sensitive

    @environment_sensitive.setter
    def environment_sensitive(self, value: bool) -> None:
        """(bool): Boolean value to select points' reproduction method."""
        self._environment_sensitive = value
        for point in self.points:
            point._environment_sensitive = self.environment_sensitive # pylint: disable=protected-access

    def reproduce_points(self) -> None:
        """Reproduces points and updates internal list."""
        pool = _pool()

        new_points = []

        if is_multiprocessing():
            if self.environment_sensitive:
                lists_of_children = pool.starmap(ColoredPoint.reproduce,
                                                 zip(self.points, [self.arr]*len(self.points)))
            else:
                lists_of_children = pool.map(ColoredPoint.reproduce, self.points)

            for list_of_children in lists_of_children:
                new_points.extend(list_of_children)
        else:
            if self.environment_sensitive:
                for point in self.points:
                    new_points.extend(point.reproduce(self.arr))
            else:
                for point in self.points:
                    new_points.extend(point.reproduce())

        self.points.extend(new_points)

    def kill_competitors(self) -> None:
        """Deletes points which have positions that have already been occupied.

            Raises:
                AssertionError: If ColoredHandler.points becomes greater than
                                its allocated length (= ColoredHandler.length ** 2).
        """
        self.points = list(set(self.points))

        assert len(self.points) <= (self.length ** 2), ('Expansion: ColoredPointHandler.points'
                                                        'is greater than allocated length'
                                                        f'({len(self.points)} > {self.length**2})!')

    def render_points(self) -> None:
        """Renders points to internal array,
            which can be exported via the
            export_as_img() or export_as_arr(),
            methods, which return a
            PIL.Image.Image and numpy.ndarray respectively.
        """
        arr = self.points[0].render(self.arr)
        for point in self.points[1:]:
            arr = point.render(arr)

        self.arr = arr

    def run_callbacks(self, callbacks: Optional[Iterable[cb.Callback]], epoch: int) -> None:
        """Executes callbacks on points given an epoch number.

            Args:
                callbacks (iterable)(expansion.callbacks.Callbacks): Callbacks to execute.
                epoch (int): Epoch number to pass to callbacks.
        """
        if callbacks is not None:
            for callback in callbacks:
                callback(epoch, self)

    def simulate(self, epochs: int = 0, callbacks: Optional[Iterable[cb.Callback]] = None,
                 close_pool_on_end: bool = True) -> None:
        """Reproduces points, then kills competitors, then renders points, then runs callbacks,
            for a given number of epochs or until image is wholly colored.

            Args:
                epochs (int): Number of epochs to simulate,
                              if 0 will simulate until image is wholly colored,
                              defaults to 0.
                callbacks (iterable)(expansion.callbacks.Callback): Callbacks to run
                                                                    once points have
                                                                    been reproduced,
                                                                    duplicates deleted,
                                                                    and array updated.
                close_pool_on_end (bool): Whether to close multiprocessing pool once
                                          function has terminated or leave it running,
                                          defaults to True.
        """
        print('Expansion: simulating!')
        print(f'Expansion: running on {_M[2]} core(s)!\n')

        pool = _pool()

        if epochs != 0:
            for epoch in range(epochs):
                self.reproduce_points()
                self.kill_competitors()
                self.render_points()
                self.run_callbacks(callbacks, epoch)
        else:
            all_done = False
            epoch = 0
            while not all_done:
                self.reproduce_points()
                self.kill_competitors()
                self.render_points()
                self.run_callbacks(callbacks, epoch)

                epoch += 1

                diff_2d = (np.mean(self.arr, axis=2)
                           != np.zeros((self.length, self.length))).tolist()

                diff_1d = [all(l) for l in diff_2d]

                all_done = all(diff_1d)

        if (is_multiprocessing() or (pool is not None)) and close_pool_on_end:
            pool.close()

        print('Expansion: finished successfully!')

    def export_as_arr(self) -> np.ndarray:
        """Exports internal array as a numpy array
            with datatype as unsigned 8-bit integers.

            Returns:
                (numpy.ndarray): Rendered RGB image in the form
                                 of a 3 ndimensional numpy array
                                 with a datatype of numpy.uint8.
        """
        return (self.arr * 255.).astype(np.uint8)

    def export_as_img(self) -> Image.Image:
        """Exports internal array as a RGB PIL image.

            Returns:
                (PIL.Image.Image): Rendered
        """
        return Image.fromarray(self.export_as_arr())


def is_multiprocessing() -> bool:
    """Checks if multiprocessing is enabled.

        Returns:
            (bool): Whether multiprocessing is enabled.
    """
    return _M[0]

def disable_multiprocessing() -> None:
    """Disables multiprocessing."""
    global _M # pylint: disable=global-statement
    print('Expansion: multiprocessing disabled!\n')

    _M[0] = False
    _M[1] = None

def enable_multiprocessing(cores_to_use: int = os.cpu_count()) -> None:
    """Enables multiprocessing.

        Args:
            cores_to_use (int): Number of cores to utilise,
                              defaults to all cores/os.cpu_count().
    """
    global _M # pylint: disable=global-statement
    print('Expansion: multiprocessing enabled!\n')

    _M[0] = True

    _M[1] = multiprocessing.Pool(cores_to_use)
    _M[2] = cores_to_use

def core_count() -> int:
    """Retrieve the number of cores utilised by multiprocessing.

        Returns:
            (int): Number of cores utilised by multiprocessing.
    """
    return _M[2]

def _pool() -> multiprocessing.pool.Pool:
    """Retrieve pool utilised by multiprocessing. If pool is None,
        instantiates a new multiprocessing.Pool with set core count.

        Returns:
            (multiprocessing.pool.Pool): Pool utilised by multiprocessing.
    """
    global _M # pylint: disable=global-statement

    if _M[1] is None and _M[0]:
        _M[1] = multiprocessing.Pool(_M[2])

    return _M[1]

def _reproduce_environment_sensitive(point: ColoredPoint, arr: np.ndarray)-> List[ColoredPoint]:
    """Reproduces point with altered color and position
        by generating new instances of ColoredPoint.
        Checks to see whether 4 immediate directions of point are within bounds,
        and will then check if an obstacle is in the way, colored in white(RGB=[1.0, 1.0, 1.0]),
        before changing color by a small increment and instantiating a new ColoredPoint.

        Args:
            point (expansion.ColoredPoint): Point to reproduce.
            arr (numpy.ndarray): An image, in the form of a numpy array with 3 ndimensions,
                                 and float values scaled between 0 and 1.

        Returns:
            (list): A list of the new ColoredPoint instances that have met the criteria.
    """
    p_space = [
        ((point.x+1 <= point.length-1 and point.x+1 >= 0)
         and (point.y <= point.length-1 and point.y >= 0)),
        ((point.x <= point.length-1 and point.x >= 0)
         and (point.y+1 <= point.length-1 and point.y+1 >= 0)),
        ((point.x-1 <= point.length-1 and point.x-1 >= 0)
         and (point.y <= point.length-1 and point.y >= 0)),
        ((point.x <= point.length-1 and  point.x >= 0)
         and (point.y-1 <= point.length-1 and point.y-1 >= 0))
        ]

    point_config = [((point.x+1, point.y), point.color_instruction(point, (1, 0))),
                    ((point.x, point.y+1), point.color_instruction(point, (0, 1))),
                    ((point.x-1, point.y), point.color_instruction(point, (-1, 0))),
                    ((point.x, point.y-1), point.color_instruction(point, (0, -1)))]

    in_bounds = []

    for index, condition in enumerate(p_space):
        if condition:
            in_bounds.append(point_config[index])
        else:
            copy = list(point_config[index])
            copy[0] = (point.x, point.y)

            in_bounds.insert(0, tuple(copy))

    approved = []

    for config_to_test in in_bounds:
        if not all(list(arr[config_to_test[0][0], config_to_test[0][1]] == [1., 1., 1.])):
            approved.append(config_to_test)
        else:
            diff_x = config_to_test[0][0] - point.x
            diff_y = config_to_test[0][1] - point.y

            if diff_x != 0 or diff_y != 0:
                copy = list(config_to_test)
                copy[0] = (copy[0][0]-diff_x, copy[0][1]-diff_y)
                copy[1] = tuple(1-channel for channel in copy[1])

                approved.append(tuple(copy))

    children = []

    for config in approved:
        children.append(ColoredPoint(point.length, *config, point.color_instruction, True))

    return children

def _reproduce_environment_insensitive(point: ColoredPoint) -> List[ColoredPoint]:
    """Reproduces point with altered color and position
        by generating new instances of ColoredPoint.
        Checks to see whether 4 immediate directions of point are within bounds,
        before changing color by a small increment and instantiating a new ColoredPoint.

        Args:
            point (expansion.ColoredPoint): Point to reproduce.

        Returns:
            (list): A list of the new ColoredPoint instances that have met the criteria.
    """
    p_space = [
        ((point.x+1 <= point.length-1 and point.x+1 >= 0)
         and (point.y <= point.length-1 and point.y >= 0)),
        ((point.x <= point.length-1 and point.x >= 0)
         and (point.y+1 <= point.length-1 and point.y+1 >= 0)),
        ((point.x-1 <= point.length-1 and point.x-1 >= 0)
         and (point.y <= point.length-1 and point.y >= 0)),
        ((point.x <= point.length-1 and  point.x >= 0)
         and (point.y-1 <= point.length-1 and point.y-1 >= 0))
        ]

    point_config = [((point.x+1, point.y), point.color_instruction(point, (1, 0))),
                    ((point.x, point.y+1), point.color_instruction(point, (0, 1))),
                    ((point.x-1, point.y), point.color_instruction(point, (-1, 0))),
                    ((point.x, point.y-1), point.color_instruction(point, (0, -1)))]

    children = []

    for index, condition in enumerate(p_space):
        if condition:
            children.append(ColoredPoint(point.length, *(point_config[index]),
                                         point.color_instruction))

    return children
