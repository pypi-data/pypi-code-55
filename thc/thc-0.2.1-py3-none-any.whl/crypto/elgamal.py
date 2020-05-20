from Crypto.PublicKey.ElGamal import generate, construct

from ..interfaces import HomomorphicCryptosystem, Computation
from ..utils import rand

from functools import partial, reduce

class ElGamal (HomomorphicCryptosystem):

    @staticmethod
    def new (size=1024):
        eg = generate(size, None)
        return ElGamal(eg.p, eg.g, eg.y, eg.x)

    def __init__ (self, p, g, y, x):
        self._p = p
        self._eg = construct((p, g, y, x))

    def get_modulus (self):
        return self._p

    def encrypt (self, m):
        r = rand(1, self._p - 1)
        return self._eg.encrypt(m, r)

    def decrypt (self, c):
        return self._eg.decrypt(c)

    def mod (self, c, mod):
        return (c[0] % mod, c[1] % mod)

class Product (Computation):

    @staticmethod
    def mul (mod, a, b):
        return (a[0] * b[0] % mod, a[1] * b[1] % mod)

    def local (self, mod, args):
        return reduce(partial(self.mul, mod), args)

    def remote (self, mod, args):
        pass

class ScalarProduct (Computation):

    def local (self, mod, args):
        return (args[0][0], args[1] * args[0][1]) % mod

    def remote (self, mod, args):
        pass
