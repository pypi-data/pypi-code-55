"""
This is the interface for interacting with the GradePage Web Service.
"""

from uw_gradepage.dao import GradePage_DAO
from restclients_core.exceptions import DataFailureException
import json


def get_resource(url, headers={}):
    response = GradePage_DAO().getURL(url, headers)

    if response.status != 200:
        raise DataFailureException(url, response.status, response.data)

    return json.loads(response.data)
