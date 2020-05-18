#!/usr/bin/env python3
#
#  utils.py
"""
General utilities.
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
import types
from collections import namedtuple, OrderedDict
from collections.abc import ItemsView, Mapping
from itertools import product


def identity(x):
	return x


def defaultnamedtuple(typename, field_names, defaults=()):
	"""
	Generates a new subclass of tuple with default values.

	Parameters
	----------
	typename : string
		The name of the class.
	field_names : str or iterable
		An iterable of splitable string.
	defaults : iterable
		Default values for ``field_names``, counting ``[-len(defaults):]``.

	Examples
	--------
	>>> Body = defaultnamedtuple('Body', 'x y z density', (1.0,))
	>>> Body.__doc__
	'Body(x, y, z, density)'
	>>> b = Body(10, z=3, y=5)
	>>> b._asdict() == dict(x=10, y=5, z=3, density=1.0)
	True

	Returns
	-------
	A new tuple subclass named ``typename``
	"""

	Tuple = namedtuple(typename, field_names)
	Tuple.__new__.__defaults__ = (None,) * len(Tuple._fields)
	if isinstance(defaults, Mapping):
		Tuple.__new__.__defaults__ = tuple(Tuple(**defaults))
	else:
		nmissing = len(Tuple._fields) - len(defaults)
		defaults = (None,) * nmissing + tuple(defaults)
		Tuple.__new__.__defaults__ = tuple(Tuple(*defaults))
	return Tuple
