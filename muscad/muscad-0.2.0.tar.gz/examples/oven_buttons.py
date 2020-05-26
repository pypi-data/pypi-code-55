from muscad import Cube, Cylinder, E, Part


class Button(Part):
    outside_diam = 5.6
    inner_diam = 4

    head = Cylinder(d=10.5, h=1.7)
    first_cylinder = Cylinder(d=outside_diam, h=14).align(
        center_x=head.center_x, center_y=head.center_y, bottom=head.top - E
    )
    bottom_throat = Cylinder(d=outside_diam, d2=inner_diam, h=2).align(
        center_x=head.center_x,
        center_y=head.center_y,
        bottom=first_cylinder.top - E,
    )
    second_cylinder = Cylinder(d=inner_diam, h=2).align(
        center_x=head.center_x,
        center_y=head.center_y,
        bottom=bottom_throat.top - E,
    )
    top_throat = Cylinder(d=inner_diam, d2=outside_diam, h=1).align(
        center_x=head.center_x,
        center_y=head.center_y,
        bottom=second_cylinder.top - E,
    )
    third_cylinder = Cylinder(d=outside_diam, h=1.4).align(
        center_x=head.center_x,
        center_y=head.center_y,
        bottom=top_throat.top - E,
    )


class OvenButtons(Part):

    button = ~Button().align(bottom=-7)
    button_holder = Cylinder(d=7.2, h=12)
    body = Cube(12, 15, 2).align(
        center_x=button_holder.center_x,
        center_y=button_holder.center_y,
        bottom=button_holder.bottom,
    )
    spacer = ~Cube(1.2, button_holder.depth, button_holder.height + 3).align(
        center_x=button_holder.center_x,
        center_y=button_holder.center_y,
        bottom=body.bottom - E,
    )


if __name__ == "__main__":
    OvenButtons().export_stl()
    # render_to_file(openscad=True)
