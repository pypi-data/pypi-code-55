from muscad import Part, Polygon
from muscad.utils.volume import Volume

GT2_2mm_profile = Polygon(
    [0.747_183, -0.5],
    [0.747_183, 0],
    [0.647_876, 0.037_218],
    [0.598_311, 0.130_528],
    [0.578_556, 0.238_423],
    [0.547_158, 0.343_077],
    [0.504_649, 0.443_762],
    [0.451_556, 0.53975],
    [0.358_229, 0.636_924],
    [0.2484, 0.707_276],
    [0.127_259, 0.750_044],
    [0, 0.76447],
    [-0.127_259, 0.750_044],
    [-0.2484, 0.707_276],
    [-0.358_229, 0.636_924],
    [-0.451_556, 0.53975],
    [-0.504_797, 0.443_762],
    [-0.547_291, 0.343_077],
    [-0.578_605, 0.238_423],
    [-0.598_311, 0.130_528],
    [-0.648_009, 0.037_218],
    [-0.747_183, 0],
    [-0.747_183, -0.5],
)


class Belt(Part):
    def init(self, profile, length, pitch, width=6, belt_depth=1, T=0.2):
        nb_tooth = int(length / pitch)
        self.tooth = sum(
            profile.leftward(i * pitch) for i in range(nb_tooth)
        ).linear_extrude(width)
        self.belt = Volume(
            left=self.tooth.left,
            right=self.tooth.right,
            back=self.tooth.back - T,
            depth=belt_depth + 2 * T,
            bottom=self.tooth.bottom,
            top=self.tooth.top,
        )

    @classmethod
    def GT2(cls, length, width=6, scale=1.0, T=0.2):
        return cls(
            profile=GT2_2mm_profile.scale(x=scale, y=scale),
            length=length,
            pitch=2.032,
            width=width,
            belt_depth=0.7,
        )
