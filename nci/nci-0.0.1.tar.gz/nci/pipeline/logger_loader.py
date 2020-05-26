from typing import (
    Dict
)
from npyetl.pipeline import AzureTableLoggerLoader
from azure.cosmosdb.table.tableservice import TableService
import uuid


class NovicellInsightsLoggerLoader(AzureTableLoggerLoader):
    
    def __init__(self,
                 customer: str,
                 table_service: TableService,
                 table_name: str):
        """
        [summary]
        :param customer: [description]
        :type customer: str
        :param pipeline_name: [description]
        :type pipeline_name: str
        """
        self._customer = customer
        super().__init__(table_service, table_name)
        
    def _format_log(self, log: Dict[str, object]) -> Dict[str, object]:
        log['PartitionKey'] = log['pipeline_name']
        log['RowKey'] = uuid.uuid4().__str__()
        log['customer'] = self._customer
        return log
