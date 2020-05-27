# -*- coding: utf-8 -*-
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
"""Core classes for geoserver entities.

In particular, it provides the Element class which other element classes derive
from.

"""


import typing


class GsElementTypeError(Exception):
    "Unkwown element type."


class ElementRegistry:
    "Registry of available elements."
    _registry: typing.Dict[str, typing.Any] = {}

    @classmethod
    def add(cls, klass):
        "Add class to element registry."
        # pylint: disable=protected-access
        for alias in klass._element_name_aliases:
            cls._registry[alias.lower()] = klass

    @classmethod
    def list(cls):
        "Get list of registered elements."
        return cls._registry

    @classmethod
    def get(cls, alias):
        "Get registered element from alias."
        if alias not in cls._registry:
            raise GsElementTypeError
        return cls._registry[alias]
