from muscad import Cylinder, EE, Part


class Pipe(Part):
    def __init__(self, outer, inner, h):
        super().__init__(self)
        self.outer = Cylinder(d=outer, h=h, center=True)
        self.inner = Cylinder(d=inner, h=h + EE, center=True)
