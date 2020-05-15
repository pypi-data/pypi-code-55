import numpy as np
import crystally.core.constants as const


class FractionalVector:
    r"""A point in fractional space - e.g. in a crystal system.

    A fractional vector has three coordinates in range [0, 1). The fractional vector space is periodic, meaning
    that values greater or equal to one can be reduced: 1.1 == 0.1 and -0.2 == 0.8
    This class is only a wrapper for the numpy array which checks the coordinates and the shape of the array. To access
    the numpy array use :meth:`value`.

    :param vector: vector like container
    :return: FractionalVector with altered coordinates

    Examples
    --------
    >>> FractionalVector([1.0, 0.1, -0.6])
    FractionalVector([0.0, 0.1, 0.4])

    """

    def __init__(self, vector):
        vector = getattr(vector, "value", vector)
        self.__value = np.array(vector) % 1.0

    def __add__(self, other):
        other = getattr(other, "value", other)
        new_vec = FractionalVector(self.value + np.array(other))
        return new_vec

    def __sub__(self, other):
        return self + other*-1

    def __truediv__(self, other: float):
        new_vec = FractionalVector(self.value / other)
        return new_vec

    def __mul__(self, other):
        other = getattr(other, "value", other)
        new_vec = FractionalVector(self.value * np.array(other))
        return new_vec

    def __round__(self, n=None):
        if not n:
            n = const.VEC_ROUNDING
        return FractionalVector([n * round(x/n) for x in self])

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return "FractionalVector({})".format(self.value.tolist())

    def __getitem__(self, item):
        return self.value[item]

    def __len__(self):
        return len(self.value)

    def __hash__(self):
        return hash(tuple(round(self).tolist()))

    def __eq__(self, other):
        rounded1 = tuple(tuple(round(self).tolist()))
        rounded2 = tuple(tuple(round(other).tolist()))
        return rounded1 == rounded2

    @property
    def value(self):
        """ Get the wrapped numpy array

        :return: numpy array
        """
        return self.__value

    @value.setter
    def value(self, vec):
        raise TypeError("FractionalVector is immutable")

    @property
    def x(self):
        """ Get the x component of this vector, is identical to vec[0]

        :return: depends on the entry in the vector (probably a float)
        """
        if len(self) < 1:
            raise IndexError("This vector does not have a x component.")
        return self[0]

    @property
    def y(self):
        """ Get the y component of this vector, is identical to vec[0]

        :return: depends on the entry in the vector (probably a float)
        """
        if len(self) < 2:
            raise IndexError("This vector does not have a y component.")
        return self[1]

    @property
    def z(self):
        """ Get the z component of this vector, is identical to vec[0]

        :return: depends on the entry in the vector (probably a float)
        """
        if len(self) < 3:
            raise IndexError("This vector does not have a z component.")
        return self[2]

    def tolist(self):
        """ Unwrap vector and get list representation of numpy array

        :return: list of entries
        """
        return self.value.tolist()

    def diff(self, other):
        """ Get the minimal distance between two FractionalVector

        :param other: vector like container
        :return: 1xN numpy array where N is the dimension of the vectors

        Examples
        --------
        >>> FractionalVector([0.2, 0, 0]).diff([0, 0, 0.2])
        array([-0.2,  0. ,  0.2])

        >>> vec1 = FractionalVector([0.5, 0.5, 0.5])
        >>> vec2 = FractionalVector([0.6, 0.7, 0.8])
        >>> vec1.diff(vec2)
        array([0.1,  0.2 ,  0.3])
        >>> vec2.diff(vec1)
        array([-0.1,  -0.2 ,  -0.3])
        """
        other = FractionalVector(other)
        vec = np.array(other.value) - self.value
        return np.array([_min_periodic_distance(c) for c in vec])


def _min_periodic_distance(x):
    """Calculate the minimal periodic distance from the origin for one coordinate

    :param x: coordinate value
    :return: distance of coordinate from origin

    Examples
    --------
    >>>_min_periodic_distance(-0.6)
    0.4
    """
    if abs(x) > 0.5:
        return _min_periodic_distance(x - np.sign(x))
    else:
        return x

