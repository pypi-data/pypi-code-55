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


# Z axis
ZBedMount().render_to_file()
ZBracketDownLeft().render_to_file()
ZBracketDownRight().render_to_file()
ZBracketUpLeft().render_to_file()
ZBracketUpRight().render_to_file()
ZStepperMount().render_to_file()

# Y axis
XYIdlerRight().render_to_file()
XYIdlerLeft().render_to_file()
XYStepperMountRight().render_to_file()
XYStepperMountLeft().render_to_file()
YBeltFixBack().render_to_file()
YBeltFixFront().render_to_file()
YBeltFixLeft().render_to_file()
YCarriageRight().render_to_file()
YCarriageLeft().render_to_file()
YClamp().render_to_file()


# X axis
ExtruderClamp().render_to_file()
XCarriage().render_to_file()
XAxisPulleys().render_to_file()


# misc
BedBracket().render_to_file()
BoardHolder().render_to_file()
Feet().render_to_file()
PowerPlugHolder().render_to_file()
PowerSupplyHolder().render_to_file()
CableClip().render_to_file()
ExtrusionEndcap().render_to_file()

# extruder
ExtruderStepperHolder().render_to_file()
BowdenExtruder().render_to_file()
ExtruderBracket().render_to_file()
SpoolHolder().render_to_file()

# Z axis
ZBedMount().export_stl()
ZBracketDownLeft().export_stl()
ZBracketDownRight().export_stl()
ZBracketUpLeft().export_stl()
ZBracketUpRight().export_stl()
ZStepperMount().export_stl()

# Y axis
XYIdlerLeft().export_stl()
XYIdlerRight().export_stl()
XYStepperMountRight().export_stl()
XYStepperMountLeft().export_stl()
YBeltFixBack().export_stl()
YBeltFixFront().export_stl()
YBeltFixLeft().export_stl()
YCarriageRight().export_stl()
YCarriageLeft().export_stl()
YClamp().export_stl()

# X axis
ExtruderClamp().export_stl()
XCarriage().export_stl()
XAxisPulleys().export_stl()

# misc
BedBracket().export_stl()
BoardHolder().export_stl()
Feet().export_stl()
PowerPlugHolder().export_stl()
PowerSupplyHolder().export_stl()
CableClip().export_stl()
ExtrusionEndcap().export_stl()
