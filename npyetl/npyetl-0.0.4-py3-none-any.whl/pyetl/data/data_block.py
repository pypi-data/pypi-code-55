from npyetl.internals.decorators import(
    override
)
from abc import(
    ABC,
    abstractmethod,
    abstractproperty
)
from typing import(
    List,
    Dict,
    Union,
    Generator,
    Any
)
import json
import uuid


class BaseDataBlock(ABC):
    """
    """
    @property
    @abstractmethod
    def records(self) -> object:
        return NotImplementedError

    @abstractmethod
    def __str__(self) -> str:
        return NotImplementedError

    def __len__(self) -> int:
        return len(self.records)
    
    def __iter__(self) -> Generator[str, None, None]:
        return (record for record in self.records)
    
    @abstractproperty
    def metadata(self) -> Dict[str, object]:
        return NotImplementedError

    @abstractproperty
    def name(self) -> str:
        return NotImplementedError


class DataBlock(BaseDataBlock):
    """
    """
    def __init__(self,
                 records: object,
                 metadata: dict = None,
                 name: str = None):
        self._records = records
        self._metadata = metadata or dict()
        self._name = name
    
    @property
    @override(BaseDataBlock)
    def records(self) -> object:
        return self._records
    
    @records.setter
    def records(self, new_value: object):
        self._records = new_value

    @property
    @override(BaseDataBlock)
    def metadata(self) -> dict:
        return self._metadata

    @property
    @override(BaseDataBlock)
    def name(self) -> str:
        return self._name or uuid.uuid4().__str__()
    
    @name.setter
    def name(self, new_name: str):
        self._name = new_name

    @override(BaseDataBlock)
    def __str__(self):
        return '\n'.join([ record.__str__() for record in records ])
    


class BaseRelationalDataBlock(DataBlock):
    """
    """
    @override(BaseDataBlock)
    def __str__(self) -> str:
        string = ''
        if self.columns:
            string += ','.join(self.columns) + '\n'
        string += '\n'.join([ ','.join(record) for record in self.records ])
        return string

    def __getitem__(self,
                    key: str) -> list:
        """Gets one column's data."""
        colIx = self._columns.index(key) 
        if colIx == -1:
            raise KeyError(f"'{key}' is not a column.")
        return [ record[colIx] for record in self.records ]


class RelationalDataBlock(BaseRelationalDataBlock):
    """
    """
    def __init__(self,
                 records: List[List[Any]],
                 columns: List[str] = None,
                 types: Dict[str, type] = None,
                 metadata: dict = None,
                 **kwargs):
        """
        :param columns: the column names for the records.
        :param records: the actual data rows.
        :param types: the types for each column.
        :param metadata: the metadata of the data block.
        """
        super().__init__(records, metadata, **kwargs)
        self._columns = columns or list()
        self._types = types or dict()
    
    @property
    def columns(self) -> List[str]:
        return self._columns
    
    @property
    def types(self) -> Dict[str, type]:
        return self._types


class JSONDataBlock(DataBlock):
    """
    """
    def __init__(self,
                 records: object,
                 schema: dict = None,
                 metadata: dict = None,
                 **kwargs):
        """
        :param records: the actual data rows.
        :param schema: the JSON schema for the rows.
        :param metadata: the metadata of the data block.
        """
        if type(records) == str:
            records = json.loads(records)
        else:
            try:
                json.dumps(records)
            except:
                raise ValueError("Invalid JSON object")
        super().__init__(records, metadata, **kwargs)
    
    @override(BaseDataBlock)
    def __str__(self) -> str:
        return json.dumps(self._records)
