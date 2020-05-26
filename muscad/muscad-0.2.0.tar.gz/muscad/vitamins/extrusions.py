from muscad import Circle, Hull, Part


class Extrusion(Part):
    def init(self, side, length, rounding=2):
        self.profile = Hull(
            Circle(d=rounding * 2).align(left=-side / 2, back=-side / 2),
            Circle(d=rounding * 2).align(left=-side / 2, front=side / 2),
            Circle(d=rounding * 2).align(right=side / 2, back=-side / 2),
            Circle(d=rounding * 2).align(right=side / 2, front=side / 2),
        ).linear_extrude(length)

    @classmethod
    def e3030(cls, length, rounding=2):
        return cls(30, length, rounding)

    @classmethod
    def e2020(cls, length, rounding=2):
        return cls(20, length, rounding)
