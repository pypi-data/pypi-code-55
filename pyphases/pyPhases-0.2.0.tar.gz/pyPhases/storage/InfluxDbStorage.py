from .Storage import Storage
from pandas import DataFrame
import pyarrow
import numpy
from ..exporter.InfluxExporter import InfluxExporter
from ..Data import DataNotFound

from influxdb import InfluxDBClient

class InfluxDbExporter(Storage):
    """ An Exporter that supports a lot of default formats using pyarrow"""

    connected = False
    client = None
    alsoAStorage = True
    acceptedExporter = [InfluxExporter]

    def initialOptions(self):
        return {
            "host": "localhost",
            "port": 8086,
            "username": "myuser",
            "username": "mypass",
            "ssl": True,
            "verify_ssl": True,
        }

    def connect(self):
        self.client = InfluxDBClient(
            host=self.getOption("host"),
            port=self.getOption("port"),
            username=self.getOption("username"),
            password=self.getOption("password"),
            ssl=self.getOption("ssl"),
            verify_ssl=self.getOption("verify_ssl")
        )
        connected = True

    def checkType(self, type):
        return type in (str, int, bool, float) or type in (numpy.ndarray, tuple) or type in (DataFrame, tuple) or type in [DataFrame, numpy.ndarray]
        # TODO: more generic with ?!

    def importData(self, byteString, options = {}):
        context = pyarrow.default_serialization_context()
        buffer = pyarrow.py_buffer(byteString)
        df = context.deserialize(buffer)

        return df

    def export(self, df, options = {}):
        context = pyarrow.default_serialization_context()
        serialized_df = context.serialize(df)
        buffer = serialized_df.to_buffer()
        byteString = buffer.to_pybytes()

        return byteString

    def read(self, path):
        try:
            file = open(self.getPath(path), "rb")
            return file.read()
        except FileNotFoundError:
            raise DataNotFound("Data was not found:" + path)

    def write(self, path, data):
        if isinstance(data, bytes):
            writeMode = "wb"
        else:
            writeMode = "w"
        file = open(self.getPath(path), writeMode)
        file.write(data)
        file.close()
