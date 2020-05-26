from abc import(
    ABC,
    abstractmethod
)
from typing import(
    List,
    Iterable,
    Dict,
    Callable,
    Any,
    Optional,
    Union
)
#
from npyetl.data import BaseDataBlock
from npyetl.internals.decorators import override

#
TransformFunction = Callable[[BaseDataBlock, Dict[str, object]], BaseDataBlock]


class BaseTransformer(ABC):
    
    def __init__(self,
                 metadata: dict = None):
        self._metadata = metadata or dict()
        
    @abstractmethod
    def transform(self,
                  input_data_blocks: Iterable[BaseDataBlock],
                  **kwargs) -> Iterable[BaseDataBlock]:
        raise NotImplementedError


class Transformer(BaseTransformer):
    
    def __init__(self,
                 transform_functions: List[TransformFunction],
                 metadata: dict = None):
        super().__init__(metadata)
        self._transform_functions = transform_functions
        
    @override(BaseTransformer)
    def transform(self,
                  input_data_blocks: Iterable[BaseDataBlock],
                  transform_functions_params: List[Dict[str, object]] = None) -> Iterable[BaseDataBlock]:
        """
        """
        if not transform_functions_params:
            transform_functions_params = [dict()]*len(self._transform_functions)
        assert len(transform_functions_params) == len(self._transform_functions)
        #
        for input_data_block in input_data_blocks:
            transformed_data_block = input_data_block
            for i, transform_function in enumerate(self._transform_functions):
                transformed_data_block = transform_function(transformed_data_block, **transform_functions_params[i])
            yield transformed_data_block
        return
