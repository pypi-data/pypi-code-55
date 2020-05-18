import warnings
import logging
import getpass
import os

from cement import App, TestApp, init_defaults
from cement.core.exc import CaughtSignal

from .controllers.base import Base
from .core.exc import SaltPacketsError
from .ext import UtilsHelper

# configuration defaults
CONFIG = init_defaults("salt-packets", "log.logging")
CONFIG["salt-packets"]["workdir"] = os.path.expanduser("~/.config/salt-packets")
CONFIG["salt-packets"]["user"] = getpass.getuser()
CONFIG["salt-packets"]["uid"] = os.getuid()
CONFIG["salt-packets"]["system_path"] = "/etc/salt/packets.yaml"
CONFIG["log.logging"]["level"] = "DEBUG"


class SaltPackets(App):
    """salt-packets primary application."""

    class Meta:
        label = "salt-packets"

        # configuration defaults
        config_defaults = CONFIG

        # call sys.exit() on close
        exit_on_close = True

        # load additional framework extensions
        extensions = ["yaml", "colorlog", "jinja2"]

        # configuration handler
        config_handler = "yaml"

        # configuration file suffix
        config_file_suffix = ".yml"

        # set the log handler
        log_handler = "colorlog"

        # set the output handler
        output_handler = "jinja2"

        # register handlers
        handlers = [Base]

        hooks = [("post_setup", lambda app: UtilsHelper.attach("utils", app))]


class SaltPacketsTest(TestApp, SaltPackets):
    """A sub-class of Spack that is better suited for testing."""

    class Meta:
        label = "salt-packets"


def main():
    with SaltPackets() as app:
        try:
            app.run()

        except AssertionError as e:
            print("AssertionError > %s" % e.args[0])
            app.exit_code = 1

            if app.debug is True:
                import traceback

                traceback.print_exc()

        except SaltPacketsError as e:
            print("SaltPacketsError > %s" % e.args[0])
            app.exit_code = 1

            if app.debug is True:
                import traceback

                traceback.print_exc()

        except CaughtSignal as e:
            # Default Cement signals are SIGINT and SIGTERM, exit 0 (non-error)
            print("\n%s" % e)
            app.exit_code = 0


if __name__ == "__main__":
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        main()
