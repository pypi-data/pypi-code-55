#  Copyright (c) 2020 Netflix.
#  All rights reserved.
from threading import Thread

import requests
from update_notipy import update_notify

# Implementation libs
from kaiju_automator_lib.__version__ import __version__


def notify_version_thread():
    vv = ".".join(__version__.split(".")[0:3])
    try:
        update_notify("kaiju_automator_lib", vv, defer=True).notify()
    except (requests.exceptions.HTTPError, ValueError):
        pass


ut = Thread(target=notify_version_thread).start()
