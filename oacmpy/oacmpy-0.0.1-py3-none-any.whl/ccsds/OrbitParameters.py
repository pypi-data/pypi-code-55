import numpy as np

from . import enumerates
from .CommonOrbitData import covariance_keys


class OrbitParameters:
    """This class is common to Opm and Omm, where there is a single object only"""

    def __init__(self):
        pass

    def get_object_name(self):
        return self.metadata["OBJECT_NAME"]

    def get_object_id(self):
        return self.metadata["OBJECT_ID"]

    def get_center_name(self):
        return self.metadata["CENTER_NAME"]

    def get_reference_frame(self):
        """Return the coordinate system of the ephemeris"""
        return enumerates.ReferenceFrame(self.metadata["REF_FRAME"])

    def get_time_system(self):
        """Return the time system used for the ephemeris point"""
        return enumerates.TimeSystem(self.metadata["TIME_SYSTEM"])

    def get_state_elements(self):
        return self.state_elements[self.get_object_name()][0]

    def get_epoch(self):
        """Return the start epoch of the ephemeris"""
        return self.get_state_elements()[0]

    def get_mean_motion(self):
        return float(self.get_state_elements()[1]["MEAN_MOTION"])

    def get_eccentricity(self):
        return float(self.get_state_elements()[1]["ECCENTRICITY"])

    def get_inclination(self):
        return float(self.get_state_elements()[1]["INCLINATION"])

    def get_raan(self):
        return float(self.get_state_elements()[1]["RA_OF_ASC_NODE"])

    def get_arg_of_pericenter(self):
        return float(self.get_state_elements()[1]["ARG_OF_PERICENTER"])

    def get_mean_anomaly(self):
        return float(self.get_state_elements()[1]["MEAN_ANOMALY"])

    def get_GM(self):
        return float(self.get_state_elements()[1]["GM"])

    def get_spacecraft_parameters(self):
        """Return spacecraft parameters"""
        return self.spacecraft_parameters

    def get_covariance_frame(self):
        """Return the orbit covariance reference frame"""
        return enumerates.ReferenceFrame(self.properties["COV_REF_FRAME"])

    def get_covariance(self):
        """Return the orbit covariance at epoch in the reference frame returned by get_reference_frame"""
        return self.covariance[self.get_object_name()]["matrix"][0]["matrix"]
