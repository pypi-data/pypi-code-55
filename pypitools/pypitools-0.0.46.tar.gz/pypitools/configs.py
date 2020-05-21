"""
Command line configurations for pypitools
"""

import os
from enum import Enum

from pytconf.config import Config, ParamCreator


class UploadMethod(Enum):
    """ Methods for uploading """
    SETUP = 0
    TWINE = 1
    GEMFURY = 2


class RegisterMethod(Enum):
    """ Methods for registering """
    SETUP = 0
    TWINE = 1
    UPLOAD = 2


class ConfigData(Config):
    """
    Parameters for the symlink install tool
    """
    upload_method = ParamCreator.create_enum(
        help_string="What upload method to use?",
        default=UploadMethod.TWINE,
        enum_type=UploadMethod,
    )
    clean_before = ParamCreator.create_bool(
        help_string="Should we clean before we start?",
        default=False,
    )
    clean_after = ParamCreator.create_bool(
        help_string="Should we clean after we finish?",
        default=False,
    )
    install_in_user_folder = ParamCreator.create_bool(
        help_string="Should we install globally or in the users folder?",
        default=False,
    )
    use_sudo = ParamCreator.create_bool(
        help_string="should we use sudo?",
        default=False,
    )
    pip_quiet = ParamCreator.create_bool(
        help_string="Should we run pip quietly?",
        default=True,
    )
    setup_quiet = ParamCreator.create_bool(
        help_string="Should we run the setup quietly?",
        default=True,
    )
    pip = ParamCreator.create_str(
        help_string="What pip to use?",
        default="pip",
    )
    gemfury_user = ParamCreator.create_str(
        help_string="What gemfury user name to use?",
        default=None,
    )
    python = ParamCreator.create_str(
        help_string="What python to use?",
        default="python",
    )
    register_method = ParamCreator.create_enum(
        help_string="What method to register the module using?",
        default=RegisterMethod.UPLOAD,
        enum_type=RegisterMethod,
    )
    module_name = ParamCreator.create_str(
        help_string="What is the module name?",
        default=os.path.basename(os.getcwd()),
    )
