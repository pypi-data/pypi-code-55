from typing import Union, Any, List, Mapping, Optional
from sqlalchemy.engine.base import Connection
from sqlalchemy.sql.selectable import Select
from sqlalchemy import MetaData, Table, create_engine

Row = Mapping[str, Any]  # type: ignore[misc] # Explicit "Any" is not allowed # noqa: F821
GatewayConfig = Union[int, bool]


class Gateway:
    def __init__(
        self,
        uri: str,
        **kwargs: GatewayConfig,
    ):
        self.engine = create_engine(uri, **kwargs)
        self.meta = MetaData(self.engine)
        self._connection: Optional[Connection] = None

    @property
    def connection(self) -> Connection:
        if self._connection is None:
            self._connection = self.engine.connect()

        return self._connection

    def disconnect(self) -> None:
        if self._connection:
            self._connection.close()
            self._connection = None

    def dataset(self, name: str) -> Table:
        if name not in self.meta.tables:
            Table(name, self.meta, autoload=True, autoload_with=self.engine)

        return self.meta.tables[name]

    def execute(self, statement: Select) -> List[Row]:
        return [
            dict(row)
            for row in self.connection.execute(statement).fetchall()  # type: ignore[no-untyped-call] # Call to untyped function "execute" in typed context # noqa: F821,E501
        ]
