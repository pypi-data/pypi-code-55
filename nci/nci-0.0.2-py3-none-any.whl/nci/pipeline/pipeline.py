from typing import (
    Union,
    Optional,
    Dict
)
import pandas
from pandas import (
    to_datetime,
    Timestamp
)
from datetime import datetime
import time
import json
from azure.cosmosdb.table.tableservice import TableService
from azure.cosmosdb.table.models import Entity
import azure.common
from npyetl.pipeline import (
    Pipeline,
    PipelineLogger,
    AzureTableLoggerLoader
)
#
import nci
from .utils import my_import
from .logger_loader import NovicellInsightsLoggerLoader


## CONSTANTS
# STORAGE ACCOUNT
STORAGE_ACCOUNT_NAME = 'pronovinsstg'
STORAGE_ACCOUNT_KEY = 'iAmMKwYp29nXfoTA1RLBVQ3r4jxv2/ZRCSHa+G2F+YoQQHLSXaWkIFEK7anrRlYJeQvkuWqlhCoUINDZcoPinw=='
TABLE_SERVICE = TableService(STORAGE_ACCOUNT_NAME, STORAGE_ACCOUNT_KEY)
# LOGGER
LOGGER_TABLE = 'PipelinesLogs'
STATES_TABLE = 'PipelinesState'


class NovicellInsightsPipeline(Pipeline):

    def __init__(self,
                 customer: str,
                 platform: str,
                 name: str,
                 start_date: str,
                 frequency: Union[int,float],                 
                 extractor_name: str,
                 loader_name: str,
                 transformer_name: Optional[str] = None,
                 active: bool = True,
                 pipeline_parameters: Optional[str] = None,
                 metadata: Optional[str] = None,
                 **kwargs):
        """
        :param kwargs: [, pipeline_parameters, metadata]
        """
        self._customer = customer
        self._platform = platform
        self._name = name
        self._start_date = to_datetime(start_date)
        self._frequency = frequency
        self._active = active
        #
        extractor = my_import(extractor_name)
        loader = my_import(loader_name)
        transformer = my_import(transformer_name) if transformer_name else None
        logger_loader = NovicellInsightsLoggerLoader(customer, TABLE_SERVICE, LOGGER_TABLE)
        #
        pipeline_parameters = self._make_pipeline_parameters(pipeline_parameters)
        metadata = json.loads(metadata)
        #
        super().__init__(extractor(), 
                         loader(), 
                         transformer() if transformer else None, 
                         name=name,
                         pipeline_parameters=pipeline_parameters,
                         metadata=metadata,
                         logger_loader=logger_loader)
        
    
    def execute(self) -> Dict[str, object]:
        start_time = self._params['extraction']['start_time']
        end_time = self._params['extraction']['end_time']
        print(datetime.fromtimestamp(start_time), datetime.fromtimestamp(end_time))
        super().execute()
        self.update_or_create_status(start_time, end_time)

    def _make_pipeline_parameters(self,
                                  pipeline_parameters: Optional[str]):
        """[summary]
        :param pipeline_parameters: [description]
        :type pipeline_parameters: str
        """
        pipeline_parameters = json.loads(pipeline_parameters or json.dumps(dict()))
        #
        start_time = self.get_start_time()
        time_params = {'start_time': start_time,
                       'end_time': min(start_time+self.frequency_in_seconds, time.time())}
        if 'extraction' in pipeline_parameters:
            pipeline_parameters['extraction'].update(time_params)
        else:
            pipeline_parameters['extraction'] = time_params
        #
        status = self.get_status()
        globals_ = status.get('globals') or dict()
        for k in pipeline_parameters:
            pipeline_parameters[k].update( globals_.get(k, dict()) )
        #
        return pipeline_parameters

    @property
    def customer(self) -> str:
        return self._customer

    @property
    def platform(self) -> str:
        return self._platform

    @property
    def start_date(self) -> pandas.Timestamp:
        return self._start_date

    @property
    def frequency(self) -> Union[int,float]:
        return self._frequency
    
    @property
    def frequency_in_seconds(self) -> Union[int,float]:
        return self._frequency*60*60

    @property
    def active(self) -> bool:
        return self._active

    def get_status(self) -> Entity:
        """
        """
        try:
            return TABLE_SERVICE.get_entity(STATES_TABLE, self._customer, self._name)
        except azure.common.AzureMissingResourceHttpError:
            return Entity()
        
    def update_or_create_status(self,
                                start_time: Union[float,int],
                                end_time: Union[float,int],
                                globals_: Optional[Dict[str, object]] = None,
                                **kwargs) -> bool:
        """
        [summary]
        :return: [description]
        """
        current_status = self.get_status()
        status = Entity(PartitionKey=self._customer,
                        RowKey=self._name,
                        start_time=min(start_time, current_status.start_time) if current_status else start_time,
                        end_time=max(end_time, current_status.end_time) if current_status else end_time,
                        globals=globals_)
        try:
            TABLE_SERVICE.update_entity(STATES_TABLE, status)
        except azure.common.AzureMissingResourceHttpError:
            TABLE_SERVICE.insert_entity(STATES_TABLE, status)

    def get_start_time(self) -> Union[int,float]:
        """
        [summary]
        :return: [description]
        """
        status = self.get_status() 
        if status:
            if status.start_time > self._start_date.timestamp():
                return self._start_date.timestamp()
            return status.end_time
        #
        return self._start_date.timestamp()
