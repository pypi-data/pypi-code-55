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
"""Attributes for geoserver entities.
"""

from ..helper import function as helperfun  # type: ignore
from ..xml import converter as c
from ..xml import schema


class ElementSchemaItem(schema.SchemaItem):
    """Metadata for every attribute in a geoserver element.

    Args:
        path: something that converts to XmlPathElement list
        converter: xml data converter
        default: default data value
        on_create: whether this attribute is mandatory for element creation.

    """

    # pylint: disable=bad-continuation
    def __init__(
        self, path, converter=c.StringConverter, default=None, on_create=False,
    ):
        super().__init__(path, converter=converter, default=default)
        self.on_create = on_create


class ElementSchema(schema.Schema):  # pylint: disable=too-many-ancestors
    "General Geoserver element attribute schema."

    @staticmethod
    def _parse_attr(key, value):
        if isinstance(value, ElementSchemaItem):
            return value
        if isinstance(value, dict):
            if "path" not in value:
                return ElementSchemaItem(
                    path=helperfun.camelcase(key), **value
                )
            return ElementSchemaItem(**value)
        raise Exception("Cannot convert to ElementSchemaItem.")


# pylint: disable=too-many-ancestors
class ElementSchemaData(schema.SchemaData):
    "Attributes of a Geoserver element."

    def to_node(self, node):
        """Push data to XML node.

        Args:
            node(XmlElement): parent node to push data to

        """
        self._schema.to_node(self, node)

    @property
    def enough(self):
        "Whether all create attributes have an effective value."
        return all(
            value for key, value in self.items() if self._schema[key].on_create
        )
