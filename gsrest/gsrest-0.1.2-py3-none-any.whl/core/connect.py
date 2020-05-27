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
"""Connection management with Geoserver instance.
"""

import base64
import dataclasses
import pprint
import typing as tp
import urllib.error as urlerr
import urllib.parse as urlparse
import urllib.request as urlreq

from ..core import url
from ..helper import logger  # type: ignore
from ..xml import converter, schema


def _content_type_xml():
    """Content-Type header for xml.

    This function is just to avoid passing a mutable object as a default value.

    """
    return {"Content-Type": "application/xml"}


@dataclasses.dataclass
class RequestParams:
    """Request parameters abstraction.

    Args:
        route (str): Suffix route string to append to Geoserver base URL.
        data (bytes): Request body.
        method (str): Uppercase HTTP method. Defaults to 'GET'.
        headers (dict): Request headers dict.
                        Defaults to {'Content-Type': 'application/xml').
        query (dict): Url query dict.

    """

    route: str
    data: bytes = b""
    method: str = "GET"
    headers: tp.Dict = dataclasses.field(default_factory=_content_type_xml)
    query: tp.Dict = dataclasses.field(default_factory=dict)

    def copy(self):
        "Copy itself."
        return RequestParams(**dataclasses.asdict(self))

    def url(self, baseurl):
        "Build an url."
        urlquery = (
            "?{}".format(urlparse.urlencode(self.query)) if self.query else ""
        )
        return f"{baseurl}/{self.route}{urlquery}"

    def as_dict(self, baseurl):
        "Return a dict from a base url."
        return dict(
            url=self.url(baseurl),
            data=self.data,
            headers=self.headers,
            method=self.method,
        )

    def request(self, baseurl):
        "Return urllib Request"
        return urlreq.Request(**self.as_dict(baseurl))

    def curl_str(self, baseurl):
        "Curl string."
        header_str = "".join(
            " -H '{}: {}'".format(k, v) for k, v in self.headers.items()
        )
        # pylint: disable=no-member
        return "curl{} -X {} {}".format(
            header_str, self.method, self.url(baseurl)
        )

    def pprint(self, baseurl):
        "Pretty print as dict."
        return pprint.PrettyPrinter().pformat(self.as_dict(baseurl))


@dataclasses.dataclass
class Connect(metaclass=logger.MetaLogger):
    """Connection management with Geoserver instance.

    Args:
        base_url (str): Base URL to locate a Geoserver instance.
                        Only HTTP has been tested.
        username (str): Geoserver username.
        password (str): Geoserver password

    Attributes:
        base_url (str): Base URL to locate a Geoserver instance.
        username (str): Geoserver username.
        password (str): Geoserver password.

    """

    base_url: str = dataclasses.field(default_factory=url.gs_base_url)
    username: str = "admin"
    password: str = "geoserver"

    def _user_pass_auth_header(self):
        "Generates the auth string for the authorization header."
        valid_uname_pw = base64.b64encode(
            ("%s:%s" % (self.username, self.password)).encode("utf-8")
        ).decode("ascii")
        return {"Authorization": f"Basic {valid_uname_pw}"}

    # do not 'headers={}', cause '{}' is somehow "mutable"
    def http(self, request_params):
        """Http request.

        Args:
            request (RequestParameters): Http Request.

        Returns:
            The content of the HTTP response.

        """
        if not self.base_url.startswith("http"):
            raise ValueError("Url must start with 'http'")
        req = request_params.copy()
        my_auth_header = self._user_pass_auth_header()
        req.headers = {**my_auth_header, **req.headers}
        # pylint: disable=no-member
        Connect.__logger.debug(req.curl_str(self.base_url))
        Connect.__logger.debug(req.pprint(self.base_url))
        with urlreq.urlopen(req.request(self.base_url)) as request:  # nosec
            content = request.read().decode("utf-8")
        return content

    @property
    def available(self):
        """Test whether geoserver is responsive.

        It will perform a parse test to the system-status request.

        """
        status_req = RequestParams(route="rest/about/system-status.xml")
        try:
            status_xml = self.http(status_req)
        except (ConnectionResetError, urlerr.URLError):
            return False
        status_reduced_schema = schema.Schema(
            available={
                "path": [
                    {"tag": "metric", "many": True},
                    "available",
                ],  # parser never takes into account xml root ('metrics')
                "converter": converter.BoolConverter,
            }
        )
        try:
            parse_data = status_reduced_schema.from_bytes(status_xml)
        except ValueError:
            # BoolConverter raises ValueError if it does not find a valid bool
            # string.
            raise Exception("A boolean string (true/false) was expected.")
        # passthrough other exceptions
        return ("available" in parse_data) and (
            parse_data["available"] is not None
        )
