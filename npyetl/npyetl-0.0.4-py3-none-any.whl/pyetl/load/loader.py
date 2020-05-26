from typing import (
    Iterable
)
from abc import(
    ABC,
    abstractmethod
)
from npyetl.data import BaseDataBlock


class BaseLoader(ABC):
    
    def __init__(self,
                 metadata: dict = None):
        self._metadata = metadata or dict()
        
    @abstractmethod
    def load(self,
             data_blocks: Iterable[BaseDataBlock],
             **kwargs) -> bool:
        raise NotImplementedError
