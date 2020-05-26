from muscad import (
    Circle,
    Cube,
    Cylinder,
    E,
    MirroredPart,
    Square,
    Chamfer,
    Volume,
    Surface,
)
from muscad.vitamins.bearings import LinearBearing
from muscad.vitamins.bolts import Bolt
from muscad.vitamins.extrusions import Extrusion
from muscad.vitamins.rods import BrassNut, Rod, ThreadedRod


class ZBedMount(MirroredPart, x=1):

    extrusion = (
        ~Extrusion.e2020(100)
        .bottom_to_right()
        .align(left=0, back=27, bottom=0)
        .debug()
    )
    z_rod = (
        ~Rod.d12(50)
        .align(center_x=65, center_y=0, center_z=extrusion.center_z)
        .debug()
    )
    bearing = (
        ~LinearBearing.LM12UU()
        .add_rod_clearance()
        .align(center_x=65, center_y=0, center_z=extrusion.center_z)
        .debug()
    )

    left_bolt = (
        ~Bolt.M6(10)
        .bottom_to_back()
        .align(
            center_x=bearing.left - 7,
            back=extrusion.back - 10,
            center_z=extrusion.center_z,
        )
        .slide(x=-10)
        .debug()
    )
    right_bolt = (
        ~Bolt.M6(10)
        .bottom_to_back()
        .align(
            center_x=bearing.right + 7,
            back=extrusion.back - 10,
            center_z=extrusion.center_z,
        )
        .slide(x=10)
        .debug()
    )
    top_bolt = ~Bolt.M6(10).align(
        center_x=bearing.center_x,
        center_y=extrusion.center_y,
        center_z=extrusion.bottom - 2,
    )

    base = Surface.free(
        Circle(d=30).align(
            center_x=bearing.center_x, center_y=bearing.center_y
        ),
        Circle(d=8).align(right=right_bolt.right, front=extrusion.front - 2),
        Circle(d=8).align(left=left_bolt.left, front=extrusion.front - 2),
        Circle(d=8).align(right=right_bolt.right, front=extrusion.back - 2),
        Circle(d=8).align(left=left_bolt.left, front=extrusion.back - 2),
    ).z_linear_extrude(bottom=extrusion.bottom - 6, top=bearing.top - E)

    insert = ~Cube(z_rod.width + 2, 40, base.height + 2).align(
        center_x=base.center_x, front=bearing.center_y, center_z=base.center_z
    )

    _arm_profile = Surface.square(
        left=0, right=z_rod.left, back=base.back + 2, center_y=0
    )

    arm = _arm_profile.z_linear_extrude(bottom=base.bottom, distance=2)
    brass_nut_cylinder = Cylinder(d=21.8, h=9).align(bottom=arm.top - E)

    t8 = (
        ~ThreadedRod.T8(100)
        .add_brass_nut(
            BrassNut.T8(
                Bolt.M3(16).add_nut(-3, inline_clearance_size=5)
            ).align(top=1)
        )
        .align(center_x=0, center_y=0, center_z=base.bottom - 1)
        .debug()
    )

    rings = (
        (
            _arm_profile
            & sum(Circle(d=8 * i) - Circle(d=8 * i - 4) for i in range(3, 15))
            + Square(arm.width, 3).align(left=0, front=arm.front)
            + Square(arm.width, 3).align(left=0, back=arm.back)
            + Square(arm.width, 3).align(left=0, center_y=arm.center_y)
        )
        .linear_extrude(7)
        .align(bottom=arm.top - E)
    )

    tilted_clearance = ~(
        Chamfer(extrusion.width, radius=extrusion.depth)
        .bottom_to_right()
        .align(
            center_x=extrusion.center_x,
            center_y=extrusion.back,
            center_z=extrusion.top,
        )
        + Volume(
            left=extrusion.left,
            right=extrusion.right,
            back=extrusion.back,
            front=extrusion.front,
            bottom=extrusion.top - 1,
            top=base.top + 1,
        )
    )


if __name__ == "__main__":
    ZBedMount().render_to_file(openscad=False)
