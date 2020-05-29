import pyparcel


class Foo:
    def __init__(self, a: int = int(), b: float = float(), c: str = str()):
        self.a: int = a
        self.b: float = b
        self.c: str = c

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.a == other.a and self.b == other.b and self.c == other.c
        return False


foo: Foo = Foo(8, 5.7, "Hello World")  # Foo(int, float, str)
data: bytes = pyparcel.pack(foo)  # b'\x08\x00\x00\x00ff\xb6@\x0b\x00\x00\x00Hello World'
# ...
baz: Foo = pyparcel.unpack(data, Foo())  # foo == baz
