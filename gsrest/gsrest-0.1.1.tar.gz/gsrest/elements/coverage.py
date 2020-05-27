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
from ..xml import schema as xs


class Coverage(e.Element):
    """Geoserver coverage store.
    """

    _traits = t.ElementTraits(
        workspace_policy=t.WorkSpacePolicy.MUST_HAVE  # type: ignore
    )
    _schema = es.ElementSchema(
        name={"on_create": True},
        store={
            "path": "store/name",
            "on_create": True,
            # sometimes, I get a 'workspace:store'
            "converter": c.ColonLastTokenConverter,
        },
        native_name={"on_create": True},
        title={},
        abstract={},
        enabled={"converter": c.BoolConverter, "default": True},
        advertised={"converter": c.BoolConverter, "default": True},
        # For some reason, dimensions are not always present.
        # They require the bands data to be loaded.
        # Anyway, they can be pushed to the server.
        dimensions={
            "path": ["dimensions", {"tag": "coverageDimension", "many": True}],
            "converter": xs.Schema(
                name={},
                description={},
                range={
                    "converter": xs.Schema(
                        min={"converter": c.DoubleConverter},
                        max={"converter": c.DoubleConverter},
                    ),
                },
                null_values={
                    "path": ["nullValues", {"tag": "double", "many": True}],
                    "converter": c.DoubleConverter,
                },
                dimension_type={"path": "dimensionType/name"},
                units={},
            ),
        },
    )

    def route(self, method="GET", anonymous=False):
        """Relative route for this element as a string.

        Args:
            method(str): route may depend on http method
            anonymous(bool): Whether to build an anonymous route.

        Returns:
            Relative url string.

        """
        prefixes = {"workspace": self.workspace}
        if method.lower() == "put":
            # pylint: disable=no-member
            prefixes.update({"coveragestore": self.store})
        return self.build_route(
            name="" if anonymous else self.identity, method=method, **prefixes,
        )
