
from pathlib import Path
from typing import Optional, Union

from .copy import copy_file
from .dummy_progress import DummyTreeProgressListener
from .index import index, Order
from .progress import TreeProgressListener, FileProgressListener
from .remove import remove


def merge(
        source_path: Union[Path, str],
        target_path: Union[Path, str],
        *,
        overwrite: bool = None,
        tree_progress_listener: Optional[TreeProgressListener] = None,
        file_progress_listener: Optional[FileProgressListener] = None,
        block_size: Optional[int] = None,
) -> None:

    source_path = Path(source_path) if not isinstance(source_path, Path) else source_path
    target_path = Path(target_path) if not isinstance(target_path, Path) else target_path

    overwrite = False if overwrite is None else overwrite
    tree_progress_listener = DummyTreeProgressListener() if tree_progress_listener is None else tree_progress_listener

    if not source_path.is_dir():
        raise ValueError(f"Given source-path is not a directory: {source_path}")

    if not target_path.is_dir():
        raise ValueError(f"Given target-path is not a directory: {target_path}")

    if str(source_path.resolve()).startswith(str(target_path.resolve())):
        raise ValueError("Cannot merge tree onto itself.")

    relative_paths = index(source_path, order=Order.PRE)

    # assert no collisions beforehand
    if not overwrite:

        relative_collision_paths = [
            relative_path
            for relative_path in index(target_path)
            if (source_path / relative_path).exists() and
               not ((source_path / relative_path).is_dir() and (target_path / relative_path).is_dir())
        ]

        if len(relative_collision_paths) > 0:
            raise ValueError(f"Target directory contains {len(relative_collision_paths)} collision(s).")

    tree_progress_listener.begin(relative_paths)

    for relative_path in relative_paths:

        tree_progress_listener.next(relative_path)

        current_source_path = source_path / relative_path
        current_target_path = target_path / relative_path

        if current_source_path.is_file():

            if current_target_path.exists():
                remove(current_target_path)

            copy_file(
                current_source_path,
                current_target_path,
                progress_listener=file_progress_listener,
                block_size=block_size,
            )

        elif current_source_path.is_dir():

            if current_target_path.exists() and not current_target_path.is_dir():
                remove(current_target_path)

            if not current_target_path.exists():
                current_target_path.mkdir()

        else:

            raise Exception(f"Cannot handle path: {current_source_path}")

    tree_progress_listener.finish()
