from ..interfaces import HomomorphicCryptosystem
from ..utils import prime, rand

class Trivial (HomomorphicCryptosystem):

    @staticmethod
    def field (size=1024):
        p = prime(size)
        return Trivial(m=p)

    @staticmethod
    def ring (size=1024):
        n = rand(2 ** (size - 1), 2 ** size)
        return Trivial(m=n)

    def __init__ (self, **kwargs):
        self._mod = kwargs['m']

    def get_modulus (self):
        return self._mod

    def encrypt (self, m):
        return m % self._mod

    def decrypt (self, c):
        return c % self._mod
