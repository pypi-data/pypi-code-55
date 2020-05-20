from typing import Union

from httpx import Client as HTTPXClient
from httpx import AsyncClient as HTTPXAsyncClient

from netauto._validate import validate_201


class BaseAuth:

    def __init__(self, session: Union[HTTPXClient, HTTPXAsyncClient], username: str, password: str):
        self._session = session
        self._username = username
        self._password = password
        self._base_url = "auth/"
        self._user_data = {"username": self._username, "password": self._password}


class Auth(BaseAuth):

    def __init__(self, session: HTTPXClient, username: str, password: str):
        super().__init__(session=session, username=username, password=password)

    def login(self) -> None:
        r = self._session.post(url=self._base_url, data=self._user_data)
        validate_201(r)
        self._session.headers["Authorization"] = f"Bearer {r.json()['access_token']}"


class AsyncAuth(BaseAuth):

    def __init__(self, session: HTTPXAsyncClient, username: str, password: str):
        super().__init__(session=session, username=username, password=password)

    async def login(self) -> None:
        r = await self._session.post(url=self._base_url, data=self._user_data)
        validate_201(r)
        self._session.headers["Authorization"] = f"Bearer {r.json()['access_token']}"
