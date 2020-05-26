from muscad import Part, E, T, Hull, Volume
from muscad.vitamins.bearings import RotationBearing
from muscad.vitamins.bolts import Bolt
from muscad.vitamins.extrusions import Extrusion


class SpoolHolder(Part):
    LENGTH = 88

    extrusion = (
        ~Extrusion.e3030(40)
        .bottom_to_left()
        .align(center_x=0, center_y=0, center_z=0)
        .debug()
    )

    thread = (
        ~Bolt.M8(LENGTH * 0.7, head=False)
        .bottom_to_front()
        .align(
            center_x=extrusion.center_x,
            center_y=extrusion.front + LENGTH / 2,
            center_z=extrusion.top + 3,
        )
        .slide(z=8)
        .debug()
    )

    bearing_center = (
        ~RotationBearing.b608zz(T=1, hole=False)
        .bottom_to_front()
        .align(
            center_x=thread.center_x,
            center_y=thread.center_y,
            center_z=thread.center_z,
        )
        .debug()
    )

    bearing_front = (
        ~RotationBearing.b608zz(T=1, hole=False)
        .bottom_to_front()
        .align(
            center_x=thread.center_x,
            center_y=thread.center_y + LENGTH / 4,
            center_z=thread.center_z,
        )
        .debug()
    )

    bearing_back = (
        ~RotationBearing.b608zz(T=1, hole=False)
        .bottom_to_front()
        .align(
            center_x=thread.center_x,
            center_y=thread.center_y - LENGTH / 4,
            center_z=thread.center_z,
        )
        .debug()
    )

    bolt_front = (
        ~Bolt.M6(16)
        .bottom_to_front()
        .align(
            center_x=extrusion.center_x + 10,
            center_y=extrusion.front,
            center_z=extrusion.center_z,
        )
    )

    stopper_front = (
        Volume(
            center_x=thread.center_x,
            width=30,
            back=extrusion.front + LENGTH,
            depth=4,
            bottom=thread.bottom - 6,
            top=bearing_front.top + 2,
        )
        .fillet_depth(12, top=True)
        .fillet_depth(12, right=True, bottom=True)
    )

    arm = (
        Volume(
            center_x=thread.center_x,
            width=30,
            back=extrusion.front,
            front=stopper_front.back + T,
            top=thread.top + 2,
            bottom=stopper_front.bottom,
        )
        .fillet_depth(8, top=True)
        .fillet_depth(12, right=True, bottom=True)
    )

    fix = (
        Volume(
            left=arm.left,
            width=32,
            back=extrusion.back + 2,
            front=extrusion.front + 6,
            bottom=extrusion.bottom + 2,
            top=extrusion.top + 6,
        )
        .fillet_depth(4, top=True)
        .fillet_depth(8, bottom=True, right=True)
    )

    reinforcement = Hull(
        Volume(
            width=6,
            left=fix.left,
            depth=1,
            back=fix.front - E,
            height=E,
            bottom=fix.bottom,
        ),
        Volume(
            width=6,
            left=fix.left,
            depth=1,
            back=fix.front - E,
            height=E,
            top=arm.bottom + E,
        ),
        Volume(
            width=6,
            left=fix.left,
            depth=1,
            front=stopper_front.front,
            height=E,
            top=arm.bottom + E,
        ),
    )

    stopper_back = Volume(
        center_x=fix.center_x,
        width=fix.width,
        back=extrusion.front,
        depth=6,
        bottom=extrusion.top,
        top=bearing_front.top + 2,
    ).fillet_depth(12, top=True)

    bolt_top = (
        ~Bolt.M6(12)
        .upside_down()
        .align(
            center_x=fix.center_x,
            center_y=extrusion.center_y,
            center_z=extrusion.top,
        )
    )


if __name__ == "__main__":
    SpoolHolder().render_to_file(openscad=False)
