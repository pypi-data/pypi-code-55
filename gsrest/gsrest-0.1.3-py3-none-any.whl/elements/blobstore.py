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
"""Geoserver Web Cache Blob Store.
"""

from ..core import element as e
from ..core import schema as es
from ..core import traits as t
from ..xml import converter as c


class BlobStore(e.Element):
    "GWC BlobStore."

    _element_name_route = "blobstore"
    _element_name_aliases = ["FileBlobStore", "blobstore"]
    # This element is created with a PUT operation.
    _crud_policy = t.CrudPolicy.ALL_BUT_CREATE
    _traits = t.ElementTraits(
        identity_attribute="id",
        workspace_policy=t.WorkSpacePolicy.NOT_ALLOWED,  # type: ignore
        belongs_to_gwc=True,
    )
    _schema = es.ElementSchema(
        id={"on_create": True},
        enabled={"converter": c.BoolConverter, "default": True},
        base_directory={"on_create": True},
        file_system_block_size={
            "default": 4096,
            "converter": c.IntegerConverter,
        },
    )
