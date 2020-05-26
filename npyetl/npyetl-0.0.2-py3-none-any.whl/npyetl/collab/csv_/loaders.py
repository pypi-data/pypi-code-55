from typing import (
    Iterable,
    Optional
)
from npyetl.data import RelationalDataBlock
from npyetl.load import BaseLoader
from npyetl.internals.decorators import override


class LoaderCSV(BaseLoader):
    """
    TODO: map flexible input to adequate child class.
    """
    @override(BaseLoader)
    def load(self,
             **kwargs) -> bool:
        raise NotImplementedError


class LoaderLocalCSV(LoaderCSV):
    """
    Loader class to a local CSV file
    """
    
    @override(BaseLoader)
    def load(self,
             data_blocks: Iterable[RelationalDataBlock],
             directory: str = '') -> bool:
        for data_block in data_blocks:
            file = open(directory + data_block.name +'.csv', 'w')
            file.write(data_block.__str__())
            file.close()
        return True
