from examples.hevo import config
from muscad import E, Part, T, distance_between, Fillet, XZSurface, Volume
from muscad.vitamins.bearings import RotationBearing
from muscad.vitamins.bolts import Bolt
from muscad.vitamins.endstops import OpticalEndstop
from muscad.vitamins.extrusions import Extrusion
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

    stepper = ~StepperMotor.nema17(
        bolt=Bolt.M3(8).upside_down(), holes=[0, 1, 3]
    ).align(
        center_x=y_rod.center_x + config.Y_ROD_CENTER_TO_SHAFT_CENTER,
        back=z_extrusion.front,
        top=y_extrusion.bottom - 52,
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
        .fillet_height(r=20, back=True, right=True)
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
        ~Bolt.M6(10)
        .bottom_to_front()
        .align(
            center_x=z_extrusion.center_x,
            front=walls.front - 1,
            center_z=walls.top - 13,
        )
    )

    clamp = (
        Volume(
            left=y_rod.left - 4,
            right=y_rod.right + 4,
            back=walls.front - E,
            front=base.front - 15,
            bottom=base.bottom,
            top=y_upper_bolt.bottom - 1,
        )
        - Volume(
            width=2,
            center_x=y_rod.center_x,
            back=walls.front,
            front=base.front,
            bottom=y_rod.center_z,
            top=walls.top,
        )
        - Volume(
            left=walls.left,
            right=walls.right,
            back=walls.front,
            depth=1,
            bottom=y_rod.bottom,
            top=walls.top,
        )
    )

    clamp_bolt = (
        ~Bolt.M3(length=16)
        .add_nut(-E, angle=90, inline_clearance_size=20)
        .bottom_to_left()
        .align(
            right=clamp.right - T, center_y=clamp.center_y, bottom=y_rod.top
        )
    )

    x_lower_bolt = (
        ~Bolt.M6(10)
        .bottom_to_right()
        .align(
            right=walls.right - 1,
            center_y=z_extrusion.center_y,
            bottom=base.top + 1,
        )
    )
    x_upper_bolt = (
        ~Bolt.M6(10)
        .bottom_to_right()
        .align(
            right=walls.right - 1,
            center_y=z_extrusion.center_y,
            center_z=walls.top - 13,
        )
    )

    clamp_wall_rounding = (
        Fillet(
            distance_between(base.top, y_rod.bottom),
            radius=distance_between(clamp.right, z_extrusion.right),
        )
        .z_rotate(180)
        .align(left=clamp.right, back=walls.front, bottom=base.top)
    )

    endstop = (
        ~OpticalEndstop()
        .add_bolts(Bolt.M3(10))
        .y_rotate(180)
        .align(left=base.left, front=base.front + 1, bottom=clamp.top + 1)
        .debug()
    )

    endstop_holder = XZSurface.regular_rounded_corners(
        2,
        left=endstop.left - 1,
        right=endstop.connector.left - 1,
        bottom=endstop.bottom - 1,
        top=endstop.top + 1,
    ).linear_extrude(2, back=clamp.front + 1)

    @classmethod
    def left_side(cls):
        part = cls()
        part.file_name = "xy_stepper_mount_left"
        return part

    @classmethod
    def right_side(cls):
        part = cls().mirror(y=1)
        part.file_name = "xy_stepper_mount_right"
        return part

    def __stl__(self):
        return self.rotate(z=90)


if __name__ == "__main__":
    XYStepperMount.left_side().render_to_file(openscad=False)
