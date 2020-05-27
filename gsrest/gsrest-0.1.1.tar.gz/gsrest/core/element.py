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

import typing

from .. import client
from ..helper import function as helperfun  # type: ignore
from ..xml import io
from . import registry, schema, traits, url


class ClientElement(client.BaseClient):
    """Logic for element/client interaction.

    To derive the client element class, subclasses may define the following
    variables:
        - _element_name_aliases: List of element name aliases for the registry,
                                 which will lowercase them before adding them.
                                 Defaults to the subclass name lowercased.
                                 Besides, the first element will be used to
                                 build the route and as root tag for the xml.
                                 Example: ["namespace", "workspace"]
        - _traits: The ElementTraits that defines the element behaviour.
        - _crud_policy (CrudPolicy): Enum of allowed CRUD operations.
                                     Defaults to all operations.

    """

    # Do not override _element_name_{route,xml} in subclasses unless required,
    # better set _element_name_aliases.
    _element_name_xml: typing.Optional[str] = None
    _element_name_route: typing.Optional[str] = None
    _element_name_aliases: typing.List[str] = []
    _traits: traits.ElementTraits = traits.ElementTraits()
    _crud_policy: traits.CrudPolicy = traits.CrudPolicy.ALL

    def __init__(self, identity=None, workspace=None):
        """Initializer.

        Args:
            identity(str): The identity (i.e. name) of the element instance.
            workspace(str): The workspace (optional).

        """
        self.identity = identity
        self.workspace = workspace

    @property
    def identity(self):
        "Identity attribute getter."
        return self._identity

    @identity.setter
    def identity(self, value):
        "Identity attribute setter."
        self._identity = value

    @property
    def full_identity(self):
        "Full identity string (with workspace if required)."
        return (
            (f"{self.workspace}:" if self.workspace else "ROOT:")
            if self._traits.workspace_policy
            > traits.WorkSpacePolicy.NOT_ALLOWED
            else ""
        ) + self.identity

    def _update_from(self, element):
        """Abstract method used when syncing from a new element."""

    def ready(self):
        """Check for availability to create."""

    def sync(self, down=False):
        """Sync up. Will sync with server, with priority for local attrs.

        This method exists because it may be specialized by subclasses.

        Args:
            down(bool): Whether to give priority to remote object.
                        Defaults to False, i.e. priority to local object.

        """

        def _sync_up():
            if self._crud_policy & traits.CrudPolicy.CREATE:
                try:
                    self.client.create(self)  # pylint: disable=no-member
                except client.GsElementAlreadyExists:
                    pass
                else:
                    return
            if self._crud_policy & traits.CrudPolicy.UPDATE:
                self.client.update(self)  # pylint: disable=no-member
            else:
                raise client.GsPolicyViolation

        def _sync_down():
            if self._crud_policy & traits.CrudPolicy.READ:
                try:
                    # pylint: disable=no-member
                    newself = self.client.read(self)
                except client.GsElementDoesNotExist:
                    # then sync up
                    pass
                else:
                    self._update_from(newself)
                    return
            else:
                raise client.GsPolicyViolation

        if not self.client:
            raise client.GsUpstreamUndefined
        if down and _sync_down():
            return
        if not self.ready():
            raise client.GsElementMissingInfo
        _sync_up()
        try:
            _sync_down()
        except client.GsPolicyViolation:
            pass

    def delete(self):
        """Delete element from client.

        This method exists because it may be specialized by subclasses.

        """
        self.client.delete(self)  # pylint: disable=too-many-function-args

    @classmethod
    def list(cls, **route_args):
        """List names of elements in server.

        Args
            cls (type): Class of element to be retrieven.
            **route_args: Any additional route args as workspace.

        Returns:
            list of strings with names of elements

        """
        return cls.client.list(cls, **route_args)

    @classmethod
    def build_route(cls, name="", method="GET", **prefixes):
        """Relative route for this class or for an element.

        Args:
            name(str): The name of the element
            method(str): route may depend on http method
            **prefixes: dict of prefixes to build the route

        Returns:
            Relative url string.
        """
        extension = (
            ""
            if method.lower() in cls._traits.url_ignore_extension
            else cls._traits.url_extension
        )
        return url.gs_relative_url(
            element=cls._element_name_route,
            identity=name,
            ext=extension,
            gwc=cls._traits.belongs_to_gwc,
            **prefixes,
        )

    def route(self, method="GET", anonymous=False):
        """Relative route for this element as a string.

        Args:
            method(str): route may depend on http method
            anonymous(bool): Whether to build an anonymous route.

        Returns:
            Relative url string.

        """
        return self.build_route(
            name="" if anonymous else self.identity,
            method=method,
            workspace=self.workspace,
        )

    @classmethod
    def list_names_from_xml_stream(cls, xml_stream):
        """Parse XML with list of elements into a list of names.

        Args:
            xml_stream (bytes): the xml stream.

        Returns:
            A list of names.

        """
        xpe_list = io.XmlPathElement.from_list(cls._traits.xmlpath_for_listing)
        for xpe in xpe_list:
            xpe.tagformat(element_name=cls._element_name_xml)
        return io.XmlAccessor(xpe_list).read_from_bytes(xml_stream)


