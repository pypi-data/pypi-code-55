
from pathlib import Path
from typing import List

from .progress import TreeProgressListener, FileProgressListener


class DummyFileProgressListener(FileProgressListener):

    def start(self, size: int) -> None:
        pass

    def progress(self, chunk_size: int) -> None:
        pass

    def end(self) -> None:
        pass


class DummyTreeProgressListener(TreeProgressListener):

    def begin(self, relative_paths: List[Path]) -> None:
        pass

    def next(self, relative_path: Path) -> None:
        pass

    def finish(self) -> None:
        pass
