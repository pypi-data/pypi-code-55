from ..datetime.Date import Date
from . import AbstractDataMessage, CommonOrbitData, OrbitParameters
from .DataParserUtils import _decode_xml_value_element
from .enumerates import FileFormat

metadata_keys = [
    "OBJECT_NAME",
    "OBJECT_ID",
    "REF_FRAME",
    "TIME_SYSTEM",
    "MEAN_ELEMENT_THEORY",
    "CENTER_NAME",
]

data_keys = [
    "EPOCH",
    "SEMI_MAJOR_AXIS",
    "MEAN_MOTION",
    "ECCENTRICITY",
    "INCLINATION",
    "RA_OF_ASC_NODE",
    "ARG_OF_PERICENTER",
    "MEAN_ANOMALY",
    "GM",
]


class Omm(
    AbstractDataMessage.AbstractDataMessage,
    OrbitParameters.OrbitParameters,
    CommonOrbitData.CommonOrbitData,
):
    """OMM contains mean orbital parameters for a single object"""

    def __init__(self, filename, fmt):
        self.properties = {}
        self.metadata = {}
        self.state_elements = {}
        self.spacecraft_parameters = {}
        self.mean_parameters = {}
        self.covariance = {}
        self.user_parameters = {}
        super().__init__(fmt)
        self.open(filename, self.fmt)
        pass

    def open(self, filename, fmt):
        """Open an OMM file for parsing. A dictionnary is returned."""
        self.set_metadata_keys(metadata_keys)

        if self.fmt == FileFormat.XML:
            self.set_xml_ephemeris_state_key("meanElements")
            self.set_segment_blocks(
                {
                    "tleParameters": self._parse_tle_parameters_xml,
                    "spacecraftParameters": self._parse_spacecraft_parameters,
                    "covarianceMatrix": self._parse_covariance_xml,
                    "userDefinedParameters": self._parse_user_parameters_xml,
                }
            )

        metadata, elements = self.load_from_file(filename, fmt)
        if fmt == FileFormat.KVN:
            for key in self.metadata_keys:
                self.metadata[key] = self.properties[key]
            self._parse_state_vector_kvn(self.get_object_name(), None, self.properties)
            self._parse_covariance_kvn(self.get_object_name(), self.properties)

        elif fmt == FileFormat.XML:
            self.state_elements = elements

    def _parse_state_vector_kvn(self, object_name, metadata, block_data):
        data = {}
        epoch = Date(block_data["EPOCH"])
        for key in data_keys:
            if (key != "EPOCH") and (key in block_data.keys()):
                data[key] = block_data[key]
        self.state_elements[object_name] = [[epoch, data]]

    def _parse_state_vector_xml(self, object_name, state_vector):
        """Decode the state vector"""
        data = {}
        epoch = Date(state_vector.find("EPOCH").text)
        sma = state_vector.find("SEMI_MAJOR_AXIS")
        if sma:
            data["SEMI_MAJOR_AXIS"] = _decode_xml_value_element(
                state_vector, "SEMI_MAJOR_AXIS", "km"
            )
        else:
            data["MEAN_MOTION"] = _decode_xml_value_element(
                state_vector, "MEAN_MOTION", "rev/day"
            )
        data["ECCENTRICITY"] = _decode_xml_value_element(
            state_vector, "ECCENTRICITY", None
        )
        data["INCLINATION"] = _decode_xml_value_element(
            state_vector, "INCLINATION", "deg"
        )
        data["RA_OF_ASC_NODE"] = _decode_xml_value_element(
            state_vector, "RA_OF_ASC_NODE", "deg"
        )
        data["ARG_OF_PERICENTER"] = _decode_xml_value_element(
            state_vector, "ARG_OF_PERICENTER", "deg"
        )
        data["MEAN_ANOMALY"] = _decode_xml_value_element(
            state_vector, "MEAN_ANOMALY", "deg"
        )
        return epoch, data

    def _parse_tle_parameters_xml(self, object_name, element):
        self.mean_parameters = self._parse_section_xml(element)

    def _parse_user_parameters_xml(self, obect_name, elements):
        self.user_parameters = self._parse_section_xml(elements)

    def get_version(self):
        """Return the OMM version"""
        return self.properties["CCSDS_OMM_VERS"]

    def get_mean_element_theory(self):
        """Get the mean element theory used for computing the orbit mean element, and required for propagation"""
        return self.metadata["MEAN_ELEMENT_THEORY"]

    def get_mean_parameters(self):
        """Return the mean elements model parameters"""
        return self.mean_parameters

    def get_mean_elements(self):
        """Return the mean state elements"""
        return self.state_elements

    def get_user_parameters(self):
        """Return user defined parameters"""
        return self.user_parameters
