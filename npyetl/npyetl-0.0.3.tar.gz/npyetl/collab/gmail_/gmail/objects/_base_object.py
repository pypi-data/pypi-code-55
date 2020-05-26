from __future__ import annotations
from abc import (
    ABC
)
import json


class _BaseObject(ABC):
    
    def __init__(self,
                 id: str):
        self._id = id
        
    @classmethod
    def from_dict(cls, dictionary: dict) -> _BaseObject:
        return cls(**dictionary)
    
    @classmethod
    def from_json(cls, json_content: str):
        return cls.from_dict(json.loads(json_content))
    
    @property
    def id(self) -> str:
        return self._id
