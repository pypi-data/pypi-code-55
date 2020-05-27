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
"""Geoserver catalog coverage.
"""

from ..core import element as e
from ..core import schema as es
from ..core import traits as t
from ..xml import converter as c


class Layer(e.Element):
    """Geoserver Layer.

    This element only deals with the publishable side of a "geoserver layer".

    """

    _crud_policy = t.CrudPolicy.READ | t.CrudPolicy.UPDATE
    _traits = t.ElementTraits(
        workspace_policy=t.WorkSpacePolicy.MUST_HAVE  # type: ignore
    )
    _schema = es.ElementSchema(
        name={"on_create": True},
        default_style={
            "path": "defaultStyle/name",
            "converter": c.ColonLastTokenConverter,
        },
    )
