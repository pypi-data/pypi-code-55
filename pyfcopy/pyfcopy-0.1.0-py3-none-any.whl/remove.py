
from pathlib import Path
from typing import Optional, Union

from .dummy_progress import DummyTreeProgressListener
from .index import index, Order
from .progress import TreeProgressListener


def remove(
        path: Union[str, Path],
        *,
        tree_progress_listener: Optional[TreeProgressListener] = None,
) -> None:

    if tree_progress_listener is None:
        tree_progress_listener = DummyTreeProgressListener()

    if not isinstance(path, Path):
        path = Path(path)

    relative_paths = index(path, order=Order.POST)

    tree_progress_listener.begin(relative_paths)

    for relative_path in relative_paths:

        tree_progress_listener.next(relative_path)

        absolute_path = path / relative_path

        if absolute_path.is_dir():

            absolute_path.rmdir()

        else:

            absolute_path.unlink()

    tree_progress_listener.finish()
