import functools
import sys

from fractions import Fraction

# this might be useful
from math import pi

BASE = 'GeV'


class UnitNotMatchError(Exception):
    pass


def sameunits(f):
    @functools.wraps(f)
    def wrapper(u1, u2):
        if not u1.has_same_units(u2):
            raise UnitNotMatchError()
        return f(u1, u2)
    return wrapper


def use_subunits(f):
    @functools.wraps(f)
    def wrapper(u1, u2):
        if isinstance(u1, Unit):
            subunits = {k: u1.subunits[k] for k in u1.subunits}
        else:
            subunits = {}

        if isinstance(u2, Unit):
            for k in u2.subunits:
                subunits[k] = u2.subunits[k]

        result = f(u1, u2)
        if isinstance(result, Unit):
            result.subunits = subunits
        return result
    return wrapper


@functools.total_ordering
class Unit(object):

    def __init__(self, coeff, subunit=None, **kwargs):
        self.coeff = 1. * coeff
        self.units = {}
        for k in kwargs:
            if kwargs[k]:
                self.units[k] = kwargs[k]

        if subunit and len(kwargs) == 1:
            k = list(kwargs.keys())[0]
            self.subunits = {k: (coeff, subunit, kwargs[k])}
        else:
            self.subunits = {}

    def __new__(cls, coeff, **kwargs):
        if any(kwargs.values()):
            return super(Unit, cls).__new__(cls)
        else:
            return coeff

    def coefficient(self):
        coeff = 1.
        for k in self.units:
            if k in self.subunits:
                c, _, m = self.subunits[k]
                coeff *= c**(self.units[k] / m)
        
        return self.coeff / coeff

    def str_expression(self, mult, power):
        res=''

        for k in self.units:
            if k in self.subunits:
                _, rn, m = self.subunits[k]
            else:
                rn = k
                m = 1

            newunit = Fraction(self.units[k], m)

            if newunit == 1:
                res += '%s %s' % (mult, rn)
            else:
                res += '%s %s%s%s' % (mult, rn, power, str(newunit))

        res = '%3.2e%s' % (self.coefficient(), res)

        return res

    def __str__(self):
        return self.str_expression('', '^')

    def __repr__(self):
        return self.str_expression(' *', '**')

    def __call__(self, coeff):
        return coeff * self

    def has_same_units(self, t):
        unit1 = set(self.units)
        if isinstance(t, Unit):
            unit2 = set(t.units)
        else:
            unit2 = set()

        if unit1 != unit2:
            return False

        for u in unit1:
            if self.units[u] != t.units[u]:
                return False

        return True

    def to_natural_unit(self):
        p = 0
        coeff = self.coeff
        for k in self.units:
            if k == 'GeV':
                p += self.units[k]
            else:
                cc, cp = Unit.unity[k]
                coeff *= cc**self.units[k]
                p += cp * self.units[k]

        return coeff, p

    def to_planck_unit(self):
        c, p = self.to_natural_unit()
        return c * Mp.coeff**(-p)

    def convert(self, t):
        sc, sp = self.to_natural_unit()
        tc, tp = t.to_natural_unit()

        if tp == 0:
            if sp == 0:
                return (sc / tc, 1)
            else:
                raise UnitNotMatchError
        else:
            return (sc / tc**(1.0 * sp / tp), Fraction(sp, tp))

    def in_(self, t):
        c, p = self.convert(t)
        return c * t**p

    def __rshift__(self, t):
        return self.in_(t)

    def inverse(self):
        return 1.0 / self

    @sameunits
    @use_subunits
    def __add__(self, t):
        return Unit(self.coeff + t.coeff, **self.units)

    @sameunits
    @use_subunits
    def __sub__(self, t):
        return Unit(self.coeff - t.coeff, **self.units)

    @use_subunits
    def __pow__(self, t):
        return Unit(self.coeff**t,
                    **{k: self.units[k] * t for k in self.units})

    @use_subunits
    def __mul__(self, t):
        if isinstance(t, Unit):
            u = {}
            for k in self.units:
                u[k] = self.units[k]
            for k in t.units:
                if k in u:
                    u[k] += t.units[k]
                else:
                    u[k] = t.units[k]
            return Unit(self.coeff * t.coeff, **u)
        else:
            return Unit(self.coeff * t, **self.units)

    def __rmul__(self, t):
        return self * t

    @use_subunits
    def __div__(self, t):
        if isinstance(t, Unit):
            u = {}
            for k in self.units:
                u[k] = self.units[k]
            for k in t.units:
                if k in u:
                    u[k] -= t.units[k]
                else:
                    u[k] = -t.units[k]

            return Unit(self.coeff / t.coeff, **u)
        else:
            return Unit(self.coeff / t, **self.units)

    __truediv__ = __div__

    @use_subunits
    def __rdiv__(self, t):
        return Unit(t / self.coeff, **{k: -self.units[k] for k in self.units})

    __rtruediv__ = __rdiv__

    @sameunits
    def __lt__(self, t):
        return self.coeff < t.coeff

    @sameunits
    def __eq__(self, t):
        return self.coeff == t.coeff

    def __hash__(self):
        return hash(self.coeff) ^ hash(self.units)

# units
GeV = Unit(1, GeV=1)
m = Unit(1, m=1)
s = Unit(1, s=1)
kg = Unit(1, kg=1)
kelvin = Unit(1, kelvin=1)
coulomb = Unit(1, coulomb=1)

# physical constants
c = 299792458 * m / s
hbar = 1.0545718e-34 * m**2 * kg / s
hbarc = 1.97326979e-16 * m * GeV
kB = 8.61733034e-14 * GeV / kelvin
G = 6.67408e-11 * m**3 * kg**-1 * s**-2
e = 1.602176634 * 10**-19 * coulomb

def __generate_unity():
    unity = {}
    # m
    unity['m'] = (1.0 / hbarc.coeff, -hbarc.units[BASE])
    # s
    hbarGeV = hbarc / c  # s GeV
    unity['s'] = (1.0 / hbarGeV.coeff, -hbarGeV.units[BASE])
    # kg
    he = c * hbarc / hbar  # GeV/kg
    unity['kg'] = (he.coeff, he.units[BASE])
    # kelvin
    unity['kelvin'] = (kB.coeff, kB.units[BASE])
    # coulomb
    unity['coulomb'] = (1.0 / e.coeff, 0)

    return unity

Unit.unity = __generate_unity()

# Planck constant
Mp = (8 * pi * G).in_(GeV).inverse()**Fraction(1, 2)

# standard suffixes
def add_subunits(basename, basecoeff, standard_unit, dim=1, suffixes=None, namespace=__name__):
    for i, sx in enumerate('zafpnum kMGTPE'):
        if suffixes and not sx in suffixes:
            continue

        if sx == ' ':
            sx = ''

        base = 10**(-21 + i * 3)
        name = '%s%s' % (sx, basename)

        if dim == 1 and standard_unit == name:
            continue

        u = Unit(base * basecoeff, subunit=name, **{standard_unit: dim})
        setattr(sys.modules[namespace], name, u)

add_subunits('eV', 1e-9, 'GeV')
add_subunits('m', 1, 'm')
add_subunits('g', 1e-3, 'kg')
add_subunits('s', 1, 's')

