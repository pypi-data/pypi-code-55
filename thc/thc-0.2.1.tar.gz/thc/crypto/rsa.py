from ..interfaces import HomomorphicCryptosystem, Computation
from ..utils import prime, modinv

from functools import reduce
from operator import mul

class RSA (HomomorphicCryptosystem):

    @staticmethod
    def new (size=1024):
        p = prime(size)
        while True:
            q = prime(size)
            if p != q:
                break
        e = prime(size // 2)
        return RSA(p, q, e)

    def __init__ (self, p, q, e):
        self._N = p * q
        self._e = e
        self._d = modinv(e, (p - 1) * (q - 1))

    def get_modulus (self):
        return self._N

    def encrypt (self, m):
        return pow(m, self._e, self._N)

    def decrypt (self, c):
        return pow(c, self._d, self._N)

class Product (Computation):

    def local (self, mod, args):
        return reduce(mul, args) % mod

    def remote (self, mod, args):
        pass
