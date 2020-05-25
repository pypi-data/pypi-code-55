from typing import Union

from httpx import Client as HTTPXClient
from httpx import AsyncClient as HTTPXAsyncClient

from netauto.models.digi import DigiList
from netauto._validate import validate_200, validate_201


class BaseDigi:

    def __init__(self, session: Union[HTTPXClient, HTTPXAsyncClient]):
        self._session = session
        self._base_url = "digi/"


class Digi(BaseDigi):

    def __init__(self, session: HTTPXClient):
        super().__init__(session=session)

    def reboot_digi(self, ip: str) -> bool:
        params = {"ip": ip}
        r = self._session.post(url=f"{self._base_url}reboot/", params=params)
        validate_201(r=r)
        return True

    def get_all_digi(self) -> DigiList:
        r = self._session.get(url=self._base_url, timeout=20)
        validate_200(r=r)
        return DigiList(**r.json())


class AsyncDigi(BaseDigi):
    def __init__(self, session: HTTPXAsyncClient):
        super().__init__(session=session)

    async def reboot_digi(self, ip: str) -> bool:
        params = {"ip": ip}
        r = await self._session.post(url=f"{self._base_url}reboot/", params=params)
        validate_201(r=r)
        return True

    async def get_all_digi(self) -> DigiList:
        print(self._session.headers["Authorization"])
        r = await self._session.get(url=self._base_url, timeout=20)
        validate_200(r=r)
        return DigiList(**r.json())
