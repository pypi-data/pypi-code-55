from abc import(
    ABC,
    abstractmethod,
    abstractstaticmethod
)
from typing import(
    List,
    Dict
)
import uuid
import json
from azure.cosmosdb.table.tableservice import TableService
from npyetl.internals import override


class BaseLoggerLoader(ABC):
    
    def load(self, log: Dict[str,object]):
        log = self._format_log(log)
        assert self._validate_log(log)
        self._insert_log(log)

    def _format_log(self, log: Dict[str, object]) -> Dict[str, object]:
        return log

    @abstractmethod
    def _insert_log(self, log: Dict[str, object]):
        return NotImplementedError
    
    @staticmethod
    @abstractstaticmethod
    def _validate_log(log: Dict[str,object]) -> bool:
        raise NotImplementedError


class LogFileLoggerLoader(BaseLoggerLoader):
    
    def __init__(self,
                 file_name: str):
        self._file_name = file_name
        self._file = open(self._file_name, 'w')
        
    @override(BaseLoggerLoader)
    def _insert_log(self, log: Dict[str,object]):
        self._file.write(json.dumps(log))

    @override(BaseLoggerLoader)
    def _validate_log(self, log: Dict[str,object]):
        try:
            json.dumps(log)
            return True
        except TypeError:
            return False


class AzureTableLoggerLoader(BaseLoggerLoader):
    
    REQUIRED_LOG_ATTRS = 'PartitionKey', 'RowKey'
    
    def __init__(self,
                 table_service: TableService,
                 table_name: str):
        self._table_service = table_service
        self._table_name = table_name
    
    @override(BaseLoggerLoader)
    def _insert_log(self, log: Dict[str,object]):
        self._table_service.insert_entity(self._table_name, log)

    @override(BaseLoggerLoader)
    def _validate_log(self, log: Dict[str,object]) -> bool:
        if all([attr in log for attr in self.REQUIRED_LOG_ATTRS]):
            return True
        return False
