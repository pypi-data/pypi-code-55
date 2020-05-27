
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List


class FileProgressListener(ABC):

    @abstractmethod
    def start(self, size: int) -> None:
        pass

    @abstractmethod
    def progress(self, chunk_size: int) -> None:
        pass

    @abstractmethod
    def end(self) -> None:
        pass


class TreeProgressListener(ABC):

    @abstractmethod
    def begin(self, relative_paths: List[Path]) -> None:
        pass

    @abstractmethod
    def next(self, relative_path: Path) -> None:
        pass

    @abstractmethod
    def finish(self) -> None:
        pass
