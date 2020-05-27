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
"""Geoserver Web Cache Layer.
"""

from ..core import element as e
from ..core import schema as es
from ..core import traits as t
from ..xml import converter as c


class GwcLayer(e.Element):
    "GWC Layer."

    _element_name_xml = "GeoServerLayer"
    _element_name_route = "layer"
    # This element is created with a PUT operation.
    _crud_policy = t.CrudPolicy.ALL_BUT_CREATE
    _traits = t.ElementTraits(
        workspace_policy=t.WorkSpacePolicy.NOT_ALLOWED,  # type: ignore
        belongs_to_gwc=True,
    )
    _schema = es.ElementSchema(
        name={"on_create": True},
        enabled={"converter": c.BoolConverter, "default": True},
        in_memory_cached={"converter": c.BoolConverter},
        blob_store_id={},
        mime_formats={
            "path": ["mimeFormats", {"tag": "string", "many": True}]
        },
        grid_subsets={
            "path": [
                "gridSubsets",
                {"tag": "gridSubset", "many": True},
                "gridSetName",
            ]
        },
        meta_width_height={
            "path": ["metaWidthHeight", {"tag": "int", "many": True}],
            "converter": c.IntegerConverter,
        },
        expire_cache={"converter": c.IntegerConverter},
        expire_clients={"converter": c.IntegerConverter},
        gutter={"converter": c.IntegerConverter},
    )
