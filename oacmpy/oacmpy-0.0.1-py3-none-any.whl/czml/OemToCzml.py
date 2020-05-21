from czml3.enums import ReferenceFrames
from czml3.types import TimeInterval

from ..ccsds.enumerates import ReferenceFrame
from .CzmlUtils import *


class ColorPalette:
    color_list = [
        [0.0, 0.5, 0.9, 0.5],  # blue
        [0.99, 0.7, 0.04, 0.5],  # amber
        [0.9, 0.3, 0.24, 0.5],  # red
        [0.2, 0.8, 0.45, 0.5],
    ]  # green

    def __init__(self):
        pass

    @staticmethod
    def set_color_list(color_list):
        ColorPalette.color_list = color_list

    @staticmethod
    def get_color_from_index(index):
        """return a color from index in a coded color palette"""
        index = index % len(ColorPalette.color_list)
        return ColorPalette.color_list[index]


def from_frame_to_cesium_frame(frame):
    """Conversion from Frames to Cesium Frames
    Cesium Frames:
        Inertial: ICRF or GCRF
        (Ellipsoid)-Fixed: ITRF
    Bias between frame transformation is not handled!
    """
    switcher = {
        ReferenceFrame.EME2000: ReferenceFrames.INERTIAL,
        ReferenceFrame.GTOD: ReferenceFrames.FIXED,
        ReferenceFrame.ITRF2000: ReferenceFrames.FIXED,
        ReferenceFrame.ITRF93: ReferenceFrames.FIXED,
        ReferenceFrame.ITRF97: ReferenceFrames.FIXED,
        ReferenceFrame.J2000: ReferenceFrames.INERTIAL,
        ReferenceFrame.TEME: ReferenceFrames.INERTIAL,
        ReferenceFrame.ICRF: ReferenceFrames.INERTIAL,
    }
    return switcher.get(frame, "Invalid frame")


class OemAemToCzml:
    color_index = 0

    def __init__(self, oem, aem=None):
        self.oem = oem
        self.aem = aem
        self.path_color = ColorPalette.get_color_from_index(OemAemToCzml.color_index)
        OemAemToCzml.color_index = OemAemToCzml.color_index + 1
        pass

    def set_color(self, path_color):
        self.path_color = path_color
        OemAemToCzml.color_index = OemAemToCzml.color_index - 1
        pass

    def dump(self):
        packets = []
        for satellite_name in self.oem.get_satellite_list():
            availability_interval = TimeInterval(
                start=self.oem.get_start_time(satellite_name).str(),
                end=self.oem.get_stop_time(satellite_name).str(),
            )
            state = self.oem.get_ephemeris(satellite_name)

            reference_frame = from_frame_to_cesium_frame(
                self.oem.get_reference_frame(satellite_name)
            )

            attitude = None
            if self.aem:
                attitude = self.aem.get_attitude(satellite_name)

            packet = add_satellite_trajectory(
                satellite_name,
                availability_interval,
                state,
                reference_frame,
                attitude=attitude,
                path_color=self.path_color,
                lead_time=6000,
                trail_time=6000,
            )
            packets.append(packet)

        return packets
