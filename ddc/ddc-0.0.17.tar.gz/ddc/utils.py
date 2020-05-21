import logging
import platform
import subprocess
from os.path import expanduser
import os
import time


def __get_os():
    if os.name == "nt":
        return "windows"

    if platform.system() == "Darwin":
        return "macos"

    return "linux"


OS_NAME = __get_os()
DDC_DIR = "/.ddc/"


def __build_path(path):
    if OS_NAME == "windows":
        path = path.replace("/", "\\")
    full_path = expanduser("~") + path
    return full_path


def read_ddc_file(path) -> str:
    """
    :param path:  example: "developer_settings.json"
    :return: dict
    """
    ret = None
    full_path = __build_path(DDC_DIR + path)
    if os.path.isfile(full_path):
        with open(full_path, "r") as myfile:
            ret = myfile.read()
    return ret


def write_ddc_file(path, value: str) -> None:
    """
    :param path:  example: "developer_settings.json"
    :param value: dict
    """
    ddc_dir = __build_path(DDC_DIR)
    os.makedirs(ddc_dir, exist_ok=True)
    full_path = __build_path(DDC_DIR + path)
    with open(full_path, "w") as myfile:
        myfile.write(value)


def get_path_ddc_file(path) -> str:
    """
    :param path:  example: "developer_settings.json"
    """
    return __build_path(DDC_DIR + path)


def exec_cmd(cmd):
    logging.info("Run cmd: " + cmd)
    return subprocess.getstatusoutput(cmd)


def stream_exec_cmd(cmd):
    os.system(cmd)


def run_if_time_has_passed(lock_key: str, ttl_min: int, callback_fn):
    """Run callback function is lock time is passed"""
    lock_file = "fce_" + lock_key + ".loc"
    current_ts = int(time.time())
    saved_ts = read_ddc_file(lock_file)
    if not saved_ts:
        saved_ts = 0
    else:
        saved_ts = int(saved_ts)
    if current_ts - saved_ts > ttl_min * 60:
        callback_fn()
        write_ddc_file(lock_file, str(current_ts))
