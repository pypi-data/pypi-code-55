from abc import ABC, abstractmethod

###
### Interfaces
###

class HomomorphicCryptosystem (ABC):

    @abstractmethod
    def __init__ (self):
        pass

    @abstractmethod
    def get_modulus (self):
        pass

    @abstractmethod
    def encrypt (self, m):
        pass

    @abstractmethod
    def decrypt (self, c):
        pass

    def mod (self, c, mod):
        # returns c % mod for a ciphertext c
        return c % mod

class Computation (ABC):

    @abstractmethod
    def local (self, mod, args):
        pass

    @abstractmethod
    def remote (self, mod, args):
        pass
