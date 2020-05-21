import numpy as np

from ..datetime.Date import Date
from . import AbstractDataMessage, CommonEphemerisData, CommonOrbitData, units
from .DataParserUtils import _decode_kvn, _decode_xml_value_element
from .enumerates import FileFormat, InterpolationMethod, ReferenceFrame, TimeSystem

METADATA_KEYS = [
    "OBJECT_NAME",
    "OBJECT_ID",
    "CENTER_NAME",
    "TIME_SYSTEM",
    "START_TIME",
    "STOP_TIME",
    "REF_FRAME",
]


class Oem(
    AbstractDataMessage.AbstractDataMessage,
    CommonOrbitData.CommonOrbitData,
    CommonEphemerisData.CommonEphemerisData,
):
    def __init__(self, filename, fmt):
        self.properties = {}
        self.metadata = {}
        self.data = {}
        self.covariance = {}
        super().__init__(fmt)
        self.open(filename, self.fmt)
        pass

    def open(self, filename, fmt):
        """Open an OEM file for parsing. A dictionnary is returned."""
        self.set_metadata_keys(METADATA_KEYS)
        if self.fmt == FileFormat.KVN:
            self.set_segment_blocks({"COVARIANCE": self._parse_covariance_kvn})
        elif self.fmt == FileFormat.XML:
            self.set_xml_ephemeris_state_key("stateVector")
            self.set_segment_blocks({"covarianceMatrix": self._parse_covariance_xml})

        dummy, self.data = self.load_from_file(filename, fmt)
        if fmt == FileFormat.KVN:
            self.metadata = dummy
            for object_name in self.metadata.keys():
                if "COVARIANCE" in self.data[object_name]:
                    self.covariance[object_name] = self.data[object_name]["COVARIANCE"]
                self.data[object_name] = self.data[object_name]["DATA"]

    def _parse_state_vector_kvn(self, object_name, metadata, lines):
        time_system = TimeSystem(metadata["TIME_SYSTEM"])
        ephemerides = []
        for line in lines:
            values = line.split()
            epoch = Date(values[0], time_system)
            x = float(values[1]) * units.km
            y = float(values[2]) * units.km
            z = float(values[3]) * units.km
            xdot = float(values[4]) * units.km
            ydot = float(values[5]) * units.km
            zdot = float(values[6]) * units.km
            ephemerides.append((epoch, [x, y, z, xdot, ydot, zdot]))
        return ephemerides

    def _parse_state_vector_xml(self, object_name, state_vector):
        """Decode the state vector"""
        epoch = Date(state_vector.find("EPOCH").text)
        x = _decode_xml_value_element(state_vector, "X", "km")
        y = _decode_xml_value_element(state_vector, "Y", "km")
        z = _decode_xml_value_element(state_vector, "Z", "km")
        xdot = _decode_xml_value_element(state_vector, "X_DOT", "km/s")
        ydot = _decode_xml_value_element(state_vector, "Y_DOT", "km/s")
        zdot = _decode_xml_value_element(state_vector, "Z_DOT", "km/s")
        return epoch, [x, y, z, xdot, ydot, zdot]

    def _parse_covariance_kvn(self, object_name, metadata, lines):
        covariances = {}
        key, value = _decode_kvn(lines[0])  # COV_REF_FRAME
        covariances[key] = value
        covariances["matrix"] = []
        for iline in range(1, len(lines), 7):
            cov = {}
            key, value = _decode_kvn(lines[iline])  # EPOCH
            cov[key] = value
            mat = np.array([[0.0] * 6] * 6)
            for row in range(0, 6):
                str_values = lines[iline + 1 + row].split()
                values = [float(val) for val in str_values]
                mat[row][0 : len(values)] = values
            mat = mat + mat.transpose()

            for idx in range(0, 6):
                mat[idx][idx] = mat[idx][idx] / 2.0
            cov["matrix"] = mat
            covariances["matrix"].append(cov)

        return covariances

    def _set_metadata(self, object_name, meta):
        self.metadata[object_name] = meta

    def get_version(self):
        """Return the OEM version"""
        return self.properties["CCSDS_OEM_VERS"]

    def get_reference_frame(self, sat_name):
        """Return the coordinate system of the ephemeris"""
        return ReferenceFrame(self.get_metadata_data(sat_name, "REF_FRAME"))

    def get_reference_frame_epoch(self, sat_name):
        """Return the coordinate system reference epoch"""
        return self.get_metadata_data(sat_name, "REF_FRAME_EPOCH")

    def get_interpolation_method(self, sat_name):
        """Get the satellite attitude information"""
        return InterpolationMethod(
            self.get_metadata_data(sat_name, "INTERPOLATION")
        )  # Note: in AEM it is INTERPOLATION_METHOD

    def get_interpolation_degree(self, sat_name):
        """Get the satellite attitude information"""
        return int(self.get_metadata_data(sat_name, "INTERPOLATION_DEGREE"))

    def get_ephemeris(self, sat_name):
        """Get the list of position and velocity vectors"""
        return self.data[sat_name]

    def get_covariances_frame(self, sat_name):
        """Get the list of reference frame for covariance"""
        return ReferenceFrame(self.covariance[sat_name]["COV_REF_FRAME"])

    def get_covariances(self, sat_name):
        """Get the list of position and velocity vectors"""
        return self.covariance[sat_name]["matrix"]
