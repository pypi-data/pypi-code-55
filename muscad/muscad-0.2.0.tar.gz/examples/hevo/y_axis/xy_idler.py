from muscad import Cylinder, E, Part, T, Volume
from muscad.vitamins.bolts import Bolt
from muscad.vitamins.extrusions import Extrusion
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
            center_x=z_extrusion.center_x, back=z_extrusion.front, center_z=-5
        )
        .debug()
    )

    top_bolt = (
        ~Bolt.M6(10)
        .bottom_to_front()
        .align(
            center_x=z_extrusion.center_x,
            front=z_extrusion.front + 4,
            center_z=y_extrusion.bottom - 13,
        )
        .debug()
    )
    bottom_bolt = (
        ~Bolt.M6(10)
        .bottom_to_front()
        .align(
            center_x=z_extrusion.center_x,
            front=z_extrusion.front + 4,
            center_z=top_bolt.center_z - 45,
        )
        .debug()
    )

    shaft = (
        ~Bolt.M3(40)
        .add_nut(-0.1, inline_clearance_size=20)
        .align(
            center_x=z_extrusion.right + 7,
            center_y=z_extrusion.front + 6,
            center_z=y_rod.center_z + 1,
        )
    )

    pulleys_holder = Volume(
        left=z_extrusion.center_x,
        right=z_extrusion.right + 15,
        back=z_extrusion.front,
        front=z_extrusion.front + 14,
        center_z=y_rod.center_z,
        height=41,
    ).fillet_height(r=6, right=True)

    top_pulley = ~Cylinder(d=24, h=10.5).align(
        center_x=shaft.center_x,
        center_y=shaft.center_y,
        center_z=y_rod.center_z + 6,
    )
    bottom_pulley = ~Cylinder(d=24, h=10.5).align(
        center_x=shaft.center_x,
        center_y=shaft.center_y,
        center_z=y_rod.center_z - 6,
    )

    body = Volume(
        left=z_extrusion.left + 2,
        right=z_extrusion.right - 2,
        bottom=bottom_bolt.bottom - 3,
        top=y_extrusion.bottom - T,
        back=z_extrusion.front,
        depth=pulleys_holder.depth,
    ).fillet_depth(r=5)

    clamp_clearance = ~(
        Volume(
            width=0.4,
            center_x=y_rod.center_x,
            back=body.back - E,
            front=body.front + E,
            bottom=y_rod.center_z,
            top=top_bolt.bottom - 1,
        )
        + Volume(
            right=y_rod.center_x,
            left=body.left - E,
            back=body.back - E,
            front=body.front + E,
            height=1,
            top=top_bolt.bottom - 1,
        )
    )

    tightening_bolt = (
        ~Bolt.M3(16)
        .add_nut(-0.1, side_clearance_size=20, angle=90)
        .bottom_to_left()
        .align(
            right=body.right - 6,
            center_y=body.center_y,
            center_z=(top_bolt.center_z + y_rod.center_z) / 2 - 1,
        )
    )

    bottom_clearance = (
        ~Cylinder(d=20, h=body.width + 2)
        .bottom_to_right()
        .align(
            center_x=body.center_x,
            back=bottom_bolt.front,
            top=pulleys_holder.bottom,
        )
    )

    top_clearance = (
        ~Cylinder(d=20, h=body.width + 2)
        .bottom_to_right()
        .align(
            center_x=body.center_x,
            back=top_bolt.front,
            bottom=pulleys_holder.top,
        )
    )

    def __stl__(self):
        return self.bottom_to_front()

    @classmethod
    def right_side(cls):
        part = cls()
        part.file_name = "xy_idler_right"
        return part

    @classmethod
    def left_side(cls):
        part = cls()
        part.file_name = "xy_idler_left"
        return part.mirror(y=1)


if __name__ == "__main__":
    XYIdler.left_side().render_to_file(openscad=False)
