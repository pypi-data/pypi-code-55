from typing import (
    List,
    Iterable
)
import os
import csv
from npyetl.extraction import BaseExtractor
from npyetl.data import (
    RelationalDataBlock,
    PandasDataBlock
)
from npyetl.internals.decorators import override


class ExtractorCSV(BaseExtractor):
    """
    TODO: map flexible input to adequate child class.
    """
    @override(BaseExtractor)
    def extract(self,
                **kwargs) -> Iterable[RelationalDataBlock]:
        raise NotImplementedError


class ExtractorLocalCSV(ExtractorCSV):
    """
    An ExtractorCSV child class for local CSV files.
    """
    @override(ExtractorCSV)  
    def extract(self,
                directory: str,
                matches: List[str] = [],
                headers: bool = True) -> Iterable[RelationalDataBlock]:
        """
        """
        for file_name in [ f for f in os.listdir(directory) if f.endswith('.csv') ]:
            if not matches or any([m in file_name for m in matches]): 
                file = open(directory + file_name, 'r')
                records = list(csv.reader(file))
                name = file_name
                if headers:
                    columns = records[0]
                    records = records[1:]
                    yield RelationalDataBlock(records, columns, name=name)
                else:
                    yield RelationalDataBlock(records, name=name)
        return


class ExtractorUrlCSV(ExtractorCSV):
    """
    An ExtractorCSV child class for urls containing CSV files.
    """
    @override(ExtractorCSV)
    def extract(self,
                file_url: str,
                sep: str = ',',
                **kwargs) -> Iterable[PandasDataBlock]:
        """
        """
        yield PandasDataBlock.read_csv(file_url, sep=sep, **kwargs)
