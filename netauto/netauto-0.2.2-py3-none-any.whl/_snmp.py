from typing import Union

from httpx import Client as HTTPXClient
from httpx import AsyncClient as HTTPXAsyncClient

from ._validate import validate_201

from netauto.models.snmp import ReturnGetData, ReturnBulkData, SnmpRequestData


class BaseSNMP:

    def __init__(self, session: Union[HTTPXClient, HTTPXAsyncClient]):
        self._session = session
        self._base_url = "snmp/"


class SNMP(BaseSNMP):

    def __init__(self, session: HTTPXClient):
        super().__init__(session=session)

    def get(self, snmp_version: int, ip_list: list, oids: list) -> ReturnGetData:
        data = SnmpRequestData(snmp_version=snmp_version, ip_list=ip_list, oids=oids)
        r = self._session.post(url=f"{self._base_url}get/", json=data.dict(), timeout=15)
        validate_201(r=r)
        return ReturnGetData(**r.json())

    def bulk_walk(self, snmp_version: int, ip_list: list, oids: list) -> ReturnBulkData:
        data = SnmpRequestData(snmp_version=snmp_version, ip_list=ip_list, oids=oids)
        r = self._session.post(url=f"{self._base_url}bulk_walk/", json=data.dict(), timeout=15)
        validate_201(r=r)
        return ReturnBulkData(**r.json())


class AsyncSNMP(BaseSNMP):

    def __init__(self, session: HTTPXAsyncClient):
        super().__init__(session=session)

    async def get(self, snmp_version: int, ip_list: list, oids: list) -> ReturnGetData:
        data = SnmpRequestData(snmp_version=snmp_version, ip_list=ip_list, oids=oids)
        r = await self._session.post(url=f"{self._base_url}get/", json=data.dict(), timeout=15)
        validate_201(r=r)
        return ReturnGetData(**r.json())

    async def bulk_walk(self, snmp_version: int, ip_list: list, oids: list) -> ReturnBulkData:
        data = SnmpRequestData(snmp_version=snmp_version, ip_list=ip_list, oids=oids)
        r = await self._session.post(url=f"{self._base_url}bulk_walk/", json=data.dict(), timeout=15)
        validate_201(r=r)
        return ReturnBulkData(**r.json())
