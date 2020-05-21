import numpy as np

from ..datetime.Date import Date
from . import AbstractDataMessage, exceptions
from .DataParserUtils import _decode_xml_value_element
from .enumerates import ConjunctionObject, FileFormat, ReferenceFrame, TimeSystem

METADATA_KEYS = [
    "OBJECT",
    "OBJECT_DESIGNATOR",
    "CATALOG_NAME",
    "OBJECT_NAME",
    "INTERNATIONAL_DESIGNATOR",
    "EPHEMERIS_NAME",
    "COVARIANCE_METHOD",
    "MANEUVERABLE",
    "REF_FRAME",
]

relative_data_keys = [
    "TCA",
    "MISS_DISTANCE",
    "RELATIVE_SPEED",
    "START_SCREEN_PERIOD",
    "STOP_SCREEN_PERIOD",
    "SCREEN_VOLUME_FRAME",
    "SCREEN_VOLUME_SHAPE",
    "SCREEN_VOLUME_X",
    "SCREEN_VOLUME_Y",
    "SCREEN_VOLUME_Z",
    "SCREEN_ENTRY_TIME",
    "SCREEN_EXIT_TIME",
    "COLLISION_PROBABILITY",
    "COLLISION_PROBABILITY_METHOD",
]
relative_sv_keys = [
    "RELATIVE_POSITION_R",
    "RELATIVE_POSITION_T",
    "RELATIVE_POSITION_N",
    "RELATIVE_VELOCITY_R",
    "RELATIVE_VELOCITY_T",
    "RELATIVE_VELOCITY_N",
]
state_keys = [
    "X",
    "Y",
    "Z",
    "X_DOT",
    "Y_DOT",
    "Z_DOT",
]
covariance_keys = [
    "CR_R",
    "CT_R",
    "CT_T",
    "CN_R",
    "CN_T",
    "CN_N",
    "CRDOT_R",
    "CRDOT_T",
    "CRDOT_N",
    "CRDOT_RDOT",
    "CTDOT_R",
    "CTDOT_T",
    "CTDOT_N",
    "CTDOT_RDOT",
    "CTDOT_TDOT",
    "CNDOT_R",
    "CNDOT_T",
    "CNDOT_N",
    "CNDOT_RDOT",
    "CNDOT_TDOT",
    "CNDOT_NDOT",
]
additional_parameters_keys = [
    "AREA_PC",
    "MASS",
    "CD_AREA_OVER_MASS",
    "CR_AREA_OVER_MASS",
    "THRUST_ACCELERATION",
    "SEDR",
]
od_keys = [
    "TIME_LASTOB_START",
    "TIME_LASTOB_END",
    "RECOMMENDED_OD_SPAN",
    "ACTUAL_OD_SPAN",
    "OBS_AVAILABLE",
    "OBS_USED",
    "TRACKS_AVAILABLE",
    "TRACKS_USED",
    "RESIDUALS_ACCEPTED",
    "WEIGHTED_RMS",
]


