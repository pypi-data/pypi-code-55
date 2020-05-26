import os

from examples.hdw.extruder.bowden_extruder import (
    ExtruderStepperHolder,
    BowdenExtruder,
    ExtruderBracket,
)
from examples.hdw.extruder.spool_holder import SpoolHolder
from examples.hdw.misc.bed_bracket import BedBracket
from examples.hdw.misc.board_holder import BoardHolder
from examples.hdw.misc.cable_clip import CableClip
from examples.hdw.misc.extrusion_endcap import ExtrusionEndcap
from examples.hdw.misc.feet import Feet
from examples.hdw.misc.power_plug_holder import PowerPlugHolder
from examples.hdw.misc.power_supply_holder import PowerSupplyHolder
from examples.hdw.x_axis.x_carriage import (
    ExtruderClamp,
    XCarriage,
    XAxisPulleys,
)
from examples.hdw.y_axis.xy_idler import XYIdlerRight, XYIdlerLeft
from examples.hdw.y_axis.xy_stepper_mount import (
    XYStepperMountRight,
    XYStepperMountLeft,
)
from examples.hdw.y_axis.y_carriage import (
    YBeltFixBack,
    YBeltFixFront,
    YBeltFixLeft,
    YCarriageRight,
    YCarriageLeft,
    YClamp,
)
from examples.hdw.z_axis.z_bed_mount import ZBedMount
from examples.hdw.z_axis.z_bracket_down import (
    ZBracketDownRight,
    ZBracketDownLeft,
)
from examples.hdw.z_axis.z_bracket_up import ZBracketUpLeft, ZBracketUpRight
from examples.hdw.z_axis.z_stepper_mount import ZStepperMount


def compare(part, scad_file):
    filepath = os.path.join(os.path.dirname(__file__), scad_file)
    with open(filepath, "rt") as finput:
        scad = "".join(finput.readlines())
    render = part.render()
    assert render == scad


def test_z_axis():
    compare(ZBedMount(), "z_bed_mount.scad")
    compare(ZBracketDownLeft(), "z_bracket_down_left.scad")
    compare(ZBracketDownRight(), "z_bracket_down_right.scad")
    compare(ZBracketUpLeft(), "z_bracket_up_left.scad")
    compare(ZBracketUpRight(), "z_bracket_up_right.scad")
    compare(ZStepperMount(), "z_stepper_mount.scad")


def test_y_axis():
    compare(XYIdlerRight(), "xy_idler_right.scad")
    compare(XYIdlerLeft(), "xy_idler_left.scad")
    compare(XYStepperMountRight(), "xy_stepper_mount_right.scad")
    compare(XYStepperMountLeft(), "xy_stepper_mount_left.scad")
    compare(YBeltFixBack(), "y_belt_fix_back.scad")
    compare(YBeltFixFront(), "y_belt_fix_front.scad")
    compare(YBeltFixLeft(), "y_belt_fix_left.scad")
    compare(YCarriageRight(), "y_carriage_right.scad")
    compare(YCarriageLeft(), "y_carriage_left.scad")
    compare(YClamp(), "y_clamp.scad")


def test_x_axis():
    compare(ExtruderClamp(), "extruder_clamp.scad")
    compare(XCarriage(), "x_carriage.scad")
    compare(XAxisPulleys(), "x_axis_pulleys.scad")


def test_misc():
    compare(BedBracket(), "bed_bracket.scad")
    compare(BoardHolder(), "board_holder.scad")
    compare(Feet(), "feet.scad")
    compare(PowerPlugHolder(), "power_plug_holder.scad")
    compare(PowerSupplyHolder(), "power_supply_holder.scad")
    compare(CableClip(), "cable_clip.scad")
    compare(ExtrusionEndcap(), "extrusion_endcap.scad")


def test_extruder():
    compare(ExtruderStepperHolder(), "extruder_stepper_holder.scad")
    compare(BowdenExtruder(), "bowden_extruder.scad")
    compare(ExtruderBracket(), "extruder_bracket.scad")
    compare(SpoolHolder(), "spool_holder.scad")
