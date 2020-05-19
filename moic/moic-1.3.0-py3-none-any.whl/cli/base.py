"""
Module for Moic configuration

Configuration file is stored under CONF_DIR and contains the following architecture

default:
    contexts:
        - name: my_context
          type: <plugin>
          login: ...
    current_context: my_context
"""
import logging
import os
import sys

import click
import keyring
import yaml
from dynaconf import LazySettings
from rich.console import Console
from rich.logging import RichHandler

PLUGINS = []

CONF_DIR = "~/.moic"

COLOR_MAP = {
    "blue-gray": "blue",
    "yellow": "yellow",
    "green": "green",
    "blue": "blue",
    "red": "red",
}

SPRINT_STATUS_COLORS = {"closed": "yellow", "active": "green", "future": "blue"}
PRIORITY_COLORS = {
    "Low": "grey70",
    "Medium": "green",
    "High": "dark_orange",
    "Critical": "red",
}

# Lazy load configuration
global_settings = LazySettings(
    DEBUG_LEVEL_FOR_DYNACONF="DEBUG",
    ENVVAR_PREFIX_FOR_DYNACONF="MOIC",
    ENVVAR_FOR_DYNACONF="MOIC_SETTINGS",
    SETTINGS_FILE_FOR_DYNACONF=[os.path.expanduser(f"{CONF_DIR}/config.yaml")],
)

# Setup logger
FORMAT = "%(message)s"
logging.basicConfig(
    level=global_settings.get("LOG_LEVEL", "ERROR").upper(), format=FORMAT, datefmt="[%X] ", handlers=[RichHandler()]
)
logger = logging.getLogger("moic")

# Setup Console
console = Console(file=sys.__stdout__, highlight=False)

# Detect installed plugins
plugin_folder = os.path.join(os.path.dirname(__file__), "..", "plugins")
logger.debug(f"Search for plugins in {plugin_folder}")
for path in os.listdir(plugin_folder):
    if os.path.isdir(os.path.join(plugin_folder, path)) and path != "__pycache__":
        logger.debug(f" - Loading {path} plugin")
        PLUGINS.append(path)


class MoicInstance:
    """
    MoicInstance Class represents the main class of the tool which should be
    herited by other Issuer Instance, such as MoicJiraInstance
    """

    instance = None
    custom_config_label = "Would you like to run custom configuration"

    def __init__(self) -> None:
        """
        Init method
        """
        # Setup home dir
        self.setup_home_dir()

    @property
    def session(self):
        """
        Property which retrieve the session to interact with the issuer
        """
        pass

    def setup_home_dir(self) -> None:
        """
        Setup configuration directory. It creates the root configuration directory
        an empty .yaml conf file and the templates directory

        Returns:
            None
        """
        if not os.path.isdir(os.path.expanduser(CONF_DIR)):
            logger.debug(" - Create configuration dir")
            os.makedirs(os.path.expanduser(CONF_DIR))
        if not os.path.isdir(os.path.expanduser(f"{CONF_DIR}/templates")):
            logger.debug(" - Create templates dir")
            os.makedirs(os.path.expanduser(f"{CONF_DIR}/templates"))
        if not os.path.isfile(os.path.expanduser(f"{CONF_DIR}/config.yaml")):
            with open(os.path.expanduser(f"{CONF_DIR}/config.yaml"), "w") as default_config:
                logger.debug(" - Create default configuration")
                default = {"default": {"current_context": "", "contexts": []}}
                yaml.dump(default, default_config)
                # Reload configuration
                CustomSettings.reload()

    def create_session_instance(self) -> None:
        """
        Setup the session instance
        """
        pass

    def add_context(self, force: bool = False) -> None:
        """
        Add a new context in the configuration

        Args:
            force (bool): If True it doesn't check the current configuration before
        """
        pass

    def set_current_context(self, context_name: str) -> None:
        """
        Set the current configuration context to use when executing commands

        Args:
            context_name (str): The context name which should be present in the contexts list
        """
        if context_name in [ctx["name"] for ctx in global_settings.get("contexts")]:
            logger.debug(f"Set current-context to {context_name}")
            self.update_config({"default": {"current_context": context_name}})
        else:
            logger.debug(f"{context_name} context doesn't exists")
            raise Exception(f"{context_name} context doesn't exists")

    def delete_context(self, context_name: str) -> None:
        """
        Delete the given context from the contexts list. If it's the current_context, set the
        current context to ''


        Args:
            context_name (str): The context name which should be deleted
        """
        if context_name in [ctx["name"] for ctx in global_settings.get("contexts")]:
            logger.debug(f"Delete {context_name} context")
            # Get the configuration
            with open(os.path.expanduser(f"{CONF_DIR}/config.yaml"), "r") as conf_file:
                conf = yaml.load(conf_file, Loader=yaml.FullLoader)
            # Remove the context
            conf["default"]["contexts"] = [ctx for ctx in conf["default"]["contexts"] if ctx["name"] != context_name]
            if conf["default"]["current_context"] == context_name:
                conf["default"]["current_context"] = ""
            # Rewrite the configuration
            with open(os.path.expanduser(f"{CONF_DIR}/config.yaml"), "w+") as conf_file:
                yaml.dump(conf, conf_file)
        else:
            logger.debug(f"{context_name} context doesn't exists")
            raise Exception(f"{context_name} context doesn't exists")

    def update_config(self, sub_conf: dict) -> None:
        """
        Update the local configuration merging in it a new dict of configuration

        Args:
            sub_conf (dict): The new configuration to merge into the config.yaml file

        Returns:
            None
        """
        logger.debug("Update configuration")
        # read configuration
        with open(os.path.expanduser(f"{CONF_DIR}/config.yaml"), "r") as conf_file:
            conf = yaml.load(conf_file, Loader=yaml.FullLoader)
        # merge configuration
        new_conf = merge_config(conf, sub_conf)
        # write configuration
        with open(os.path.expanduser(f"{CONF_DIR}/config.yaml"), "w+") as conf_file:
            yaml.dump(new_conf, conf_file)


