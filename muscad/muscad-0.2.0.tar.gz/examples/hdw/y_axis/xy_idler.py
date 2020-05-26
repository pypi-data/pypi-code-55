from examples.hdw import config
from muscad import Cylinder, E, Part, T, middle_of, Volume
from muscad.vitamins.belts import Belt
from muscad.vitamins.bolts import Bolt
from muscad.vitamins.endstops import MechanicalSwitchEndstop
from muscad.vitamins.extrusions import Extrusion
from muscad.vitamins.pulleys import Pulley
from muscad.vitamins.rods import Rod


class XYIdler(Part):
    z_extrusion = (
        ~Extrusion.e3030(120).align(left=0, front=0, center_z=0).debug()
    )
    y_extrusion = (
        ~Extrusion.e3030(100)
        .bottom_to_front()
        .align(
            center_x=z_extrusion.center_x,
            back=z_extrusion.front,
            top=z_extrusion.top,
        )
        .debug()
    )
    x_extrusion = (
        ~Extrusion.e3030(100)
        .bottom_to_right()
        .align(
            left=z_extrusion.right,
            center_y=z_extrusion.center_y,
            top=z_extrusion.top,
        )
        .debug()
    )

    y_rod = ~(
        Rod.d12(30)
        .x_rotate(90)
        .align(
            center_x=z_extrusion.center_x,
            back=z_extrusion.front - E,
            center_z=-5,
        )
        .debug()
    )

    front_top_bolt = (
        ~Bolt.M6(12)
        .bottom_to_front()
        .align(
            center_x=z_extrusion.center_x,
            back=z_extrusion.front - 6,
            center_z=y_extrusion.bottom - 13,
        )
        .debug()
    )
    front_bottom_bolt = ~front_top_bolt.z_mirror(center=y_rod.center_z)

    right_top_bolt = (
        ~Bolt.M6(12)
        .bottom_to_right()
        .align(
            left=z_extrusion.right - 8,
            center_y=z_extrusion.center_y,
            center_z=x_extrusion.bottom - 13,
        )
    )
    right_bottom_bolt = ~right_top_bolt.z_mirror(y_rod.center_z)

    inner_y_pulley = (
        ~Pulley.placeholder(18, 10.3)
        .add_clearance(10, 270)
        .add_belt_clearance(10, 270)
        .add_belt_clearance(40, 0, True)
        .add_bolt(
            Bolt.M3(20).add_nut(-E, side_clearance_size=20).upside_down()
        )
        .align(
            center_x=y_rod.center_x
            + config.Y_ROD_CENTER_TO_STEPPER_SHAFT_CENTER
            + 10,
            center_y=z_extrusion.front,
            bottom=y_rod.center_z + config.Y_PULLEYS_Z_OFFSET,
        )
    )

    body = (
        Volume(
            left=z_extrusion.left + 2,
            right=z_extrusion.right + 6,
            back=z_extrusion.back + 2,
            front=z_extrusion.front + 14,
            top=y_extrusion.bottom - T,
            center_z=y_rod.center_z,
        )
        .fillet_height(r=2, right=True)
        .fillet_width(back=True)
        .fillet_depth(left=True)
    )

    pulleys_holder = Volume(
        left=z_extrusion.right,
        right=inner_y_pulley.right,
        back=body.back,
        front=body.front,
        bottom=right_bottom_bolt.top,
        top=right_top_bolt.bottom,
    ).fillet_depth(right=True)

    clamp_clearance = ~(
        Volume(
            width=1,
            center_x=y_rod.center_x,
            back=body.back - E,
            front=body.front + E,
            bottom=y_rod.center_z,
            top=front_top_bolt.bottom - 1,
        )
        + Volume(
            right=y_rod.center_x,
            left=body.left - E,
            back=body.back - E,
            front=body.front + E,
            height=1,
            top=front_top_bolt.bottom - 1,
        )
    )

    tightening_bolt = (
        ~Bolt.M3(16)
        .add_nut(-0.1, side_clearance_size=20, angle=90)
        .bottom_to_left()
        .align(
            left=body.left + 3,
            center_y=middle_of(body.front, z_extrusion.front),
            center_z=(front_top_bolt.center_z + y_rod.center_z) / 2 - 1,
        )
    )

    endstop = (
        ~MechanicalSwitchEndstop(10)
        .add_bolts(Cylinder(12, 1))
        .align(
            left=body.right + E,
            front=body.front + E,
            top=pulleys_holder.bottom - E,
        )
    )

    def __stl__(self):
        return self.front_to_bottom()


