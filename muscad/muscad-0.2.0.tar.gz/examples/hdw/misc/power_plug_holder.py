from muscad import Part, T, E, Volume
from muscad.vitamins.bolts import Bolt
from muscad.vitamins.extrusions import Extrusion


class PowerPlugHolder(Part):
    z_extrusion = ~Extrusion.e3030(100).debug()
    x_extrusion = (
        ~Extrusion.e3030(80)
        .bottom_to_left()
        .align(bottom=z_extrusion.bottom, right=z_extrusion.left)
        .debug()
    )

    holder = Volume(
        right=z_extrusion.left - T,
        width=60,
        back=x_extrusion.back + 2,
        front=x_extrusion.front - 2,
        bottom=x_extrusion.top + T,
        height=50,
    ).fillet_depth(3, left=True, top=True)

    hollow = (
        ~Volume(
            center_x=holder.center_x,
            center_y=holder.center_y,
            center_z=holder.center_z,
            width=48,
            depth=z_extrusion.depth,
            height=28,
        )
        .chamfer_depth(3, right=True)
        .fillet_depth(1, left=True)
        .debug()
    )

    fixation_bolt_left = (
        ~Bolt.M6(10)
        .upside_down()
        .align(
            center_x=holder.left - 8,
            center_y=x_extrusion.center_y,
            center_z=x_extrusion.top,
        )
        .debug()
    )
    fixation_bolt_top = (
        ~Bolt.M6(10)
        .bottom_to_left()
        .align(
            center_x=z_extrusion.left,
            center_y=z_extrusion.center_y,
            center_z=holder.top + 8,
        )
        .debug()
    )

    fixation_left = Volume(
        right=holder.left - E,
        width=15,
        center_y=z_extrusion.center_y,
        depth=holder.depth,
        bottom=x_extrusion.top,
        height=4,
    ).fillet_height(9, left=True)
    fixation_top = Volume(
        right=z_extrusion.left,
        width=4,
        center_y=z_extrusion.center_y,
        depth=holder.depth,
        bottom=holder.top - E,
        height=15,
    ).fillet_width(9, top=True)


if __name__ == "__main__":
    PowerPlugHolder().render_to_file(openscad=False)
