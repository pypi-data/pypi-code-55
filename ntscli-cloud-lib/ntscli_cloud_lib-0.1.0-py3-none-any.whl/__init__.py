"""Main module."""
import re

# Implementation libs
from netflix_update_notify import UpdateNotifier

from . import __version__


def host_to_rae_name(userstring: str) -> str:
    """
    Return a RAE serial string from most things a user types

    :param userstring: The RAE host/ip or connection configuration to connect to.
    :return: None
    """
    pattern = r"r\d{7}"
    foundparts = re.findall(pattern, userstring)
    if len(foundparts) > 0:
        return foundparts[0]
    return ""


UpdateNotifier.notify_of_updates("ntscli-cloud-lib", __version__.__version__)
