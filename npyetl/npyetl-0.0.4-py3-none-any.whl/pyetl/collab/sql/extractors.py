from typing import (
    List,
    Tuple,
    Any,
    Union
)
import pyodbc
from npyetl.extraction import BaseExtractor
from npyetl.data import (
    RelationalDataBlock,
    PandasDataBlock
)
from npyetl.internals.decorators import override


class ExtractorSQL(BaseExtractor):
    """
    An Extractor class for SQL Databases.
    """
    @override(BaseExtractor)
    def extract(self,
                connection_string: str,
                query: str,
                query_params: Union[List[Any], Tuple[Any, ...]] = ()) -> List[RelationalDataBlock]:
        """
        """
        data_base = pyodbc.connect(connection_string)
        return PandasDataBlock.from_sql(data_base, query % query_params)


class ExtractorSQLFunction(ExtractorSQL):
    """
    An ExtractorSQL child class for SQL Database Functions.
    """
    FUNCTION_QUERY = "SELECT * FROM %s(%s)"
    
    @override(ExtractorSQL)
    def extract(self,
                connection_string: str,
                function_name: str,
                function_parameters: dict) -> List[RelationalDataBlock]:
        """
        """
        query = self.FUNCTION_QUERY % (function_name, tuple(function_parameters.values()))
        return super(ExtractorSQLFunction, self).extract(connection_string, query)
