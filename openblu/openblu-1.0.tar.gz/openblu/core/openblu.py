import requests
from typing import Union
import json
import os
import logging
from ..objects import Server, ServerListing, OpenBluError, UnauthorizedAccess, ServerNotFound
from collections import defaultdict


class OpenBluAPI:
    """Python wrapper around the OpenBlu API

       :param access_key: The access key from the OpenBlu dashboard
       :type access_key: str
       :raises TypeError: If the access key is not a string
    """

    API_ENDPOINT = "https://api.intellivoid.net/openblu/v1"   # API endpoint for OpenBlu
    ERROR_CODES = defaultdict(lambda: OpenBluError, {401: UnauthorizedAccess, 404: ServerNotFound})

    def __init__(self, access_key: str):
        """Object constructor"""

        if not isinstance(access_key, str):
            raise TypeError("access_key must be string!")
        self.access_key = access_key

    def __repr__(self):
        """Implements repr(self)
           Follows the convention that eval(repr(self)) == self
        """

        return f"OpenBluAPI('{self.access_key}')"


    def __str__(self):
        """Implements str(self)"""

        return f"<openblu.OpenBluAPI object at {hex(id(self))}, key='{self.key}'"

    def _raise_exception(self, code: int, message: str):
        """Raises the appropriate exception based on the status code

           :param code: The status code of the request
           :type code: int
        """

        raise self.ERROR_CODES[code](message)

    def get_server(self, uuid: str, verbose: bool = False):
        """Fetches a single OpenVPN server from the OpenBlu API, given its unique ID

	   :param uuid: The unique ID of the desired server
	   :type uuid: string
	   :param verbose: If ``True``, make output verbose, default to ``False``
	   :type verbose: bool, optional
	   :returns: A class:Server object
	   :rtype: class: Server
           :raises OpenBluError: An proper subclass of OpenBluError is raised if something goes wrong. If the error cannot be determined, a generic OpenBluError is raised
        """

        link = self.API_ENDPOINT + "/servers/get"
        if verbose:
            logging.info(f"API key is {self.access_key}")
            logging.info(f"Fetching from {link}...")
        post_data = {}
        post_data["access_key"] = self.access_key
        post_data["id"] = uuid
        response = requests.post(link, data=post_data)
        data = json.loads(response.text)
        if data["response_code"] == 200:
            return Server(data["server"])
        else:
            self._raise_exception(data["response_code"], data["error"]["message"])


    def list_servers(self, filter_by: Union[None, tuple] = None, order_by: Union[None, str] = None, sort_by: Union[None, str] = None, verbose: bool = False):
        """Fetches OpenVPN servers from the OpenBlu API

	   :param filter_by: If not ``None``, filter the results by the given parameter. It must be a tuple containing a country name and either one of these strings (In this order): "country", "country_short". If "country_short" is the second element of the tuple, the country name must be the short form of its name (e.g. 'de' for germany or 'jp' for Japan) otherwise, the full extended form is required. Defaults to ``None``
           :type filter_by: tuple, None, optional
	   :param order_by: If not ``None``, order the results by this order. It can either be ``'ascending'`` or ``'descending'``, defaults to ``None``.
	   :type order_by: str, None, optional
	   :param sort_by: Sorts the list by the given condition, defaults to ``None`` (no sorting). Possible choices are "score", "ping", "sessions", "total_sessions", "last_updated" and "created"
	   :type sort_by: str, None, optional
	   :param verbose: If ``True``, make the output verbose, default to ``False``
	   :type verbose: bool, optional
	   :returns servers_list: A list of class:ServerListing objects
	   :rtype servers_list: list
           :raises OpenBluError: An proper subclass of OpenBluError is raised if something goes wrong. If the error cannot be determined, a generic OpenBluError is raised
        """

        link = self.API_ENDPOINT + "/servers/list"
        if verbose:
            logging.info(f"API key is {self.access_key}")
            logging.info(f"Fetching from {link}...")
        post_data = {}
        post_data["access_key"] = self.access_key
        if filter_by:
            post_data["by"] = filter_by[0]
            post_data["filter"] = filter_by[1]
        if order_by:
            post_data["order_by"] = order_by
        if sort_by:
            post_data["sort_by"] = sort_by
        response = requests.post(link, data=post_data)
        data = json.loads(response.text)
        if data["response_code"] == 200:
            return [ServerListing(server) for server in data["servers"]]
        else:
            self._raise_exception(data["response_code"], data["error"]["message"])

