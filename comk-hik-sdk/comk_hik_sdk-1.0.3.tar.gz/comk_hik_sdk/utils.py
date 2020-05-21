import os

from ctypes import *

import platform

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CALL_PATH_LINUX = '{}/callso/call.so'.format(BASE_DIR)


def load():
    return cdll.LoadLibrary(CALL_PATH_LINUX)


def GetPlatformName():
    """

    :return: Windows、Linux、Darwin（苹果电脑） or other
    """
    return platform.system()


def set_renturn_type(fun, fun_retrurn_struct):
    fun.restype = fun_retrurn_struct
    return fun


def python_str_to_c_str(pstr, size: int, encoding='utf-8'):
    return create_string_buffer(pstr.encode(encoding), size)


def python_str_to_c_ubyte_array(pstr, size: int, encoding='utf-8'):
    return (c_ubyte * size)(*bytearray(pstr.encode(encoding)))


def c_type_array_to_python_str(c_array):
    return bytearray(c_array).decode('utf-8')


def print_c_type_array(c_array):
    p_str = c_type_array_to_python_str(c_array)
    print(p_str)
    return p_str
