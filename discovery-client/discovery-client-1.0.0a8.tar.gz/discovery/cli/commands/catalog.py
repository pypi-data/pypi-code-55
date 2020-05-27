import asyncio
import logging
import pickle
import sys

from cleo import Command

from discovery.client import Consul
from discovery.engine import AioEngine, aiohttp_session

logging.getLogger().addHandler(logging.NullHandler())


loop = asyncio.get_event_loop()
session = loop.run_until_complete(aiohttp_session())
client = Consul(AioEngine(session=session))


class CatalogCommand(Command):
    """
    Interact with Consul's catalog.

    catalog
        {--s|services : List services catalog.}
        {--d|deregister= : Deregister a ser vice in the Consul's catalog.}
    """

    def handle(self):
        if self.option("services"):
            resp = loop.run_until_complete(client.catalog.services())
            resp = loop.run_until_complete(resp.json())
            for svc in resp.keys():
                self.line(f"{svc}")
            sys.exit(0)
        elif self.option("deregister"):
            try:
                with open(self.option("deregister"), "rb") as f:
                    services = pickle.loads(f.read())
            except FileNotFoundError:
                self.line("<error>[!]</error> arquivo não localizado")
                sys.exit(1)
            for svc, data in services.items():
                loop.run_until_complete(client.agent.service.deregister(data.get("id")))
            sys.exit(0)
