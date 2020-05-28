import os

import pydmt.version
import pylogconf.core
import sys
import pathlib

from pytconf.config import register_function_group, register_endpoint

from pydmt.builders.sphinx import Sphinx
from pydmt.core.pydmt import PyDMT
from pydmt.features.templating import Templating


GROUP_NAME_DEFAULT = "default"
GROUP_DESCRIPTION_DEFAULT = "all pydmt commands"


def register_group_default():
    """
    register the name and description of this group
    """
    register_function_group(
        function_group_name=GROUP_NAME_DEFAULT,
        function_group_description=GROUP_DESCRIPTION_DEFAULT,
    )


@register_endpoint(
    group=GROUP_NAME_DEFAULT,
)
def version() -> None:
    """
    Print version
    """
    print(pydmt.version.VERSION_STR)


@register_endpoint(
    group=GROUP_NAME_DEFAULT,
)
def build():
    """ build the project """
    # parameters
    debug = False
    sphinx = True
    add_import_of_cwd = True
    add_import_of_home = True
    add_import_of_shared = True
    if add_import_of_shared:
        folder = "/etc/pydmt"
        if folder not in sys.path:
            sys.path.insert(0, folder)
    if add_import_of_home:
        folder = os.path.join(str(pathlib.Path.home()), ".config/pydmt")
        if folder not in sys.path:
            sys.path.insert(0, folder)
    if add_import_of_cwd:
        if "" not in sys.path:
            sys.path.insert(0, "")

    pylogconf.core.setup()
    if debug:
        print("system path is [{}]".format(sys.path))
    p = PyDMT()

    # add templating support
    t = Templating()
    t.setup(p)

    # add sphinx builder support
    if sphinx and os.path.isdir("sphinx"):
        import config.project
        p.add_builder(Sphinx(package_name=config.project.project_name))
    stats = p.build_all()
    sys.exit(stats.get_os_error_code())
