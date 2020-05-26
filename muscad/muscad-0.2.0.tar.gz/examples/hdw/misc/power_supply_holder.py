from muscad import Part, Volume
from muscad.vitamins.boards import Board
from muscad.vitamins.bolts import Bolt
from muscad.vitamins.extrusions import Extrusion


class PowerSupplyHolder(Part):
    z_extrusion = ~Extrusion.e3030(150).debug()
    x_extrusion = (
        ~Extrusion.e3030(50)
        .bottom_to_left()
        .align(
            left=z_extrusion.right,
            front=z_extrusion.front,
            bottom=z_extrusion.bottom,
        )
        .debug()
    )
    y_extrusion = (
        ~Extrusion.e3030(120)
        .bottom_to_front()
        .align(
            right=z_extrusion.right,
            back=z_extrusion.front,
            bottom=z_extrusion.bottom,
        )
        .debug()
    )

    board = (
        ~Board.smps300rs(bolt=Bolt.M3(20).add_nut(-1).upside_down())
        .bottom_to_left()
        .align(
            left=y_extrusion.center_x - 5,
            back=z_extrusion.front + 10,
            bottom=y_extrusion.top + 10,
        )
        .debug()
    )

    holder = (
        Volume(
            left=z_extrusion.left + 2,
            width=6,
            back=z_extrusion.front,
            front=board.front + 2,
            top=board.top + 2,
            bottom=y_extrusion.top,
        ).fillet_width()
        - Volume(
            left=z_extrusion.left,
            width=10,
            back=z_extrusion.front + 10,
            front=board.front - 10,
            top=board.top - 10,
            bottom=y_extrusion.top + 20,
        ).fillet_width()
    )

    z_bolt = (
        ~Bolt.M6(10)
        .bottom_to_front()
        .align(
            center_x=z_extrusion.center_x,
            center_y=z_extrusion.front,
            center_z=holder.top + 10,
        )
    )
    z_attach = (
        Volume(
            center_x=z_extrusion.center_x,
            width=26,
            back=z_extrusion.front,
            depth=6,
            bottom=y_extrusion.top,
            top=z_bolt.top + 5,
        )
        .fillet_depth(13, top=True)
        .fillet_width(back=True, bottom=True)
    )

    y_bolt = (
        ~Bolt.M6(10)
        .upside_down()
        .align(
            center_x=y_extrusion.center_x,
            center_y=holder.front + 10,
            center_z=y_extrusion.top,
        )
    )
    y_attach = (
        Volume(
            center_x=z_extrusion.center_x,
            width=26,
            back=z_extrusion.front,
            front=y_bolt.front + 5,
            bottom=y_extrusion.top,
            height=6,
        )
        .fillet_height(13, front=True)
        .fillet_width(back=True, bottom=True)
    )


if __name__ == "__main__":
    PowerSupplyHolder().render_to_file(openscad=False)
