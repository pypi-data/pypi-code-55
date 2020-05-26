#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  utils.py
"""
Various tools
"""
#  Copyright (c) 2019-2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
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
#  Based on PubChemPy https://github.com/mcs07/PubChemPy/blob/master/LICENSE
#  |  Copyright 2014 Matt Swain <m.swain@me.com>
#  |  Licensed under the MIT License
#  |
#  |  Permission is hereby granted, free of charge, to any person obtaining a copy
#  |  of this software and associated documentation files (the "Software"), to deal
#  |  in the Software without restriction, including without limitation the rights
#  |  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  |  copies of the Software, and to permit persons to whom the Software is
#  |  furnished to do so, subject to the following conditions:
#
#  |  The above copyright notice and this permission notice shall be included in
#  |  all copies or substantial portions of the Software.
#
#  |  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  |  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  |  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  |  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  |  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  |  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#  |  THE SOFTWARE.
#

# stdlib
from collections.abc import Sequence, Set

# this package
from chemistry_tools.pubchem import API_BASE


def format_string(stringwithmarkup):
	"""
	Convert a PubChem formatted string into an HTML formatted string
	"""

	string = list(stringwithmarkup["String"])
	try:
		markup_list = stringwithmarkup["Markup"]
	except KeyError:
		markup_list = []

	for markup in markup_list:
		style = None
		start = markup["Start"]
		end = markup["Length"] + start - 1
		if markup["Type"] == "Italics":
			style = "i"
		# handle Other formats

		if style is None:
			print(markup)
			continue

		string[start] = f"<{style}>{string[start]}"
		string[end] = f"{string[end]}</{style}>"

	string = ''.join(string)

	return string


def _force_sequence_or_csv(value, name):
	if not value:
		raise ValueError(f"Please supply one or more {name}, either as a comma-separated string or a list of strings.")

	if isinstance(value, str):
		value = value.split(",")

	elif isinstance(value, int):
		value = [str(value)]

	elif isinstance(value, (Sequence, Set)):

		output = []

		for idx, val in enumerate(value):
			if isinstance(val, str):
				output.append(val)
			elif isinstance(val, int):
				output.append(str(val))
			else:
				raise ValueError(f"'{name}' must be either a comma-separated string or a Sequence of strings")

		value = output

	else:
		raise ValueError(f"'{name}' must be either a comma-separated string or a Sequence of strings")

	return value


def _make_base_url(namespace, identifier):

	identifier = _force_sequence_or_csv(identifier, "identifier")
	namespace = str(namespace)
	return f"{API_BASE}/compound/{namespace}/{','.join(identifier)}"