class XYIdlerRight(XYIdler):
    outer_x_pulley = (
        ~Pulley.placeholder(18, 10.3)
        .add_clearance(20, 180)
        .add_belt_clearance(40, 0, True)
        .add_belt_clearance(40, 270)
        .align(
            center_x=XYIdler.y_rod.center_x
            + config.Y_ROD_CENTER_TO_STEPPER_SHAFT_CENTER,
            center_y=XYIdler.z_extrusion.center_y + config.BACK_BELT_Y_OFFSET,
            top=XYIdler.y_rod.center_z + config.X_PULLEYS_Z_OFFSET,
        )
    )

    inner_x_belt = (
        ~Belt.GT2(42, 15, scale=1.1)
        .front_to_left()
        .align(
            center_x=XYIdler.inner_y_pulley.center_x - 5,
            back=outer_x_pulley.front,
            top=XYIdler.y_rod.center_z + config.X_PULLEYS_Z_OFFSET - 1,
        )
        .debug()
    )

    outer_y_pulley = (
        ~Pulley.placeholder(18, 10.3)
        .add_clearance(20, 180)
        .add_belt_clearance(40, 0, True)
        .add_belt_clearance(70, 270)
        .add_bolt(
            Bolt.M3(35)
            .add_nut(29)
            .upside_down()
            .align(top=XYIdler.pulleys_holder.top),
            center_z=False,
        )
        .align(
            center_x=XYIdler.y_rod.center_x
            + config.Y_ROD_CENTER_TO_STEPPER_SHAFT_CENTER,
            center_y=XYIdler.z_extrusion.center_y + config.BACK_BELT_Y_OFFSET,
            bottom=XYIdler.y_rod.center_z + config.Y_PULLEYS_Z_OFFSET,
        )
    )


class XYIdlerLeft(XYIdler):
    outer_y_pulley = (
        ~Pulley.placeholder(18, 10.3)
        .add_clearance(20, 180)
        .add_belt_clearance(40, 0, True)
        .add_belt_clearance(70, 270)
        .add_bolt(
            Bolt.M3(20)
            .add_nut(-0.6, side_clearance_size=30)
            .upside_down()
            .align(top=XYIdler.pulleys_holder.top),
            center_z=False,
        )
        .align(
            center_x=XYIdler.y_rod.center_x
            + config.Y_ROD_CENTER_TO_STEPPER_SHAFT_CENTER,
            center_y=XYIdler.z_extrusion.center_y + config.BACK_BELT_Y_OFFSET,
            bottom=XYIdler.y_rod.center_z + config.Y_PULLEYS_Z_OFFSET,
        )
    )

    x_pulley = (
        ~Pulley.placeholder(18, 10.3)
        .add_clearance(10, 270)
        .add_belt_clearance(10, 270)
        .add_belt_clearance(40, 0, True)
        .add_bolt(Bolt.M3(20).add_nut(-0.3))
        .align(
            center_x=outer_y_pulley.center_x + 10,
            center_y=XYIdler.z_extrusion.center_y + config.BACK_BELT_Y_OFFSET,
            top=XYIdler.y_rod.center_z + config.X_PULLEYS_Z_OFFSET - 1,
        )
    )

    def __stl__(self):
        return self.y_mirror().back_to_bottom()


if __name__ == "__main__":
    XYIdlerRight().render_to_file(openscad=False)
    XYIdlerLeft().render_to_file(openscad=False)
