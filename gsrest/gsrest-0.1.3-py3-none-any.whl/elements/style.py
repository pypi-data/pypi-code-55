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
"""Geoserver catalog style.
"""

from ..core import element as e
from ..core import schema as es
from ..core import traits as t

# Just if needed
RO_IDENTITIES = ["generic", "line", "point", "polygon", "raster"]


class Style(e.Element):
    """Geoserver style.
    """

    _schema = es.ElementSchema(
        name={"on_create": True}, filename={"on_create": True},
    )
    _traits = t.ElementTraits(url_ignore_extension=["post", "delete"])


class Sld10(e.RawElement):
    """Geoserver style data.
    """

    _element_name_xml = "style"
    _crud_policy = t.CrudPolicy.READ | t.CrudPolicy.UPDATE
    _traits = t.ElementTraits(
        url_extension="sld", content_type="application/vnd.ogc.sld+xml"
    )
