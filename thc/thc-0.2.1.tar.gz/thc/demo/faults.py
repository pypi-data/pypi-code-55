import random
from .. import THC
from ..utils import prime
from ..crypto.trivial import Trivial
from ..crypto.rsa import RSA
from ..crypto.elgamal import ElGamal
from ..crypto.paillier import Paillier
from ..crypto.he1 import HE1
from ._computations import Product, PairProduct, RandomPolynomial

if __name__ ==  '__main__':

    nums = random.sample(range(2**8), 5)

    ### RSA

    thc = THC(RSA.new(512), Product(), prime(32))
    print('> Multiplications with RSA:')
    print(' * '.join([str(n) for n in nums]) + ' =', thc.compute(nums))

    print('')

    ### ElGamal

    thc = THC(ElGamal.new(512), PairProduct(), prime(32))
    print('> Multiplications with ElGamal:')
    print(' * '.join([str(n) for n in nums]) + ' =', thc.compute(nums))

    print('')

    ### Paillier

    thc = THC(Paillier.new(512), Product(), prime(32))
    print('> Additions with Paillier:')
    print(' + '.join([str(n) for n in nums]) + ' =', thc.compute(nums))

    print('')

    ### HE1

    rp = RandomPolynomial(5, 2**8)
    thc = THC(HE1.new(256), rp, prime(32))
    print('> Polynomial with HE1:')
    print('random polynomial P(x) =', rp)
    for n in nums:
        print('P(' + str(n) + ') =', thc.compute([n]))
