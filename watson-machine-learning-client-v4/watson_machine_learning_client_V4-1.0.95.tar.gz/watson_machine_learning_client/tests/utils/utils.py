import json
import os
from configparser import ConfigParser

__all__ = [
    "get_wml_credentials",
    "get_cos_credentials",
    "get_env",
    "is_cp4d"
]

if "ENV" in os.environ:
    environment = os.environ['ENV']
else:
    environment = "YP_QA"


timeouts = "TIMEOUTS"
credentials = "CREDENTIALS"
training_data = "TRAINING_DATA"
configDir = "./config.ini"

config = ConfigParser()
config.read(configDir)


def get_env():
    return environment


def get_wml_credentials(env=environment):
    return json.loads(config.get(env, 'wml_credentials'))


def get_cos_credentials(env=environment):
    return json.loads(config.get(env, 'cos_credentials'))


def is_cp4d():
    if "CP4D" in get_env():
        return True
    elif "ICP" in get_env():
        return True
    elif "OPEN_SHIFT" in get_env():
        return True
    elif "CPD" in get_env():
        return True

    return False



