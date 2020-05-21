from ..datetime.Date import Date
from . import enumerates, exceptions


class CommonEphemerisData:
    def __init__(self):
        pass

    def get_satellite_count(self):
        """Get the number of satellites available in the OEM/AEM"""
        return len(self.metadata)

    def get_satellite_list(self):
        """Get the list of satellites available in the OEM/AEM"""
        return self.metadata.keys()

    def get_satellite_info(self, sat_name):
        """Get the satellite information"""
        return self.metadata[sat_name]

    def get_metadata_data(self, sat_name, key):
        try:
            metadata = self.metadata[sat_name]
        except KeyError as e:
            raise exceptions.CcsdsObjectNotFoundError(
                "No object with name {:s} found".format(sat_name)
            )
        try:
            return metadata[key]
        except KeyError as e:
            raise exceptions.CcsdsParameterNotFoundError(
                "No value {:s} for object {:s}".format(key, sat_name)
            )

    def get_object_id(self, sat_name):
        return self.get_metadata_data(sat_name, "OBJECT_ID")

    def get_center_name(self, sat_name):
        return self.get_metadata_data(sat_name, "CENTER_NAME")

    def get_time_system(self, sat_name):
        """Return the time system used for the ephemeris point"""
        return enumerates.TimeSystem(self.get_metadata_data(sat_name, "TIME_SYSTEM"))

    def has_time_system(self, sat_name):
        """Return true if a time system is specified"""
        return "TIME_SYSTEM" in self.metadata[sat_name]

    def get_start_time(self, sat_name):
        """Return the start epoch of the ephemeris"""
        return Date(
            self.get_metadata_data(sat_name, "START_TIME"),
            self.get_time_system(sat_name),
        )

    def get_useable_start_time(self, sat_name):
        """Return the start epoch of the ephemeris"""
        return Date(
            self.get_metadata_data(sat_name, "USEABLE_START_TIME"),
            self.get_time_system(sat_name),
        )

    def get_useable_stop_time(self, sat_name):
        """Return the start epoch of the ephemeris"""
        return Date(
            self.get_metadata_data(sat_name, "USEABLE_STOP_TIME"),
            self.get_time_system(sat_name),
        )

    def get_stop_time(self, sat_name):
        """Return the start epoch of the ephemeris"""
        return Date(
            self.get_metadata_data(sat_name, "STOP_TIME"),
            self.get_time_system(sat_name),
        )
