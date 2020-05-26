from muscad import Cube, Cylinder, E, EE, Part


class Fillet(Part):
    def init(self, length, radius=4):
        self.box = Cube(radius + EE, radius + EE, length).align(
            back=-E, left=-E, center_z=0
        )
        self.fillet = ~Cylinder(d=radius * 2, h=length + 2)

    @property
    def back(self):
        return 0

    @property
    def left(self):
        return 0


class Chamfer(Part):
    def init(self, length, radius=4):
        self.box = Cube(radius, radius, length).align(
            back=0, left=0, center_z=0
        )
        chamfer_width = ((radius ** 2) * 2) ** 0.5
        self.chamfer = ~Cube(
            chamfer_width, chamfer_width, length + 2
        ).z_rotate(45)
