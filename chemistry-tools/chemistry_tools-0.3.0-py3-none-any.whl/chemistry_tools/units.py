#!/usr/bin/env python3
#
#  units.py
"""
The units module provides the following attributes:

- ``chempy.units.SI_base_registry``

together with some functions.

Currently `quantities <https://pypi.python.org/pypi/quantities>`_ is used as
the underlying package to handle units. If it is possible you should try to
only use the ``chempy.units`` module (since it is likely that ``ChemPy``
will change this backend at some point in the future). Therefore you should not
rely on any attributes of the ``Quantity`` instances (and rather use
getter & setter functions in `chempy.units`).

"""
#
#  Copyright (c) 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#  Based on ChemPy (https://github.com/bjodah/chempy)
#  |  Copyright (c) 2015-2018, Björn Dahlgren
#  |  All rights reserved.
#  |
#  |  Redistribution and use in source and binary forms, with or without modification,
#  |  are permitted provided that the following conditions are met:
#  |
#  |    Redistributions of source code must retain the above copyright notice, this
#  |    list of conditions and the following disclaimer.
#  |
#  |    Redistributions in binary form must reproduce the above copyright notice, this
#  |    list of conditions and the following disclaimer in the documentation and/or
#  |    other materials provided with the distribution.
#  |
#  |  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
#  |  ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
#  |  WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#  |  DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
#  |  ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
#  |  (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
#  |  LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
#  |  ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#  |  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#  |  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#


# stdlib
from collections import OrderedDict
from functools import reduce
from operator import mul

# 3rd party
import numpy as np
import quantities

# this package
from chemistry_tools.dicts import ArithmeticDict
from chemistry_tools.utils import defaultnamedtuple


def is_quantity(arg):
	# this check works even if quantities is not installed.
	return bool(arg.__class__.__name__ == 'Quantity')


energy = ArithmeticDict(int, {'mass': 1, 'length': 2, 'time': -2})
volume = ArithmeticDict(int, {'length': 3})
concentration = {'amount': 1} - volume


def get_derived_unit(registry, key):
	"""
	Get the unit of a physcial quantity in a provided unit system.

	Parameters
	----------
	registry: dict (str: unit)
		mapping 'length', 'mass', 'time', 'current', 'temperature',
		'luminous_intensity', 'amount'. If registry is ``None`` the
		function returns 1.0 unconditionally.
	key: str
		one of the registry keys or one of: 'diffusivity', 'electricalmobility',
		'permittivity', 'charge', 'energy', 'concentration', 'density',
		'radiolytic_yield'.

	Examples
	--------
	>>> m, s = quantities.meter, quantities.second
	>>> get_derived_unit(SI_base_registry, 'diffusivity') == m**2/s
	True

	"""
	if registry is None:
		return 1.0

	derived = {
			'diffusivity': registry['length'] ** 2 / registry['time'],
			'electrical_mobility': registry['current'] * registry['time'] ** 2 / registry['mass'],
			'permittivity': (
					registry['current'] ** 2 * registry['time'] ** 4
					/ (registry['length'] ** 3 * registry['mass'])),
			'charge': registry['current'] * registry['time'],
			'energy': registry['mass'] * registry['length'] ** 2 / registry['time'] ** 2,
			'concentration': registry['amount'] / registry['length'] ** 3,
			'density': registry['mass'] / registry['length'] ** 3,
			}
	derived['diffusion'] = derived['diffusivity']  # 'diffusion' is deprecated
	derived['radiolytic_yield'] = registry['amount'] / derived['energy']
	derived['doserate'] = derived['energy'] / registry['mass'] / registry['time']
	derived['linear_energy_transfer'] = derived['energy'] / registry['length']

	try:
		return derived[key]
	except KeyError:
		return registry[key]


