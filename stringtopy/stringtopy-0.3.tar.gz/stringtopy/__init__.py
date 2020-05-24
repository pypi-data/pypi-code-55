# coding: utf-8
"""
stringtopy is a small library to convert strings to a specified type (e.g.
int, float or bool), allowing more human friendly input similar to
configparser.

:copyright: (c) 2016 James Tocknell
:license: 3-clause BSD
"""

from fractions import Fraction

# versioneer stuff
from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

BOOLEAN_TRUE = {'1', 'yes', 'true', 'on', }
BOOLEAN_FALSE = {'0', 'no', 'false', 'off', }


def str_to_float_converter(use_none_on_fail=False):
    """
    Returns a human friendly float converter, can use use_none_on_fail to
    return None if value cannot be converted.
    """
    def str_to_float_func(s):
        """
        Convert a string to a float
        """
        try:
            return float(Fraction(s))
        except ValueError:
            if use_none_on_fail:
                return None
            raise
    return str_to_float_func


def str_to_int_converter(use_none_on_fail=False):
    """
    Returns a human friendly int converter, can use use_none_on_fail to return
    None if value cannot be converted.
    """
    def str_to_int_func(s):
        """
        Convert a string to a int
        """
        try:
            frac = Fraction(s)
            if frac.denominator == 1:
                return int(frac)
            raise ValueError("{} is not an integer".format(frac))
        except ValueError:
            if use_none_on_fail:
                return None
            raise
    return str_to_int_func


def str_to_bool_converter(
    boolean_true=None, boolean_false=None, additional=True
):
    """
    Returns a human friendly bool converter.

    Parameters
    ----------
    additional : bool
        If True, include the stringtopy defaults for True and False to the list
        of items considered True and False.
    boolean_true : iterable of str
        List of str to consider as True
    boolean_false : iterable of str
        List of str to consider as False
    """
    if boolean_true is None:
        boolean_true = set()
    else:
        boolean_true = set(boolean_true)
    if boolean_false is None:
        boolean_false = set()
    else:
        boolean_false = set(boolean_false)
    if additional:
        boolean_true.update(BOOLEAN_TRUE)
        boolean_false.update(BOOLEAN_FALSE)
    if not boolean_true.isdisjoint(boolean_false):
        raise ValueError(
            "{} are both True and False".format(boolean_true & boolean_false)
        )

    def str_to_bool_func(s):
        """
        Convert a string to a bool, based on settings
        """
        s = s.strip().lower()
        if s in boolean_true:
            return True
        if s in boolean_false:
            return False
        raise ValueError("{} is neither True nor False.".format(s))
    return str_to_bool_func


# versions using defaults so that users can import the actual functions, rather
# than creating their own
str_to_float = str_to_float_converter()
str_to_int = str_to_int_converter()
str_to_bool = str_to_bool_converter()
