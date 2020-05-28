#!/usr/bin/env python

import sys

sys.path.insert(0, "../")

from config import *

dicts_name = [
    "keyvault",
    "auth",
    "blob",
    "acr",
    "aci",
    "dls",
    "dls_glob",
    "tables",
    "databricks",
]
safe_values = [
    "client_secret",
    "storage_connection_string",
    "storage_key",
    "sas_key",
    "sas_url",
    "token",
]


def displaydict(dict_name):
    dict = eval(dict_name)
    print("\n{} = {}".format(dict_name, "{"))
    for key, value in dict.items():
        if key in safe_values:
            value = "<redacted>"
        print(f'    "{key}": "{value}",')
    print("}")


for dict_name in dicts_name:
    displaydict(dict_name)