def unit_registry_to_human_readable(unit_registry):
	"""
	Serialization of a unit registry.
	"""

	if unit_registry is None:
		return None

	new_registry = {}
	integer_one = 1
	for k in SI_base_registry:
		if unit_registry[k] is integer_one:
			new_registry[k] = 1, 1
		else:
			dim_list = list(unit_registry[k].dimensionality)
			if len(dim_list) != 1:
				raise TypeError("Compound units not allowed: {}".format(
						dim_list))
			u_symbol = dim_list[0].u_symbol
			new_registry[k] = float(unit_registry[k]), u_symbol
	return new_registry


def _latex_from_dimensionality(dim):
	# see https://github.com/python-quantities/python-quantities/issues/148
	from quantities.markup import format_units_latex
	return format_units_latex(dim, mult=r'\\cdot')


def latex_of_unit(quant):
	"""
	Returns LaTeX reperesentation of the unit of a quantity

	Examples
	--------
	>>> print(latex_of_unit(1/quantities.kelvin))
	\\mathrm{\\frac{1}{K}}
	"""

	return _latex_from_dimensionality(quant.dimensionality).strip('$')


def unicode_of_unit(quant):
	"""
	Returns unicode reperesentation of the unit of a quantity

	Examples
	--------
	>>> print(unicode_of_unit(1/quantities.kelvin))
	1/K
	"""

	return quant.dimensionality.unicode


def html_of_unit(quant):
	"""
	Returns HTML reperesentation of the unit of a quantity

	Examples
	--------
	>>> print(html_of_unit(2*quantities.m**2))
	m<sup>2</sup>
	"""

	return quant.dimensionality.html


def unit_registry_from_human_readable(unit_registry):
	"""
	Deserialization of unit_registry.
	"""

	if unit_registry is None:
		return None

	new_registry = {}
	for k in SI_base_registry:
		factor, u_symbol = unit_registry[k]
		if u_symbol == 1:
			unit_quants = [1]
		else:
			unit_quants = list(quantities.Quantity(0, u_symbol).dimensionality.keys())

		if len(unit_quants) != 1:
			raise TypeError("Unknown UnitQuantity: {}".format(unit_registry[k]))
		else:
			new_registry[k] = factor * unit_quants[0]
	return new_registry


# Abstraction of underlying package providing units and dimensional analysis:

def is_unitless(expr):
	"""
		Returns ``True`` if ``expr`` is unitless, otherwise ``False``

	Examples
	--------
	>>> is_unitless(42)
	True
	>>> is_unitless(42*quantities.kilogram)
	False

	"""
	if hasattr(expr, 'dimensionality'):
		if expr == quantities.dimensionless:
			return True
		else:
			return expr.simplified.dimensionality == quantities.dimensionless.dimensionality
	if isinstance(expr, dict):
		return all(is_unitless(_) for _ in expr.values())
	elif isinstance(expr, (tuple, list)):
		return all(is_unitless(_) for _ in expr)
	return True


def unit_of(expr, simplified=False):
	"""
		Returns the unit of a quantity

	Examples
	--------
	>>> unit_of(42*pq.second) == unit_of(12*pq.second)
	True
	>>> unit_of(42)
	1

	"""
	if isinstance(expr, (tuple, list)):
		return unit_of(uniform(expr)[0], simplified)
	elif isinstance(expr, dict):
		return unit_of(list(uniform(expr).values())[0], simplified)

	try:
		if simplified:
			return expr.units.simplified
		else:
			return expr.units
	except AttributeError:
		return 1


def rescale(value, unit):
	try:
		return value.rescale(unit)
	except AttributeError:
		if unit == 1:
			return value
		else:
			raise


