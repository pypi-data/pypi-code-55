#  !/usr/bin/env python
#   -*- coding: utf-8 -*-
#
#  __init__.py
#
#  Copyright (c) 2019-2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  assay, Atom, Bond, Compound, Constants, Errors, Lookup, Substance and
#  Utils based on PubChemPy by Matt Swain <m.swain@me.com>
#  Available under the MIT License
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


from . import assay
from . import atom
from . import bond
from . import compound
from . import errors
from . import substance
from . import utils


__all__ = [
		"assay",
		"atom",
		"bond",
		"compound",
		"errors",
		"substance",
		"utils",
		]
