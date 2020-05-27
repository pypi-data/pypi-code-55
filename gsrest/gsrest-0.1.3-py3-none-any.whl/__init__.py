#
# Copyright (c) 2020 Instituto Tecnológico de Canarias, S.A.
#
# This file is part of GsRest
# (see https://github.com/esuarezsantana/gsrest).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
"""Geoserver Rest API Client.
"""
__version__ = "0.1.3"

import logging

from .elements import *  # noqa: F401,F403

# pylint: disable=unused-wildcard-import, wildcard-import
# Previous wildcard import is required
# to register all elements into the ElementRegistry.
# For some reason 'pylint disable' and black work together fine here,
# but it whines when importing elements is moved to '..core.registry'.

logging.getLogger(__name__).addHandler(logging.NullHandler())
