""" Load Synthetic dataset references tables
"""
import pandas as pd

from .tables import glob, load_table, DATASET_TABLES, SCHEMA_VERSION
from .validation import NoRecordError


class AnnotationDefinitions:
    """Load annotation_definitions table

    For more detail, see schema design here:
    #todo update link
    https://docs.google.com/document/d/
    1lKPm06z09uX9gZIbmBUMO6WKlIGXiv3hgXb_taPOnU0/edit#heading=h.i6217crabzpe

    Attributes:
        table (pd): a collection of annotation_definitions records
    """

    TABLE_NAME = "annotation_definitions"
    FILE_PATTERN = DATASET_TABLES[TABLE_NAME].file

    def __init__(self, data_root, version=SCHEMA_VERSION):
        """ Initialize AnnotationDefinitions

        Args:
            data_root (str): the root directory of the dataset containing
        tables
            version (str): desired schema version
        """
        self.table = self.load_annotation_definitions(data_root, version)

    def load_annotation_definitions(self, data_root, version):
        """Load annotation definition files.
        #todo update link
        https://docs.google.com/document/d/
        1lKPm06z09uX9gZIbmBUMO6WKlIGXiv3hgXb_taPOnU0/
        edit#bookmark=id.4qtn5ym9nsy6
        Args:
            data_root (str): the root directory of the dataset containing
        tables
            version (str): desired schema version

        Returns:
            A Pandas dataframe with annotation definition records.
            Columns: 'id' (annotation id), 'name' (annotation name),
            'description' (string description), 'format'
            (string describing format), 'spec' ( Format-specific specification
            for the annotation values)
        """
        definitions = []
        for def_file in glob(data_root, self.FILE_PATTERN):
            definition = load_table(def_file, self.TABLE_NAME, version)
            definitions.append(definition)
        combined = pd.concat(definitions, axis=0).drop_duplicates(subset="id")

        return combined

    def get_definition(self, def_id):
        """Get the annotation definition for a given definition id

        Args:
            def_id (int): annotation definition id used to filter results

        Returns:
            a dictionary containing the annotation definition
        """
        mask = self.table.id == def_id
        definition = self.table[mask]
        if definition.empty:
            raise NoRecordError(
                f"No records are found in the annotation_definitions file "
                f"that matches the specified definition id: {def_id}"
            )
        definition = definition.to_dict("records")[0]

        return definition


class MetricDefinitions:
    """Load metric_definitions table

    For more detail, see schema design here:
    #todo update link
    https://docs.google.com/document/d/
    1lKPm06z09uX9gZIbmBUMO6WKlIGXiv3hgXb_taPOnU0/edit#bookmark=id.hzkb7u68plnp
    Attributes:
        table (pd): a collection of metric_definitions records with columns: id
    (id for metric definition), name, description, spec (definition specific
    spec)
    """

    TABLE_NAME = "metric_definitions"
    FILE_PATTERN = DATASET_TABLES[TABLE_NAME].file

    def __init__(self, data_root, version=SCHEMA_VERSION):
        """ Initialize MetricDefinitions
        Args:
            data_root (str): the root directory of the dataset containing
        tables
            version (str): desired schema version
        """
        self.table = self.load_metric_definitions(data_root, version)

    def load_metric_definitions(self, data_root, version):
        """Load metric definition files.
        https://docs.google.com/document/d/
        1lKPm06z09uX9gZIbmBUMO6WKlIGXiv3hgXb_taPOnU0/
        edit#bookmark=id.hzkb7u68plnp
        Args:
            data_root (str): the root directory of the dataset containing tables
            version (str): desired schema version

        Returns:
            A Pandas dataframe with metric definition records.
        a collection of metric_definitions records with columns: id
    (id for metric definition), name, description, spec (definition specific
    spec)
        """
        definitions = []
        for def_file in glob(data_root, self.FILE_PATTERN):
            definition = load_table(def_file, self.TABLE_NAME, version)
            definitions.append(definition)

        combined = pd.concat(definitions, axis=0).drop_duplicates(subset="id")

        return combined

    def get_definition(self, def_id):
        """Get the metric definition for a given definition id

        Args:
            def_id (int): metric definition id used to filter results

        Returns:
            a dictionary containing metric definition
        """
        mask = self.table.id == def_id
        definition = self.table[mask]
        if definition.empty:
            raise NoRecordError(
                f"No records are found in the metric_definitions file "
                f"that matches the specified definition id: {def_id}"
            )
        definition = definition.to_dict("records")[0]

        return definition


