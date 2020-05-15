"""
Internal base utilities.
"""

from typing import Optional, Tuple, Any, Sequence
from json.decoder import JSONDecodeError

import time
import requests
from .exceptions import BaseXToolsException, NotFound, TooManyEdits

BASE_URL = "https://xtools.wmflabs.org/api"
START_TIME = "2000-01-01"
END_TIME = "2050-12-31"


def url(path: str) -> str:
    """
    Return a full API URL.
    :param path:
    :return:
    """
    return BASE_URL + path


def error_exception(response: dict) -> Optional[BaseXToolsException]:
    """
    Return an optional Exception instance for an error response. Return ``None`` if the given response is not an error.
    :param response: response from the API.
    :return: ``None`` or a ``BaseXToolsException`` (or subclass) instance.
    """
    if "error" not in response:
        return

    error = response["error"]

    # 'error' can be a dict or a string
    if isinstance(error, dict):
        code = error["code"]
        if code == 404:
            return NotFound(error["message"])

        return BaseXToolsException(error["message"], code)

    if error.startswith("No matching result") \
            or error.endswith("is not a valid project") \
            or error == "The requested user does not exist":
        return NotFound(error)

    if error.startswith("User has made too many edits!"):
        return TooManyEdits(error)

    return BaseXToolsException(str(error))


def get(path: str, params=None, retry=3, retry_delay=1):
    """
    Perform a GET request against the API.
    :param path:
    :param params:
    :param retry:
    :param retry_delay:
    :return:
    """
    r = requests.get(url(path), params=params)
    # 'Proxy error'
    if r.status_code == 502:
        if retry > 0:
            time.sleep(retry_delay)
            return get(path, params, retry - 1)
        r.raise_for_status()

    try:
        response = r.json()
    except JSONDecodeError as e:
        r.raise_for_status()
        raise e

    exception = error_exception(response)
    if exception:
        raise exception
    return response


def build_path(path_format: str, params: Sequence[Tuple[str, Any, str]]) -> str:
    """
    Build a path for the XTools API.

    Examples:

        >>> build_path("/{a}", [("a", "foo", "bar")])
        "/foo"
        >>> build_path("/{a}", [("a", "", "bar")])
        "/bar"
        >>> build_path("/{a}/{b}/{c}", [("a", "", "x"), ("b", "B", "x"), ("c", "", "x")])
        "/x/B"

    :param path_format:
    :param params:
    :return:
    """
    params_dict = {}

    def has_more(index):
        for _, val, _ in params[index+1:]:
            if val:
                return True
        return False

    for i, (name, value, default) in enumerate(params):
        if value:
            param_value = str(value)
        else:
            param_value = ""

            if has_more(i):
                if default:
                    param_value = default
                # safe defaults
                elif name == "start":
                    param_value = START_TIME
                elif name == "end":
                    param_value = END_TIME

        params_dict[name] = param_value

    path = path_format.format(**params_dict).rstrip("/")
    return path