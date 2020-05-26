# inspired from https://www.thingiverse.com/thing:16627


from muscad import Cube, Cylinder, EE, Part
from muscad.vitamins.belts import GT2_2mm_profile


class Pulley(Part):
    def init(
        self,
        outer_dia,  # outer diameter of the thooted part
        height,  # height of the thooted part
    ):
        self.body = Cylinder(d=outer_dia, h=height)

    def tooth(self, profile, count):
        self.tooth = ~sum(
            profile.linear_extrude(height=self.body.height - EE)
            .align(back=self.body.back, center_z=self.body.center_z)
            .z_rotate(360 / count * i)
            for i in range(count)
        )
        return self

    def add_flange(self, diameter, height, top=True, bottom=True):
        if height > 0 and top:
            self.top_flange = Cylinder(d=diameter, h=height).align(
                center_x=self.body.center_x,
                center_y=self.body.center_y,
                bottom=self.body.top,
            )
        if height > 0 and bottom:
            self.bottom_flange = Cylinder(d=diameter, h=height).align(
                center_x=self.body.center_x,
                center_y=self.body.center_y,
                top=self.body.bottom,
            )
        return self

    def add_bolt(self, bolt, center_z=True, **kwargs):
        if center_z is True:
            self.bolt = bolt.align(center_z=self.center_z, **kwargs).misc()
        elif center_z or kwargs:
            self.bolt = bolt.align(center_z=center_z, **kwargs).misc()
        else:
            self.bolt = bolt.misc()
        return self

    def add_clearance(self, length, angle, T=0):
        self.clearance = (
            Cube(self.body.width, length, self.body.height)
            .align(
                center_x=self.body.center_x,
                back=self.body.center_y,
                center_z=self.body.center_z,
            )
            .z_rotate(angle)
            .misc()
        )
        return self

    def add_belt_clearance(self, length, angle, left=False):
        self.belt_clearance = (
            Cube(self.body.width / 2, length, self.body.height)
            .align(
                left=self.body.left if left else self.body.center_x,
                back=self.body.center_y,
                center_z=self.body.center_z,
            )
            .z_rotate(angle)
            .misc()
        )
        return self

    def add_shaft_clearance(self, d=5, lenght=20, T=0.2, **align):
        self.shaft = (
            Cylinder(d=d + 2 * T, h=lenght, center=True).align(**align).misc()
        )
        return self

    @classmethod
    def GT2(cls, tooth_count, height=6, shaft_dia=3, T=0.2):
        if tooth_count < 10:
            raise ValueError(
                "Unable to draw a GT2 pulley with less than 10 tooth"
            )
        outer_dia = tooth_outer_diameter(tooth_count, 2, 0.254)
        return cls(outer_dia, height, shaft_dia)

    @classmethod
    def placeholder(cls, diameter, height, T=0.2):
        return cls(outer_dia=diameter + 2 * T, height=height + 2 * T)


def tooth_outer_diameter(tooth_count, tooth_pitch, pitch_line_offset):
    return 2 * (
        (tooth_count * tooth_pitch) / (3.141_592_65 * 2) - pitch_line_offset
    )


if __name__ == "__main__":
    Pulley.placeholder(20, 6).tooth(GT2_2mm_profile, 20).render_to_file(
        openscad=True
    )
