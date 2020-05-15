from typing import Optional

from .console import Console, ConsoleOptions, RenderableType, RenderResult


class Constrain:
    """Constrain the width of a renderable to a given number of characters.
    
    Args:
        renderable (RenderableType): A renderable object.
        width (int, optional): The maximum width (in characters) to render. Defaults to 80.
    """

    def __init__(self, renderable: RenderableType, width: Optional[int] = 80) -> None:
        self.renderable = renderable
        self.width = width

    def __console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        if self.width is None:
            yield self.renderable
        else:
            child_options = options.update(width=min(self.width, options.max_width))
            yield from console.render(self.renderable, child_options)