def to_unitless(value, new_unit=None):
	"""
	Nondimensionalization of a quantity.

	Parameters
	----------
	value: quantity
	new_unit: unit

	Examples
	--------
	>>> '%.1g' % to_unitless(1*quantities.metre, quantities.nm)
	'1e+09'
	>>> '%.1g %.1g' % tuple(to_unitless([1*quantities.m, 1*quantities.mm], quantities.nm))
	'1e+09 1e+06'

	"""
	integer_one = 1
	if new_unit is None:
		new_unit = quantities.dimensionless

	if isinstance(value, (list, tuple)):
		return np.array([to_unitless(elem, new_unit) for elem in value])
	elif isinstance(value, np.ndarray) and not hasattr(value, 'rescale'):
		if is_unitless(new_unit) and new_unit == 1 and value.dtype != object:
			return value
		return np.array([to_unitless(elem, new_unit) for elem in value])
	elif isinstance(value, dict):
		new_value = dict(value.items())  # value.copy()
		for k in value:
			new_value[k] = to_unitless(value[k], new_unit)
		return new_value
	elif isinstance(value, (int, float)) and new_unit is integer_one or new_unit is None:
		return value
	elif isinstance(value, str):
		raise ValueError("str not supported")
	else:
		try:
			try:
				result = (value * quantities.dimensionless / new_unit).rescale(quantities.dimensionless)
			except AttributeError:
				if new_unit == quantities.dimensionless:
					return value
				else:
					raise
			else:
				if result.ndim == 0:
					return float(result)
				else:
					return np.asarray(result)
		except TypeError:
			return np.array([to_unitless(elem, new_unit) for elem in value])


def uniform(container):
	"""
	Turns a list, tuple or dict with mixed units into one with uniform units.

	Parameters
	----------
	container : tuple, list or dict

	Examples
	--------
	>>> km, m = quantities.kilometre, quantities.metre
	>>> uniform(dict(a=3*km, b=200*m))  # doctest: +SKIP
	{'b': array(200.0) * m, 'a': array(3000.0) * m}

	"""
	if isinstance(container, (tuple, list)):
		unit = unit_of(container[0])
	elif isinstance(container, dict):
		unit = unit_of(list(container.values())[0])
		return container.__class__([(k, to_unitless(v, unit) * unit) for k, v in container.items()])
	else:
		return container
	return to_unitless(container, unit) * unit


def get_physical_dimensionality(value):
	if is_unitless(value):
		return {}

	_quantities_mapping = {
			quantities.UnitLength: 'length',
			quantities.UnitMass: 'mass',
			quantities.UnitTime: 'time',
			quantities.UnitCurrent: 'current',
			quantities.UnitTemperature: 'temperature',
			quantities.UnitLuminousIntensity: 'luminous_intensity',
			quantities.UnitSubstance: 'amount'
			}

	return {
			_quantities_mapping[k.__class__]: v for k, v
			in uniform(value).simplified.dimensionality.items()
			}


def _get_unit_from_registry(dimensionality, registry):
	return reduce(mul, [registry[k] ** v for k, v in dimensionality.items()])


def default_unit_in_registry(value, registry):
	_dimensionality = get_physical_dimensionality(value)

	if _dimensionality == {}:
		return 1

	return _get_unit_from_registry(_dimensionality, registry)


def unitless_in_registry(value, registry):
	_default_unit = default_unit_in_registry(value, registry)
	return to_unitless(value, _default_unit)


# NumPy like functions for compatibility:

def compare_equality(a, b):
	"""
	Returns True if two arguments are equal.

	Both arguments need to have the same dimensionality.

	Parameters
	----------
	a : quantity
	b : quantity

	Examples
	--------
	>>> km, m = quantities.kilometre, quantities.metre
	>>> compare_equality(3*km, 3)
	False
	>>> compare_equality(3*km, 3000*m)
	True

	"""
	# Work around for https://github.com/python-quantities/python-quantities/issues/146
	try:
		a + b
	except TypeError:
		# We might be dealing with e.g. None (None + None raises TypeError)
		try:
			len(a)
		except TypeError:
			# Assumed scalar
			return a == b
		else:
			if len(a) != len(b):
				return False
			return all(compare_equality(_a, _b) for _a, _b in zip(a, b))
	except ValueError:
		return False
	else:
		return a == b


