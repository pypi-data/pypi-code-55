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
"""Geoserver Web Cache Grid Set.
"""

from ..core import element as e
from ..core import schema as es
from ..core import traits as t
from ..xml import converter as c

# Just if needed
RO_IDENTITIES = [
    "GlobalCRS84Pixel",
    "EPSG:4326",
    "GoogleCRS84Quad",
    "EPSG:900913",
    "GlobalCRS84Scale",
]


class GridSet(e.Element):
    "GWC GridSet."

    _element_name_aliases = ["gridSet"]
    # This element is created with a PUT operation.
    _crud_policy = t.CrudPolicy.ALL_BUT_CREATE
    _traits = t.ElementTraits(
        workspace_policy=t.WorkSpacePolicy.NOT_ALLOWED,  # type: ignore
        belongs_to_gwc=True,
    )
    _schema = es.ElementSchema(
        name={"on_create": True},
        description={},
        srs_number={"path": "srs/number", "converter": c.IntegerConverter},
        extent_coords={
            "path": ["extent", "coords", {"tag": "double", "many": True}],
            "converter": c.DoubleConverter,
        },
        align_top_left={"converter": c.BoolConverter},
        resolutions={
            "path": ["resolutions", {"tag": "double", "many": True}],
            "converter": c.DoubleConverter,
        },
        meters_per_unit={"converter": c.DoubleConverter},
        pixel_size={"converter": c.DoubleConverter},
        scale_names={"path": ["scaleNames", {"tag": "string", "many": True}]},
        tile_height={"converter": c.IntegerConverter},
        tile_width={"converter": c.IntegerConverter},
        y_coordinate_first={"converter": c.BoolConverter},
    )
