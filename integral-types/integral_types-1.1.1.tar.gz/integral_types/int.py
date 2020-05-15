from integral_types.errors import *


class Int:
    """
    Class: Int

    Description:
        Represents a signed 64-bit integer.
    """

    def __init__(self, value):
        self.value: Int = value

        if value in range(-2147483648, 2147483647):
            pass
        else:
            if value > 2147483647:
                raise ValueOverflowException(f"The value supplied ({value}) is bigger than 2147483647 (Int).")
            elif value < -2147483648:
                raise ValueUnderflowException(f"The value supplied ({value}) is smaller than -2147483648 (Int).")

    def __add__(self, other):
        return Int(value=(self.value + other))

    def __sub__(self, other):
        return Int(value=(self.value - other))

    def __mul__(self, other):
        return Int(value=(self.value * other))

    def __floordiv__(self, other):
        return Int(value=(self.value // other))

    def __truediv__(self, other):
        return Int(value=(self.value / other))

    def __mod__(self, other):
        return Int(value=(self.value % other))

    def __pow__(self, other):
        return Int(value=(self.value ** other))

    def compare_to(self, value):
        return self.value - value

    def equals(self, value) -> bool:
        return self.value == value

    @classmethod
    def parse(cls, value: str):
        return Int(int(value))

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
        return Int(-2147483648)

    @property
    def max_value(self):
        return Int(2147483647)