def allclose(a, b, rtol=1e-8, atol=None):
	"""
		Analogous to ``numpy.allclose``. """
	try:
		d = abs(a - b)
	except Exception:
		try:
			if len(a) == len(b):
				return all(allclose(_a, _b, rtol, atol) for _a, _b in zip(a, b))
			else:
				return False
		except Exception:
			return False
	lim = abs(a) * rtol
	if atol is not None:
		lim += atol

	try:
		len(d)
	except TypeError:
		return d <= lim
	else:
		try:
			len(lim)
		except TypeError:
			return np.all([_d <= lim for _d in d])
		else:
			return np.all([_d <= _lim for _d, _lim in zip(d, lim)])


def logspace_from_lin(start, stop, num=50):
	"""
		Logarithmically spaced data points

	Examples
	--------
	>>> abs(logspace_from_lin(2, 8, num=3)[1] - 4) < 1e-15
	True

	"""
	unit = unit_of(start)
	start_ = np.log2(to_unitless(start, unit))
	stop_ = np.log2(to_unitless(stop, unit))
	return np.exp2(np.linspace(start_, stop_, num)) * unit


def _sum(iterable):
	try:
		result = next(iterable)
	except TypeError:
		result = iterable[0]
		for elem in iterable[1:]:
			result += elem
		return result
	else:
		try:
			while True:
				result += next(iterable)
		except StopIteration:
			return result
		else:
			raise ValueError("Not sure how this point was reached")


class Backend:
	"""
	Wrapper around modules such as numpy and math

	Instances of Backend wraps a module, e.g. `numpy` and ensures that
	arguments passed on are unitless, i.e. it raises an error if a
	transcendental function is used with quantities with units.

	Parameters
	----------
	underlying_backend : module, str or tuple of str
		e.g. 'numpy' or ('sympy', 'math')

	Examples
	--------
	>>> import math
	>>> km, m = quantities.kilometre, quantities.metre
	>>> math.exp(3*km) == math.exp(3*m)
	True
	>>> be = Backend('math')
	>>> be.exp(3*km)
	Traceback (most recent call last):
		...
	ValueError: Unable to convert between units of "km" and "dimensionless"
	>>> import numpy as np
	>>> np.sum([1000*pq.metre/pq.kilometre, 1])
	1001.0
	>>> be_np = Backend(np)
	>>> be_np.sum([[1000*pq.metre/pq.kilometre, 1], [3, 4]], axis=1)
	array([2., 7.])

	"""

	def __init__(self, underlying_backend=('numpy', 'math')):
		if isinstance(underlying_backend, tuple):
			for name in underlying_backend:
				try:
					self.be = __import__(name)
				except ImportError:
					continue
				else:
					break
			else:
				raise ValueError(f"Could not import any of {str(underlying_backend)}")
		elif isinstance(underlying_backend, str):
			self.be = __import__(underlying_backend)
		else:
			self.be = underlying_backend

	def __getattr__(self, attr):
		be_attr = getattr(self.be, attr)
		if callable(be_attr):
			return lambda *args, **kwargs: be_attr(*map(to_unitless, args), **kwargs)
		else:
			return be_attr


# TODO: decide whether to deprecate in favor of "number_to_scientific_latex"?
def format_string(value, precision='%.5g', tex=False):
	"""
	Formats a scalar with unit as two strings

	:param value: Value with unit
	:type value: float
	:param precision:
	:type precision: str, optional
	:param tex: Whether the string should be formatted for LaTex. Default :const:`False`
	:type tex: bool, optional

	:return:
	:rtype:

	Examples
	--------
	>>> print(' '.join(format_string(0.42*quantities.mol/quantities.decimetre**3)))
	0.42 mol/decimetre**3
	>>> print(' '.join(format_string(2/quantities.s, tex=True)))
	2 \\mathrm{\\frac{1}{s}}
	"""

	if tex:
		unit_str = latex_of_unit(value)
	else:
		from quantities.markup import config
		attr = 'unicode' if config.use_unicode else 'string'
		unit_str = getattr(value.dimensionality, attr)
	return precision % float(value.magnitude), unit_str


