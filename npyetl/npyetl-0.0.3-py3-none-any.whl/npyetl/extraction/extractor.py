from typing import (
    Iterable
)
from abc import (
    ABC,
    abstractmethod
)
from npyetl.data import BaseDataBlock


class BaseExtractor(ABC):
    
    def __init__(self,
                 metadata: dict = None):
        self._metadata = metadata or dict()
    
    @abstractmethod
    def extract(self) -> Iterable[BaseDataBlock]:
        raise NotImplementedError
