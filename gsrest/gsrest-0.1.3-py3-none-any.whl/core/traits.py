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
"""Core element for geoserver entities.
"""

import dataclasses
import enum
import typing

from ..helper import types as helpertypes  # type: ignore


# pylint: disable=too-few-public-methods
class WorkSpacePolicy(helpertypes.OrderedEnum):
    """WorkSpace Policy for Element (Enum type).

    Possible values (self-explanatory):
        - NOT_ALLOWED
        - MAY_HAVE
        - MUST_HAVE
        - EVEN_ON_XML

    """

    NOT_ALLOWED = 1
    MAY_HAVE = 2
    MUST_HAVE = 3
    EVEN_ON_XML = 4


class CrudPolicy(enum.Flag):
    """CRUD Policy for Element (Enum type).

    Possible values (self-explanatory):
        - CREATE
        - READ
        - UPDATE
        - WRITE
        - LIST

    """

    CREATE = enum.auto()
    READ = enum.auto()
    UPDATE = enum.auto()
    DELETE = enum.auto()
    LIST = enum.auto()
    ALL_BUT_CREATE = READ | UPDATE | DELETE | LIST
    ALL = CREATE | READ | UPDATE | DELETE | LIST


def _default_xmlpath_for_listing():
    # cannot set it for a dataclass
    return [{"tag": "{element_name}", "many": True}, "name"]


def _default_url_ignore_extension():
    # cannot set it for a dataclass
    return ["delete"]


# pylint: disable=too-many-instance-attributes
@dataclasses.dataclass
class ElementTraits:
    """Traits for element.

    Args:
        identity_attribute (str): name of the attribute used to identify the
                                  element. Defaults to 'name'.
        workspace_policy (WorkSpacePolicy): See WorkSpacePolicy.
                                            Defaults to MAY_HAVE.
        belongs_to_gwc (bool): Whether this element belongs to GeoWebCache.
                               Defaults to False.
        url_extension (str): Extension to build the URL. Defaults to 'xml'.
        url_ignore_extension (List[str]): http methods where extension should
                                          be ignored. Defaults to ['delete'].
        content_type (str): Content-type to be sent.
                            Defaults to "application/xml".
        xmlpath_for_listing (Any): List of xml path elements, in order to parse
                                   the XML with the listing of all elements.
                                   Use the default value for now.
        register (bool): Whether to add this element to the register.
                         Defaults to True.
    """

    identity_attribute: str = "name"
    workspace_policy: WorkSpacePolicy = WorkSpacePolicy.MAY_HAVE  # type:ignore
    belongs_to_gwc: bool = False
    url_extension: str = "xml"
    url_ignore_extension: typing.List[str] = dataclasses.field(
        default_factory=_default_url_ignore_extension
    )
    content_type: str = "application/xml"
    xmlpath_for_listing: typing.List[typing.Any] = dataclasses.field(
        default_factory=_default_xmlpath_for_listing
    )
    register: bool = True