def concatenate(arrays, **kwargs):
	"""
	Patched version of numpy.concatenate

	Examples
	--------
	>>> from chemistry_tools.units import quantities
	>>> all(concatenate(([2, 3]*quantities.s, [4, 5]*quantities.s)) == [2, 3, 4, 5]*quantities.s)
	True

	"""
	unit = unit_of(arrays[0])
	result = np.concatenate([to_unitless(arr, unit) for arr in arrays], **kwargs)
	return result * unit


def fold_constants(arg):
	if hasattr(arg, 'dimensionality'):
		m = arg.magnitude
		d = 1
		for k, v in arg.dimensionality.items():
			if isinstance(k, quantities.UnitConstant):
				m = m * k.simplified ** v
			else:
				d = d * k ** v
		return m * d
	else:
		return arg


def _sanity_check_quantities(pq):
	# See https://github.com/python-quantities/python-quantities/pull/116
	a = pq.UncertainQuantity([1, 2], pq.m, [.1, .2])
	assert (-a).uncertainty[0] == (a * -1).uncertainty[0]

	# See https://github.com/python-quantities/python-quantities/pull/126
	assert (3 * pq.m) ** 0 == 1 * pq.dimensionless


_sanity_check_quantities(quantities)

# Additional units to complement quantities
per100eV = quantities.UnitQuantity(
		'per_100_eV',
		1 / (100 * quantities.eV * quantities.constants.Avogadro_constant),
		u_symbol='(100eV)**-1')
dm = decimetre = quantities.UnitQuantity('decimetre', quantities.m / 10.0, u_symbol='dm')
m3 = quantities.metre ** 3
dm3 = decimetre ** 3
cm3 = quantities.centimetre ** 3
nanomolar = quantities.UnitQuantity('nM', 1e-6 * quantities.mole / m3, u_symbol='nM')
molal = quantities.UnitQuantity('molal', quantities.mole / quantities.kg, u_symbol='molal')
micromole = quantities.UnitQuantity('micromole', quantities.mole / 1e6, u_symbol='μmol')
nanomole = quantities.UnitQuantity('nanomole', quantities.mole / 1e9, u_symbol='nmol')
kilojoule = quantities.UnitQuantity('kilojoule', 1e3 * quantities.joule, u_symbol='kJ')
kilogray = quantities.UnitQuantity('kilogray', 1e3 * quantities.gray, u_symbol='kGy')
perMolar_perSecond = 1 / quantities.molar / quantities.s
umol_per_J = quantities.umol / quantities.joule

# unit registry data and logic:
SI_base_registry = {
		'length': quantities.metre,
		'mass': quantities.kilogram,
		'time': quantities.second,
		'current': quantities.ampere,
		'temperature': quantities.kelvin,
		'luminous_intensity': quantities.candela,
		'amount': quantities.mole
		}


dimension_codes = OrderedDict(zip(
		'length mass time current temperature amount'.split(),  # not considering luminous_intensity
		'L M T I Θ N'.split()
		))


class DimensionalitySI(defaultnamedtuple('DimensionalitySIBase', dimension_codes.keys(), (0,) * len(dimension_codes))):

	def __mul__(self, other):
		return self.__class__(*(x + y for x, y in zip(self, other)))

	def __truediv__(self, other):
		return self.__class__(*(x - y for x, y in zip(self, other)))

	def __pow__(self, exp):
		return self.__class__(*(x * exp for x in self))


base_registry = {name: DimensionalitySI(**{name: 1}) for name in dimension_codes}