class Cdm(AbstractDataMessage.AbstractDataMessage):
    def __init__(self, filename, fmt):
        self.properties = {}
        self.relative_metadata = {}
        self.metadata = {}
        self.data = {}
        self.current_sat = []
        self.obj_name_map = {}
        super().__init__(fmt)
        self.open(filename, self.fmt)
        pass

    def open(self, filename, fmt):
        """Open an CDM file for parsing. A dictionary is returned."""
        # relative metadata
        # self.set_metadata_keys(["TCA", "MISS_DISTANCE", "TIME_SYSTEM"])
        # metadata for each object
        self.set_metadata_keys(METADATA_KEYS)
        if self.fmt == FileFormat.XML:
            self.set_common_blocks(
                {
                    "relativeMetadataData": self._parse_relative_metadata,
                    "relativeStateVector": self._parse_relative_state_vector,
                }
            )

            # segment has two block: metadata and data. This defines the sub-blocks of the data block
            self.set_xml_ephemeris_state_key("stateVector")
            self.set_segment_blocks(
                {
                    "odParameters": self._parse_od_parameters,
                    "additionalParameters": self._parse_additional_parameters,
                    "covarianceMatrix": self._parse_covariance,
                }
            )

        self.load_from_file(filename, fmt)

        # check we have exactly two sections

    def _set_metadata(self, sat_name, meta):
        obj = ConjunctionObject(
            meta["OBJECT"]
        )  # refer metadata by OBJECT1 and OBJECT2, not by name
        self.obj_name_map[sat_name] = obj
        self.metadata[obj] = meta

    def _set_property(self, key, value):
        if self.fmt == FileFormat.KVN:
            self._set_kvn_property(key, value)
        else:
            self.properties[key] = value

    def _set_kvn_property(self, key, value):
        if key == "OBJECT":
            obj = ConjunctionObject(value)
            self.current_sat = obj
            self.metadata[obj] = {}
            self.data[obj] = {}

        if self.current_sat:
            if key in self.metadata_keys:
                self.metadata[self.current_sat][key] = value
            else:
                self.data[self.current_sat][key] = value
        else:
            if key in relative_data_keys:
                self.relative_metadata[key] = value
            else:
                self.properties[key] = value
        pass

    def _get_property(self, key):
        try:
            return self.properties[key]
        except KeyError as e:
            raise exceptions.CcsdsParameterNotFoundError(
                "No value for property {:s}".format(key)
            )

    def set_xml_value(self, object_name, keys, state):
        if object_name not in self.relative_metadata:
            self.relative_metadata[object_name] = {}

        for key in keys:
            val = state.find(key)
            if val is None:
                continue
            self.relative_metadata[object_name][key] = _decode_xml_value_element(
                state, key, None
            )

    def _set_relative_metadata(self, keys, state):
        for key in keys:
            val = state.find(key)
            if val is None:
                continue
            self.relative_metadata[key] = _decode_xml_value_element(state, key, None)

    def _get_relative_metadata(self, key):
        try:
            return self.relative_metadata[key]
        except KeyError as e:
            raise exceptions.CcsdsParameterNotFoundError(
                "No value for relative metadata {:s}".format(key)
            )

    def _set_xml_data_value(self, object_name, keys, state):
        if object_name not in self.data.keys():
            self.data[object_name] = {}

        for key in keys:
            val = state.find(key)
            if val is None:
                continue
            self.data[object_name][key] = _decode_xml_value_element(state, key, None)

    def _get_data_value(self, object_name=None, sat_name=None):
        if sat_name:
            object_name = self.obj_name_map[sat_name]
        try:
            return self.data[object_name]
        except KeyError as e:
            raise exceptions.CcsdsObjectNotFoundError(
                "No data for object={:s} name={:s}".format(object_name, sat_name)
            )

    def _parse_relative_metadata(self, state):
        if self.fmt == FileFormat.XML:
            self._set_relative_metadata(relative_data_keys, state)

    def _parse_relative_state_vector(self, state):
        if self.fmt == FileFormat.XML:
            self._set_relative_metadata(relative_sv_keys, state)

    def _parse_od_parameters(self, sat_name, state):
        if self.fmt == FileFormat.XML:
            object_name = self.obj_name_map[sat_name]
            self._set_xml_data_value(object_name, od_keys, state)

    def _parse_additional_parameters(self, sat_name, state):
        if self.fmt == FileFormat.XML:
            object_name = self.obj_name_map[sat_name]
            self._set_xml_data_value(object_name, additional_parameters_keys, state)

    def _parse_state_vector_xml(self, sat_name, state):
        """Decode the state vector"""
        if self.fmt == FileFormat.XML:
            object_name = self.obj_name_map[sat_name]
            self._set_xml_data_value(object_name, state_keys, state)

    def _parse_covariance(self, sat_name, state):
        if self.fmt == FileFormat.XML:
            object_name = self.obj_name_map[sat_name]
            self._set_xml_data_value(object_name, covariance_keys, state)

    def get_version(self):
        """Return the CDM version"""
        return self.properties["CCSDS_CDM_VERS"]

    def get_satellite_count(self):
        """Get the number of satellites available in the CDM"""
        return len(self.metadata)

    def get_satellite_list(self):
        """Get the list of satellites available in the CDM"""
        return [self.get_primary_satellite_name(), self.get_secondary_satellite_name()]

    def get_primary_satellite_name(self):
        """Get the primary object name"""
        return self.metadata[ConjunctionObject.OBJECT1]["OBJECT_NAME"]

    def get_secondary_satellite_name(self):
        """Get the primary object name"""
        return self.metadata[ConjunctionObject.OBJECT2]["OBJECT_NAME"]

    def get_tca(self):
        """Get the time of closest approach"""
        return Date(self._get_relative_metadata("TCA"), TimeSystem.UTC)

    def get_miss_distance(self):
        """Get the miss distance"""
        return float(self._get_relative_metadata("MISS_DISTANCE"))

    def get_probability(self):
        """Get the probability of collision"""
        return float(self._get_relative_metadata("COLLISION_PROBABILITY"))

    def get_relative_state(self):
        """Get the relative state at TCA in the RTN local orbital frame of OBJECT1"""
        relative_state = []
        for key in relative_sv_keys:
            relative_state.append(float(self._get_relative_metadata(key)))
        return relative_state

    def get_coordinate_system(self, obj_name):
        """Return the coordinate system of the state for sat_name"""
        return ReferenceFrame(self.metadata[obj_name]["REF_FRAME"])

    def get_state_vector(self, obj_name=None, sat_name=None):
        """Get the satellite state vector (x,y,z,xdot,ydot,zdot)"""
        data = self._get_data_value(object_name=obj_name, sat_name=sat_name)
        x = float(data["X"])
        y = float(data["Y"])
        z = float(data["Z"])
        xdot = float(data["X_DOT"])
        ydot = float(data["Y_DOT"])
        zdot = float(data["Z_DOT"])
        return [x, y, z, xdot, ydot, zdot]

    def get_covariance(self, obj_name=None, sat_name=None):
        """Get the satellite covariance in RTN local orbital frame"""
        data = self._get_data_value(object_name=obj_name, sat_name=sat_name)
        cov_keys = [
            ["CR_R", None, None, None, None, None],
            ["CT_R", "CT_T", None, None, None, None],
            ["CN_R", "CN_T", "CN_N", None, None, None],
            ["CRDOT_R", "CRDOT_T", "CRDOT_N", "CRDOT_RDOT", None, None],
            ["CTDOT_R", "CTDOT_T", "CTDOT_N", "CTDOT_RDOT", "CTDOT_TDOT", None],
            ["CNDOT_R", "CNDOT_T", "CNDOT_N", "CNDOT_RDOT", "CNDOT_TDOT", "CNDOT_NDOT"],
        ]
        covariance = [[0.0] * 6] * 6
        covariance = np.array(covariance)
        for row in range(0, 6):
            for col in range(0, row + 1):
                key = cov_keys[row][col]
                covariance[row][col] = float(data[key])
                covariance[col][row] = covariance[row][col]
        return covariance
