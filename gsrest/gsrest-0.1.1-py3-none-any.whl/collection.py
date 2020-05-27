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
"""Geoserver element collection.
"""

from collections import abc as abccl

from .core import element


# pylint: disable=too-many-ancestors
class ElementCollection(abccl.MutableSequence):
    "A simple list of Geoserver elements."

    def __init__(self, *args):
        self._elems = list(args)

    def __getitem__(self, index):
        return self._elems.__getitem__(index)

    def __setitem__(self, index, value):
        self._assert_type(value)
        self._elems.__setitem__(index, value)

    def __delitem__(self, index):
        self._elems.__delitem__(index)

    def __len__(self):
        return len(self._elems)

    @staticmethod
    def _assert_type(value):
        if not isinstance(value, element.ClientElement):
            raise ValueError

    def insert(self, index, value):
        self._assert_type(value)
        self._elems.insert(index, value)

    def sync(self, down=False):
        "Sync all elements."
        for item in self:
            item.sync(down)

    def delete(self):
        "Delete all elements."
        for item in self:
            item.delete()
