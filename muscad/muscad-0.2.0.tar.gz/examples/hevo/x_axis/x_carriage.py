from examples.hevo import config
from muscad import E, Import, Part, Volume
from muscad.vitamins.bearings import LinearBearing
from muscad.vitamins.bolts import Bolt
from muscad.vitamins.extruders import E3Dv6Extruder
from muscad.vitamins.pulleys import Pulley
from muscad.vitamins.rods import Rod


class XCarriage(Part):
    x_top_rod = (
        ~Rod.d8(100)
        .bottom_to_right()
        .align(center_x=0, center_y=0, center_z=config.X_RODS_DISTANCE / 2)
        .debug()
    )
    x_bottom_rod = ~x_top_rod.mirror(z=1)

    x_bearing_top_left = (
        ~LinearBearing.LM8UU(hollow=False)
        .add_rod_clearance()
        .bottom_to_left()
        .align(
            right=x_top_rod.center_x - 2,
            center_y=x_top_rod.center_y,
            center_z=x_top_rod.center_z,
        )
        .debug()
    )
    x_bearing_top_right = (
        ~LinearBearing.LM8UU(hollow=False)
        .add_rod_clearance()
        .bottom_to_right()
        .align(
            left=x_top_rod.center_x + 2,
            center_y=x_top_rod.center_y,
            center_z=x_top_rod.center_z,
        )
        .debug()
    )
    x_bearing_bottom_left = ~x_bearing_top_left.mirror(z=1)
    x_bearing_bottom_right = ~x_bearing_top_right.mirror(z=1)

    body = (
        Volume(
            left=x_bearing_top_left.left,
            right=x_bearing_top_right.right,
            back=x_bearing_top_left.back + 3,
            front=x_bearing_top_left.front + 3,
            bottom=x_bearing_bottom_left.bottom - 3,
            top=x_bearing_top_left.top + 3,
        )
        .fillet_depth()
        .fillet_width(r=6, back=True)
    )

    top_rod_clearance = ~Volume(
        left=x_bearing_top_left.right - E,
        right=x_bearing_top_right.left + E,
        back=body.back - 1,
        front=x_bearing_top_right.center_y,
        bottom=x_top_rod.bottom,
        top=x_top_rod.top,
    )
    bottom_rod_clearance = ~top_rod_clearance.mirror(z=1)

    central_bolt = (
        ~Bolt.M3(25)
        .add_nut(-E)
        .bottom_to_back()
        .align(
            center_x=body.center_x, back=body.back - E, center_z=body.center_z
        )
        .debug()
    )

    left_top_bolt = (
        ~Bolt.M3(20)
        .add_nut(-E, inline_clearance_size=20, angle=90)
        .bottom_to_back()
        .align(
            center_x=body.left + 9,
            front=body.front,
            top=x_bearing_top_left.bottom + 1.5,
        )
    )
    left_bottom_bolt = ~left_top_bolt.z_mirror()

    right_top_bolt = ~left_top_bolt.x_mirror()
    right_bottom_bolt = ~right_top_bolt.z_mirror()

    extruder = ~E3Dv6Extruder().align(center_x=0, center_y=48, top=17).debug()

    left_top_pulley = (
        ~Pulley.placeholder(15, 9, False)
        .add_clearance(20, angle=90)
        .add_clearance(20, angle=180)
        .align(right=body.center_x - 2, center_y=x_top_rod.center_y, bottom=1)
    )

    right_top_pulley = ~left_top_pulley.x_mirror()

    left_bottom_pulley = ~left_top_pulley.z_mirror()
    right_bottom_pulley = ~left_bottom_pulley.x_mirror()

    left_pulley_shaft = (
        ~Bolt.M3(60, head=False)
        .align(
            center_x=left_top_pulley.center_x,
            center_y=left_top_pulley.center_y,
            bottom=x_bearing_bottom_left.top + 2,
        )
        .debug()
    )
    right_pulley_shaft = ~left_pulley_shaft.x_mirror()

    left_top_fixation_shaft = (
        ~Bolt.M3(15, head=False)
        .bottom_to_front()
        .align(
            center_x=body.center_x - 12,
            back=left_pulley_shaft.front + 1,
            center_z=left_top_bolt.center_z,
        )
        .debug()
    )

    left_bottom_fixation_shaft = ~left_top_fixation_shaft.z_mirror()
    right_top_fixation_shaft = ~left_top_fixation_shaft.x_mirror()
    right_bottom_fixation_shaft = ~right_top_fixation_shaft.z_mirror()

    # belt_holder_clearance = ~Volume(
    #         left=x_bearing_top_left.left - 2,
    #         right=x_bearing_top_right.right + 2,
    #         back=x_top_rod.center_y - 10,
    #         front=x_top_rod.center_y + 8,
    #         bottom=x_bearing_bottom_left.top + 5,
    #         top=left_pulley.top+T,
    # )


if __name__ == "__main__":
    (
        XCarriage().root()
        + Import("Extruder_Mount_1.0.stl")
        .bottom_to_front()
        .front_to_back()
        .forward(12)
        .up(15)
        .background()
        + Import("X_Carriage_1.0.stl").bottom_to_front().forward(12).disable()
    ).render_to_file(openscad=True)
