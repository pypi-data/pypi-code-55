import logging
import platform
import subprocess
from os.path import expanduser
import os


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
