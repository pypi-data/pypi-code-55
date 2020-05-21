from ..datetime.Date import Date
from . import AbstractDataMessage, CommonOrbitData, OrbitParameters
from .DataParserUtils import _decode_xml_value_element
from .enumerates import FileFormat

metadata_keys = ["OBJECT_NAME", "OBJECT_ID", "REF_FRAME", "TIME_SYSTEM", "CENTER_NAME"]
data_keys = ["EPOCH", "X", "Y", "Z", "X_DOT", "Y_DOT", "Z_DOT"]
spacecraft_parameters_keys = [
    "MASS",
    "SOLAR_RAD_AREA",
    "SOLAR_RAD_COEFF",
    "DRAG_AREA",
    "DRAG_COEFF",
]


class Opm(
    AbstractDataMessage.AbstractDataMessage,
    OrbitParameters.OrbitParameters,
    CommonOrbitData.CommonOrbitData,
):
    """OPM contains orbital parameters for a single object"""

    def __init__(self, filename, fmt):
        self.properties = {}
        self.metadata = {}
        self.state_elements = {}
        self.spacecraft_parameters = {}
        self.covariance = {}
        super().__init__(fmt)
        self.open(filename, self.fmt)
        pass

    def open(self, filename, fmt):
        """Open an OPM file for parsing. A dictionnary is returned."""
        self.set_metadata_keys(metadata_keys)

        if self.fmt == FileFormat.XML:
            self.set_xml_ephemeris_state_key("stateVector")
            self.set_segment_blocks(
                {
                    "spacecraftParameters": self._parse_spacecraft_parameters,
                    "covarianceMatrix": self._parse_covariance_xml,
                }
            )

        dummy, state = self.load_from_file(filename, fmt)
        if fmt == FileFormat.KVN:
            for key in self.metadata_keys:
                self.metadata[key] = self.properties[key]

            self._parse_spacecraft_parameters_kvn(self.properties)
            self._parse_state_vector_kvn(self.get_object_name(), None, self.properties)
            self._parse_covariance_kvn(self.get_object_name(), self.properties)

        elif fmt == FileFormat.XML:
            self.state_elements = state

    def _parse_state_vector_kvn(self, object_name, metadata, block_data):
        epoch = Date(block_data["EPOCH"])
        x = float(block_data["X"])
        y = float(block_data["Y"])
        z = float(block_data["Z"])
        x_dot = float(block_data["X_DOT"])
        y_dot = float(block_data["Y_DOT"])
        z_dot = float(block_data["Z_DOT"])
        self.state_elements[object_name] = [[epoch, [x, y, z, x_dot, y_dot, z_dot]]]

    def _parse_spacecraft_parameters_kvn(self, properties):
        for key in spacecraft_parameters_keys:
            self.spacecraft_parameters[key] = float(properties[key])

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

    def get_version(self):
        """Return the OPM version"""
        return self.properties["CCSDS_OPM_VERS"]

    def get_x(self):
        return float(self.get_state_elements()[1][0])

    def get_y(self):
        return float(self.get_state_elements()[1][1])

    def get_z(self):
        return float(self.get_state_elements()[1][2])

    def get_xdot(self):
        return float(self.get_state_elements()[1][3])

    def get_ydot(self):
        return float(self.get_state_elements()[1][4])

    def get_zdot(self):
        return float(self.get_state_elements()[1][5])
