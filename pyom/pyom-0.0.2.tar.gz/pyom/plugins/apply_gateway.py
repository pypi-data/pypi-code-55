from ..container import Container
from ..relation import Relation


class ApplyGateway:
    def __init__(self, container: Container, gateway: str):
        self.container = container
        self.gateway = gateway

    def relation(self, name: str) -> Relation:
        return self.container.relation(name).__class__(gateway=self.container.gateway(self.gateway))
