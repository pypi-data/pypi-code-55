from integral_types.errors import *


class Byte:
    """
    Class: Byte

    Description:
        Represents a signed 8-bit integer.
    """

    def __init__(self, value):
        self.value: Byte = value

        if value in range(-128, 127):
            pass
        else:
            if value > 127:
                raise ValueOverflowException(f"The value supplied ({value}) is bigger than 127 (Byte).")
            elif value < -128:
                raise ValueUnderflowException(f"The value supplied ({value}) is smaller than -128 (Byte).")

    def __add__(self, other):
        return Byte(value=(self.value + other))

    def __sub__(self, other):
        return Byte(value=(self.value - other))

    def __mul__(self, other):
        return Byte(value=(self.value * other))

    def __floordiv__(self, other):
        return Byte(value=(self.value // other))

    def __truediv__(self, other):
        return Byte(value=(self.value / other))

    def __mod__(self, other):
        return Byte(value=(self.value % other))

    def __pow__(self, other):
        return Byte(value=(self.value ** other))

    def compare_to(self, value):
        return self.value - value

    def equals(self, value) -> bool:
        return self.value == value

    @classmethod
    def parse(cls, value: str):
        return Byte(int(value))

    def to_string(self) -> str:
        return str(self.value)

    @classmethod
    def try_parse(cls, value: str, expected_output) -> bool:
        try:
            if cls.parse(value=value) == expected_output:
                return True
        except Exception as exception:
            return False

    @property
    def min_value(self):
        return Byte(-128)

    @property
    def max_value(self):
        return Byte(127)