class CustomSettings:
    """
    Class representing the current settings. It's a subtree of global_settings
    containing only the configuration contained into the current context
    """

    def __init__(self):
        """
        Init method
        """
        pass

    def reload():
        """
        Force reloading configurat from {CONF_DIR}/config.yaml
        """
        global_settings.reload()

    def get(self, value, default=None) -> str:
        """
        Get a value into the Box element returned by global_settings (dynaconf.LazySetting)

        Args:
            value (str): The key value to return

        Returns:
            str: The value within the configuration
        """
        if not global_settings.get("contexts"):
            return None

        # Return password which is not stored in context
        if value == "password":
            current_context_name = global_settings.get("current_context")
            current_context = [
                context for context in global_settings.get(f"contexts") if context.get("name") == current_context_name
            ][0]
            if keyring.get_password(f"moic-{current_context_name}", current_context.get("login")):
                self.password = keyring.get_password(f"moic-{current_context_name}", current_context.get("login"))
            else:
                console.print(f"[yellow]No password stored in keyring for {current_context.get('name')}[/yellow]")
                self.password = click.prompt("password", hide_input=True)
            return self.password

        settings_in_context = [
            context
            for context in global_settings.get("contexts")
            if context["name"] == global_settings.get("current_context")
        ]

        if not settings_in_context:
            console.print("[yellow]No context selected[/yellow]")
            exit(0)
        else:
            settings_in_context = settings_in_context[0]
        keys = value.split(".")
        conf_value = self.drill_down(settings_in_context, keys)
        return conf_value if conf_value is not None else default

    def drill_down(self, conf: dict, keys: list) -> str:
        """
        Drill down into the configuration tree when the search key is composite
        For example : key.subkey.subsubkey

        Args:
            conf (dict): The configuration to drill down
            keys (list): The keys list which should be used to browse the conf

        Returns:
            str: The value of the key in the conf
        """
        if keys[0] not in conf.keys():
            return None
        if len(keys) == 1:
            return conf.get(keys[0])
        else:
            return self.drill_down(conf.get(keys[0]), keys[1:])


settings = CustomSettings()


def merge_config(a: dict, b: dict, path: str = None) -> dict:
    """
    Merge two config dict together

    Args:
        a (dict): The main config dict
        b (dict): The secondary config dict which should be merged into a
        path (str): The path where to merde

    Returns:
        dict: The merged dict
    """
    if path is None:
        path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge_config(a[key], b[key], path + [str(key)])
            elif isinstance(a[key], list) and isinstance(b[key], list):
                if key == "contexts":
                    a[key] = merge_contexts(a[key], b[key])
                else:
                    a[key] = b[key]
            elif a[key] == b[key]:
                pass  # same leaf value
            elif isinstance(a[key], str) and isinstance(b[key], str):
                a[key] = b[key]
            else:
                raise Exception(f"Conflict at %s" % ".".join(path + [str(key)]))
        else:
            a[key] = b[key]
    return a


def merge_contexts(current_contexts: list, new_contexts: list) -> list:
    """
    Merge two context list based on the context.name key
    It will update exiting contexts with new values and append non existing contexts

    Args:
        current_contexts (list): The context list present in the configuration
        new_contexts (list): The new context list to merge into the configuration

    Returns:
        list: The aggregated context list
    """
    ret = []
    for ctx in new_contexts:
        if ctx["name"] not in [c["name"] for c in current_contexts]:
            ret.append(ctx)
        else:
            ret.append(merge_config([c for c in current_contexts if c["name"] == ctx["name"]][0], ctx))
    return ret
