from muscad import Cube, E, Part, Circle, Surface, Volume
from muscad.vitamins.bolts import Bolt
from muscad.vitamins.extrusions import Extrusion
from muscad.vitamins.rods import Rod


class ZBracketDownLeft(Part):
    extrusion = (
        ~Extrusion.e3030(50)
        .y_rotate(90)
        .align(center_x=0, back=0, bottom=0)
        .debug()
    )
    rod = ~Rod.d12(50).align(center_x=0, center_y=-22, bottom=-8 - E).debug()

    body = (
        Volume(
            left=rod.left - 18,
            right=rod.right - 10,
            back=extrusion.back - 6,
            front=extrusion.front - 3,
            bottom=rod.bottom + E,
            top=extrusion.top - 4,
        )
        .fillet_depth(4, top=True)
        .fillet_height(6, front=True)
        .fillet_height(4, left=True, back=True)
    )

    rod_holder = Surface.free(
        Circle(d=8).align(left=body.left, back=body.back),
        Circle(d=6).align(left=rod.left - 3, back=rod.back - 3),
        Circle(d=6).align(right=rod.right + 5, back=rod.back - 3),
        Circle(d=4).align(right=rod.right + 5, front=rod.front + 13),
    ).z_linear_extrude(bottom=body.bottom, distance=15)

    rod_holder_bolt = (
        ~Bolt.M3(20)
        .add_nut(-0.1, angle=90, inline_clearance_size=20)
        .y_rotate(90)
        .align(
            right=rod_holder.right,
            center_y=rod.front + 5,
            center_z=rod_holder.center_z,
        )
    )
    rod_holder_clearance = ~Cube(2, 20, rod_holder.height + 1).align(
        center_x=rod.center_x, back=rod.front - 1, center_z=rod_holder.center_z
    )

    bottom_bolt = ~Bolt.M6(10).align(
        center_x=body.center_x,
        center_y=extrusion.center_y,
        center_z=extrusion.bottom - 2,
    )

    front_bolt = (
        ~Bolt.M6(10)
        .slide(x=-20)
        .x_rotate(-90)
        .align(
            center_x=body.center_x,
            center_y=extrusion.back - 2,
            center_z=extrusion.center_z,
        )
    )


class ZBracketDownRight(ZBracketDownLeft):
    def __stl__(self):
        return self.y_mirror()


if __name__ == "__main__":
    ZBracketDownLeft().render_to_file(openscad=True)
    ZBracketDownRight().render_to_file(openscad=False)
