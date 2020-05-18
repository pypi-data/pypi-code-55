#!/usr/bin/env python3
#
#  dataarray.py
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

# stdlib
from abc import abstractmethod

#  3rd party
import pandas
import tabulate
from cawdrey import FrozenOrderedDict


class DataArray(FrozenOrderedDict):
	"""
	A class that can output data as an array, to CSV, as a pandas DataFrame,
	or as a pretty-printed table in a variety of formats.
	"""

	def __init__(self, formula, data):
		"""

		:param formula: A :class:`Formula` object to create the distribution for
		:type formula: :class:`Formula`
		:param data: A dictionary of data to add to the internal
			:class:`~cawdrey.frozenordereddict.FrozenOrderedDict`
		:type data: dict
		"""

		super().__init__(**data)
		self.formula = formula

	def as_csv(self, *args, sep=",", **kwargs):
		"""
		Returns the data as a CSV formatted string

		:param sep: The separator for the CSV data. Default ``,``
		:type sep: str, optional

		Any additional arguments taken by ``as_array`` can also be used here.

		:rtype: str
		"""

		return "\n".join(sep.join(x) for x in self.as_array(*args, **kwargs))

	_as_array_kwargs = set()

	@abstractmethod
	def as_array(self, *args, **kwargs):
		pass

	def as_dataframe(self, *args, **kwargs):
		"""
		Returns the isotope distribution data as a pandas DataFrame

		Any arguments taken by ``as_array`` can also be used here.

		:rtype: :class:`pandas.DataFrame`
		"""

		array = self.as_array(*args, **kwargs)
		return pandas.DataFrame.from_records(array[1:], columns=array[0])

	_as_table_alignment = []
	_as_table_float_format = []

	def as_table(self, *args, **kwargs):
		"""
		Returns the isotope distribution data as a table using
		`tabulate <https://github.com/astanin/python-tabulate>`_

		Any arguments taken by ``as_array`` can also be used here.

		Additionally, any valid keyword argument for :func:`tabulate.tabulate` can be used.

		:rtype: str
		"""

		tabulate_kwargs = {}
		array_kwargs = {}
		for arg, val in kwargs.items():
			if arg in self._as_array_kwargs:
				array_kwargs[arg] = val
			else:
				tabulate_kwargs[arg] = val

		if "colalign" not in tabulate_kwargs:
			tabulate_kwargs["colalign"] = self._as_table_alignment
		if "floatfmt" not in tabulate_kwargs:
			tabulate_kwargs["floatfmt"] = self._as_table_float_format

		array = self.as_array(*args, **array_kwargs)
		return tabulate.tabulate(array[1:], array[0], **tabulate_kwargs)

	def __str__(self):
		return self.__repr__()

	def __repr__(self):
		return f"<{self.__class__.__name__}({self.formula})>"
