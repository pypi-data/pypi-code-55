# -*- coding: utf-8 -*-
# @author: leesoar

"""tools"""

import json
import os

import requests
from retrying import retry

from anole import setting, error


@retry(stop_max_attempt_number=setting.HTTP_RETRY)
def get(url):
    res = requests.get(url)
    if res.status_code != 200:
        raise error.AnoleCrawlError("Download cache failed, please check.")
    return res


def update(path, data):
    os.path.exists(path) and os.remove(path)
    open(path, encoding="utf-8", mode="w").write(data)


def read(path):
    return json.loads(open(path, encoding="utf-8").read())


def load_cached(path, url=setting.UA_CACHE_URL):
    if not os.path.exists(path):
        update(path, get(url).text)
    return read(path)
