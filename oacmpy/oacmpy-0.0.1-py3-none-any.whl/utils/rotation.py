from math import cos, sin, sqrt

import numpy as np

from ..ccsds.exceptions import CcsdsError


def dcm_to_quat(m):
    """Conversion of DCM to quaternion.
    The DCM performs the conversion of a vector in inertial axes to a vector in body axes
    :param m: 3x3 rotation matrix
    """
    m = np.transpose(m)
    det = np.linalg.det(m)
    # print("q*q'=", np.dot(m, np.transpose(m)))
    if np.abs(det - 1.0) > 1e-4:
        raise CcsdsError("Not a rotation matrix! det={:f}".format(det))

    trace = np.trace(m)  # 1 + 2*cos(theta)
    if trace > 0.0:
        t = trace + 1.0
        qs = t
        qx = m[1, 2] - m[2, 1]
        qy = m[2, 0] - m[0, 2]
        qz = m[0, 1] - m[1, 0]
    else:
        diag = np.diag(m)
        if (diag[0] < diag[1]) & (diag[2] < diag[1]):
            t = 1.0 - diag[0] + diag[1] - diag[2]
            qs = m[2, 0] - m[0, 2]
            qx = m[0, 1] + m[1, 0]
            qy = t
            qz = m[1, 2] + m[2, 1]
        elif diag[0] < diag[2]:
            t = 1.0 - diag[0] - diag[1] + diag[2]
            qs = m[0, 1] - m[1, 0]
            qx = m[2, 0] + m[0, 2]
            qy = m[1, 2] + m[2, 1]
            qz = t
        else:
            t = 1.0 + diag[0] - diag[1] - diag[2]
            qs = m[1, 2] - m[2, 1]
            qx = t
            qy = m[0, 1] + m[1, 0]
            qz = m[2, 0] + m[0, 2]

    q = np.array([qx, qy, qz, qs])  # Cesium convention: scalar last
    q = q * 0.5 / sqrt(t)
    return q


def rot_x(theta):
    """ Rotation matrix of angle theta around the X-axis"""
    c = cos(theta)
    s = sin(theta)
    return np.array(
        [
            [1, 0, 0],
            [0, c, -s],
            [0, s, c],
        ]
    )


def rot_y(theta):
    """Rotation matrix of angle theta around the Y-axis"""
    c = cos(theta)
    s = sin(theta)
    return np.array(
        [
            [c, 0, s],
            [0, 1, 0],
            [-s, 0, c],
        ]
    )


def rot_z(theta):
    """Rotation matrix of angle theta around the Z-axis"""
    c = cos(theta)
    s = sin(theta)
    return np.array(
        [
            [c, -s, 0],
            [s, c, 0],
            [0, 0, 1],
        ]
    )


def angles2matrix(axes, angles):
    """ Rotation angles to transformation matrix, combination of successive elementary rotations, each elementary rotation
        being described by an axis number (1=x-axis, 2=y-axis, 3=z-axis) and an angle.
        The result matrix is such that
            R(u) = M' * u

        Parameters
        naxes : Axis numbers: 1=x-axis, 2=y-axis or 3=z-axis (1xP or Px1)
        angles : Rotation angles around respective axes [rad] (PxN)
    """
    n_rotations = len(angles)
    if len(axes) != n_rotations:
        raise ValueError("axes and angles should have the same size")

    m_rot = np.eye(3, 3)
    for k in range(0, n_rotations):
        if axes[k] == 1:
            m = rot_x(angles[k])
        elif axes[k] == 2:
            m = rot_y(angles[k])
        elif axes[k] == 3:
            m = rot_z(angles[k])
        else:
            raise ValueError("wrong axis. t should be in {1, 2, 3};")
        m_rot = m @ m_rot
    return m_rot
