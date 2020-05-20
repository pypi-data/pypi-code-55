from dataclasses import dataclass
from typing import List
from pyspark_config.transformations.transformations import Transformation
from pyspark_config.spark_utils.dataframe_extended import DataFrame_Extended
from pyspark_config.yamlConfig.config import dataclass_json
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass_json
@dataclass
class Output:
    type: str = None
    name: str = None
    path: str = None
    transformations: List[Transformation] = None

    def __apply_transformation__(self, df):
        """
        Apply multiple transformations to a dataFrame determined
        by the transformation configuration indicated in the `config`
        attribute of this class.

        :return: class:`DataFrame_Extended`. DataFrame as an output
        of the performed transformations.

        """
        if self.transformations:
            for trans in self.transformations:
                df = trans.transform(df=df)
        return df

    def save(self, df: DataFrame_Extended):
        pass


@dataclass_json
@dataclass
class Csv(Output):
    type="Csv"
    delimiter: str =","

    def save(self, df: DataFrame_Extended):
        df_transformed=self.__apply_transformation__(df)
        name="{}/{}.csv".format(self.path, self.name)
        df_transformed\
            .repartition(1)\
            .write\
            .csv(name,
                 header=True,
                 mode="overwrite"
                 )
        return logger.info('The output {} has been '
                           'created sucessfully.'.format(self.name))


@dataclass_json
@dataclass
class Json(Output):
    type="Json"

    def apply(self, df: DataFrame_Extended):
        name="{}/{}.json".format(self.path,self.name)
        return logger.info('The output {} has been '
                           'created sucessfully.'.format(self.name))


@dataclass_json
@dataclass
class Parquet(Output):
    type="Parquet"
    partitionCols: List[str] =None

    def save(self, df: DataFrame_Extended):
        name="{}/{}.parquet".format(self.path, self.name)
        df.coalesce(1).write.parquet(name, mode='overwrite')
        return logger.info('The output {} has been '
                           'created sucessfully.'.format(self.name))


@dataclass_json
@dataclass
class TFRecord(Output):
    type="TFRecord"

    def save(self, df: DataFrame_Extended):
        name='{}/{}.tfrecord'.format(self.path, self.name)
        df.coalesce(1).write.format("tfrecords").option("recordType", "Example").save(name)
        return logger.info('The output {} has been '
                           'created sucessfully.'.format(self.name))
