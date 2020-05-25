import jsonschema
import yaml
import json


def load_file(path: str) -> dict:
    with open(str(path)) as f:
        return load_string(f.read())


def load_string(data: str) -> dict:
    try:
        return load_json(data)
    except json.JSONDecodeError:
        return load_yaml(data)


def load_json(data: str) -> dict:
    return json.loads(data)


def load_yaml(data: str) -> dict:
    return yaml.safe_load(data)
