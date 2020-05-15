from integral_types.errors import *


class ULong:
    """
    Class: Short

    Description:
        Represents an unsigned 64-bit integer.
    """

    def __init__(self, value):
        self.value: ULong = value

        if value in range(0, 18446744073709551615):
            pass
        else:
            if value > 18446744073709551615:
                raise ValueOverflowException(f"The value supplied ({value}) is bigger than 18446744073709551615 (ULong).")
            elif value < 0:
                raise ValueUnderflowException(f"The value supplied ({value}) is smaller than 0 (ULong).")

    def __add__(self, other):
        return ULong(value=(self.value + other))

    def __sub__(self, other):
        return ULong(value=(self.value - other))

    def __mul__(self, other):
        return ULong(value=(self.value * other))

    def __floordiv__(self, other):
        return ULong(value=(self.value // other))

    def __truediv__(self, other):
        return ULong(value=(self.value / other))

    def __mod__(self, other):
        return ULong(value=(self.value % other))

    def __pow__(self, other):
        return ULong(value=(self.value ** other))

    def compare_to(self, value):
        return self.value - value

    def equals(self, value) -> bool:
        return self.value == value

    @classmethod
    def parse(cls, value: str):
        return ULong(int(value))

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
        return ULong(0)

    @property
    def max_value(self):
        return ULong(18446744073709551615)
