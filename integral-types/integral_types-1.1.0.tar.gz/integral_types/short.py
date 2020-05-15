from integral_types.errors import *


class Short:
    """
    Class: Short

    Description:
        Represents a signed 16-bit integer.
    """

    def __init__(self, value):
        self.value: Short = value

        if value in range(-32768, 32767):
            pass
        else:
            if value > 32767:
                raise ValueOverflowException(f"The value supplied ({value}) is bigger than 32767 (Short).")
            elif value < -32768:
                raise ValueUnderflowException(f"The value supplied ({value}) is smaller than -32768 (Short).")

    def __add__(self, other):
        return Short(value=(self.value + other))

    def __sub__(self, other):
        return Short(value=(self.value - other))

    def __mul__(self, other):
        return Short(value=(self.value * other))

    def __floordiv__(self, other):
        return Short(value=(self.value // other))

    def __truediv__(self, other):
        return Short(value=(self.value / other))

    def __mod__(self, other):
        return Short(value=(self.value % other))

    def __pow__(self, other):
        return Short(value=(self.value ** other))

    def compare_to(self, value):
        return self.value - value

    def equals(self, value) -> bool:
        return self.value == value

    @classmethod
    def parse(cls, value: str):
        return Short(int(value))

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
        return Short(-32768)

    @property
    def max_value(self):
        return Short(32767)
