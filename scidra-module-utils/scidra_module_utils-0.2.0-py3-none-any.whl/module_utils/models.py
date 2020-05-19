
from typing import List, Optional
from humps.camel import case
from pydantic import BaseModel


def to_camel(string):
    return case(string)


class CamelModel(BaseModel):
    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class FileRef(CamelModel):
    id: str
    name: str
    url: Optional[str] = None
    path: Optional[str] = None
    size_bytes: Optional[int]


class Output(CamelModel):
    output_json: str
    files: Optional[List[FileRef]] = None
