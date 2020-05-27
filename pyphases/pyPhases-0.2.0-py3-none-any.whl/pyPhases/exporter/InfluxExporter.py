from .DataExporter import DataExporter
from pandas import DataFrame
import pyarrow
import numpy

class InfluxExporter(DataExporter):
    """ An Exporter that supports a lot of default formats using pyarrow"""
    def checkType(self, type):
        return type in [object]
