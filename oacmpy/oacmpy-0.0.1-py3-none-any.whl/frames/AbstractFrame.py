import numpy as np

from ..CelestialBody import Earth
from ..errors import FrameError


class FrameTransform:
    def __init__(self, translation=None, rotation=None, omega=None):
        if translation is None:
            translation = np.array([0, 0, 0])
        self.offset = translation
        if rotation is None:
            rotation = np.eye(3, 3)
        self.rotation = rotation
        if omega is None:
            omega = np.array([0, 0, 0])
        self.omega = omega

    def compose(self, transform):
        """Compose two frame transformations"""
        translation = transform.offset + transform.rotation @ self.offset
        rotation = transform.rotation @ self.rotation
        omega = self.omega + self.rotation.transpose() @ transform.omega
        return FrameTransform(translation, rotation, omega)

    def apply(self, pv_state):
        """Apply the frame transformation to a pv-state vector"""
        pos = self.rotation @ (self.offset + pv_state[0:3])
        vel = self.rotation @ (pv_state[3:6] - np.cross(self.omega, pv_state[0:3]))
        return np.array([pos[0], pos[1], pos[2], vel[0], vel[1], vel[2]])

    def apply_inverse(self, pv_state):
        """Apply the inverse frame transformation to a pv-state vector"""
        pos = np.transpose(self.rotation) @ pv_state[0:3] - self.offset
        vel = np.transpose(self.rotation) @ pv_state[3:6] + np.cross(self.omega, pv_state[0:3])
        return np.array([pos[0], pos[1], pos[2], vel[0], vel[1], vel[2]])


class AbstractFrame:
    """Frame base class
    """

    def __init__(self, name, parent, center=Earth):
        """

        :param name:
        :param parent:
        :param center:
        """
        self.name = name
        self.parent = parent
        self.center = center
        self.eop = None

    def transform(self, date, pv_state, new_frame):
        """Change the frame of the cartesian state

        :param date date
        :param pv_state  array position, velocity at date
        :param new_frame (str)
        Return:
            numpy.ndarray with pv in new_frame
        """
        # find common ancestor frame
        frame_list1 = self.get_ancestors()
        frame_list2 = new_frame.get_ancestors()
        common_frames = list(set(frame_list1).intersection(frame_list2))
        if len(common_frames) == 0:
            raise FrameError("Cannot find a common frame")
        # take the fastest path
        idx = 0
        jdx = 0
        cost = len(frame_list1)
        for f in common_frames:
            c = frame_list1.index(f) + frame_list2.index(f)
            if c < cost:
                idx = jdx
            jdx += 1
        common_frame = common_frames[idx]

        transform_frame1_to_common = FrameTransform()
        frame = self
        while common_frame != frame:
            transform_frame1_to_common = transform_frame1_to_common.compose(
                frame.get_frame_transform(date)
            )
            frame = frame.parent

        transform_frame2_to_common = FrameTransform()
        frame = new_frame
        while common_frame != frame:
            transform_frame2_to_common = transform_frame2_to_common.compose(
                frame.get_frame_transform(date)
            )
            frame = frame.parent

        return transform_frame2_to_common.apply_inverse(
            transform_frame1_to_common.apply(pv_state)
        )

    def get_frame_transform(self, date) -> FrameTransform:
        """

        :param date:
        :return:
        """
        direct_transform = "{}_to_{}".format(self.name, self.parent.name)
        rotation, offset = getattr(self, direct_transform)(date)
        return FrameTransform(offset, rotation)

    def get_ancestors(self):
        """Get all ancestor frames"""
        frame = self
        ancestors = [frame]
        while frame:
            frame = frame.parent
            if frame:
                ancestors.append(frame)
        return ancestors
