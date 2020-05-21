from ..datetime.Date import Date
from . import AbstractDataMessage, enumerates, exceptions


class Apm(AbstractDataMessage.AbstractDataMessage):
    def __init__(self, filename, fmt):
        self.attitude = {}
        self.metadata = {}
        super().__init__(fmt)
        self.open(filename, self.fmt)
        pass

    def open(self, filename, fmt):
        """Open an APM file for parsing. A dictionary is returned."""
        self.set_metadata_keys(["OBJECT_NAME", "OBJECT_ID", "TIME_SYSTEM"])
        self.metadata, _ = self.load_from_file(filename, fmt)

    def get_metadata_data(self, key, default_value=None):
        try:
            return self.metadata[key]
        except KeyError as e:
            if default_value:
                return default_value
            raise exceptions.CcsdsObjectNotFoundError("No object with name {:s} found")

    def get_coordinate_system(self):
        """Return the coordinate system of the ephemeris"""
        return self.metadata["REF_FRAME"]

    def get_time_system(self):
        """Return the time system used for the ephemeris point"""
        return self.metadata["TIME_SYSTEM"]

    def get_epoch(self):
        """Return the epoch of the attitude state"""
        return Date(self.metadata["EPOCH"])

    def get_ref_frame_a(self):
        return enumerates.AttitudeFrame(self.get_metadata_data("REF_FRAME_A"))

    def get_ref_frame_b(self):
        return enumerates.AttitudeFrame(self.get_metadata_data("REF_FRAME_B"))

    def get_attitude_dir(self):
        return enumerates.EulerDir(self.get_metadata_data("Q_DIR"))

    def get_quaternion_type(self):
        return enumerates.QuaternionConvention.LAST

    def get_quaternion(self):
        q1 = float(self.get_metadata_data("Q1"))
        q2 = float(self.get_metadata_data("Q2"))
        q3 = float(self.get_metadata_data("Q3"))
        qc = float(self.get_metadata_data("QC"))
        return [q1, q2, q3, qc]

    def get_euler_dir(self):
        return enumerates.EulerDir(self.get_metadata_data("EULER_DIR"))

    def get_euler_rotation_sequence(self):
        seq_str = self.get_metadata_data("EULER_ROT_SEQ")
        return [int(c) for c in seq_str]

    def get_euler_frame_A(self):
        return self.get_metadata_data("EULER_FRAME_A")

    def get_euler_frame_B(self):
        return self.get_metadata_data("EULER_FRAME_B")

    def get_euler_angle(self):
        rot_seq = self.get_euler_rotation_sequence()
        x_angle = float(self.get_metadata_data("X_ANGLE", 0.0))
        y_angle = float(self.get_metadata_data("Y_ANGLE", 0.0))
        z_angle = float(self.get_metadata_data("Z_ANGLE", 0.0))
        angles = [x_angle, y_angle, z_angle]
        return angles[rot_seq]

    def get_euler_rate_frame(self):
        return enumerates.RateFrame(self.get_metadata_data("RATE_FRAME"))

    def get_euler_rate(self):
        rot_seq = self.get_euler_rotation_sequence()
        z_rate = float(self.get_metadata_data("Z_RATE", 0.0))
        x_rate = float(self.get_metadata_data("X_RATE", 0.0))
        y_rate = float(self.get_metadata_data("Z_RATE", 0.0))
        rates = [x_rate, y_rate, z_rate]
        return rates[rot_seq]

    def get_maneuver_start_epoch(self):
        return self.get_metadata_data("MAN_EPOCH_START")

    def get_maneuver_duration(self):
        return self.get_metadata_data("MAN_DURATION")

    def get_maneuver_frame(self):
        return self.get_metadata_data("MAN_REF_FRAME")

    def get_maneuver_torque(self):
        return [
            self.get_metadata_data("MAN_TOR_1"),
            self.get_metadata_data("MAN_TOR_2"),
            self.get_metadata_data("MAN_TOR_3"),
        ]
