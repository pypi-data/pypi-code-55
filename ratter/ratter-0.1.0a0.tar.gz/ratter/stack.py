import sympy as sp
from .symbols import LAMBDA_VAC
from functools import reduce


def fresnel_r(n1, n2):
    return (n1-n2)/(n1+n2)


def fresnel_t(n1, n2):
    return 2*n1/(n1+n2)


class Layerstack(object):
    delta = sp.IndexedBase("delta")
    r = sp.IndexedBase("r")
    t = sp.IndexedBase("t")

    def __init__(self, layers):
        self.layers = layers

    def _layercount(self):
        return len(self.layers)

    def _M_list(self, n):
        return sp.Mul(sp.Matrix([[sp.exp(-sp.I*self.delta[n]), 0],
                                 [0, sp.exp(sp.I*self.delta[n])]]) *
                      sp.Matrix([[1, self.r[n, n+1]],
                                 [self.r[n, n+1], 1]]))*1 / self.t[n, n+1]

    def transfer_matrix(self):
        """Calculates the transfer-matrix for this stack

        Returns
        -------
        expression
            the transfer matrix of the stack, possibly with free symbols
        """
        subs = self.substitutions

        def tm(i):
            return self._M_list(i).subs(subs)
        transfer_matrices = [tm(i) for i in range(0, self._layercount()-1)]

        return reduce(lambda a, b: a*b, transfer_matrices)

    @property
    def substitutions(self):
        subst = []

        N = self._layercount()

        # r and t substitutions
        for i in range(N-1):
            n1_l = self.layers[i].material.n_symbol
            n2_l = self.layers[i+1].material.n_symbol
            subst.append((self.r[i, i+1], fresnel_r(n1_l, n2_l)))
            subst.append((self.t[i, i+1], fresnel_t(n1_l, n2_l)))
        subst.append((self.r[N-1, N], 0))
        subst.append((self.t[N-1, N], 1))

        # delta and d substitutions
        for i, layer in enumerate(self.layers):
            if i == 0:
                subst.append((self.delta[i], sp.pi))
            elif i == N-1:
                subst.append((self.delta[i], 0))
            else:
                n_l = layer.material.n_symbol
                d_l = layer.thickness_symbol

                subst.append((self.delta[i], 2*sp.pi*n_l*d_l/LAMBDA_VAC))

            # n substitutions
            subst += layer.substitutions

        return subst

    def reflectance_amplitude(self):
        """(complex) amplitude of the reflectance of this stack.
        The total reflectance is calculated as the absolute value of this
        amplitude

        Returns
        -------
        expression
            Amplitude of reflectance
        """
        transm = self.transfer_matrix()
        return transm[1, 0] / transm[0, 0]

    def transmittance_amplitude(self):
        """(complex) amplitude of the transmittance of this stack.
        The total transmittance is calculated as the absolute value of this
        amplitude

        Returns
        -------
        expression
            Amplitude of transmittance
        """
        transm = self.transfer_matrix()
        return 1 / transm[0, 0]
