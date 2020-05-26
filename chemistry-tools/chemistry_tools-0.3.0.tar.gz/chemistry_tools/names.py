#!/usr/bin/env python3
#
#  names.py
"""
Functions for working with IUPAC names for chemicals
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

# stdlib
import re

# this package
from chemistry_tools.constants import prefixes

multiplier_regex = "*".join([f"({prefix})" for prefix in prefixes.values()])

re_strings = [
		r"((\d+),?)+(\d+)-",
		fr"{multiplier_regex}*",
		r"nitro",
		r"phenyl",
		r"aniline",
		r"anisole",
		r"benzene",
		r"centralite",
		r"formamide",
		r"glycerine",
		r"nitrate",
		r"glycol",
		r"phthalate",
		r"picrate",
		r"toluene",
		r" ",
		]


def get_IUPAC_parts(string):
	split_points = set()

	for regex in re_strings:
		for match in list(re.finditer(regex, string.lower())):
			start, end = match.span()
			if start != end:
				split_points.add(start)
				split_points.add(end)

	split_points.discard(0)
	split_points = sorted(split_points)
	start_point = 0

	string_chars = list(string)
	elements = []
	for point in split_points:
		elements.append("".join(string_chars[start_point:point]))
		start_point = point

	elements.append("".join(string_chars[start_point:]))

	while not elements[-1]:
		elements = elements[:-1]

	return elements


#
# from string import ascii_letters
# alphabet = ascii_letters + "0123456789" + ",'" + "- " + '!"#$%&()*+./:;<=>?@[\\]^_`{|}~'


def sort_IUPAC_names(iupac_names):
	"""
	Sort the list of IUPAC names into order.

	:param iupac_names:
	:type iupac_names: List[str]

	:return:
	:rtype: List[str]
	"""

	sort_order = get_IUPAC_sort_order(iupac_names)

	# return [iupac_names[split_names.index(name)] for name in sorted_names]
	return sorted(iupac_names, key=lambda x: sort_order[x])


def get_IUPAC_sort_order(iupac_names):
	"""
	Returns the order the names should be sorted in.

	Useful when sorting arrays containing data in addition to the name.
	e.g.
	>>> sort_order = get_IUPAC_sort_order([row[0] for row in data])
	>>> sorted_data = sorted(data, key=lambda row: sort_order[row[0]])

	where row[0] would be the name of the compound

	:param iupac_names:
	:type iupac_names: List[str]

	:return:
	:rtype: List[int]
	"""

	split_names, sorted_names = _get_split_and_sorted_lists(iupac_names)

	sort_order = {}
	for index, name in enumerate(sorted_names):
		sort_order[iupac_names[split_names.index(name)]] = index

	return sort_order


def get_sorted_parts(iupac_names):
	"""
	Returns parts of the IUPAC names sorted into order.
	# The parts are in reverse order (i.e. diphenylamine becomes ["amine", "phenyl", "di"]).

	:param iupac_names:
	:type iupac_names: List[str]

	:return:
	:rtype: List[List[str]]
	"""

	split_names, sorted_names = _get_split_and_sorted_lists(iupac_names)

	return [split_names[split_names.index(name)] for name in sorted_names]


def _get_split_and_sorted_lists(iupac_names):
	split_names = []

	for name in iupac_names:
		split_name = get_IUPAC_parts(name.lower())

		if split_name[0].lower() in prefixes.values():
			# no positional information at beginning
			split_name = [" ", *split_name]

		split_names.append(split_name[::-1])

	sorted_names = sorted(split_names)

	return split_names, sorted_names


def sort_array_by_name(array, name_col=0):
	"""
	Sort a list of lists by the IUPAC name in each row.

	:param array:
	:type array: List[List]
	:param name_col: The index of the column containing the IUPAC names
	:type name_col: int

	:return:
	:rtype:
	"""

	names = [row[name_col] for row in array]
	sort_order = get_IUPAC_sort_order(names)
	sorted_array = sorted(array, key=lambda row: sort_order[row[0]])
	return sorted_array




