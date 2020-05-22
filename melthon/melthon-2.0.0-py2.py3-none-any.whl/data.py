from pathlib import Path

import yaml


def get_yaml_data(path):
    data = {}
    for filename in Path(path).glob('*.yml'):
        data[filename.stem] = load_yaml_file(filename)
    return data


def load_yaml_file(path):
    '''Load and parse the YAML file at path'''
    with path.open(mode='r') as file_config:
        return yaml.safe_load(file_config)
