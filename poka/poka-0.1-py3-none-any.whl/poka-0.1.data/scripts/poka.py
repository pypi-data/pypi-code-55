from typing import Dict
import mysql.connector as connector
import typing
from abc import ABC, abstractmethod
from QueryBuilder import QueryBuilder

instanceStatus = typing.TypeVar("instanceStatus", bound="Parent")

class Parent(ABC):
    @abstractmethod
    def settype(self: instanceStatus) -> instanceStatus:
        pass

class Poka(object):
    def __init__(self, cfg: Dict) -> None:
        """
        Initialize Pokabase instance 
        """
        self._cfg: Dict = cfg
        self.sql: str
        self.params: Dict
        self.params = {
            "where": [],
            "whereIn": [],
            "whereNotNull": [],
            "orderBy": [],
            "take": []
        }

    def table(self: instanceStatus, table: str) -> instanceStatus:
        """
        Set table to instance
        """
        self._table: str = table
        return self
        
    def where(self: instanceStatus, col: str, oper: str, val: str) -> instanceStatus:
        """
        Function imitize sql feature where
        """
        self.params["where"]: str
        if len(self.params["whereIn"]) != 0  or len(self.params["whereNotNull"]) != 0 or len(self.params["where"]) != 0:
            self.params["where"].append(f"AND `{ col }` { oper } '{ val }'")
        else:
            self.params["where"].append(f"WHERE `{ col }` { oper } '{ val }'")

        return self

    def whereIn(self: instanceStatus, col: str, args: list) -> instanceStatus:
        """
        Function imitize sql feature where in
        """
        self.params["whereIn"]: str

        if len(self.params["where"]) != 0  or len(self.params["whereNotNull"]) != 0 or len(self.params["whereIn"]) != 0:
            self.params["whereIn"].append(f"AND { col } IN ({ ','.join(str(arg) for arg in args) })")
        else:
            self.params["whereIn"].append(f"WHERE { col } IN ({ ','.join(str(arg) for arg in args) })")
        return self

    def orderBy(self: instanceStatus, col: str, param="asc") -> instanceStatus:
        """
        Function imitize sql feature orderBy
        """
        self.params["orderBy"]: str
        self.params["orderBy"].append(f"ORDER BY { col } { param }")
        return self

    def whereNotNull(self, col: str) -> instanceStatus:
        """
        Function imitize sql feature IS NOT NULL
        """
        self.params["whereNotNull"]: str

        if len(self.params["whereIn"]) != 0  or len(self.params["where"]) != 0 or len(self.params["whereNotNull"]) != 0:
            self.params["whereNotNull"].append(f"AND { col } IS NOT NULL")
        else:
            self.params["whereNotNull"].append(f"WHERE { col } IS NOT NULL")
        return self

    def take(self: instanceStatus, count: int) -> instanceStatus:
        """
        Function imitize sql feature LIMIT :count:
        """
        self.params["take"]: str
        self.params["take"].append(f"LIMIT { count }")
        return self

    def get(self) -> Dict:
        """
        SELECT feature constructor function
        Consctruct all self.params to sql query SELECT
        """
        opers = [ param for param in self.params.items() if param[1] is not None]
        
        sql = f"SELECT * FROM { self._table }"
        for oper in opers:
            for query in oper[1]:
                sql += f" { query }"

        result = QueryBuilder.fetch(self._cfg, sql, buffered=True, fetch=True)

        return result

    def insert(self, args) -> bool:
        """
        INSERT feature constructor function
        Consctruct all self.params to sql query INSERT
        """
        sql = f"INSERT INTO { self._table } ("
        
        counter = 0
        for arg in args.items():
            if counter == 0:
                sql += f"`{ arg[0] }`"
            else:
                sql += f",`{ arg[0] }`"
            counter += 1
        sql += ") VALUES ("

        counter = 0
        for arg in args.items():
            if counter == 0:
                if type(arg[1]) is str:
                    sql += f"'{ arg[1] }'"
                else:
                    sql += f"{ arg[1] }" 
            else:
                if type(arg[1]) is str:
                    sql += f",'{ arg[1] }'"
                else:
                    sql += f",{ arg[1] }"
            counter += 1
        sql += ")"

        result = QueryBuilder.fetch(self._cfg, sql)

        return result

    def update(self, args):
        """
        UPDATE feature constructor function
        Consctruct all self.params to sql query UPDATE
        """
        sql = f"UPDATE { self._table } SET "

        counter = 0
        for arg in args.items():
            if counter == 0:
                if type(arg[1]) is str:
                    sql += f"`{ arg[0] }` = '{ arg[1] }'"
                else: 
                    sql += f"`{ arg[0] }` = { arg[1] }"
            else:
                if type(arg[1]) is str:
                    sql += f",`{ arg[0] }` = '{ arg[1] }'"
                else: 
                    sql += f",`{ arg[0] }` = { arg[1] }"
            counter += 1

        opers = [ param for param in self.params.items() if param[1] is not None]

        for oper in opers:
            for query in oper[1]:
                sql += f" { query }"
        
        print(sql)
        result = QueryBuilder.fetch(self._cfg, sql)

        return result
