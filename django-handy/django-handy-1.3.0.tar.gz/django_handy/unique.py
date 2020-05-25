from typing import Hashable, Iterable, List

from django_handy.attrs import get_attribute


def unique_ordered(sequence: Iterable[Hashable]) -> List:
    return list(dict.fromkeys(sequence))


def get_unique_objs(objs: List[object], unique_attrs: List[str]) -> List[object]:
    """
       Get list of unique objs from sequence,
        preserving order when the objs first occurred in original sequence
    """

    seen_obj_footprints = set()
    unique_objs = []
    for obj in objs:
        obj_footprint = tuple(get_attribute(obj, field) for field in unique_attrs)
        if obj_footprint in seen_obj_footprints:
            continue

        seen_obj_footprints.add(obj_footprint)
        unique_objs.append(obj)
    return unique_objs
