from examples.hdw import config
from muscad import Cylinder, E, Part, T, Volume
from muscad.vitamins.bearings import RotationBearing
from muscad.vitamins.belts import Belt
from muscad.vitamins.bolts import Bolt
from muscad.vitamins.endstops import MechanicalSwitchEndstop
from muscad.vitamins.extrusions import Extrusion
from muscad.vitamins.pulleys import Pulley
from muscad.vitamins.rods import Rod
from muscad.vitamins.steppers import StepperMotor


class XYStepperMount(Part):
    z_extrusion = (
        ~Extrusion.e3030(100).align(left=0, back=0, center_z=20).debug()
    )
    x_extrusion = (
        ~Extrusion.e3030(50)
        .bottom_to_right()
        .align(
            left=z_extrusion.right,
            center_y=z_extrusion.center_y,
            top=z_extrusion.top,
        )
        .debug()
    )
    y_extrusion = (
        ~Extrusion.e3030(50)
        .bottom_to_front()
        .align(
            center_x=z_extrusion.center_x,
            back=z_extrusion.front,
            top=z_extrusion.top,
        )
        .debug()
    )

    y_rod = (
        ~Rod.d12(50)
        .bottom_to_front()
        .align(
            center_x=z_extrusion.center_x,
            back=z_extrusion.front - E,
            center_z=y_extrusion.bottom
            - config.Y_ROD_CENTER_TO_TOP_EXTRUSION_BOTTOM,
        )
        .debug()
    )

    stepper = (
        ~StepperMotor.nema17(bolt=Bolt.M3(8).upside_down(), holes=[0, 1, 3])
        .align(
            center_x=y_rod.center_x
            + config.Y_ROD_CENTER_TO_STEPPER_SHAFT_CENTER,
            back=z_extrusion.back + 2,
            top=y_extrusion.bottom - 55,
        )
        .debug()
    )

    base = (
        Volume(
            left=z_extrusion.left + 2,
            right=stepper.right,
            back=z_extrusion.back + 2,
            front=stepper.front,
            bottom=stepper.top + E,
            height=8,
        )
        .fillet_height(r=5, front=True)
        .fillet_height(r=5, back=True, right=True)
    )

    walls = Volume(
        left=base.left,
        right=z_extrusion.right + 6,
        back=base.back,
        front=z_extrusion.front + 6,
        bottom=base.bottom,
        top=y_extrusion.bottom,
    ).fillet_height(r=3)

    shaft_bearing = ~RotationBearing.b605zz().align(
        center_x=stepper.center_x, center_y=stepper.center_y, top=base.top + E
    )

    y_upper_bolt = (
        ~Bolt.M6(8)
        .bottom_to_front()
        .align(
            center_x=z_extrusion.center_x,
            back=z_extrusion.front - 4,
            center_z=walls.top - 13,
        )
    )

    clamp = Volume(
        left=walls.left,
        center_x=y_rod.center_x,
        back=z_extrusion.front - E,
        front=base.front,
        bottom=base.bottom,
        top=y_upper_bolt.bottom - 2,
    )

    clamp_clearance = ~(
        Volume(
            width=1,
            center_x=y_rod.center_x,
            back=z_extrusion.front - E,
            front=base.front + E,
            bottom=y_rod.center_z,
            top=clamp.top + 1,
        )
        + Volume(
            left=walls.left - E,
            right=y_rod.center_x,
            back=z_extrusion.front - E,
            front=clamp.front + E,
            bottom=clamp.top,
            height=1,
        )
    )

    clamp_bolt = (
        ~Bolt.M3(length=20)
        .add_nut(-E, inline_clearance_size=10)
        .bottom_to_left()
        .align(
            right=clamp.right - T, center_y=clamp.front - 5, bottom=y_rod.top
        )
    )

    x_lower_bolt = (
        ~Bolt.M6(8)
        .bottom_to_right()
        .align(
            left=z_extrusion.right - 4,
            center_y=z_extrusion.center_y,
            bottom=base.top + 1,
        )
    )
    x_upper_bolt = (
        ~Bolt.M6(8)
        .bottom_to_right()
        .align(
            left=z_extrusion.right - 4,
            center_y=z_extrusion.center_y,
            center_z=walls.top - 13,
        )
    )

    inner_y_pulley = ~Pulley.placeholder(13, 10.3).align(
        center_x=stepper.center_x,
        front=base.front,
        bottom=y_rod.center_z + config.Y_PULLEYS_Z_OFFSET,
    )

    endstop = (
        ~MechanicalSwitchEndstop()
        .add_bolts(Cylinder(10, 1))
        .align(
            right=stepper.left - E, front=base.front + E, top=base.bottom - E
        )
    )


