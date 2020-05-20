"""For printing the versions from tox.ini."""

from __future__ import print_function

import platform

import flask


print(
    "{} {}; Flask {}".format(
        platform.python_implementation(),
        platform.python_version(),
        flask.__version__
    )
)
