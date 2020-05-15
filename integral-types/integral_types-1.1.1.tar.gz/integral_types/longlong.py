from integral_types.errors import *


class LongLong:
    """
    Class: LongLong

    Description:
        Represents a signed 128-bit integer.
    """

    def __init__(self, value):
        self.value: LongLong = value

        if value in range(-170141183460469231731687303715884015728, 170141183460469231731687303715884015727):
            pass
        else:
            if value > 9223372036854775807:
                raise ValueOverflowException(f"The value supplied ({value}) is bigger than 170141183460469231731687303715884015727 (Long).")
            elif value < -9223372036854775808:
                raise ValueUnderflowException(f"The value supplied ({value}) is smaller than -170141183460469231731687303715884015728 (Long).")

    def __add__(self, other):
        return LongLong(value=(self.value + other))

    def __sub__(self, other):
        return LongLong(value=(self.value - other))

    def __mul__(self, other):
        return LongLong(value=(self.value * other))

    def __floordiv__(self, other):
        return LongLong(value=(self.value // other))

    def __truediv__(self, other):
        return LongLong(value=(self.value / other))

    def __mod__(self, other):
        return LongLong(value=(self.value % other))

    def __pow__(self, other):
        return LongLong(value=(self.value ** other))

    def compare_to(self, value):
        return self.value - value

    def equals(self, value) -> bool:
        return self.value == value

    @classmethod
    def parse(cls, value: str):
        return LongLong(int(value))

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
        return LongLong(-170141183460469231731687303715884015728)

    @property
    def max_value(self):
        return LongLong(170141183460469231731687303715884015727)
