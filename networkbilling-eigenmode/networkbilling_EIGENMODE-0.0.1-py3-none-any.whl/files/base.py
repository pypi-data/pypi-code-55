from typing import Callable, List, Iterable

import abc


class UnexpectedRecordType(Exception):
    pass


class UnexpectedNumberOfRows(Exception):
    pass


class MissingHeader(Exception):
    pass


class MissingFooter(Exception):
    pass


class NetworkRow(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def from_row(row: List[str]):
        ...

    @staticmethod
    @abc.abstractmethod
    def record_type() -> int:
        ...

    def is_header(self) -> bool:
        return False

    def is_footer(self) -> bool:
        return False


class HeaderRow(NetworkRow):
    def is_header(self) -> bool:
        return True


class FooterRow(NetworkRow):
    def is_footer(self) -> bool:
        return True
