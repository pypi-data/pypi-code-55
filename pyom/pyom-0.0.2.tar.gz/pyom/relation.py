from __future__ import annotations
from typing import Callable, Union, Any, List, TypeVar, Optional, Type
from sqlalchemy.sql.base import ImmutableColumnCollection
from sqlalchemy.sql.schema import Table
from sqlalchemy.sql.selectable import Select
from .mapper import Mapper
from .immutable_object import ImmutableObject
from .exceptions import PomError
from .gateway import Gateway, Row

RelationType = TypeVar("RelationType", bound="Relation")
EntityType = TypeVar("EntityType", bound="Entity")


class Entity:
    def __init__(self, kwargs: Row):
        pass


class Relation(ImmutableObject):
    __gateway__: str = "default"
    __table_name__: str
    __register_as__: str

    def __init__(
        self,
        gateway: Gateway,
        entity_class: Type[EntityType] = dict,  # type: ignore[assignment] # noqa: F821
        dataset: Optional[Table] = None,
        query: Optional[Select] = None,
        mapper_class: Type[Mapper] = Mapper,
    ):
        self.gateway = gateway
        self.dataset = (
            self.gateway.dataset(self.__class__.__table_name__)
            if dataset is None
            else dataset
        )
        self.query = (
            self.dataset.select().order_by(*self.dataset.primary_key.columns.values())
            if query is None
            else query
        )
        self.entity_class = entity_class
        self.mapper_class = mapper_class

    def map_with(
        self: RelationType,
        mapper_class: Type[Mapper],
    ) -> RelationType:
        return self.with_props(mapper_class=mapper_class)

    def map_to(
        self: RelationType,
        entity_class: Type[EntityType],
    ) -> RelationType:
        return self.with_props(entity_class=entity_class)

    def where(  # type: ignore[misc] # Explicit "Any" is not allowed # noqa: F821
        self: RelationType,
        function: Optional[Callable[[ImmutableColumnCollection], Any]] = None,
        **kwargs: Union[str, int, bool, List[str], List[int]],
    ) -> RelationType:
        if function is not None and not callable(function):
            raise PomError("It should be a lambda")

        query = self.query

        if function:
            query = query.where(function(self.dataset.c))

        for key, value in kwargs.items():
            if isinstance(value, list):
                condition = self.dataset.c[key].in_(value)
            else:
                condition = self.dataset.c[key] == value

            query = query.where(condition)

        return self.with_props(query=query)

    def by_pk(
        self: RelationType,
        key: Union[int, List[int]],
    ) -> RelationType:
        pks = self.dataset.primary_key.columns.values()

        if len(pks) > 1:
            raise PomError("`by_pk` is not supposed to be used with composite primary keys. Use `where` instead.")

        if isinstance(key, list):
            condition = pks[0].in_(key)
        else:
            condition = pks[0] == key

        return self.with_props(query=self.query.where(condition))

    def limit(
        self: RelationType,
        number: int,
    ) -> RelationType:
        return self.with_props(query=self.query.limit(number))

    def all(self) -> List[EntityType]:
        return [
            self.entity_class(**self.mapper_class()(dict(record)))
            for record in self.gateway.execute(self.query)
        ]

    def one(self) -> EntityType:
        return self.entity_class(
            **self.mapper_class()(dict(self.gateway.execute(self.query)[0]))
        )

    def insert(self: RelationType, **kwargs: Union[str, int, bool]) -> int:
        return self.gateway.connection.execute(  # type: ignore[no-any-return, no-untyped-call] # noqa: F723
            self.dataset.insert().values(**kwargs),
        ).inserted_primary_key[0]
