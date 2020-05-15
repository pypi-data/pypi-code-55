from humps.camel import case
from pydantic import BaseModel


def to_camel(string):
    return case(string)


class CamelModel(BaseModel):
    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class FileDownloadRef(CamelModel):
    name: str
    url: str
    extension: str
    size: int
