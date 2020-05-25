from typing import Callable

from dash_infra.core import Component
from dash_infra.html_helpers.divs import Row


class ComponentGroup(Component):
    """
    An abstraction on components allowing to group them in
    a common container.
    The container is a Callable returning an HTML component.
    """

    def __init__(
        self, id: str, *components: str, container: Callable = Row
    ) -> "ComponentGroup":
        super().__init__(id)
        self.components = components
        self.container = container

    def layout(self):
        return self.container([c.layout() for c in self.components], id=self.id)
