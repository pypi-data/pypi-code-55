#!/usr/bin/env python
#
#
#  atom.py
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

from chemistry_tools.elements import ELEMENTS
from .errors import deprecated


class Atom:
	"""Class to represent an atom in a :class:`~pubchempy.Compound`."""

	def __init__(self, aid, number, x=None, y=None, z=None, charge=0):
		"""Initialize with an atom ID, atomic number, coordinates and optional change.

		:param int aid: Atom ID
		:param int number: Atomic number
		:param float x: X coordinate.
		:param float y: Y coordinate.
		:param float z: (optional) Z coordinate.
		:param int charge: (optional) Formal charge on atom.
		"""

		self.aid = aid
		# The atom ID within the owning Compound.
		self.number = number
		# The atomic number for this atom.
		self.x = x
		# The x coordinate for this atom.
		self.y = y
		# The y coordinate for this atom.
		self.z = z
		# The z coordinate for this atom. Will be ``None`` in 2D Compound records.
		self.charge = charge
		# The formal charge on this atom.

	def __repr__(self):
		return 'Atom({}, {})'.format(self.aid, self.element)

	def __eq__(self, other):
		return (
				isinstance(other, type(self)) and
				self.aid == other.aid and
				self.element == other.element and
				self.x == other.x and
				self.y == other.y and
				self.z == other.z and
				self.charge == other.charge
				)

	@deprecated('Dictionary style access to Atom attributes is deprecated')
	def __getitem__(self, prop):
		"""Allow dict-style access to attributes to ease transition from when atoms were dicts."""
		if prop in {'element', 'x', 'y', 'z', 'charge'}:
			return getattr(self, prop)
		raise KeyError(prop)

	@deprecated('Dictionary style access to Atom attributes is deprecated')
	def __setitem__(self, prop, val):
		"""Allow dict-style setting of attributes to ease transition from when atoms were dicts."""
		setattr(self, prop, val)

	@deprecated('Dictionary style access to Atom attributes is deprecated')
	def __contains__(self, prop):
		"""Allow dict-style checking of attributes to ease transition from when atoms were dicts."""
		if prop in {'element', 'x', 'y', 'z', 'charge'}:
			return getattr(self, prop) is not None
		return False

	@property
	def element(self):
		"""The element symbol for this atom."""
		return ELEMENTS[self.number].symbol

	def to_dict(self):
		"""Return a dictionary containing Atom data."""
		data = {'aid': self.aid, 'number': self.number, 'element': self.element}
		for coord in {'x', 'y', 'z'}:
			if getattr(self, coord) is not None:
				data[coord] = getattr(self, coord)
		if self.charge != 0:
			data['charge'] = self.charge
		return data

	def set_coordinates(self, x, y, z=None):
		"""Set all coordinate dimensions at once."""
		self.x = x
		self.y = y
		self.z = z

	@property
	def coordinate_type(self):
		"""Whether this atom has 2D or 3D coordinates."""
		return '2d' if self.z is None else '3d'
