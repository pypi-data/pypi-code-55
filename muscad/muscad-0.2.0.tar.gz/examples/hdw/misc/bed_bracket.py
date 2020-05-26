from muscad import Circle, Hull, Part, Volume
from muscad.vitamins.bolts import Bolt
from muscad.vitamins.extrusions import Extrusion


class BedBracket(Part):
    extrusion = (
        ~Extrusion.e2020(60)
        .bottom_to_front()
        .align(left=0, center_y=0, top=0)
        .debug()
    )
    _base = (
        Volume(
            left=extrusion.left - 11,
            right=extrusion.right - 4,
            center_y=extrusion.center_y,
            depth=20,
            bottom=extrusion.top,
            height=6,
        )
        .fillet_height(r=2, right=True)
        .fillet_height(r=5, left=True)
    )

    side_bolt_holder = Volume(
        right=extrusion.left,
        width=6,
        back=_base.back,
        front=_base.front,
        bottom=extrusion.bottom + 4,
        top=extrusion.top,
    ).fillet_width(r=2, bottom=True, back=True, front=True)

    top_bolt = (
        ~Bolt.M6(10)
        .slide(x=10)
        .upside_down()
        .align(
            center_x=extrusion.center_x,
            center_y=extrusion.center_y,
            center_z=extrusion.top + 2,
        )
    )
    side_bolt = (
        ~Bolt.M6(10)
        .slide(x=10)
        .bottom_to_left()
        .align(
            center_x=extrusion.left - 2,
            center_y=extrusion.center_y,
            center_z=extrusion.center_z,
        )
    )

    clearance = ~Volume(
        left=extrusion.left - 60,
        right=extrusion.left - 6,
        back=extrusion.center_y - 6,
        front=extrusion.center_y + 6,
        bottom=extrusion.bottom,
        height=extrusion.height,
    ).fillet_height(r=2, right=True, front=True, back=True)

    def init(self, distance=12):
        bolt_holder = (
            Circle(d=10)
            .align(
                center_x=self.extrusion.left - distance,
                center_y=self.extrusion.center_y,
            )
            .linear_extrude(self._base.height)
        )
        self.base = Hull(self._base, bolt_holder).align(
            bottom=self.extrusion.top
        )
        self.bed_bolt = (
            ~Bolt.M3(40)
            .add_nut(-1)
            .upside_down()
            .align(
                center_x=bolt_holder.center_x,
                center_y=bolt_holder.center_y,
                bottom=self.extrusion.top - 2,
            )
        )
        self.reinforcement = Hull(self.base, self.side_bolt_holder)


if __name__ == "__main__":
    BedBracket().render_to_file(openscad=False)
