from ..interfaces import HomomorphicCryptosystem, Computation
from ..utils import prime, rand, modinv

from functools import reduce
from operator import mul

class Paillier (HomomorphicCryptosystem):

    @staticmethod
    def new (size=1024):
        p = prime(size)
        while True:
            q = prime(size)
            if p != q:
                break
        return Paillier(p, q)

    def __init__ (self, p, q):
        self._N = p * q
        self._Nsqr = self._N * self._N
        self._phi_N = (p - 1) * (q - 1)
        self._g = self._N + 1
        self._lambda = self._phi_N
        self._mu = modinv(self._phi_N, self._N)

    def get_modulus (self):
        return self._Nsqr

    def encrypt (self, m):
        r = rand(1, self._N - 1)
        gm = pow(self._g, m, self._Nsqr)
        rN = pow(r, self._N, self._Nsqr)
        return gm * rN % self._Nsqr

    def decrypt (self, c):
        L = (pow(c, self._lambda, self._Nsqr) - 1) // self._N
        return L * self._mu % self._N

class Sum (Computation):

    def local (self, mod, args):
        return reduce(mul, args) % mod

    def remote (self, mod, args):
        pass

class Product (Computation):

    def local (self, mod, args):
        return (args[0] ** args[1]) % mod

    def remote (self, mod, args):
        pass
