from typing import (
    Iterable,
    Optional
)
import json
from npyetl.data import JSONDataBlock
from npyetl.load import BaseLoader
from npyetl.internals.decorators import override


class LoaderJSON(BaseLoader):
    """
    TODO: map flexible input to adequate child class.
    """
    @override(BaseLoader)
    def load(self,
             data_blocks: Iterable[JSONDataBlock],
             **kwargs) -> bool:
        raise NotImplementedError


class LoaderLocalJSON(LoaderJSON):
    """
    Loader class to a local JSON file
    """
    
    @override(BaseLoader)
    def load(self,
             data_blocks: Iterable[JSONDataBlock],
             directory: str = '') -> bool:
        for data_block in data_blocks:
            file = open(directory + data_block.name +'.json', 'w')
            json.dump(data_block.records, file)
        return True
