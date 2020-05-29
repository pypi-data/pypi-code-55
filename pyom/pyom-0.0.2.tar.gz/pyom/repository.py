from typing import Union
from .container import Container
from .relation import EntityType


class Repository:
    __register_as__: str
    __relation__: str

    def __init__(self, container: Container):
        self.container = container
        self.relation = container.relation(self.__class__.__relation__)

    def create(self, **kwargs: Union[str, bool]) -> EntityType:
        pk = self.relation.insert(**kwargs)
        return self.relation.by_pk(pk).one()
