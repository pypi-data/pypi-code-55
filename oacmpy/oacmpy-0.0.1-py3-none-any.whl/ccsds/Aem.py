from ..datetime.Date import Date
from . import AbstractDataMessage, CommonEphemerisData, enumerates, exceptions
from .DataParserUtils import _decode_xml_value_element
from .enumerates import AttitudeType

METADATA_KEYS = ["OBJECT_NAME", "OBJECT_ID", "TIME_SYSTEM"]


class Aem(
    AbstractDataMessage.AbstractDataMessage, CommonEphemerisData.CommonEphemerisData
):
    def __init__(self, filename, fmt):
        self.metadata = {}
        self.properties = {}
        self.attitude = {}
        super().__init__(fmt)
        self.open(filename, self.fmt)
        pass

    def open(self, filename, fmt):
        """Open an AEM file for parsing. A dictionary is returned."""
        self.set_metadata_keys(METADATA_KEYS)
        if self.fmt == enumerates.FileFormat.KVN:
            self.set_segment_blocks({"DATA": self._parse_state_vector_kvn})
        elif self.fmt == enumerates.FileFormat.XML:
            self.set_xml_ephemeris_state_key("attitudeState")
            self.set_segment_blocks({})

        dummy, self.attitude = self.load_from_file(filename, fmt)
        if fmt == enumerates.FileFormat.KVN:
            self.metadata = dummy
            for object_name in self.metadata.keys():
                self.attitude[object_name] = self.attitude[object_name]["DATA"]

    def _parse_quaternion_kvn(self, attitude_type, values):
        quat = values[0:4]
        if attitude_type == AttitudeType.QUATERNION:
            return quat
        elif attitude_type == AttitudeType.QUATERNION_DERIVATIVE:
            quat_dot = values[4:9]
            return [quat, quat_dot]
        elif attitude_type == AttitudeType.QUATERNION_RATE:
            quat_rate = values[4:8]
            return [quat, quat_rate]

    def _parse_euler_kvn(self, attitude_type, values):
        angles = values[0:4]
        if attitude_type == AttitudeType.EULER_ANGLE:
            return angles

        if attitude_type == AttitudeType.EULER_ANGLE_RATE:
            rate = values[4:8]
            return [angles, rate]

    def _parse_spin_kvn(self, attitude_type, values):
        spin = values[0:5]
        if attitude_type == AttitudeType.SPIN:
            return spin

        if attitude_type == AttitudeType.SPIN_NUTATION:
            nutation = values[5:8]
            return [spin, nutation]

    def _parse_state_vector_kvn(self, object_name, metadata, lines):
        time_system = enumerates.TimeSystem(metadata["TIME_SYSTEM"])
        attitudes = []
        for line in lines:
            str_values = line.split()
            epoch = Date(str_values[0], time_system)
            values = [float(val) for val in str_values[1:]]
            attitude_type = AttitudeType(metadata["ATTITUDE_TYPE"])

            if (
                attitude_type == AttitudeType.QUATERNION
                or attitude_type == AttitudeType.QUATERNION_DERIVATIVE
                or attitude_type == AttitudeType.QUATERNION_RATE
            ):
                att = self._parse_quaternion_kvn(attitude_type, values)
            elif (
                attitude_type == AttitudeType.SPIN
                or attitude_type == AttitudeType.SPIN_NUTATION
            ):
                att = self._parse_spin_kvn(attitude_type, values)
            else:
                att = self._parse_euler_kvn(attitude_type, values)
            attitudes.append((epoch, att))
        return attitudes

    def _parse_quaternion_xml(self, attitude_type, element):
        if attitude_type == AttitudeType.QUATERNION:
            root_element = element.find("quaternionState")
        elif attitude_type == AttitudeType.QUATERNION_DERIVATIVE:
            root_element = element.find("quaternionDerivative")
        elif attitude_type == AttitudeType.QUATERNION_RATE:
            root_element = element.find("quaternionEulerRate")
        epoch = Date(root_element.find("EPOCH").text)

        quat_element = root_element.find("quaternion")
        q0 = _decode_xml_value_element(quat_element, "QC", "")
        q1 = _decode_xml_value_element(quat_element, "Q1", "")
        q2 = _decode_xml_value_element(quat_element, "Q2", "")
        q3 = _decode_xml_value_element(quat_element, "Q3", "")
        quat = [q0, q1, q2, q3]  # FIRST

        if attitude_type == AttitudeType.QUATERNION:
            return epoch, quat

        if attitude_type == AttitudeType.QUATERNION_DERIVATIVE:
            quat_der_element = root_element.find("quaternionRate")
            q0_dot = _decode_xml_value_element(quat_der_element, "QC_DOT", "")
            q1_dot = _decode_xml_value_element(quat_der_element, "Q1_DOT", "")
            q2_dot = _decode_xml_value_element(quat_der_element, "Q2_DOT", "")
            q3_dot = _decode_xml_value_element(quat_der_element, "Q3_DOT", "")
            return epoch, [quat, [q0_dot, q1_dot, q2_dot, q3_dot]]

        if attitude_type == AttitudeType.QUATERNION_RATE:
            quat_rate_element = root_element.find("rotationRates")
            rot1 = _decode_xml_value_element(quat_rate_element, "rotation1", "deg/")
            rot2 = _decode_xml_value_element(quat_rate_element, "rotation2", "deg/s")
            rot3 = _decode_xml_value_element(quat_rate_element, "rotation3", "deg/s")
            return epoch, [quat, [rot1, rot2, rot3]]

    def _parse_euler_xml(self, attitude_type, element):
        if attitude_type == AttitudeType.EULER_ANGLE:
            root_element = element.find("eulerAngle")
        elif attitude_type == AttitudeType.EULER_ANGLE_RATE:
            root_element = element.find("eulerAngleRate")
        epoch = Date(root_element.find("EPOCH").text)

        euler_element = root_element.find("rotationAngles")
        rot1 = _decode_xml_value_element(euler_element, "rotation1", "deg")
        rot2 = _decode_xml_value_element(euler_element, "rotation2", "deg")
        rot3 = _decode_xml_value_element(euler_element, "rotation3", "deg")
        angles = [rot1, rot2, rot3]
        if attitude_type == AttitudeType.EULER_ANGLE:
            return epoch, angles

        if attitude_type == AttitudeType.EULER_ANGLE_RATE:
            euler_rate_element = root_element.find("rotationRates")
            rot1 = _decode_xml_value_element(euler_rate_element, "rotation1", "deg/s")
            rot2 = _decode_xml_value_element(euler_rate_element, "rotation2", "deg/s")
            rot3 = _decode_xml_value_element(euler_rate_element, "rotation3", "deg/s")
            return epoch, [angles, [rot1, rot2, rot3]]

    def _parse_spin_xml(self, attitude_type, element):
        if attitude_type == AttitudeType.SPIN:
            root_element = element.find("spin")
        elif attitude_type == AttitudeType.SPIN_NUTATION:
            root_element = element.find("spinNutation")
        epoch = Date(root_element.find("EPOCH").text)

        spin_element = root_element
        spin_alpha = _decode_xml_value_element(spin_element, "SPIN_ALPHA", "deg")
        spin_delta = _decode_xml_value_element(spin_element, "SPIN_DELTA", "deg")
        spin_angle = _decode_xml_value_element(spin_element, "SPIN_ANGLE", "deg")
        spin_angle_vel = _decode_xml_value_element(
            spin_element, "SPIN_ANGLE_VEL", "deg/s"
        )
        spin = [spin_alpha, spin_delta, spin_angle, spin_angle_vel]
        if attitude_type == AttitudeType.SPIN:
            return epoch, spin

        if attitude_type == AttitudeType.SPIN_NUTATION:
            nutation_element = root_element.find("eulerAngle")
            spin_nut = _decode_xml_value_element(nutation_element, "NUTATION", "deg")
            spin_nut_per = _decode_xml_value_element(
                nutation_element, "NUTATION_PER", "s"
            )
            spin_nut_phase = _decode_xml_value_element(
                nutation_element, "NUTATION_PHASE", "deg"
            )
            return epoch, [spin, [spin_nut, spin_nut_per, spin_nut_phase]]

    def _parse_state_vector_xml(self, object_name, state_vector):
        """Decode the state vector"""
        attitude_type = self.get_attitude_type(object_name)
        if (
            attitude_type == AttitudeType.QUATERNION
            or attitude_type == AttitudeType.QUATERNION_DERIVATIVE
            or attitude_type == AttitudeType.QUATERNION_RATE
        ):
            return self._parse_quaternion_xml(attitude_type, state_vector)
        if (
            attitude_type == AttitudeType.SPIN
            or attitude_type == AttitudeType.SPIN_NUTATION
        ):
            return self._parse_spin_xml(attitude_type, state_vector)
        return self._parse_euler_xml(attitude_type, state_vector)

    def _set_metadata(self, object_name, meta):
        self.metadata[object_name] = meta

    def get_version(self):
        """Return the AEM version"""
        return self.properties["CCSDS_AEM_VERS"]

    def get_ref_frame_a(self, sat_name):
        return enumerates.AttitudeFrame(self.get_metadata_data(sat_name, "REF_FRAME_A"))

    def get_ref_frame_b(self, sat_name):
        return enumerates.AttitudeFrame(self.get_metadata_data(sat_name, "REF_FRAME_B"))

    def get_attitude_dir(self, sat_name):
        return enumerates.EulerDir(self.get_metadata_data(sat_name, "ATTITUDE_DIR"))

    def get_attitude_type(self, sat_name):
        """Get the satellite attitude information type"""
        return enumerates.AttitudeType(
            self.get_metadata_data(sat_name, "ATTITUDE_TYPE")
        )

    def get_quaternion_type(self, sat_name):
        """Get the satellite attitude quaternion type (convention: scalar in first or last position)"""
        if (
            self.get_attitude_type(sat_name) == enumerates.AttitudeType.QUATERNION
            or self.get_attitude_type(sat_name)
            == enumerates.AttitudeType.QUATERNION_DERIVATIVE
            or self.get_attitude_type(sat_name)
            == enumerates.AttitudeType.QUATERNION_RATE
        ):
            return enumerates.QuaternionConvention(
                self.get_metadata_data(sat_name, "QUATERNION_TYPE")
            )
        raise ValueError(
            "Cannot request quaternion type when attitude type if not of type QUATERNION"
        )

    def get_interpolation_method(self, sat_name):
        """Get the satellite attitude information"""
        return enumerates.InterpolationMethod(
            self.get_metadata_data(sat_name, "INTERPOLATION_METHOD").upper()
        )

    def get_interpolation_degree(self, sat_name):
        """Get the satellite attitude information"""
        return int(self.get_metadata_data(sat_name, "INTERPOLATION_DEGREE"))

    def get_euler_rotation_sequence(self, sat_name):
        seq_str = self.get_metadata_data(sat_name, "EULER_ROT_SEQ")
        return [int(c) for c in seq_str]

    def get_euler_rate_frame(self, sat_name):
        return enumerates.RateFrame(self.get_metadata_data(sat_name, "RATE_FRAME"))

    def get_attitude(self, sat_name):
        """Get the satellite attitude information"""
        try:
            return self.attitude[sat_name]
        except KeyError:
            raise exceptions.CcsdsObjectNotFoundError(
                "No object named {:s}".format(sat_name)
            )
