"""Main."""
from typing import Union, List


def yaml2instances(
    loading_data: Union[dict, List[dict]], search_modules: list, **kwargs
) -> list:
    """From the list of modules, find the class written in yaml and instantiate it."""
    instance_list = []
    if isinstance(loading_data, list):
        for conf in loading_data:
            for instance in _loading_data_to_instance(conf, search_modules, **kwargs):
                instance_list.append(instance)
    elif isinstance(loading_data, dict):
        for instance in _loading_data_to_instance(
            loading_data, search_modules, **kwargs
        ):
            instance_list.append(instance)
    else:
        TypeError

    return instance_list


def _loading_data_to_instance(loading_data: dict, search_modules, **kwargs):
    modules_dict = {}
    for _item, _kwargs in loading_data.items():
        if _kwargs is not None:
            kwargs.update(_kwargs)
        for module in search_modules:
            _modules = module.__dict__
            modules_dict.update(_modules)
        instance = modules_dict[_item](**(kwargs or {}))
        yield instance
