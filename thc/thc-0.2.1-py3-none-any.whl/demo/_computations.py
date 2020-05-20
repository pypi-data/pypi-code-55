import random
from functools import partial, reduce
from operator import mul

from ..interfaces import Computation

class Product (Computation):

    def local (self, mod, args):
        return reduce(mul, args) % mod

    def remote (self, mod, args):
        if bool(random.randint(0, 1)):
            print('⚡ ', end='')
            fault = random.randint(0, mod)
        else:
            print('  ', end='')
            fault = 1
        return (reduce(mul, args) * fault) % mod

class PairProduct (Computation):

    @staticmethod
    def mul (mod, a, b):
        return (a[0] * b[0] % mod, a[1] * b[1] % mod)

    def local (self, mod, args):
        return reduce(partial(self.mul, mod), args)

    def remote (self, mod, args):
        if bool(random.randint(0, 1)):
            print('⚡ ', end='')
            if bool(random.randint(0, 1)):
                args.append((1, random.randint(0, mod)))
            else:
                args.append((random.randint(0, mod), 1))
        else:
            print('  ', end='')
        return reduce(partial(self.mul, mod), args)

class RandomPolynomial (Computation):

    def __init__ (self, degree, max_coeff=100):
        self._c = [random.randint(0, max_coeff) for i in range(degree + 1)]

    def __str__ (self):
        s = ''
        for i in range(len(self._c)):
            s = str(self._c[i]) + 'x^' + str(i) + ' + ' + s
        return s[:-6]

    def local (self, mod, args):
        x = args[0] % mod
        res = 0
        for i in range(len(self._c)):
            res += (x ** i * self._c[i]) % mod
        return res % mod

    def remote (self, mod, args):
        x = args[0] % mod
        if bool(random.randint(0, 1)):
            print('⚡ ', end='')
            fault = random.randint(0, mod)
        else:
            print('  ', end='')
            fault = 0
        res = fault
        for i in range(len(self._c)):
            res += (x ** i * self._c[i]) % mod
        return res % mod

class RandomBinaryPolynomial (Computation):

    def __init__ (self, degree, max_coeff=100):
        self._cx = [random.randint(0, max_coeff) for i in range(degree + 1)]
        self._cy = [random.randint(0, max_coeff) for i in range(degree + 1)]

    def __str__ (self):
        s = ''
        for i in range(len(self._cx)):
            x = str(self._cx[i]) + 'x^' + str(i) + ' + '
            y = str(self._cy[i]) + 'y^' + str(i) + ' + '
            s = x + y + s
        return s.replace('x^0', '').replace('y^0 + ', '')

    def local (self, mod, args):
        x = args[0] % mod
        y = args[1] % mod
        res = 0
        for i in range(len(self._cx)):
            res += (x ** i * self._cx[i]) % mod
            res += (y ** i * self._cy[i]) % mod
        return res % mod

    def remote (self, mod, args):
        deg = random.randint(0, len(self._cx) - 1)
        xy = random.choice(['x', 'y'])
        fault = random.randint(0, mod)
        x = args[0] % mod
        y = args[1] % mod
        res = 0
        print('⚡ ', end='')
        for i in range(len(self._cx)):
            if xy == 'x' and deg == i:
                # print('x^'+str(i)+' faulted: '+str(fault))
                res = (res + fault) % mod
            else:
                res = (res + (x ** i * self._cx[i])) % mod
            if xy == 'y' and deg == i:
                # print('y^'+str(i)+' faulted: '+str(fault))
                res = (res + fault) % mod
            else:
                res = (res + (y ** i * self._cy[i])) % mod
        return res % mod

    def mod (self, m):
        comp = RandomBinaryPolynomial(0, 0)
        comp._cx = [c % m for c in self._cx]
        comp._cy = [c % m for c in self._cy]
        return comp
