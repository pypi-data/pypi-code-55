#!/usr/env python3

import aiohttp
import async_timeout
from enum import Enum


class AladdinConnectDoorStates(Enum):
    UNKNOWN = 0
    OPEN = 1
    OPENING = 2
    TIMEOUT_OPENING = 3
    CLOSED = 4
    CLOSING = 5
    TIMEOUT_CLOSING = 6
    NOT_CONFIGURED = 7


class AladdinConnection:

    LOGIN_URL = "https://genie.exosite.com/api/portals/v1/users/_this/token"
    USER_URL = "https://genie.exosite.com/api/portals/v1/users/_this"
    PORTAL_URL = "https://genie.exosite.com/api/portals/v1/users/{user_id}/portals"
    PORTAL_DETAIL_URL = "https://genie.exosite.com/api/portals/v1/portals/{portal_id}"
    DOOR_URL = "https://genie.m2.exosite.com/onep:v1/rpc/process"

    STATIC_HEADERS = {
        "AppVersion": "2.10.1",
        "BundleName": "com.geniecompany.AladdinConnect",
        "User-Agent": "Aladdin Connect Android v2.10.1",
        "BuildVersion": "131",
    }

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.connected = False
        self.token = ""
        self.user_id = ""

    async def _check_credential(self) -> bool:
        async with aiohttp.ClientSession() as session:
            with async_timeout.timeout(10):
                async with session.get(
                    self.LOGIN_URL,
                    headers=self.STATIC_HEADERS,
                    auth=aiohttp.BasicAuth(self.username, self.password),
                ) as response:
                    if response.status == 200:
                        self.token = await response.text()
                        return True
        return False

    async def connect(self) -> bool:
        self.connected = await self._check_credential()
        if self.connected:
            print(f"Connection established with token {self.token}")
            return True
        else:
            print("Connection failed.")
            return False

    async def _get_user_id(self, session) -> str:
        async with session.get(
            self.USER_URL,
            headers=self.STATIC_HEADERS,
            auth=aiohttp.BasicAuth(self.username, self.password),
        ) as response:
            if response.status == 200:
                response_json = await response.json()
                return response_json["id"]

    async def _get_portal_ids(self, session) -> str:
        async with session.get(
            self.PORTAL_URL.format(user_id=self.user_id),
            headers=self.STATIC_HEADERS,
            auth=aiohttp.BasicAuth(self.username, self.password),
        ) as response:
            if response.status == 200:
                response_json = await response.json()
                return [x["PortalID"] for x in response_json]

    async def _get_portal_keys(self, session) -> str:
        portal_keys = []
        portal_device_ids = []

        for portal_id in self.portal_ids:
            async with session.get(
                self.PORTAL_DETAIL_URL.format(portal_id=portal_id),
                headers=self.STATIC_HEADERS,
                auth=aiohttp.BasicAuth(self.username, self.password),
            ) as response:
                if response.status == 200:
                    response_json = await response.json()
                    portal_keys.append(response_json["info"]["key"])
                    portal_device_ids.append(response_json["devices"][0])
        return dict(zip(portal_device_ids, portal_keys))

    async def _get_door_info(self, session, door_id, door_key):
        get_door_body = {
            "auth": {"cik": door_key, "client_id": door_id},
            "calls": [
                {
                    "arguments": [{"alias": "dps1.door_status"}, {}],
                    "id": 1,
                    "procedure": "read",
                },
                {
                    "arguments": [{"alias": "dps1.name"}, {}],
                    "id": 2,
                    "procedure": "read",
                },
            ],
        }

        get_door_headers = self.STATIC_HEADERS.copy()
        get_door_headers["Content-Type"] = "application/json"

        async with session.post(
            self.DOOR_URL,
            json=get_door_body,
            headers=get_door_headers,
            auth=aiohttp.BasicAuth(self.username, self.password),
        ) as response:
            return await response.json()

    async def _set_door_state(self, session, door_id, door_key, new_state):
        get_door_body = {
            "auth": {"cik": door_key, "client_id": door_id},
            "calls": [
                {
                    "arguments": [{"alias": "dps1.desired_status"}, new_state],
                    "id": 1,
                    "procedure": "write",
                },
                {
                    "arguments": [{"alias": "dps1.desired_status_user"}, self.username],
                    "id": 2,
                    "procedure": "write",
                },
            ],
        }

        get_door_headers = self.STATIC_HEADERS.copy()
        get_door_headers["Content-Type"] = "application/json"

        async with session.post(
            self.DOOR_URL,
            json=get_door_body,
            headers=get_door_headers,
            auth=aiohttp.BasicAuth(self.username, self.password),
        ) as response:
            return await response.json()

    async def discover_doors(self):
        if not self.connected:
            raise Exception("call connect() first.")
        async with aiohttp.ClientSession() as session:
            with async_timeout.timeout(10):
                self.user_id = await self._get_user_id(session)
                self.portal_ids = await self._get_portal_ids(session)
                self.portal_keys = await self._get_portal_keys(session)
                door_id = list(self.portal_keys.keys())[0]
                door_key = list(self.portal_keys.values())[0]
                door_data = await self._get_door_info(session, door_id, door_key)
                self.door = {
                    "cik": door_key,
                    "client_id": door_id,
                    "name": door_data[1]["result"][0][1],
                    "state": AladdinConnectDoorStates(door_data[0]["result"][0][1]),
                }
                print(self.door)

    async def open_door(self):
        if not self.connected:
            raise Exception("call connect() first.")
        async with aiohttp.ClientSession() as session:
            with async_timeout.timeout(10):
                await self._set_door_state(
                    session, self.door["client_id"], self.door["cik"], 1
                )

    async def close_door(self):
        if not self.connected:
            raise Exception("call connect() first.")
        async with aiohttp.ClientSession() as session:
            with async_timeout.timeout(10):
                await self._set_door_state(
                    session, self.door["client_id"], self.door["cik"], 0
                )
