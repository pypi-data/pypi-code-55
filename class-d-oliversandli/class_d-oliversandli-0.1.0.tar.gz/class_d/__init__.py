#!/usr/bin/env python3
"""__init__"""

import requests


def get_license_list():
    """get a list of current licenses available from GitHub"""
    response = requests.get("https://api.github.com/licenses")
    if not response:
        raise Exception("Could not get 'https://api.github.com/licenses'")
    return dict(zip([i["spdx_id"] for i in response.json()],
                    [j["key"] for j in response.json()]))


def get_license(key):
    """get license from GitHub"""
    response = requests.get(f"https://api.github.com/licenses/{key}")
    if not response:
        raise Exception(
            f"Could not get 'https://api.github.com/licenses{key}'")
    return response.json()["body"]
