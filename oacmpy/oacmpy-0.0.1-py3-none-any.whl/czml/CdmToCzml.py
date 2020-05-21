from datetime import timedelta
from math import sqrt

import numpy as np
from czml3.properties import Orientation
from czml3.types import TimeInterval
from numpy import linalg as LA

from ..ccsds.enumerates import ConjunctionObject, ReferenceFrame
from ..frames import frames
from ..utils.rotation import dcm_to_quat
from .CzmlUtils import *


class RtnMatrix:
    """RTN to ECF transformation matrix"""

    def __init__(self, pos, vel):
        """
        :param pos: position vector in ECF (inertial or fixed)
        :param vel: velocity vector in ECF (inertial or fixed)
        """
        p = np.array(pos)
        v = np.array(vel)
        r = p / np.linalg.norm(p)
        n = np.cross(r, v)
        n = n / np.linalg.norm(n)
        t = np.cross(n, r)
        t = t / np.linalg.norm(t)
        self.mat_rtn_to_eci = np.transpose([r, t, n])
        pass

    def get_mat(self):
        return self.mat_rtn_to_eci

    def to_eci(self, v_rtn):
        return np.dot(self.mat_rtn_to_eci, v_rtn)


class Covariance:
    """Computation for the covariance ellipsoid, drawn in RTN local orbital frame (see Cdm)."""

    def __init__(self, matrix, pos_vel_frame, date, frame=ReferenceFrame.ITRF2000):
        """
        :param matrix: covariance matrix in RTN
        :param pos_vel_ecf: position-velocity vector in ECF (inertial or fixed)
        :param date: date for pos, vel
        :param frame: define the ECF frame
        """
        self.matrix = matrix

        self.pos_vel_ecf = pos_vel_frame
        if frame == ReferenceFrame.EME2000:
            byd_date = date
            self.pos_vel_ecf = frames.EME2000.transform(byd_date, pos_vel_frame, frames.ITRF)

        eigval, self.m_ell2rtn = LA.eig(np.array(self.matrix[0:3, 0:3]))
        # p_rtn is an orthogonal matrix, with det =+/- 1, and C = P*D*P'
        # We need to be sure it is actually a rotation matrix, det=1, since there exist a rotation from RTN to the
        # ellipsoid axes!
        # This can be done by swaping the first two columns
        det = np.linalg.det(self.m_ell2rtn)
        if det < 0:
            self.m_ell2rtn = np.array(
                [self.m_ell2rtn[:][1], self.m_ell2rtn[:][0], self.m_ell2rtn[:][2]]
            )
            eigval = np.array([eigval[1], eigval[0], eigval[2]])

        self.radii = np.sqrt(eigval)

        self.m_rtn2ecf = RtnMatrix(
            self.pos_vel_ecf[0:3], self.pos_vel_ecf[3:6]
        ).get_mat()

        self.q_ell2rtn = dcm_to_quat(self.m_ell2rtn)

        self.m_ell2ecf = np.dot(self.m_rtn2ecf, self.m_ell2rtn)
        self.q_ell2ecf = dcm_to_quat(self.m_ell2ecf)

    def get_axis(self):
        """Return the radii of the position covariance ellipsoid"""
        return np.array(self.radii)

    def get_orientation_quaternion_ecf(self):
        """Return the transformation quaternion from ECF to ellipsoid axes
        Quaternion convention has scalar as the last element: q = [q0 q1 q2 qs]
        """
        return self.q_ell2ecf

    def get_orientation_quaternion_rtn(self):
        """Return the transformation quaternion from RTN to ellipsoid axes
        Quaternion convention has scalar as the last element: q = [q0 q1 q2 qs]
        (Cesium convention: (x, y, z, w))
        """
        return self.q_ell2rtn

    def get_orientation_matrix(self):
        """Return the transformation matrix from ellipsoid axes frame to RTN
            u_rtn = M * u_ell
        """
        return self.m_ell2rtn

    def get_orientation_matrix_ecf(self):
        """Return the transformation matrix from ellipsoid axes frame to ECF
            u_eci = M * u_ell
        """
        return self.m_ell2ecf

    def get_transform_rtn2ecf(self):
        """Transformation matrix from RTN to ECF
            u_ecf = M * u_rtn
        """
        return self.m_rtn2ecf

    def get_position_ecf(self):
        """Get the object position in ECF"""
        return self.pos_vel_ecf[0:3]


class CdmToCzml:
    """Produce Czml data for displaying conjunction event"""

    def __init__(self, cdm):
        self.cdm = cdm
        self.primary_color = [0, 0, 255, 100]
        self.secondary_color = [255, 0, 0, 100]
        self.lead_time = timedelta(minutes=30)
        self.scale = 1.0
        pass

    def set_primary_color(self, path_color):
        self.primary_color = path_color
        pass

    def set_secondary_color(self, path_color):
        self.secondary_color = path_color
        pass

    def set_lead_time(self, t_sec: timedelta):
        """Set the lead time before TCA to start showing the ellipsoids of uncertainty"""
        self.lead_time = t_sec

    def set_scale(self, scale):
        """Set visual scale of the ellipsoid (i.e. multiply ellipsoid dimension by a scale factor).
        """
        self.scale = scale

    def _packet_ellipsoid(
        self, satellite_name, availability_interval, color, cov, sigma
    ):
        axes = list(cov.get_axis() * self.scale * sigma)
        orientation = Orientation(
            unitQuaternion=list(cov.get_orientation_quaternion_ecf())
        )
        return add_ellipsoid(
            satellite_name,
            availability_interval,
            entity_id="Satellite/"
            + satellite_name
            + "/{:.0f}s_ellipsoid".format(sigma),
            raxis=axes,
            orientation=orientation,
            outline_color=color,
        )

    def dump(self):
        tca = self.cdm.get_tca()
        start = tca.datetime - self.lead_time
        availability_interval = TimeInterval(start=start, end=tca.datetime)

        packets = []

        # draw ellipsoid for close approaches
        satellite_name = self.cdm.get_primary_satellite_name()
        cov = Covariance(
            self.cdm.get_covariance(ConjunctionObject.OBJECT1),
            self.cdm.get_state_vector(ConjunctionObject.OBJECT1),
            tca,
            self.cdm.get_coordinate_system(ConjunctionObject.OBJECT1),
        )
        packets.append(
            self._packet_ellipsoid(
                satellite_name, availability_interval, self.primary_color, cov, 1.0
            )
        )
        packets.append(
            self._packet_ellipsoid(
                satellite_name, availability_interval, self.primary_color, cov, 3.0
            )
        )

        satellite_name = self.cdm.get_secondary_satellite_name()
        cov = Covariance(
            self.cdm.get_covariance(ConjunctionObject.OBJECT2),
            self.cdm.get_state_vector(ConjunctionObject.OBJECT2),
            tca,
            self.cdm.get_coordinate_system(ConjunctionObject.OBJECT2),
        )
        packets.append(
            self._packet_ellipsoid(
                satellite_name, availability_interval, self.secondary_color, cov, 1.0
            )
        )
        packets.append(
            self._packet_ellipsoid(
                satellite_name, availability_interval, self.secondary_color, cov, 3.0
            )
        )

        return packets
