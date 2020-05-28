from pyparcel import Long, UnsignedLongLong, Double


class Foo:
    def __init__(self, a: int, b: int, c: int, d: long):
        self.a = a
        self.b = Long(b)
        self.c = UnsignedLongLong(c)
        self.d = Double(d)
