from abc import ABC, abstractmethod
from collections import namedtuple
from dataclasses import dataclass

OperatorInfo = namedtuple("Info", ["name", "is_binary", "return_type"])


@dataclass
class AbstractOperator(ABC):

    is_binary: bool

    @abstractmethod
    def apply(self, lhs, rhs):
        pass


class GreaterThan(AbstractOperator):
    def __init__(self):
        super().__init__(True)

    def apply(self, lhs, rhs):
        return lhs > rhs


class GreaterThanEquals(AbstractOperator):
    def __init__(self):
        super().__init__(True)

    def apply(self, lhs, rhs):
        return lhs >= rhs


class LessThan(AbstractOperator):
    def __init__(self):
        super().__init__(True)

    def apply(self, lhs, rhs):
        return lhs < rhs


class LessThanEquals(AbstractOperator):
    def __init__(self):
        super().__init__(True)

    def apply(self, lhs, rhs):
        return lhs <= rhs


class Equals(AbstractOperator):
    def __init__(self):
        super().__init__(True)

    def apply(self, lhs, rhs):
        return lhs == rhs


class Between_Ends_Inclusive(AbstractOperator):
    def __init__(self):
        super().__init__(True)

    def apply(self, lhs, rhs):
        assert len(rhs) == 2
        return rhs[0] <= lhs <= rhs[1]


class Between_Ends_Exclusive(AbstractOperator):
    def __init__(self):
        super().__init__(True)

    def apply(self, lhs, rhs):
        assert len(rhs) == 2
        return rhs[0] < lhs < rhs[1]


class Invert(AbstractOperator):
    def __init__(self):
        super().__init__(False)

    def apply(self, lhs, rhs=None):
        return not lhs


class NotEquals(AbstractOperator):
    def __init__(self):
        super().__init__(False)

    def apply(self, lhs, rhs):
        return not (lhs == rhs)


class Contains(AbstractOperator):
    def __init__(self):
        super().__init__(True)

    def apply(self, lhs, rhs):
        for val in lhs:
            if val == rhs:
                return True
        return False


class In(AbstractOperator):
    def __init__(self):
        super().__init__(True)

    def apply(self, lhs, rhs):
        for val in rhs:
            if val == lhs:
                return True
        return False


class AnyIn(AbstractOperator):
    def __init__(self):
        super().__init__(True)

    def apply(self, lhs, rhs):
        for lhs_val in lhs:
            if lhs_val in rhs:
                return True
        return False
