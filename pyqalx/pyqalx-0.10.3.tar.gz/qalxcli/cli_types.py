from importlib import import_module

import click

from pyqalx import Bot, QalxSession
from pyqalx.config import UserConfig, BotConfig
from pyqalx.core.entities import QalxEntity


class QalxImport(click.ParamType):
    """
    A custom type to handle how the cli does imports.
    Expects a string in the format `my.dotted.module:attr_to_import`.
    """

    name = "import path"

    def __init__(self, expected_class, is_instance=False, *args, **kwargs):
        """
        :param expected_class: The class that this import should be an
        instance/subclass of
        :param is_instance: Should we do an `isinstance` check?  Defaults to
        doing an `issubclass` check
        """
        self.expected_class = expected_class
        self.is_instance = is_instance
        super(QalxImport, self).__init__(*args, **kwargs)

    def convert(self, value, param, ctx):
        module_name, variable_name = value.split(":")
        try:
            module = import_module(module_name)
        except ImportError:
            self.fail(f"Failed to import `{module_name}`")
        if variable_name not in dir(module):
            self.fail(f"`{variable_name}` not found in `{module_name}`.")
        _import_target = getattr(module, variable_name)

        method = issubclass
        message = "a subclass"

        if self.is_instance:
            method = isinstance
            message = "an instance"
        if not method(_import_target, self.expected_class):
            self.fail(
                f"`{variable_name}` isn't {message} "
                f"of `{self.expected_class.__name__}`."
            )
        return _import_target


BOT_IMPORT = QalxImport(Bot, is_instance=True)
QALX_SESSION_IMPORT = QalxImport(QalxSession)
USER_CONFIG_IMPORT = QalxImport(UserConfig)
BOT_CONFIG_IMPORT = QalxImport(BotConfig)
QALX_ENTITY_IMPORT = QalxImport(QalxEntity)