class Egos:
    """Load egos table

    For more detail, see schema design here:
    #todo update link
    https://docs.google.com/document/d/
    1lKPm06z09uX9gZIbmBUMO6WKlIGXiv3hgXb_taPOnU0/edit#heading=h.3rpgtair2cli

    Attributes:
        table (pd): a collection of egos records
    """

    TABLE_NAME = "egos"
    FILE_PATTERN = DATASET_TABLES[TABLE_NAME].file

    def __init__(self, data_root, version=SCHEMA_VERSION):
        """Initialize Egos
        #todo update link
        https://docs.google.com/document/d/1lKPm06z09uX9gZIbmBUMO6WKlIGXiv3hgXb_taPOnU0/edit#bookmark=id.x9sve3w8ahpv
        Args:
            data_root (str): the root directory of the dataset containing
            ego tables. Two columns: id (ego id) and description
            version (str): desired schema version
        """
        self.table = self.load_egos(data_root, version)

    def load_egos(self, data_root, version):
        """Load egos files.
        #todo update link
        https://docs.google.com/document/d/
        1lKPm06z09uX9gZIbmBUMO6WKlIGXiv3hgXb_taPOnU0/
        edit#bookmark=id.x9sve3w8ahpv
        Args:
            data_root (str): the root directory of the dataset containing
            ego tables
            version (str): desired schema version

        Returns:
            A pandas dataframe with all ego records with two columns: id
            (ego id) and description
        """
        egos = []
        for ego_file in glob(data_root, self.FILE_PATTERN):
            ego = load_table(ego_file, self.TABLE_NAME, version)
            egos.append(ego)
        combined = pd.concat(egos, axis=0).drop_duplicates(subset="id")

        return combined


class Sensors:
    """Load sensors table

    For more detail, see schema design here:
    #todo update link
    https://docs.google.com/document/
    d/1lKPm06z09uX9gZIbmBUMO6WKlIGXiv3hgXb_taPOnU0/
    edit#bookmark=id.ch2kop9kkj86
    Attributes:
        table (pd): a collection of sensors records with columns:
        'id' (sensor id), 'ego_id', 'modality'
        ({camera, lidar, radar, sonar,...} -- Sensor modality), 'description'

    """

    TABLE_NAME = "sensors"
    FILE_PATTERN = DATASET_TABLES[TABLE_NAME].file

    def __init__(self, data_root, version=SCHEMA_VERSION):
        """ Initialize Sensors

        Args:
            data_root (str): the root directory of the dataset containing
        tables
            version (str): desired schema version
        """
        self.table = self.load_sensors(data_root, version)

    def load_sensors(self, data_root, version):
        """Load sensors files.
        #todo update link
        https://docs.google.com/document/d/
        1lKPm06z09uX9gZIbmBUMO6WKlIGXiv3hgXb_taPOnU0/
        edit#bookmark=id.ch2kop9kkj86
        Args:
            data_root (str): the root directory of the dataset containing
        tables
            version (str): desired schema version

        Returns:
            A pandas dataframe with all sensors records  with columns:
        'id' (sensor id), 'ego_id', 'modality'
        ({camera, lidar, radar, sonar,...} -- Sensor modality), 'description'
        """
        sensors = []
        for sensor_file in glob(data_root, self.FILE_PATTERN):
            sensor = load_table(sensor_file, self.TABLE_NAME, version)
            sensors.append(sensor)
        combined = pd.concat(sensors, axis=0).drop_duplicates(subset="id")

        return combined
