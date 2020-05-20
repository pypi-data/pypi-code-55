from typing import List, Union

from httpx import Client as HTTPXClient
from httpx import AsyncClient as HTTPXAsyncClient

from netauto._validate import validate_201
from netauto.models.tools import PortScanResp, SendMail


class BaseTools:

    def __init__(self, session: Union[HTTPXClient, HTTPXAsyncClient]):
        self._session = session
        self._base_url = "tools/"


class Tools(BaseTools):

    def __init__(self, session: HTTPXClient):
        super().__init__(session=session)

    def port_scan(self, ip: str, port: int) -> PortScanResp:
        params = {"ip": ip, "port": port}
        r = self._session.post(url=f"{self._base_url}port_scan/", params=params)
        validate_201(r=r)
        return PortScanResp(**r.json())

    def send_mail(self, to: List[str], subject: str, content: str) -> SendMail:
        data = {"to": to, "subject": subject, "content": content}
        r = self._session.post(url=f"{self._base_url}send_mail/", json=data)
        validate_201(r=r)
        return SendMail(**r.json())


class AsyncTools(BaseTools):

    def __init__(self, session: HTTPXAsyncClient):
        super().__init__(session=session)

    async def port_scan(self, ip: str, port: int) -> PortScanResp:
        params = {"ip": ip, "port": port}
        r = await self._session.post(url=f"{self._base_url}port_scan/", params=params)
        validate_201(r=r)
        return PortScanResp(**r.json())

    async def send_mail(self, to: List[str], subject: str, content: str) -> SendMail:
        data = {"to": to, "subject": subject, "content": content}
        r = await self._session.post(url=f"{self._base_url}send_mail/", json=data)
        validate_201(r=r)
        return SendMail(**r.json())
