import sympy as sp


class Material(object):
    def __init__(self, name, refractive_index_value=None):
        self.name = name
        self.n_symbol = sp.Symbol("n_"+name)
        self.n_value = refractive_index_value

    @property
    def substitutions(self):
        if self.n_value is None:
            return []
        else:
            return [(self.n_symbol, self.n_value)]
