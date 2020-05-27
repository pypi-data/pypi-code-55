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
"""Geoserver rest API client.
"""

import logging
import typing
from urllib import error as urlerr

from .core import connect, url
from .helper import decorator  # type: ignore

_LOGGER = logging.getLogger(__name__)


class GsUpstreamUndefined(Exception):
    "When geoserver client has not been defined."


class GsElementAlreadyExists(Exception):
    "When trying to create an element that already exists."


class GsElementDoesNotExist(Exception):
    "When trying to operate on an element that does not exist."


class GsElementMissingInfo(Exception):
    "When trying to create an element but not all required info is available."


class GsPolicyViolation(Exception):
    "Crud Forbidden Operation."


class GsClient:
    """GeoServer API Rest Client.

    This class provides the main client interaction with a Geoserver instance.

    """

    def __init__(self):
        self._base_url = url.gs_base_url()
        self._username = "admin"
        self._password = "geoserver"
        self._update_connect()
        # Update client for all elements!
        BaseClient.client = self

    @property
    def username(self):
        "Username to connect to geoserver."
        return self._username

    @username.setter
    def username(self, username):
        self._username = username
        self._update_connect()

    @property
    def password(self):
        "Password to connect to geoserver."
        return self._password

    @password.setter
    def password(self, password):
        self._password = password
        self._update_connect()

    @property
    def base_url(self):
        """Geoserver base url.

        Example: http://localhost:8080/geoserver

        """
        return self._base_url

    @base_url.setter
    def base_url(self, base_url):
        self._base_url = base_url
        self._update_connect()

    def _update_connect(self):
        self._connect = connect.Connect(
            base_url=self._base_url,
            username=self._username,
            password=self._password,
        )

    def ready(self):
        "Whether the client is ready to be used (server available)."
        return self._connect.available

    def _get(self, *args, **kwargs):
        return self._connect.http(
            connect.RequestParams(*args, method="GET", **kwargs)
        )

    def _post(self, *args, **kwargs):
        return self._connect.http(
            connect.RequestParams(*args, method="POST", **kwargs)
        )

    def _put(self, *args, **kwargs):
        return self._connect.http(
            connect.RequestParams(*args, method="PUT", **kwargs)
        )

    def _delete(self, *args, **kwargs):
        return self._connect.http(
            connect.RequestParams(*args, method="DELETE", **kwargs)
        )

    def list(self, cls, **route_args):
        """Get list of names of available elements.

        Args
            cls (type): Class of element to be retrieven.
            route_args: Any additional route args as workspace.

        Returns:
            list of strings with names of elements

        """
        _LOGGER.info("Getting list for %s", cls.__name__)
        resp = self._get(route=cls.build_route(method="GET", **route_args))
        _LOGGER.debug(resp)
        return cls.list_names_from_xml_stream(resp)

    def create(self, elem, query=None):
        """Create new element (POST).

        Post method allows to create a new element in the catalog. Since post
        method is not idempotent, this method won't work to update an existing
        element.

        Args:
            elem (Element): An geoserver element.
            query (dict): extra arguments for the query

        Raises:
            GsElementMissingInfo: not enough element attrs
            GsElementAlreadyExists: element already exists
            HTTPError: something went wrong
                       (maybe we did not detect missing info)

        """
        if not elem.ready():
            raise GsElementMissingInfo
        try:
            self._post(
                route=elem.route(method="POST", anonymous=True),
                data=elem.content,
                headers={"Content-Type": elem.content_type},
                query=(query if query else {}),
            )
        except urlerr.HTTPError as err:
            # pylint: disable=bad-continuation
            if err.code == 500 and elem.identity in self.list(
                elem.__class__, workspace=elem.workspace,
            ):
                raise GsElementAlreadyExists(err.msg)
            with err:
                raise Exception(err.read())

    def read(self, obj, name=None, query=None, **route_args):
        """Read an element into a new element (may populate unknown attrs).

        Accepts both an instance of an element object or a class of an element.
        If an element instance is passed, then a new element object will be
        created from the identity of the former.

        Args:
            obj (Element|type): An element object or a class.
            name (str): If obj is a class, this argument is required to
                        identify the element. If obj is an element (instance),
                        this argument is ignored.
            query (dict): extra arguments for the query
            **route_args: If obj is a class, any additional route args required
                          by some elements, like the workspace. Some elements
                          may use it to build a route, e.g. coverages.

        Returns:
            Element: The requested element.

        Raises:
            GsElementDoesNotExist: when element does not exist

        """
        klass, route, identity, workspace = (
            (
                obj,
                obj.build_route(name, method="GET", **route_args),
                name,
                route_args.get("workspace", None),
            )
            if isinstance(obj, type)
            else (
                obj.__class__,
                obj.route(method="GET"),
                obj.identity,
                obj.workspace,
            )
        )
        try:
            resp = self._get(
                route=route,
                headers={"Content-Type": obj.content_type},
                query=(query if query else {}),
            )
        except urlerr.HTTPError as err:
            if err.code == 404:
                raise GsElementDoesNotExist
            with err:
                raise Exception(err.read())
        _LOGGER.debug(resp)
        return klass(identity=identity, content=resp, workspace=workspace)

    def read_all(self, cls, **route_args):
        """Get all available elements.

        Args
            cls (type): Class of element to be retrieved.
            route_args: Any additional route args required by some elements.
                        Some elements may use it to build a route, e.g.
                        coverages.

        Returns:
            list of elements

        """
        return [
            self.read(cls, name, **route_args)
            for name in self.list(cls, **route_args)
        ]

    def update(self, elem, query=None):
        """Updates an existing element or its data (PUT).

        Data elements are data attached to common geoserver elements.

        Update never uses extra route args, cause the element already exist and
        must have a full knowledge of its route.

        Args:
            elem (Element|ElementData): An geoserver element or its data.
            query (dict): extra arguments for the query

        Returns:
            The updated element (may have more attributes).

        Raises:
            GsElementDoesNotExist: when element does not exist

        """
        try:
            self._put(
                route=elem.route(method="PUT"),
                data=elem.content,
                headers={"Content-Type": elem.content_type},
                query=(query if query else {}),
            )
        except urlerr.HTTPError as err:
            if err.code == 404:
                raise GsElementDoesNotExist
            with err:
                raise Exception(err.read())

    def delete(self, obj, name=None, query=None, **route_args):
        """Delete an element.

        Accepts both an instance of an element object or a class of an element.

        Args:
            obj (Element|type): An element object or a class.
            name (str): If obj is a class, this argument is required to
                        identify the element. If obj is an element (instance),
                        this argument is ignored.
            query (dict): extra arguments for the query
            **route_args: If obj is a class, any additional route args required
                          by some elements, e.g. a workspace. Some elements may
                          use other arguments, e.g. coverages.

        Raises:
            GsElementDoesNotExist: when element does not exist

        """
        route = (
            obj.build_route(name, method="DELETE", **route_args)
            if isinstance(obj, type)
            else obj.route(method="DELETE")
        )
        try:
            self._delete(route=route, query=(query if query else {}))
        except urlerr.HTTPError as err:
            if err.code == 404:
                raise GsElementDoesNotExist
            with err:
                raise Exception(err.read())


# pylint: disable=too-few-public-methods
class BaseClient:
    """Dummy client for a better design.

    This avoid circular import dependencies.

    """

    # 'client' will be updated by GsClient itself
    client: typing.Optional[GsClient] = None
