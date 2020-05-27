
import os
from pathlib import Path
from typing import Union, Optional

from .dummy_progress import DummyFileProgressListener
from .progress import FileProgressListener


def copy_file(
        source_path: Union[Path, str],
        target_path: Union[Path, str],
        *,
        progress_listener: Optional[FileProgressListener] = None,
        block_size: Optional[int] = None,
    ) -> int:

    source_path = Path(source_path) if not isinstance(source_path, Path) else source_path
    target_path = Path(target_path) if not isinstance(target_path, Path) else target_path

    progress_listener = DummyFileProgressListener() if progress_listener is None else progress_listener
    block_size = pow(2, 16) if block_size is None else block_size

    if not source_path.is_file():
        raise ValueError(f"Given source-path is not a file: {source_path}")

    if source_path.is_symlink():
        raise ValueError(f"Cannot copy symlink: {source_path}")

    if target_path.exists():
        raise ValueError(f"Given target-path does already exist: {target_path}")

    if block_size < 1:
        raise ValueError(f"Invalid block-size: {block_size}")

    source_stat = source_path.stat()
    file_size = source_stat.st_size

    progress_listener.start(file_size)

    source_fd = os.open(source_path, os.O_RDONLY)
    target_fd = os.open(target_path, os.O_WRONLY | os.O_CREAT)

    current_position: int = 0
    while current_position < file_size:

        chunk_size = os.sendfile(target_fd, source_fd, offset=current_position, count=block_size)

        progress_listener.progress(chunk_size)

        current_position += chunk_size

    os.close(target_fd)
    os.close(source_fd)

    progress_listener.end()

    return current_position
