from typing import Any, Dict
from .strict_type import Int


class Architecture:
    def __init__(
        self,
        str_length: type = Int,
        encoding: str = "utf-8",
    ):
        self._data: Dict[Any, type] = {
            "str_length": str_length,
        }
        self.encoding = encoding

    def __getitem__(self, key: Any) -> type:
        if key not in self._data:
            raise IndexError
        return self._data[key]

    def size_of(self, key: Any) -> int:
        if key not in self._data:
            raise IndexError
        return self._data[key].STANDARD_SIZE

    def format_of(self, key: Any) -> str:
        if key not in self._data:
            raise IndexError
        return self._data[key].FORMAT
