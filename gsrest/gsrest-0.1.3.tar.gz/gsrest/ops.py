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
"""Geoserver common operations.
"""

from . import client
from .elements import blobstore, gridset, style, workspace


# pylint: disable=too-few-public-methods
class Ops(client.BaseClient):
    "Common operations"

    @staticmethod
    def purge():
        "Purge everything."
        for wspc in Ops.client.read_all(workspace.WorkSpace):
            wspc.delete(recurse=True)

        for sty in Ops.client.read_all(style.Style):
            if sty.name not in style.RO_IDENTITIES:
                sty.delete()

        for gset in Ops.client.read_all(gridset.GridSet):
            if gset.name not in gridset.RO_IDENTITIES:
                gset.delete()

        for bstr in Ops.client.read_all(blobstore.BlobStore):
            bstr.delete()
