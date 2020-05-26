from muscad import Part, T, E, Text, Volume
from muscad.vitamins.boards import Board
from muscad.vitamins.bolts import Bolt
from muscad.vitamins.brackets import CastBracket
from muscad.vitamins.extrusions import Extrusion


class BoardHolder(Part):
    z_extrusion = ~Extrusion.e3030(80).debug()
    x_extrusion = (
        ~Extrusion.e3030(150)
        .bottom_to_left()
        .align(
            right=z_extrusion.left,
            front=z_extrusion.front,
            bottom=z_extrusion.bottom,
        )
        .debug()
    )
    y_extrusion = (
        ~Extrusion.e3030(150)
        .bottom_to_front()
        .align(
            right=z_extrusion.right,
            back=z_extrusion.front,
            bottom=z_extrusion.bottom,
        )
        .debug()
    )

    bracket = (
        ~CastBracket.bracket3030()
        .z_rotate(90)
        .align(
            right=y_extrusion.left,
            back=x_extrusion.front,
            center_z=y_extrusion.center_z,
        )
        .debug()
    )

    board = (
        ~Board.mks_sbase(bolt=Bolt.M3(20).add_nut(-1).upside_down())
        .align(
            right=y_extrusion.center_x + 4,
            back=z_extrusion.front + 4,
            bottom=y_extrusion.top + 8,
        )
        .debug()
    )

    right_bolt = (
        ~Bolt.M6(10)
        .upside_down()
        .align(
            center_x=y_extrusion.center_x,
            center_y=board.front + 10,
            center_z=y_extrusion.top,
        )
    )

    y_holder = (
        Volume(
            left=y_extrusion.left + 2,
            right=y_extrusion.right - 2,
            back=z_extrusion.front + T,
            front=right_bolt.front + 10,
            bottom=y_extrusion.top,
            height=6,
        )
        .fillet_height(13, front=True)
        .fillet_height(2, right=True, back=True)
    )

    left_holder = (
        Volume(
            center_x=board.left + 4,
            width=y_extrusion.width - 4,
            back=x_extrusion.back + 2,
            front=board.front + 10,
            bottom=x_extrusion.top,
            height=6,
        )
        .fillet_height(13, front=True)
        .fillet_height(13, back=True, left=True)
    )

    x_holder = Volume(
        left=left_holder.right - E,
        right=z_extrusion.left - T,
        back=x_extrusion.back + 2,
        front=x_extrusion.front - 2,
        bottom=x_extrusion.top,
        height=6,
    ).fillet_height(2, right=True, back=True)

    bolt_left_back = (
        ~Bolt.M6(10)
        .upside_down()
        .align(
            center_x=left_holder.center_x,
            center_y=x_extrusion.center_y,
            center_z=x_extrusion.top,
        )
    )
    bolt_right_back = (
        ~Bolt.M6(10)
        .upside_down()
        .align(
            center_x=z_extrusion.left - 10,
            center_y=x_extrusion.center_y,
            center_z=x_extrusion.top,
        )
    )

    bracket_hider = Volume(
        left=bracket.left,
        right=y_holder.left,
        back=x_holder.front,
        front=bracket.front,
        bottom=x_holder.bottom,
        top=x_holder.top,
    ).fillet_height(30, front=True, left=True)

    brand = (
        ~Text("Hypercube DWG", font="Fira code", size=8)
        .linear_extrude(6)
        .align(
            left=x_holder.left, back=x_holder.back + 6, bottom=x_holder.top - 1
        )
    )


if __name__ == "__main__":
    BoardHolder().render_to_file(openscad=False)
