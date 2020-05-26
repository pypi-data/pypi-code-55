from muscad import Part, Polygon, Square


class HeadSetHolder(Part):
    body = (
        Square(35, 45).align(right=0, center_y=0)
        - Square(35, 35).align(right=-5, center_y=0)
        + Square(45, 20).align(left=0, back=0)
        - Square(40, 20).align(back=10)
        + Polygon([0, 0], [30, 0], [0, -15])
    ).linear_extrude(30)


if __name__ == "__main__":
    HeadSetHolder().render_to_file(openscad=True)