class RawElement(ClientElement):
    """Element abstract class to be derived for raw geoserver elements.

    Raw elements require an identity to deal with, and some content to R/W.

    See __init__ doc for invocation args.

    """

    def __init__(self, identity=None, content=None, workspace=None):
        """Initializer."
        super().__init__()

        Args:
            identity(str): The identity (e.g. name) of the element instance.
            content(bytes): XML content of the element.
            workspace(str): The workspace (optional, depends on element).

        For RawElements, identity and content and independent attributes.

        """
        self.content = content
        super().__init__(identity=identity, workspace=workspace)

    def __init_subclass__(cls, **kwargs):
        "Register subclasses into Registry."
        # default name and aliases
        helperfun.set_if_missing(
            cls, "_element_name_aliases", [cls.__name__.lower()]
        )
        # pylint: disable=unsubscriptable-object
        helperfun.set_if_missing(
            cls, "_element_name_xml", cls._element_name_aliases[0]
        )
        helperfun.set_if_missing(
            cls, "_element_name_route", cls._element_name_xml.lower()
        )
        # direct access for external usage
        cls.content_type = cls._traits.content_type
        # add to registry
        if cls._traits.register:
            registry.ElementRegistry.add(cls)
        super().__init_subclass__(**kwargs)

    @property
    def content(self):
        "Content getter"
        if isinstance(self._content, str):
            return self._content.encode("utf-8")
        return bytes(self._content)

    @content.setter
    def content(self, bytestream):
        "Content setter"
        self._content = bytestream

    def __str__(self):
        lcontent = len(bytes(self.content))
        return f"{self.__class__.__name__}('{self.full_identity}'[{lcontent}])"

    __repr__ = __str__
    fullstr = __str__

    def __eq__(self, other):
        return (
            self.identity == other.identity
            and self.workspace == self.workspace
            and self.content == self.content
        )

    def ready(self):
        "Whether all create attributes have an effective value."
        return bool(
            self.identity
            and self.content
            and (
                self._traits.workspace_policy
                <= traits.WorkSpacePolicy.MAY_HAVE
                or self.workspace
            )
        )

    def _update_from(self, element):
        self.content = element.content