class XYStepperMountLeft(XYStepperMount):

    x_belt_holder = Volume(
        center_x=XYStepperMount.stepper.center_x,
        width=20,
        back=XYStepperMount.stepper.center_y + 8,
        front=XYStepperMount.base.front,
        bottom=XYStepperMount.base.top,
        height=10,
    ).fillet_height()

    x_belt = ~(
        Belt.GT2(60, 15, scale=1.1)
        .front_to_right()
        .align(
            center_x=XYStepperMount.inner_y_pulley.center_x + 5,
            back=XYStepperMount.base.back - 1,
            bottom=XYStepperMount.base.top + T,
        )
        + Belt.GT2(60, 15, scale=1.1)
        .front_to_left()
        .align(
            center_x=XYStepperMount.inner_y_pulley.center_x - 5,
            back=XYStepperMount.base.back - 1,
            bottom=XYStepperMount.base.top + T,
        )
        + Volume(
            center_x=x_belt_holder.center_x,
            width=10,
            back=x_belt_holder.back - E,
            depth=2,
            bottom=XYStepperMount.base.top,
            height=15,
        )
    )


class XYStepperMountRight(XYStepperMount):

    x_inner_belt_clearance = ~Volume(
        width=5,
        depth=15,
        height=10,
        center_x=XYStepperMount.inner_y_pulley.center_x + 5,
        front=XYStepperMount.base.front + 1,
        bottom=XYStepperMount.base.top + T,
    )
    x_outer_belt_clearance = ~Volume(
        width=5,
        depth=15,
        height=10,
        center_x=XYStepperMount.inner_y_pulley.center_x - 5,
        front=XYStepperMount.base.front + 1,
        bottom=XYStepperMount.base.top + T,
    )
    pulleys_box = Volume(
        left=XYStepperMount.inner_y_pulley.left - 5,
        right=XYStepperMount.inner_y_pulley.right + 5,
        back=XYStepperMount.inner_y_pulley.back,
        front=XYStepperMount.base.front,
        bottom=XYStepperMount.base.top - E,
        top=XYStepperMount.inner_y_pulley.top + 6,
    ).fillet_height() - Volume(
        left=XYStepperMount.inner_y_pulley.left - 1,
        right=XYStepperMount.inner_y_pulley.right + 1,
        back=XYStepperMount.inner_y_pulley.back - 1,
        front=XYStepperMount.inner_y_pulley.front + 1,
        bottom=XYStepperMount.base.top + 10,
        top=XYStepperMount.inner_y_pulley.top + 0.3,
    )

    inner_shaft = (
        ~Bolt.M3(35)
        .add_nut(-E, angle=90)
        .upside_down()
        .align(
            center_x=XYStepperMount.inner_y_pulley.center_x,
            center_y=XYStepperMount.inner_y_pulley.center_y,
            bottom=XYStepperMount.base.bottom,
        )
    )

    def __stl__(self):
        return self.y_mirror()


if __name__ == "__main__":
    XYStepperMountLeft().render_to_file(openscad=False)
    XYStepperMountRight().render_to_file(openscad=False)
