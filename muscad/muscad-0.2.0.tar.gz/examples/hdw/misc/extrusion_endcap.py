from muscad import Part, TT, Circle, Square, Volume, Surface


class Extrusion3030Insert(Part):
    def init(self, length=50):
        self.body = Volume(width=8 - TT, depth=length, height=6).fillet_depth(
            0.5, bottom=True
        )
        self.wings = Surface.free(
            Circle(d=1.5, segments=20).align(center_x=6, back=-0.5),
            Circle(d=1.5, segments=20).align(center_x=-6, back=-0.5),
            Square(width=8, depth=1).align(center_x=0, front=3),
        ).y_linear_extrude(length)


class ExtrusionEndcap(Part):
    base = Volume(width=30, depth=30, height=6).fillet_height(4)
    x_insert = (
        Extrusion3030Insert(25)
        .front_to_right()
        .align(left=base.right, center_y=base.center_y, bottom=base.bottom)
    )
    y_insert = Extrusion3030Insert(25).align(
        center_x=base.center_x, back=base.front, bottom=base.bottom
    )
    x_insert_left = (
        Extrusion3030Insert(25)
        .back_to_top()
        .back_to_left()
        .align(left=base.left, center_y=base.center_y, bottom=base.top)
    )
    z_insert_back = (
        Extrusion3030Insert(25)
        .bottom_to_back()
        .align(center_x=base.center_x, back=base.back, bottom=base.top)
    )


if __name__ == "__main__":
    ExtrusionEndcap().render_to_file()
