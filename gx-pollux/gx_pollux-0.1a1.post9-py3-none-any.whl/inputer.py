import os
from pollux.license import *


def select_license():
    """
    Select license and

    Generate LICENSE file

    Configure setup.py
    """

    char = ' '
    while char.lower() not in 'mga':
        char = input("Please select license [mga]: \n"
                     "[M]: MIT\n"
                     "[G]: GPL.v3\n"
                     "[A] for Apache\n"
                     "[N]: No License\n"
                     )
    char = char.lower()
    return char


def input_py_version() -> str:
    version = -1
    version_dict = {
        1: "Programming Language :: Python :: 2.7",
        2: "Programming Language :: Python :: 3.6",
        3: "Programming Language :: Python :: 3.7",
        4: "Programming Language :: Python :: 3.8"
    }
    while version not in [1, 2, 3, 4]:
        version = int(input("Please select python version [1234]\n"
                            "[1] Python 2.x\n"
                            "[2] Python 3.6\n"
                            "[3] Python 3.7\n"
                            "[4] Python 3.8\n"))
    return version_dict[version]



def _types():
    pkg_type = ''
    while pkg_type not in 'cn':
        pkg_type = input("Please select package type: \n"
                         "[C]: Command Line\n"
                         "[N]: Normal Package Lib\n")
    pkg_type = pkg_type.lower()
