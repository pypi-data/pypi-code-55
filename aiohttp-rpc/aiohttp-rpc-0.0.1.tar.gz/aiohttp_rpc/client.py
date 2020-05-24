import abc
import json
import uuid
from contextlib import asynccontextmanager
from functools import partial

import aiohttp
import typing

from .exceptions import JsonRpcError
from .protocol import JsonRpcRequest, JsonRpcResponse


class BaseJsonRpcClient(abc.ABC):
    def call(self):
        pass


class JsonRpcHTTPClient:
    _json_serialize = partial(json.dumps, default=lambda x: repr(x))
    _session: typing.Optional[aiohttp.ClientSession] = None
    _url: str = None

    def __init__(self, url: str, *,  session: typing.Optional[aiohttp.ClientSession] = None) -> None:
        self._url = url
        self._session = session

    def __getattr__(self, method) -> typing.Callable:
        return partial(self.call, method)

    async def call(self, method: str, *args, **kwargs) -> typing.Any:
        rpc_request = JsonRpcRequest(msg_id=uuid.uuid4(), method=method, args=args, kwargs=kwargs)
        rpc_response = await self.raw_call(rpc_request)

        if rpc_response.error:
            raise rpc_response.error

        return rpc_response.result

    async def raw_call(self, rpc_request: JsonRpcRequest) -> JsonRpcResponse:
        raw_response = await self._session.post(self._url, json=rpc_request.to_dict())
        data = await raw_response.json()
        rpc_response = JsonRpcResponse.from_dict(data)
        return rpc_response

    async def __aenter__(self):
        if not self._session:
            self._session = aiohttp.ClientSession(json_serialize=self._json_serialize)

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._session.close()
        self._session = None
        return False
