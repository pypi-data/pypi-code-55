from typing import(
    Generator,
    List
)
#
import pandas as pd
#
from npyetl.data import BaseRelationalDataBlock
from npyetl.internals.decorators import override


class PandasDataBlock(BaseRelationalDataBlock,
                      pd.DataFrame):

    def __init__(self, *args, **kwargs):
        super(pd.DataFrame, self).__init__(*args, **kwargs)

    @classmethod
    def from_sql(cls, con, query):
        return cls(pd.read_sql(query, con))

    @override(BaseRelationalDataBlock)
    def records(self) -> List[pd.Series]:
        return [ list(record) for _, record in self.iterrows() ]
    
    @override(pd.DataFrame)
    def __iter__(self) -> Generator[pd.Series, None, None]:
        return ( record for _, record in self.iterrows() )
