from integral_types.errors import *


class Long:
    """
    Class: Long

    Description:
        Represents a signed 64-bit integer.
    """

    def __init__(self, value):
        self.value: Long = value

        if value in range(-9223372036854775808, 9223372036854775807):
            pass
        else:
            if value > 9223372036854775807:
                raise ValueOverflowException(f"The value supplied ({value}) is bigger than 9223372036854775807 (Long).")
            elif value < -9223372036854775808:
                raise ValueUnderflowException(f"The value supplied ({value}) is smaller than -9223372036854775808 (Long).")

    def __add__(self, other):
        return Long(value=(self.value + other))

    def __sub__(self, other):
        return Long(value=(self.value - other))

    def __mul__(self, other):
        return Long(value=(self.value * other))

    def __floordiv__(self, other):
        return Long(value=(self.value // other))

    def __truediv__(self, other):
        return Long(value=(self.value / other))

    def __mod__(self, other):
        return Long(value=(self.value % other))

    def __pow__(self, other):
        return Long(value=(self.value ** other))

    def compare_to(self, value):
        return self.value - value

    def equals(self, value) -> bool:
        return self.value == value

    @classmethod
    def parse(cls, value: str):
        return Long(int(value))

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
        return Long(-9223372036854775808)

    @property
    def max_value(self):
        return Long(9223372036854775807)
