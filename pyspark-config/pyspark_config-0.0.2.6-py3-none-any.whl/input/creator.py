from typing import List
from dataclasses import dataclass
import pyspark.sql.functions as F
from pyspark_config.yamlConfig.config import dataclass_json


@dataclass_json
@dataclass
class Creator:
    type: str = None

    def create(self, spark_session):
        raise NotImplementedError("Create method not implemented")

@dataclass_json
@dataclass
class Join(Creator):
    type = "Join"
    left: str = None
    right: str = None
    left_on: List[str] = None
    right_on: List[str] = None
    how: str = None

    def create(self, spark_session):
        left_df = spark_session.sql("Select * from "+self.left)
        right_df = spark_session.sql("Select * from "+self.right)
        def get_on(left_on, right_on):
            if len(left_on) != len(right_on):
                raise IndexError("list 'left_on' and list 'right_on' "
                                 "must have the same length.")
            elif len(left_on)==0 and len(right_on)==0:
                raise IndexError("list 'left_on' and list 'right_on' "
                                 "must have at least one entry.")
            else:
                return [F.col(f) == F.col(s) for (f, s) in zip(left_on, right_on)]

        return left_df.join(
            other=right_df,
            on=get_on(self.left_on, self.right_on),
            how=self.how
        )
