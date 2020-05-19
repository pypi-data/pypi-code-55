from typing import List, Tuple, Callable, TypeVar, Optional
from abc import ABCMeta, abstractmethod
import copy
import numpy

from ..error import PatternError, PatternLockedError
from ..utils import is_scalar, rotation_matrix_2d, vector2, layer_t


T = TypeVar('T', bound='Positionable')


class Positionable(metaclass=ABCMeta):
    """
    Abstract class for all positionable entities
    """
    __slots__ = ('_offset',)

    _offset: numpy.ndarray
    """ `[x_offset, y_offset]` """

    # --- Abstract methods
    @abstractmethod
    def get_bounds(self) -> numpy.ndarray:
        """
        Returns `[[x_min, y_min], [x_max, y_max]]` which specify a minimal bounding box for the entity.
        """
        pass

    # ---- Non-abstract properties
    # offset property
    @property
    def offset(self) -> numpy.ndarray:
        """
        [x, y] offset
        """
        return self._offset

    @offset.setter
    def offset(self, val: vector2):
        if not isinstance(val, numpy.ndarray):
            val = numpy.array(val, dtype=float)

        if val.size != 2:
            raise PatternError('Offset must be convertible to size-2 ndarray')
        self._offset = val.flatten()


    # ---- Non-abstract methods
    def translate(self: T, offset: vector2) -> T:
        """
        Translate the entity by the given offset

        Args:
            offset: [x_offset, y,offset]

        Returns:
            self
        """
        self.offset += offset
        return self

    def lock(self: T) -> T:
        """
        Lock the entity, disallowing further changes

        Returns:
            self
        """
        self.offset.flags.writeable = False
        return self

    def unlock(self: T) -> T:
        """
        Unlock the entity

        Returns:
            self
        """
        self.offset.flags.writeable = True
        return self
