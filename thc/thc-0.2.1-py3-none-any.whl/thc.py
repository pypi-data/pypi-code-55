###
### Trustable Homomorphic Computation
###

class THC:

    def __init__ (self, hc, comp, modext_param):
        self._hc = hc
        self._comp = comp
        self._N = hc.get_modulus()
        self._r = modext_param
        self._Nr = self._N * self._r

    def compute (self, args):
        enc_Nr = [self._hc.mod(self._hc.encrypt(a), self._Nr) for a in args]
        enc_r = [self._hc.mod(c, self._r) for c in enc_Nr]
        result_Nr = self._comp.remote(self._Nr, enc_Nr)
        result_r = self._comp.local(self._r, enc_r)
        return self.verify(result_Nr, result_r)

    def verify (self, result_Nr, result_r):
        if result_r == self._hc.mod(result_Nr, self._r):
            return self._hc.decrypt(self._hc.mod(result_Nr, self._N))
        return False
