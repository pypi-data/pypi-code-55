from typing import (
    List,
    Iterable
)
import os
import json
import requests
#
from npyetl.extraction import BaseExtractor
from npyetl.data import (
    JSONDataBlock
)
from npyetl.internals.decorators import override


class ExtractorJSON(BaseExtractor):
    """
    TODO: map flexible input to adequate child class.
    """
    @override(BaseExtractor)
    def extract(self,
                **kwargs) -> Iterable[JSONDataBlock]:
        raise NotImplementedError


class ExtractorLocalJSON(ExtractorJSON):
    """
    An ExtractorJSON child class for local JSON files.
    """
    @override(ExtractorJSON)  
    def extract(self,
                directory: str,
                matches: List[str] = [],
                headers: bool = True) -> Iterable[JSONDataBlock]:
        """
        """
        for file_name in [ f for f in os.listdir(directory) if f.endswith('.json') ]:
            if not matches or any([m in file_name for m in matches]): 
                file = open(directory + file_name, 'r')
                records = json.load(file)
                yield JSONDataBlock(records, name=file_name)
        return


class ExtractorUrlJSON(ExtractorJSON):
    """
    An ExtractorJSON child class for urls containing JSON files.
    """
    @override(ExtractorJSON)
    def extract(self,
                file_url: str,
                **kwargs) -> Iterable[JSONDataBlock]:
        """
        """
        records = json.loads(requests.get(file_url).content)
        yield JSONDataBlock(records)
