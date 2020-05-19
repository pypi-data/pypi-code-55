from dataclasses import dataclass
from typing import List
import logging

from pyspark_config.yamlConfig.config import dataclass_json
from pyspark_config.input import Source
from pyspark_config.input.creator import Creator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass_json
@dataclass
class Input:
    sources: List[Source] = None
    creations: List[Creator] = None

    def find(self, label):
        for source in self.sources:
            if source.label==label:
                return source
        raise Exception("The input source {} is not define.".format(label))


    def table_dict(self, spark_session):
        """
        List of all input dataFrames alias DFOs.

        :return: List of DFOs.

        """
        for source in self.sources:
            source.apply(spark_session).registerTempTable(source.label)

    def get_input(self, spark_session):
        """
        Created the input dataFrame.

        """
        self.table_dict(spark_session)

        if not self.creations:
            if not self.sources:
                raise Exception("Missing input.")
            elif len(self.sources)==1:
                return spark_session.table(next(iter(self.sources)).label)
            else:
                raise Exception("Multiple sources to choose from. "
                                "Specify transformations in order "
                                "to handle all sources or delete sources.")
        elif len(self.creations)== 1:
            return next(iter(self.creations)).create(spark_session=spark_session)
        else:
            creations=self.creations[1:]
            return next(iter(self.creations)).create(spark_session=spark_session)