class Element(ClientElement):
    """Element abstract class to be derived for geoserver elements.

    See __init__ doc for invocation args.

    To derive the element class, subclasses may define the RawElement
    subclasses, and:

        - _schema: The ElementSchema for the attributes of this element.

    """

    _schema: schema.ElementSchema = schema.ElementSchema()

    # pylint: disable=super-init-not-called
    def __init__(self, identity=None, content=None, **kwargs):
        """Initializer.

        Args:
            identity(str) : The identity (e.g. name) of the instance.
                            It will be redirected to an element attribute.
                            Takes precedence over content and kwargs.
            content(bytes) : XML content to be imported.
            **kwargs: If the element admits a workspace, it will be taken from
                      the named args. The remaining named args will be
                      processed afterwards, setting the attributes of the
                      element from the named arg.
                      Takes precedence over content.

        Warning: 'content', 'identity' and 'workspace' are special keywords not
        meant to be present in attributes.

        For an Element class, identity will already included in content.

        """
        if content:
            self.content = content
        else:
            self.attrs = schema.ElementSchemaData(self._schema)
        # take 'workspace' out of kwargs
        workspace = kwargs.pop("workspace", None)
        # pylint: disable=bad-continuation
        if workspace and (
            self._traits.workspace_policy == traits.WorkSpacePolicy.NOT_ALLOWED
        ):
            raise client.GsPolicyViolation
        self.attrs.update(kwargs)
        final_identity = identity if identity else self.identity
        super().__init__(identity=final_identity, workspace=workspace)

    # The __init_subclass__ is enough in this case, so there is no need
    # - to init in a metaclass
    # - to decorate the class
    @classmethod
    def __init_subclass__(cls, **kwargs):
        """Prepare geoserver elements.

        - Turn element attributes into properties.
        - Set some defaults.
        - Register element into Registry.

        """
        # properties
        for sub in cls._schema.keys():  # pylint: disable=no-member
            setattr(cls, sub, property(*helperfun.subaccessors("attrs", sub)))
        # default name and aliases
        helperfun.set_if_missing(
            cls, "_element_name_aliases", [cls.__name__.lower()]
        )
        # pylint: disable=unsubscriptable-object
        helperfun.set_if_missing(
            cls, "_element_name_xml", cls._element_name_aliases[0]
        )
        helperfun.set_if_missing(
            cls, "_element_name_route", cls._element_name_xml.lower()
        )
        # direct access for external usage
        cls.content_type = cls._traits.content_type
        # add to registry
        if cls._traits.register:
            registry.ElementRegistry.add(cls)
        super().__init_subclass__(**kwargs)

    @property
    def identity(self):
        "Identity string."
        return self.attrs[self._traits.identity_attribute]

    @identity.setter
    def identity(self, value):
        "Identity string setter."
        self.attrs[self._traits.identity_attribute] = value

    @property
    def content(self):
        "Content ready to create"
        return bytes(self.xml())

    @content.setter
    def content(self, value):
        """Parse content.

        Will not modify the workspace.

        """
        newself = self.from_xml_stream(value)
        self.attrs = newself.attrs

    def __str__(self):
        return f"{self.__class__.__name__}('{self.full_identity}')"

    __repr__ = __str__

    def fullstr(self):
        "Get a full dump (for debugging)."
        workspace_name = self.workspace if self.workspace else "ROOT"
        return (
            f"{self.__class__.__name__}@{workspace_name}"
            f"({self.attrs.attr_str()})"
        )

    def __eq__(self, other):
        return self.attrs == other.attrs and self.workspace == other.workspace

    def ready(self):
        "Whether all create attributes have an effective value."
        return bool(
            self.attrs.enough
            and (
                self._traits.workspace_policy
                <= traits.WorkSpacePolicy.MAY_HAVE
                or self.workspace
            )
        )

    def _update_from(self, element):
        self.attrs = element.attrs

    def xml(self):
        """Creates an XML from the element.

        Returns:
            An XMLBuider object already populated.

        """
        builder = io.XmlBuilder(self._element_name_xml)
        self.attrs.to_node(builder.tree)
        if self._traits.workspace_policy >= traits.WorkSpacePolicy.EVEN_ON_XML:
            builder.write(self.workspace, path="workspace/name")

        return builder

    @classmethod
    def from_xml_stream(cls, xml_stream, workspace=None):
        """Factory to create an element from an xml tree.

        Args:
            xml_stream (bytes): the xml stream.
            workspace (str): workspace

        Returns:
            A new object of the type of the class.

        """
        # pylint: disable=no-member
        attr_dkt = cls._schema.from_bytes(xml_stream)
        if cls._traits.workspace_policy >= traits.WorkSpacePolicy.MAY_HAVE:
            attr_dkt.update({"workspace": workspace})

        return cls(**attr_dkt)
