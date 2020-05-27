from ..util.Optionizable import Optionizable

class InfluxDataRow(Optionizable):
    """Checks an instance, if its type is compatible with the current Exporter
    """
    def checkType(self, check) -> bool:
        """ Checks an instance, if its type is compatible with the current Exporter
        """
        pass

    def importData(self, raw, options):
        """ this methods transforms raw data from the storage into a specific dataformat (defined by the exporter)
        """
        pass

    def export(self):

        """ this method transforms a specific data type into a raw data that the storage can save
        """
        pass
