from __future__ import annotations
from typing import Dict, Any, Optional, TYPE_CHECKING, TypeVar
from cached_property import cached_property
from sqlalchemy import func
from sqlalchemy.sql.selectable import Select
from ..gateway import Gateway
from ..relation import Relation
from ..immutable_object import ImmutableObject

PaginationType = TypeVar("PaginationType", bound="RestliPagination")


class Pager(ImmutableObject):
    def __init__(
        self,
        gateway: Gateway,
        query: Select,
        count: int,
        start: int = 0,
    ):
        self.gateway = gateway
        self.query = query
        self.count = count
        self.start = start

    @cached_property
    def total(self) -> int:
        return int(self.gateway.execute(
            self.query.select_from(*self.query.froms)
            .with_only_columns([func.count()])
            .order_by(None)
            .limit(None)
            .offset(None)
        )[0]["count_1"])

    @cached_property
    def prev_start(self) -> int:
        if self.start - self.count < 0:
            return 0
        else:
            return self.start - self.count

    @cached_property
    def next_start(self) -> int:
        return self.start + self.count

    @cached_property
    def has_prev(self) -> bool:
        return self.start != 0

    @cached_property
    def has_next(self) -> bool:
        return self.total - self.start - self.count >= 0

    def at(self, query: Select, start: int, count: Optional[int] = None) -> Pager:
        count = self.count if count is None else count

        return self.with_props(
            query=query.offset(start).limit(count),
            count=count,
            start=start,
        )


if TYPE_CHECKING:
    PaginationBase = Relation
else:
    PaginationBase = object


class RestliPagination(PaginationBase):
    __pager_count__: int

    def __init__(  # type: ignore[misc] # Explicit "Any" is not allowed # noqa: F821
        self,
        pager: Optional[Pager] = None,
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        self.pager = (
            Pager(
                gateway=self.gateway, query=self.query, count=self.__class__.__pager_count__
            )
            if pager is None
            else pager
        )

    def paginate(self: PaginationType, paging: Dict[str, int]) -> PaginationType:
        count = paging["count"] if "count" in paging else self.pager.count

        next_pager = self.pager.at(
            query=self.query, start=self.pager.start, count=count,
        )

        if "start" in paging:
            next_pager = next_pager.at(query=self.query, start=paging["start"])

        return self.with_props(query=next_pager.query, pager=next_pager)
