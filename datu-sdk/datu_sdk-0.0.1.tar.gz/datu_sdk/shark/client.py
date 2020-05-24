"""Datu API.
"""
from typing import Any, Dict, Optional
import os

import requests

from .common.enums import RequestType, RouteType


class Client():
    """API Client: shape the request, submit the request to the server and
    process the response.
    """

    def __init__(self, address: str = 'http://localhost', port: int = 5000):
        """Initializing the DatuClient.
        """
        self.address = address
        self.port = port
        self.server_address = '%s:%d' % (self.address, self.port)

    def send_request(self,
                     request_type: RequestType,
                     route: RouteType,
                     payload: Optional[Dict[str, Any]],
                     files: Optional[Dict[str, Any]] = None
                     ) -> Optional[Dict[str, Any]]:
        """Sending post request to the API server.

        Args:
            request_type: Specify whether it's a POST or GET request.
            route: The name of the route to be handled by the server.
            payload: The JSON payload to be sent off the API server.
            files: Special type for sending file object to API server.
        """
        address = os.path.join(self.server_address, route)
        if request_type == RequestType.POST:
            response = requests.post(address, json=payload, files=files)
        elif request_type == RequestType.GET:
            response = requests.get(address, json=payload)
        else:
            raise ValueError('request_type not supported')

        json_response: Dict[str, Any] = response.json()
        return json_response
