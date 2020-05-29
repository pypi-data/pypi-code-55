import sympy as sp


class Layer(object):
    def __init__(self, name, material, thickness_value=None):
        """
        A layer is specified by a material and a thickness. You can give
        the layer a name, for example "bulk" or "anti-reflection coating".

        Parameters
        ----------
        name : string
            descriptive name for the layer
        material : Material
            Material that the layer is made of
        thickness_value : float (optional)
            if the thickness of the layer is fixed, and not to be
            used as a variable, you can give the thickness here
        """
        self.name = name
        self.material = material
        self.thickness_symbol = sp.Symbol("d_"+name, real=True)
        self.thickness_value = thickness_value

    @property
    def substitutions(self):
        """List of symbol-value pairs, that are known substitutions
        to simplify the description of this layer

        Returns
        -------
        list of tuples(sympy.Symbol, value)
            a list of symbols with the values they can be replaced with
        """
        if self.thickness_value is None:
            res = []
        else:
            res = [(self.thickness_symbol, self.thickness_value)]

        return res + self.material.substitutions
