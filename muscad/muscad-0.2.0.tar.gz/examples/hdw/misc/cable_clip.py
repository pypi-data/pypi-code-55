from muscad import Part, E, Volume


class CableClip(Part):
    body = (
        Volume(width=12, depth=5, back=-1.5, height=6)
        .fillet_height(1, back=True)
        .fillet_height(4, front=True)
    )

    center_clearance = ~Volume(
        center_x=body.center_x,
        width=6,
        back=0,
        front=body.front + E,
        bottom=body.bottom - E,
        top=body.top + E,
    ).fillet_height(1, back=True)

    side_clearance_right = ~Volume(
        left=4,
        width=5,
        front=2,
        back=0,
        bottom=body.bottom - E,
        top=body.top + E,
    )
    side_clearance_left = ~side_clearance_right.x_mirror()


if __name__ == "__main__":
    CableClip().render_to_file()
