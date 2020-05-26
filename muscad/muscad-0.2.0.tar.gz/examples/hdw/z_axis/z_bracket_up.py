from muscad import E, Part, Circle, Fillet, Surface, Volume
from muscad.vitamins.bolts import Bolt
from muscad.vitamins.extrusions import Extrusion
from muscad.vitamins.rods import Rod


class ZBracketUpLeft(Part):
    extrusion = (
        ~Extrusion.e3030(50)
        .y_rotate(90)
        .align(center_x=0, back=0, bottom=0)
        .debug()
    )
    rod = ~Rod.d12(50).align(center_x=21, center_y=-22, top=61 + E).debug()

    body = (
        Volume(
            left=rod.left - 18,
            right=rod.right - 10,
            back=extrusion.back - 6,
            front=extrusion.front - 3,
            top=rod.top - E,
            bottom=extrusion.bottom + 4,
        )
        .fillet_height(10, front=True)
        .fillet_height(4, back=True)
        .fillet_depth(4, bottom=True)
    )

    rod_holder = Surface.free(
        Circle(d=8).align(left=body.left, back=body.back),
        Circle(d=6).align(left=rod.left - 5, back=rod.back - 3),
        Circle(d=6).align(right=rod.right + 5, back=rod.back - 3),
        Circle(d=4).align(right=rod.right + 5, front=rod.front + 14),
    ).z_linear_extrude(top=body.top, distance=10)

    rod_holder_bolt = (
        ~Bolt.M3(20)
        .add_nut(-0.1, angle=90)
        .y_rotate(90)
        .align(
            right=rod_holder.right + E,
            center_y=rod.front + 5,
            center_z=rod_holder.center_z,
        )
    )
    rod_holder_clearance = ~Volume(
        center_x=rod.center_x,
        width=2,
        back=rod.front - 1,
        depth=20,
        center_z=rod_holder.center_z,
        height=rod_holder.height + 1,
    )

    top_bolt = (
        ~Bolt.M6(12)
        .upside_down()
        .align(
            center_x=body.center_x,
            center_y=extrusion.center_y,
            center_z=extrusion.top + 2,
        )
    )

    front_bolt = (
        ~Bolt.M6(12)
        .bottom_to_back()
        .align(
            center_x=body.center_x,
            center_y=extrusion.back - 2,
            center_z=extrusion.center_z,
        )
        .slide(z=-20)
    )

    rounding = (
        Fillet(rod_holder.height, 6)
        .z_rotate(180)
        .align(
            top=rod_holder.top, back=extrusion.back - 1.5, left=body.right - E
        )
    )

    def __stl__(self):
        return self.upside_down()


class ZBracketUpRight(ZBracketUpLeft):
    def __stl__(self):
        return self.mirror(y=1).upside_down()


if __name__ == "__main__":
    ZBracketUpLeft().render_to_file(openscad=True)
    ZBracketUpRight().render_to_file(openscad=True)
