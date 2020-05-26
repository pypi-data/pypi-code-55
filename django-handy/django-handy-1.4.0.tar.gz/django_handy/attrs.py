import collections
from typing import Sized


def get_attribute(instance, name):
    """
        Similar to Python's built in `getattr(instance, attr)`,
        but takes a list of nested attributes, instead of a single attribute.

        Also accepts either attribute lookup on objects or dictionary lookups.
    """

    attrs = name.split('.')
    for attr in attrs:
        if isinstance(instance, collections.Mapping):
            try:
                instance = instance[attr]
            except KeyError as exc:
                raise AttributeError(exc) from exc
        else:
            instance = getattr(instance, attr)
    return instance


def has_attribute(obj, name):
    """
        Like normal hasattr, but follows dotted paths
    """
    try:
        get_attribute(obj, name)
    except AttributeError:
        return False

    return True


def is_empty(val):
    """
        Check where value is logically `empty` - does not contain information.
        False and 0 are not considered empty, but empty collections are.
    """
    if val is None or isinstance(val, Sized) and len(val) == 0:  # Empty string is also Sized of len 0
        return True
    return False
