from RRExceptions.Exceptions import AbstractMethodException


class _BaseChecker:
    def __init__(self):
        pass

    def check(self):
        raise AbstractMethodException()




