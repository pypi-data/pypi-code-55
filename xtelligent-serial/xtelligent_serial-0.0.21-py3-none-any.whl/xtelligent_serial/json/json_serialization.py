from json import dumps, loads
from typing import Type

# pylint: disable=redefined-builtin

from .. import to_serializable, from_serializable, JSONSerializable

def to_json(target: JSONSerializable, **kwargs) -> str:
    d = to_serializable(target)
    return dumps(d, **kwargs)

def from_json(type: Type, json_text: str, **kwargs) -> JSONSerializable:
    d = loads(json_text, **kwargs)
    return from_serializable(type, d)
