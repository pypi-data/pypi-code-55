from typing import (
    List,
    Dict
)
import time
from npyetl.pipeline.logger_loader import BaseLoggerLoader


class PipelineLogger:
    
    def __init__(self,
                 pipeline_name: str,
                 loader: BaseLoggerLoader = None):
        self._pipeline_name = pipeline_name
        self._loader = loader
        self._logs = list()
        
    def log(self, log: Dict[str, object]):
        self._logs.append(log)
        if self._loader:
            self._loader.load(log)

    def log_start(self, **kwargs):
        self.log(self._make_log('start', **kwargs))
    
    def log_end(self, **kwargs):
        self.log(self._make_log('end', **kwargs))

    def _make_log(self,
                  status: str,
                  **kwargs) -> Dict[str, str]:
        """
        [summary]
        :param status: [description]
        :return: [description]
        """
        log = { 'pipeline_name': self._pipeline_name, 'status':status }
        log.update(kwargs)
        return log
