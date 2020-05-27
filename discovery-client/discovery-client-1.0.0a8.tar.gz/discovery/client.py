import asyncio
import json
import pickle
from functools import partial

from discovery import log
from discovery.abc import BaseClient
from discovery.engine.aio import has_aiohttp
from discovery.exceptions import ServiceNotFoundException
from discovery.model.agent.service import service
from discovery.utils import select_one_rr

if has_aiohttp:
    import aiohttp


class Consul(BaseClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.managed_services = {}
        self._leader_id = None
        self.__id = None

    async def reconnect(self):
        for key, value in self.managed_services.items():
            await self.agent.service.deregister(value.get("id"))
            svc = service(key, value.get("port"), check=value.get("check"))
            await self.agent.service.register(svc)

        self.__id = await self.leader_current_id()
        log.debug(f"Consul ID: {self.__id}")
        log.info("Service successfully re-registered")

    async def check_consul_health(self):
        if not has_aiohttp:
            raise ModuleNotFoundError("aiohttp module not found.")
        while True:
            try:
                await asyncio.sleep(self.timeout)
                current_id = await self.leader_current_id()
                log.debug(f"Consul ID: {current_id}")
                if current_id != self.__id:
                    await self.reconnect()
            except (
                aiohttp.ClientConnectorError,
                aiohttp.ServerDisconnectedError,
            ) as err:
                log.warning("Failed to connect on Consul")
                log.warning(f"reconnect will occur in {self.timeout} seconds.")
                log.error(err)
                await asyncio.sleep(self.timeout)
                await self.check_consul_health()

    async def find_service(self, name, fn=select_one_rr):
        response = await self.find_services(name)
        if not response:
            raise ServiceNotFoundException
        func = partial(fn, response)
        return func()

    async def find_services(self, name):
        resp = await self.catalog.service(name)
        response = await self._get_response(resp)
        return response

    async def register(self, service_name: str, service_port: int, check=None) -> None:
        svc = service(service_name, service_port, check=check)
        try:
            await self.agent.service.register(svc)
            self.managed_services[service_name] = {
                "id": f"{json.loads(svc).get('id')}",
                "port": service_port,
                "check": check,
            }
            self.__id = await self.leader_current_id()
            log.debug(f"Consul ID: {self.__id}")
            with open(".service", "wb") as f:
                f.write(pickle.dumps(self.managed_services))
        except aiohttp.ClientConnectorError as err:
            log.error("Failed to connect on Consul...")
            raise err

    async def leader_current_id(self):
        consul_leader = await self.leader_ip()
        consul_instances = await self.consul_healthy_instances()

        current_id = [
            instance.get("Node").get("ID")
            for instance in consul_instances
            if instance.get("Node").get("Address") == consul_leader
        ]
        if current_id is not None:
            current_id = current_id[0]
        return current_id

    async def leader_ip(self):
        leader_response = await self.status.leader()
        leader_response = await self._get_response(leader_response)
        try:
            consul_leader, _ = leader_response.split(":")
        except ValueError:
            log.error("Error to identify Consul's leader")
        return consul_leader

    async def _get_response(self, resp):
        if asyncio.iscoroutinefunction(resp.json):
            response = await resp.json()
            return response
        return resp.json()

    async def consul_healthy_instances(self):
        health_response = await self.health.service("consul")
        consul_instances = await self._get_response(health_response)
        return consul_instances

    async def deregister(self) -> None:
        for svc, data in self.managed_services.items():
            await self.agent.service.deregister(data.get("id"))
        self.managed_services.clear()

    def dump_managed_services(self):
        with open(".services", "wb") as f:
            f.write(pickle.dumps(self.managed_services))
