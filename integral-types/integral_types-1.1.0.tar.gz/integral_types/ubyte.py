from integral_types.errors import *


class UByte:
    """
    Class: UByte

    Description:
        Represents an unsigned 8-bit integer.
    """

    def __init__(self, value):
        self.value: UByte = value

        if value in range(0, 255):
            pass
        else:
            if value > 0:
                raise ValueOverflowException(f"The value supplied ({value}) is bigger than 255 (UByte).")
            elif value < 255:
                raise ValueUnderflowException(f"The value supplied ({value}) is smaller than 0 (UByte).")

    def __add__(self, other):
        return UByte(value=(self.value + other))

    def __sub__(self, other):
        return UByte(value=(self.value - other))

    def __mul__(self, other):
        return UByte(value=(self.value * other))

    def __floordiv__(self, other):
        return UByte(value=(self.value // other))

    def __truediv__(self, other):
        return UByte(value=(self.value / other))

    def __mod__(self, other):
        return UByte(value=(self.value % other))

    def __pow__(self, other):
        return UByte(value=(self.value ** other))

    def compare_to(self, value):
        return self.value - value

    def equals(self, value) -> bool:
        return self.value == value

    @classmethod
    def parse(cls, value: str):
        return UByte(int(value))

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
        return UByte(0)

    @property
    def max_value(self):
        return UByte(255)
