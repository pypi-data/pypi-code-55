#!/usr/bin/env python3
#
#  dicts.py
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
from collections import defaultdict
from itertools import chain


class AttrDict(dict):
	"""
	Subclass of dict with attribute access to keys
	"""

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__dict__ = self


class defaultkeydict(defaultdict):
	"""
	defaultdict where default_factory should have the signature key -> value

	Examples
	--------
	>>> d = defaultkeydict(lambda k: f'[{k}]' , {'a': '[a]', 'b': '[B]'})
	>>> d['a']
	'[a]'
	>>> d['b']
	'[B]'
	>>> d['c']
	'[c]'
	"""

	def __missing__(self, key):
		if self.default_factory is None:
			raise KeyError(f"Missing key: {key}")
		else:
			self[key] = self.default_factory(key)
		return self[key]


def _imul(d1, d2):
	if hasattr(d2, 'keys'):
		for k in set(chain(d1.keys(), d2.keys())):
			d1[k] = d1[k] * d2[k]
	else:
		for k in d1:
			d1[k] *= d2


def _itruediv(d1, d2):
	if hasattr(d2, 'keys'):
		for k in set(chain(d1.keys(), d2.keys())):
			d1[k] = d1[k] / d2[k]
	else:
		for k in d1:
			d1[k] /= d2


class ArithmeticDict(defaultdict):
	"""
		A dictionary which supports arithmetics

	Subclassed from defaultdict, with support for addition, subtraction,
	multiplication and division. If other term/factor has a :meth:`keys` method
	the arithmetics are performed on a key per key basis. If :meth:`keys` is
	missing, the operation is broadcasted onto all values.
	Nonexisting keys are interpreted to signal a zero.

	Notes
	-----
	``__eq__`` ignores values equal to ``self.default_factory()``

	Examples
	--------
	>>> d1 = ArithmeticDict(float, {'a': 2.0, 'b': 3.0})
	>>> d2 = ArithmeticDict(float, {'b': 5.0, 'c': 7.0})
	>>> (d1 + d2) == {'a': 2., 'b': 8., 'c': 7., 'd': 0.}
	True
	>>> (d1 * d1) == {'a': 4.0, 'b': 9.0, 'z': 0}
	True
	>>> (d1 * d2) == {'b': 15}
	True
	>>> d1*2 == {'a': 4, 'b': 6}
	True
	>>> (d1 / {'a': 2, 'b': 11})['b'] == 3./11
	True
	>>> d2/3 == {'b': 5./3, 'c': 7./3}
	True

	"""

	def copy(self):
		return self.__class__(self.default_factory, self.items())

	def __iadd__(self, other):
		try:
			for k, v in other.items():
				self[k] += v
		except AttributeError:
			for k in self:
				self[k] += other
		return self

	def __isub__(self, other):
		try:
			for k, v in other.items():
				self[k] -= v
		except AttributeError:
			for k in self:
				self[k] -= other
		return self

	def __add__(self, other):
		a = self.copy()
		a += other
		return a

	def __sub__(self, other):
		a = self.copy()
		a -= other
		return a

	def __radd__(self, other):
		return self + other

	def __rsub__(self, other):
		return -1 * self + other

	def __imul__(self, other):
		_imul(self, other)
		return self

	def __mul__(self, other):
		a = self.copy()
		a *= other
		return a

	def __rmul__(self, other):
		return self * other

	def __itruediv__(self, other):
		_itruediv(self, other)
		return self

	def __truediv__(self, other):
		a = self.copy()
		a /= other
		return a

	def __rtruediv__(self, other):
		"""
		other / self """
		return self.__class__(
				self.default_factory,
				{k: other / v for k, v in self.items()})

	def __ifloordiv__(self, other):
		if hasattr(other, 'keys'):
			for k in set(chain(self.keys(), other.keys())):
				self[k] = self[k] // other[k]
		else:
			for k in self:
				self[k] //= other
		return self

	def __floordiv__(self, other):
		a = self.copy()
		a //= other
		return a

	def __rfloordiv__(self, other):
		"""
		other // self """
		return self.__class__(
				self.default_factory,
				{k: other // v for k, v in self.items()})

	def __repr__(self):
		return f"{self.__class__.__name__}({repr(self.default_factory)}, {dict(self)})"

	def _element_eq(self, a, b):
		return a == b

	def _discrepancy(self, other, cb):
		default = self.default_factory()
		_self = self.copy()  # getitem is not idempotent on defaultdict
		_other = other.copy()
		try:
			for k in set(chain(_self.keys(), _other.keys())):
				if not cb(_self[k], _other.get(k, default)):
					return False
			return True
		except TypeError:
			return False

	def __eq__(self, other):
		return self._discrepancy(other, self._element_eq)

	def isclose(self, other, rtol=1e-12, atol=None):
		def _isclose(a, b):
			lim = abs(rtol * b)
			if atol is not None:
				lim += atol
			return abs(a - b) <= lim
		return self._discrepancy(other, _isclose)

	def all_non_negative(self):
		for v in self.values():
			if v < v * 0:
				return False
		return True
