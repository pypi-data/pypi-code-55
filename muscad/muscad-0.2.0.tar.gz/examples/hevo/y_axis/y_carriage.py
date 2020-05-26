from examples.hevo import config
from muscad import (
    Circle,
    Cube,
    Cylinder,
    E,
    EE,
    Hull,
    T,
    distance_between,
    Part,
    YZSurface,
    Volume,
)
from muscad.vitamins.bearings import LinearBearing
from muscad.vitamins.bolts import Bolt, Nut
from muscad.vitamins.pulleys import Pulley
from muscad.vitamins.rods import Rod


class YCarriage(Part):
    y_bearing = (
        ~LinearBearing.LM12UU(hollow=False)
        .add_rod_clearance()
        .bottom_to_front()
        .align(center_x=0, center_y=0, center_z=0)
        # .z_mirror()
        # .debug()
    )

    x_rod = (
        ~Rod.d8(50)
        .bottom_to_right()
        .align(
            left=y_bearing.center_x - E,
            center_y=y_bearing.center_y,
            center_z=y_bearing.center_z + config.X_RODS_DISTANCE / 2,
        )
        .z_mirror()
        .debug()
    )

    belt_clearance_y = ~Volume(
        width=Nut.M3().width,
        left=12.5,
        depth=100,
        center_y=y_bearing.center_y,
        bottom=1,
        height=9,
    )

    bottom_pulley = (
        ~Pulley(outer_dia=20, height=11)
        .add_bolt(Bolt.M3(16))
        .add_clearance(30, angle=0)
        .add_belt_clearance(30, angle=-90)
        .align(back=-4, left=12.5, top=0)
    )

    top_pulley = (
        ~Pulley(outer_dia=20, height=11)
        .add_bolt(Bolt.M3(16).upside_down())
        .add_clearance(30, angle=180)
        .add_belt_clearance(30, angle=-90, left=True)
        .align(front=6, left=20.5, bottom=-E)
    )

    _body_square_profile = YZSurface.rounded_corners(
        tb=8,
        tf=8,
        back=y_bearing.back - 2,
        front=y_bearing.front + 2,
        bottom=x_rod.bottom - 1,
        top=0,
    )

    _body_clamps_profile = YZSurface.rounded_corners(
        tb=8,
        tf=30,
        back=y_bearing.back - 2,
        front=y_bearing.front + 2,
        bottom=x_rod.top + 3,
        top=0,
    )

    body_with_clamps = _body_clamps_profile.linear_extrude(
        left=y_bearing.center_x, distance=27
    ).z_mirror()
    body = _body_square_profile.linear_extrude(
        left=body_with_clamps.right, distance=20
    ).z_mirror()

    y_clamp_nut_top = (
        ~Bolt.M3(16)
        .add_nut(placement=-E, side_clearance_size=30, angle=90)
        .y_rotate(90)
        .align(right=10, center_y=body.front - 4.5, center_z=body.top - 4)
        .y_mirror()
    )
    clamp_clearance = (
        ~Cube(body_with_clamps.width + EE, body_with_clamps.depth, 1.5)
        .align(
            left=body_with_clamps.left - E,
            front=body_with_clamps.center_y,
            bottom=x_rod.bottom,
        )
        .z_mirror()
    )

    clamp_bolt = (
        ~Bolt.M3(12)
        .add_nut(-E, side_clearance_size=30, angle=90)
        .upside_down()
        .align(
            center_x=belt_clearance_y.center_x,
            center_y=body.back + 9,
            bottom=body.top - 4,
        )
        .z_mirror()
    )

    # bottom_clearance = ~(
    #         Cube(20, 50, 11).align(
    #                 left=bottom_belt_pulley.left,
    #                 back=bottom_belt_pulley.center_y,
    #                 top=bottom_belt_pulley.top,
    #         )
    #         + Cube(50, 8, 11).align(
    #         left=bottom_belt_pulley.center_x,
    #         back=bottom_belt_pulley.back + E,
    #         top=bottom_belt_pulley.top + E,
    #     )
    # )


