from Crypto.Util.number import getPrime, getStrongPrime, inverse
from Crypto.Random.random import StrongRandom

###
### Utils
###

def prime (bits):
    if bits > 512 and bits % 128 == 0:
        return getStrongPrime(bits)
    return getPrime(bits)

def rand (min, max):
    return StrongRandom().randint(min, max)

def modinv (e, m):
    return inverse(e, m)
