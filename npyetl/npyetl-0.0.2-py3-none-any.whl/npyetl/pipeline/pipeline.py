from typing import(
    List,
    Dict,
    Iterable,
    Optional
)
#
import multiprocessing as mp 
import datetime
import time
import json
import uuid
#
from npyetl.data import BaseDataBlock
from npyetl.extraction import BaseExtractor
from npyetl.transformation import BaseTransformer
from npyetl.load import BaseLoader
from npyetl.pipeline.logger import (
    PipelineLogger,
    BaseLoggerLoader
)


class Pipeline:
    
    def __init__(self,
                 extractor: BaseExtractor,
                 loader: BaseLoader,
                 transformer: BaseTransformer = None,
                 logger_loader: BaseLoggerLoader = None,
                 pipeline_parameters: Optional[Dict[str, object]] = None,
                 name: str = None,
                 metadata: dict = None):
        """[summary]
        :param extractor: [description]
        :type extractor: BaseExtractor
        :param loader: [description]
        :type loader: BaseLoader
        :param transformer: [description], defaults to None
        :type transformer: BaseTransformer, optional
        :param logger: [description], defaults to None
        :type logger: PipelineLogger, optional
        :param pipeline_params: [description], defaults to None
        :type pipeline_params: Optional[Dict[str, object]], optional
        :param name: [description], defaults to None
        :type name: str, optional
        :param metadata: [description], defaults to None
        :type metadata: dict, optional
        """
        self._extractor = extractor
        self._transformer = transformer
        self._loader = loader
        self._params = pipeline_parameters or dict()
        self._name = name
        self._metadata = metadata or dict()
        #
        self._logger = PipelineLogger(self._name, logger_loader) if logger_loader else None
        
    @classmethod
    def from_dict(cls, dictionary: dict) -> 'Pipeline':
        return cls(**dictionary)

    @classmethod
    def from_json(cls, json_content: str) -> 'Pipeline':
        return cls.from_dict(json.loads(json_content))

    @property
    def name(self) -> str:
        return self._name or self.__class__.__name__
    
    @property
    def id(self) -> str:
        return uuid.uuid4().__str__()

    @property
    def metadata(self) -> Optional[dict]:
        return self._metadata

    @property 
    def state(self) -> str:
        return self._state

    @property
    def logger(self) -> Optional[PipelineLogger]:
        return self._logger

    @property
    def params(self) -> Optional[Dict[str,object]]:
        return self._params

    ##################################################################################
    def execute(self) -> Dict[str,object]:
        """
        """
        start = time.time()
        self._log_start()
        succesful = self._load(self._transform(self._extract()))
        stats = {'execution_time': time.time()-start,
                 'pipeline_name': self.name,
                 'succesful': succesful}
        self._log_end(**stats)
        return stats

    def _extract(self) -> Iterable[BaseDataBlock]:
        extract_params = self._params.get('extraction', dict())
        yield from self._extractor.extract(**extract_params)
        return

    def _transform(self, data_blocks: Iterable[BaseDataBlock]) -> Iterable[BaseDataBlock]:
        if self._transformer:
            transformation_params = self._params.get('transformation', dict())
            yield from self._transformer.transform(data_blocks, **transformation_params)
            return
        yield from data_blocks
        return
        

    def _load(self, data_blocks: Iterable[BaseDataBlock]) -> bool:
        load_params = self._params.get('load', dict())
        load_status = self._loader.load(data_blocks, **load_params)
        return load_status
    
    ################################################################################
    def _log_start(self, **kwargs):
        if self._logger:
            self._logger.log_start(**kwargs)

    def _log_end(self, **kwargs):
        if self._logger:
            self._logger.log_end(**kwargs)


class PipelinePool:

    def __init__(self,
                 pipelines: List[Pipeline],
                 max_threads: int = 32,
                 metadata: dict = None):
        self._pipelines = pipelines
        self._num_of_pipelines = len(pipelines)
        self._max_threads = max_threads
        self._metadata = metadata

    @property
    def pipelines(self) -> List[Pipeline]:
        return self._pipelines

    @property
    def loggers(self) -> Dict[str, Optional[PipelineLogger]]:
        return { pipeline.id: pipeline.logger for pipeline in self._pipelines }

    @property
    def metadata(self) -> Optional[dict]:
        return self._metadata

    def execute(self) -> Iterable[Dict[str, object]]:
        with mp.Pool(min(self._max_threads, self._num_of_pipelines)) as pool:
            yield from list(pool.map(lambda p: p.execute(), self._pipelines))
