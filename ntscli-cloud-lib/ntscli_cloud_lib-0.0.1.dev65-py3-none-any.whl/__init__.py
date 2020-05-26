"""Main module."""
import re
from threading import Thread

# Implementation libs
import requests
from update_notipy import update_notify

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


def notify_version_thread():
    try:
        vv = ".".join(__version__.__version__.split(".")[0:3])
        update_notify("ntscli_cloud_lib", vv, defer=True).notify()
    except (requests.exceptions.HTTPError, ValueError):
        # early prereleases do this
        pass


ut = Thread(target=notify_version_thread).start()
