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
from ..xml import converter as c
from ..xml import schema as xs


class LayerGroup(e.Element):
    """Geoserver Layer.

    This element only deals with the publishable side of a "geoserver layer".

    At the moment it can only aggregate layers.
    """

    _element_name_aliases = ["layerGroup"]
    _schema = es.ElementSchema(
        name={"on_create": True},
        title={},
        abstract_txt={},
        publishables={
            "path": [
                "publishables",
                {"tag": "published", "many": True, "attr": {"type": "layer"}},
                "name",
            ]
        },
        styles={"path": ["styles", {"tag": "style", "many": True}, "name"]},
        bounds={
            "converter": xs.Schema(
                minx={"converter": c.DoubleConverter},
                maxx={"converter": c.DoubleConverter},
                miny={"converter": c.DoubleConverter},
                maxy={"converter": c.DoubleConverter},
                crs={},
            )
        },
    )
