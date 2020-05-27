

class PiecewiseLinearFunction:
    def __init__(self, a, b, name=None):
        self.a = a
        self.b = b
        self.name = name

    @property
    def lb(self):
        return min(self.a)

    @property
    def ub(self):
        return max(self.a)

    def __len__(self):
        return len(self.a)

    def __repr__(self):
        return "<{}({})>".format(self.__class__.__name__, self.name or "")
