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
"""Gsrest URL build functions.
"""


# pylint: disable=bad-continuation
def gs_base_url(
    protocol: str = "http",
    host: str = "localhost",
    port: int = 8080,
    context: str = "geoserver",
):
    """Build a base URL for Geoserver: defaults and sanitize.

    Args:
        protocol (str)
        host (str)
        port (int)
        context (str)

    """
    sanitized_context = context.strip("/")
    return f"{protocol}://{host}:{port}/{sanitized_context}"


def gs_relative_url(
    element: str,
    identity=None,
    ext: str = "xml",
    gwc: bool = False,
    **prefixes,
):
    "Simple relative URL for geoserver."
    atom_name = "/{}".format(atom_link_encode(identity)) if identity else ""
    gwc_prefix = "gwc/" if gwc else ""
    wsp_prefix = "".join(
        f"{key}s/{value}/" for key, value in prefixes.items() if value
    )
    extension = f".{ext}" if ext else ""

    return f"{gwc_prefix}rest/{wsp_prefix}{element}s{atom_name}{extension}"


def atom_link_encode(name):
    """Translates the name of an element into atom-link code.

    I have no idea how this translation works, but it is not an standard url
    quotation and e.g. it converts whitespaces into plus signs.

    Args:
        name(str): Name to encode.

    Returns:
        a str with the encoded name.

    """
    # TODO: At the moment, minimal atom link name translation
    return name.replace(" ", "+")
