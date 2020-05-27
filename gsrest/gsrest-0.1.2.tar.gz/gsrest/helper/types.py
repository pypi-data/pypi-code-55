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
"""Helper types for the gsrest package.
"""

import enum


class OrderedEnum(enum.Enum):
    """Ordered Enum without using EnumInt.

    See https://docs.python.org/3/library/enum.html#orderedenum

    """
    # pylint: disable=comparison-with-callable
    def __ge__(self, other):
        if self.__class__ is other.__class__:
            return self.value >= other.value
        return NotImplemented

    def __gt__(self, other):
        if self.__class__ is other.__class__:
            return self.value > other.value
        return NotImplemented

    def __le__(self, other):
        if self.__class__ is other.__class__:
            return self.value <= other.value
        return NotImplemented

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented
