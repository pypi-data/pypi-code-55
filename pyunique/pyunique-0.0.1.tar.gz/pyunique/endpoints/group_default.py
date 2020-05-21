"""
The default group of operations that pyunique has
"""

import os  # for walk, getcwd, symlink, listdir, unlink, mkdir
import os.path  # for join, expanduser, realpath, abspath, islink, isdir, isfile
import sys

from pytconf.config import register_endpoint, register_function_group

import pyunique
import pyunique.version

GROUP_NAME_DEFAULT = "default"
GROUP_DESCRIPTION_DEFAULT = "all pyunique commands"


def register_group_default():
    """
    register the name and description of this group
    """
    register_function_group(
        function_group_name=GROUP_NAME_DEFAULT,
        function_group_description=GROUP_DESCRIPTION_DEFAULT,
    )


@register_endpoint(
    configs=[],
    suggest_configs=[],
    group=GROUP_NAME_DEFAULT,
)
def version() -> None:
    """
    Print version
    """
    print(pyunique.version.VERSION_STR)
