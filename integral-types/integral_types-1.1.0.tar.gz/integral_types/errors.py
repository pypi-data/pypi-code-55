class NumberException(Exception):
    def __init__(self, message):
        self.message = message


class ValueOverflowException(NumberException):
    pass


class ValueUnderflowException(NumberException):
    pass
