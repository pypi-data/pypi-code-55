from typing import Mapping, Dict, Tuple, Type
from .relation import Relation
from .gateway import Gateway, GatewayConfig

ContainerConfig = Tuple[str, str, Mapping[str, GatewayConfig]]


class Container:
    def __init__(self, **kwargs: ContainerConfig):
        self.gateways: Dict[str, Gateway] = {}
        self.relations: Dict[str, Relation] = {}
        self.configure(**kwargs)

    def configure(self, **kwargs: ContainerConfig) -> None:
        for key, value in kwargs.items():
            adapter, uri, settings = value
            self.gateways[key] = Gateway(uri, **settings)

    def register_relation(self, relation_class: Type[Relation]) -> None:
        self.relations[relation_class.__register_as__] = relation_class(
            gateway=self.gateways[relation_class.__gateway__],
        )

    def gateway(self, name: str) -> Gateway:
        return self.gateways[name]

    def relation(self, name: str) -> Relation:
        return self.relations[name]

    def disconnect(self) -> None:
        for _, v in self.gateways.items():
            v.disconnect()
