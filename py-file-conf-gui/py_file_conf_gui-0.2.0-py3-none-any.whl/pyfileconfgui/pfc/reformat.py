from typing import List


def nested_dict_to_paths(d: dict, begin_path: str = '', sep: str = '/') -> List[str]:
    paths = []
    base_path_parts = [begin_path] if begin_path else []
    for key, value in d.items():
        path_parts = base_path_parts + [key]
        if isinstance(value, str):
            path = sep.join(path_parts + [value])
            paths.append(path)
        elif isinstance(value, list):
            for v in value:
                if not isinstance(v, str):
                    raise ValueError(f'expected only strings inside lists, got {v} of type {type(v)}')
                path = sep.join(path_parts + [v])
                paths.append(path)
        elif isinstance(value, dict):
            nested_begin_path = sep.join(path_parts)
            paths.extend(nested_dict_to_paths(value, begin_path=nested_begin_path, sep=sep))
        else:
            raise ValueError(f'expected only dicts, lists, and strings, got {value} of type {type(value)}')
    return paths


def convert_name_to_id(name: str) -> str:
    return name.replace(' ', '-').replace('_', '-')
