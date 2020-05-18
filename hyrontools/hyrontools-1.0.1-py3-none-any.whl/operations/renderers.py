from hyron.renderers.renderer import Renderer
from .operation import Operation


class ListRenderers(Operation, register="renderers"):
    """
        List the available renderers.
    """

    def run(self, *args):
        self.console.print_iter(
            "Available renderers",
            Renderer.registry.enum())
