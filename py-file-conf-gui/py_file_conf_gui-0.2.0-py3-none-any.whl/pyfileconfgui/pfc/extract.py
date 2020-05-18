from copy import deepcopy
from typing import Union, List

from pyfileconf import Selector
from pyfileconf.basemodels.collection import Collection
from pyfileconf.logic.get import _get_public_name_or_special_name
from pyfileconf.pipelines.models.collection import PipelineCollection
from pyfileconf.views.object import ObjectView


def full_dict_from_selector(s: Selector) -> dict:
    pc_dict = s._structure.copy()
    out_dict: dict = {}
    pc: Collection
    for manager_key, manager_dict in pc_dict.items():
        out_dict[manager_key] = {}
        for key, pc in manager_dict.items():
            if key == '_general':
                # Skip level of _general dict
                out_dict[manager_key].update(_collection_to_dict(manager_dict['_general']))
            else:
                # Specific class dict, keep level
                out_dict[manager_key][key] = _collection_to_dict(pc)
    return out_dict


def _collection_to_dict(pc: Collection) -> Union[dict, str]:
    out_dict = pc.name_dict.copy()
    value: Union[Collection, ObjectView, List[ObjectView]]
    if len(out_dict) == 1 and all(isinstance(val, ObjectView) for val in out_dict.values()):
        return list(out_dict.values())[0].name
    if (
            len(out_dict) == 1 and
            hasattr(pc, 'klass') and
            pc.klass is not None and
            all(isinstance(val, pc.klass) for val in out_dict.values())
    ):
        return getattr(list(out_dict.values())[0], pc.key_attr)
    for key, value in out_dict.items():
        if isinstance(value, ObjectView):
            # replace with str of name
            out_dict[key] = value.name
        elif isinstance(value, list):
            out_dict[key] = [val.name for val in value]
        elif isinstance(value, Collection):
            # recursively convert PipelineCollection to dict
            out_dict[key] = _collection_to_dict(value)
        elif hasattr(pc, 'klass') and pc.klass is not None and isinstance(value, pc.klass):
            name = getattr(value, pc.key_attr)
            out_dict[key] = name
        else:
            raise ValueError(f'expected one of PipelineCollection, ObjectView, List[ObjectView], or specific class, '
                             f'got {value} of type {type(value)}')
    return out_dict
