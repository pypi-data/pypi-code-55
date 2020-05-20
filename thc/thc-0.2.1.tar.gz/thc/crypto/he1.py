from ..interfaces import HomomorphicCryptosystem, Computation
from ..utils import prime, rand

from functools import reduce
from operator import add, mul

class HE1 (HomomorphicCryptosystem):

    @staticmethod
    def new (size=1024):
        p = prime(size)
        while True:
            q = prime(HE1.eta(size))
            if p != q:
                break
        return HE1(p, q)

    def __init__ (self, p, q):
        self._p = p
        self._q = q
        self._mod = p * q

    def get_modulus (self):
        return self._mod

    def encrypt (self, m):
        r = rand(1, self._q)
        return (m + self._p * r) % self._mod

    def decrypt (self, c):
        return c % self._p

    @staticmethod
    def eta (lam):
        # Gives the desired size of q in bits given the size of p in bits.
        return lam ** 2 // 32 - lam

class Sum (Computation):

    def local (self, mod, args):
        return reduce(add, args) % mod

    def remote (self, mod, args):
        pass

class Product (Computation):

    def local (self, mod, args):
        return reduce(mul, args) % mod

    def remote (self, mod, args):
        pass
