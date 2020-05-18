#!/usr/bin/env python
#
#  bond.py
#
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as
#  published by the Free Software Foundation; either version 3 of the
#  License, or (at your option) any later version.
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

from .errors import deprecated


class BondType:
	SINGLE = 1
	DOUBLE = 2
	TRIPLE = 3
	QUADRUPLE = 4
	DATIVE = 5
	COMPLEX = 6
	IONIC = 7
	UNKNOWN = 255


class Bond:
	"""
	Class to represent a bond between two atoms in a :class:`~pubchempy.Compound`.
	"""

	def __init__(self, aid1, aid2, order=BondType.SINGLE, style=None):
		"""Initialize with begin and end atom IDs, bond order and bond style.

		:param int aid1: Begin atom ID.
		:param int aid2: End atom ID.
		:param int order: Bond order.
		"""
		self.aid1 = aid1
		# ID of the begin atom of this bond.
		self.aid2 = aid2
		# ID of the end atom of this bond.
		self.order = order
		# Bond order.
		self.style = style
		# Bond style annotation.

	def __repr__(self):
		return 'Bond({}, {}, {})'.format(self.aid1, self.aid2, self.order)

	def __eq__(self, other):
		return (
				isinstance(other, type(self)) and
				self.aid1 == other.aid1 and
				self.aid2 == other.aid2 and
				self.order == other.order and
				self.style == other.style
				)

	@deprecated('Dictionary style access to Bond attributes is deprecated')
	def __getitem__(self, prop):
		"""Allow dict-style access to attributes to ease transition from when bonds were dicts."""
		if prop in {'order', 'style'}:
			return getattr(self, prop)
		raise KeyError(prop)

	@deprecated('Dictionary style access to Bond attributes is deprecated')
	def __setitem__(self, prop, val):
		"""Allow dict-style setting of attributes to ease transition from when bonds were dicts."""
		setattr(self, prop, val)

	@deprecated('Dictionary style access to Atom attributes is deprecated')
	def __contains__(self, prop):
		"""Allow dict-style checking of attributes to ease transition from when bonds were dicts."""
		if prop in {'order', 'style'}:
			return getattr(self, prop) is not None
		return False

	@deprecated('Dictionary style access to Atom attributes is deprecated')
	def __delitem__(self, prop):
		"""Delete the property prop from the wrapped object."""
		if not hasattr(self.__wrapped, prop):
			raise KeyError(prop)
		delattr(self.__wrapped, prop)

	def to_dict(self):
		"""Return a dictionary containing Bond data."""
		data = {'aid1': self.aid1, 'aid2': self.aid2, 'order': self.order}
		if self.style is not None:
			data['style'] = self.style
		return data
