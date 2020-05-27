
from pathlib import Path
from typing import Optional, Union

from .copy_file import copy_file
from .dummy_progress import DummyTreeProgressListener
from .index import index, Order
from .progress import FileProgressListener, TreeProgressListener


def copy(
        source_path: Union[Path, str],
        target_path: Union[Path, str],
        *,
        tree_progress_listener: Optional[TreeProgressListener] = None,
        file_progress_listener: Optional[FileProgressListener] = None,
        block_size: Optional[int] = None,
) -> int:

    source_path = Path(source_path) if not isinstance(source_path, Path) else source_path
    target_path = Path(target_path) if not isinstance(target_path, Path) else target_path

    tree_progress_listener = DummyTreeProgressListener() if tree_progress_listener is None else tree_progress_listener

    if not source_path.exists():
        raise ValueError(f"Given source-path does not exist: {source_path}")

    if source_path.is_symlink():
        raise ValueError(f"Given source-path is a symlink: {source_path}")

    if target_path.exists():
        raise ValueError(f"Given target-path does already exist: {target_path}")

    if str(target_path.resolve()).startswith(str(source_path.resolve())):
        raise ValueError("Cannot copy tree into itself.")

    relative_paths = index(source_path, order=Order.PRE)

    tree_progress_listener.begin(relative_paths)

    for current_relative_path in relative_paths:

        tree_progress_listener.next(current_relative_path)

        current_source_path = source_path / current_relative_path
        current_target_path = target_path / current_relative_path

        if current_source_path.is_file():

            copy_file(current_source_path, current_target_path,
                      progress_listener=file_progress_listener, block_size=block_size)

        elif current_source_path.is_dir():

            current_target_path.mkdir()

        else:

            raise Exception()

    tree_progress_listener.finish()

    return len(relative_paths)