class XYCarriage(Part):
    y_rod_clearance = ~Cylinder(d=16, h=80, center=True).x_rotate(90)
    y_bearing = ~LinearBearing.LM12UU().x_rotate(90)

    _body_profile = Hull(
        Circle(d=8).align(front=17, right=17),
        Circle(d=8).align(back=-17, right=17),
        Circle(d=8).align(front=17, left=-17),
        Circle(d=8).align(back=-17, left=-17),
    )
    body = (
        _body_profile.linear_extrude(45)
        .y_rotate(90)
        .align(left=0, center_y=0, center_z=0)
    )

    y_clamp_bolt_top_left = (
        ~Bolt.M3(14)
        .add_nut(placement=-E, side_clearance_size=30, angle=90)
        .y_rotate(90)
        .align(right=10, center_y=body.front - 4.5, center_z=body.top - 4)
    )
    y_clamp_bolt_top_right = (
        ~Bolt.M3(14)
        .add_nut(placement=-E, side_clearance_size=30, angle=-90)
        .y_rotate(90)
        .align(right=10, center_y=body.back + 4.5, center_z=body.top - 4)
    )
    y_clamp_bolt_bottom_left = (
        ~Bolt.M3(14)
        .add_nut(placement=-E, side_clearance_size=30, angle=90)
        .y_rotate(90)
        .align(right=10, center_y=body.front - 4.5, center_z=body.bottom + 4)
    )
    y_clamp_bolt_bottom_right = (
        ~Bolt.M3(14)
        .add_nut(placement=-E, side_clearance_size=30, angle=-90)
        .y_rotate(90)
        .align(right=10, center_y=body.back + 4.5, center_z=body.bottom + 4)
    )

    belt_clearance_y = ~Cube(Nut.M3().width, body.depth + EE, 9).align(
        left=12.5, center_y=body.center_y, bottom=1
    )

    bottom_belt_pulley = ~Cylinder(d=20, h=11).align(back=-4, left=12.5, top=0)
    bottom_clearance = ~(
        Cube(20, 50, 11).align(
            left=bottom_belt_pulley.left,
            back=bottom_belt_pulley.center_y,
            top=bottom_belt_pulley.top,
        )
        + Cube(50, 8, 11).align(
            left=bottom_belt_pulley.center_x,
            back=bottom_belt_pulley.back + E,
            top=bottom_belt_pulley.top + E,
        )
    )

    bottom_bolt = (
        ~Bolt.M3(22)
        .add_nut(placement=2.3)
        .add_nut(placement=14.3)
        .align(
            center_x=bottom_belt_pulley.center_x,
            center_y=bottom_belt_pulley.center_y,
            bottom=body.bottom + 2,
        )
    )

    top_belt_pulley = ~Cylinder(d=20, h=11).align(left=25, front=4, top=11)
    top_clearance = ~(
        Cube(50, 50, top_belt_pulley.height).align(
            left=top_belt_pulley.left,
            front=top_belt_pulley.center_y,
            top=top_belt_pulley.top,
        )
        + Cube(50, 20, 11).align(
            left=top_belt_pulley.center_x,
            front=top_belt_pulley.front,
            top=top_belt_pulley.top,
        )
    )

    top_pulley_bolt = (
        ~Bolt.M3(22, head_clearance=T)
        .add_nut(placement=14.5)
        .add_nut(placement=2.3)
        .upside_down()
        .align(
            center_x=top_belt_pulley.center_x,
            center_y=top_belt_pulley.center_y,
            top=body.top - 2,
        )
    )

    top_rod = ~Cylinder(d=8, h=50).y_rotate(90).up(22).leftward(E).debug()

    bottom_rod = ~Cylinder(d=8, h=50).y_rotate(90).down(22).leftward(E).debug()

    # clamps
    clamps = (
        Hull(
            Circle(d=20).align(right=top_rod.top + 2, center_y=body.center_y),
            Circle(d=4).align(right=top_rod.top + 2, back=body.back),
            Circle(d=20).align(
                left=bottom_rod.bottom - 2, center_y=body.center_y
            ),
            Circle(d=4).align(left=bottom_rod.bottom - 2, back=body.back),
            _body_profile,
        )
        .linear_extrude(distance_between(body.left, top_pulley_bolt.left) - 2)
        .bottom_to_left()
        .align(center_y=body.center_y, left=0)
    )

    top_clamp_clearance = ~Cube(clamps.width + EE, clamps.depth, 1.5).align(
        left=clamps.left - E, front=clamps.center_y, bottom=top_rod.bottom
    )

    bottom_clamp_clearance = ~Cube(clamps.width + EE, clamps.depth, 1.5).align(
        left=clamps.left - E, front=clamps.center_y, top=bottom_rod.top
    )

    top_clamp_bolt = (
        ~Bolt.M3(12)
        .add_nut(-E, side_clearance_size=30, angle=90)
        .upside_down()
        .align(
            center_x=belt_clearance_y.center_x,
            center_y=body.back + 9,
            bottom=top_clamp_clearance.bottom - 5,
        )
    )

    bottom_clamp_bolt = (
        ~Bolt.M3(12)
        .add_nut(-E, side_clearance_size=30, angle=-90)
        .align(
            center_x=belt_clearance_y.center_x,
            center_y=body.back + 7,
            top=bottom_clamp_clearance.top + 5,
        )
    )

    def __stl__(self):
        return self.y_rotate(90)

    @classmethod
    def left_side(cls):
        part = cls()
        part.file_name = "xy_carriage_left"
        return part


class YClamp(Part):
    body = (
        XYCarriage._body_profile.linear_extrude(12)
        .y_rotate(90)
        .align(right=0, center_y=0, center_z=0)
    )
    y_rod_clearance = XYCarriage.y_rod_clearance
    y_bearing = XYCarriage.y_bearing
    y_clamp_bolt_top_left = XYCarriage.y_clamp_bolt_top_left
    y_clamp_bolt_top_right = XYCarriage.y_clamp_bolt_top_right
    y_clamp_bolt_bottom_left = XYCarriage.y_clamp_bolt_bottom_left
    y_clamp_bolt_bottom_right = XYCarriage.y_clamp_bolt_bottom_right

    def __stl__(self):
        return self.rotate(y=-90)


if __name__ == "__main__":
    YCarriage().render_to_file(openscad=True)
    (
        XYCarriage().background()
        + YCarriage().background()
        # + Import("Y_Carriage_xDia8_LM10UU_1.0.stl").y_rotate(90).background()
        + YClamp()
    ).render_to_file(openscad=True)
    # XYCarriage().mirror(1, 0, 0).render_to_file("xy_carriage_right.scad", debug=True, openscad=False)
