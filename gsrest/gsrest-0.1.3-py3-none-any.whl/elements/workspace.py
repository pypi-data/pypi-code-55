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
"""Geoserver catalog workspace.
"""

from ..core import element as e
from ..core import schema as es
from ..core import traits as t
from ..xml import converter as c


class StoreWorkSpace(e.RawElement):
    """Geoserver workspace for stores.

    It is just required to recursively delete a workspace.
    """

    _element_name_aliases = ["workspace"]
    _traits = t.ElementTraits(register=False)

    def delete_stores(self):
        "Delete store workspace from client."
        self.client.delete(self, query={"recurse": True})


class WorkSpace(e.Element):
    """Geoserver workspace.
    """

    _element_name_aliases = ["namespace", "workspace"]
    _schema = es.ElementSchema(
        prefix={"on_create": True},
        uri={"on_create": True},
        isolated={"converter": c.BoolConverter},
    )
    _traits = t.ElementTraits(
        identity_attribute="prefix",
        workspace_policy=t.WorkSpacePolicy.NOT_ALLOWED,  # type: ignore
    )

    def delete(self, recurse=False):  # pylint: disable=arguments-differ
        """Delete workspace from client.

        Args:
            recurse: Whether to recurse content of Workspace.

        """
        if recurse:
            StoreWorkSpace(self.identity).delete_stores()
        else:
            self.client.delete(self)
