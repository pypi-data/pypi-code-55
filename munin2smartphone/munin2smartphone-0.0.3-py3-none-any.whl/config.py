import argparse
import errno
import logging
import os
import pytz

import coloredlogs
import quicklogging
import xdg.BaseDirectory

from . import APP_NAME
from . import APP_DESCRIPTION
from .exceptions import ConfigError


class ConfigValueUnspecified:
    """This special object works for incremental values"""
    def __add__(self, value):
        return value


class Config:
    _UNSPECIFIED = ConfigValueUnspecified()
    DEFAULT_TIMEZONE = "Europe/Paris"
    DEFAULT_PORT = 8765
    DEFAULT_LISTENING_ADDRESS = "127.0.0.1"
    DEFAULT_REPORTS = {
        "report": {
            "accepted_checklevels": ("warning", "critical"),
            "ignored_keyvalues": {"title": "Pending packages"},
        },
        "all": {},
    }

    def __init__(self, withcli=True, config=None):
        self._cfgbackend = self._config_defaults()

        if config:
            self._cfgbackend.update(config)

        if withcli:
            cli_config = vars(Config.cli_config())
            for key, value in cli_config.items():
                if value is Config._UNSPECIFIED:
                    continue
                self._cfgbackend[key] = value

        self._sanity()

    def _sanity(self):
        self._sanity_loglevel()
        self._sanity_timezone()
        self._sanity_cachedir()

    def _sanity_timezone(self):
        timezone = self._cfgbackend["timezone"]
        tz_object = pytz.timezone(timezone)
        self._cfgbackend["timezone"] = tz_object
        quicklogging.debug("Times displayed in timezone: %s", timezone)

    def _sanity_loglevel(self):
        verbosity = self._cfgbackend["verbose"]
        logger = quicklogging.get_logger()
        if verbosity == 0:
            level, logmsg = logging.ERROR, "error"
        elif verbosity == 1:
            level, logmsg = logging.WARNING, "warning"
        elif verbosity == 2:
            level, logmsg = logging.INFO, "info"
        else:
            level, logmsg = logging.DEBUG, "debug"

        if self._cfgbackend["coloredlogs"]:
            coloredlogs.install(level=level)
        else:
            logging.basicConfig(level=level)

        logger.info("Logging level set to %s", logmsg)

    def _sanity_cachedir(self):
        cache_directory = self.cache_directory
        quicklogging.debug("Cache directory is %s", cache_directory)
        if os.path.exists(cache_directory):
            if os.path.isdir(cache_directory):
                return
            raise ConfigError(
                "Cache directory ({}) exists and is not a directory.".format(
                    cache_directory
                )
            )

        # only for non default cache dir (otherwise xdg takes care of this)
        try:
            quicklogging.warning(
                "Creating cache directory %s",
                cache_directory,
            )
            os.makedirs(cache_directory)
        except OSError as err:
            raise ConfigError(
                "Error creating cache directory ({}): {}".format(
                    cache_directory,
                    errno.errorcode(err.errno)
                )
            )

    @property
    def timezone(self):
        return self._cfgbackend["timezone"]

    @property
    def port(self):
        return self._cfgbackend["port"]

    @property
    def listening_address(self):
        return self._cfgbackend["listening-address"]

    @property
    def cache_directory(self):
        return self._cfgbackend["cache_directory"]

    @property
    def outputdir(self):
        return self._cfgbackend["outputdir"]

    @property
    def reports(self):
        # TODO: read a config value for reports
        return self.DEFAULT_REPORTS

    @staticmethod
    def _config_defaults():
        default_cache_dir = xdg.BaseDirectory.save_cache_path(APP_NAME)
        default_outputdir = os.path.abspath(os.getcwd())
        return {
            "cache_directory": default_cache_dir,
            "outputdir": default_outputdir,
            "port": Config.DEFAULT_PORT,
            "listening-address": Config.DEFAULT_LISTENING_ADDRESS,
            "timezone": Config.DEFAULT_TIMEZONE,
            "verbose": 0,
            "coloredlogs": True,
        }

    @staticmethod
    def cli_config():

        confdef = Config._config_defaults()
        parser = argparse.ArgumentParser(
            description=APP_DESCRIPTION,
        )

        parser.add_argument(
            "-V",
            "--version",
            action="version",
            version="0 - unpackaged",
            # version="%(prog)s {version}".format(version=__version__),
        )

        parser.add_argument(
            "-v",
            "--verbose",
            help="increase output verbosity -can be called multiple times: "
            "Levels: 0 time: error, 1 time: warning, 2 times: info, 3 times:"
            "debug",
            action="count",
            default=Config._UNSPECIFIED,
        )

        parser.add_argument(
            "--coloredlogs",
            help="terminal logs are colored (using coloredlogs): default",
            default=Config._UNSPECIFIED,
            action="store_true",
        )

        parser.add_argument(
            "--no-coloredlogs",
            help="terminal logs are NOT colored: default \
            is colored logs ",
            dest="coloredlogs",
            action="store_false",
        )

        parser.add_argument(
            "-o",
            "--outputdir",
            help=f"html output directory (default: {confdef['outputdir']})",
            default=Config._UNSPECIFIED,
        )

        parser.add_argument(
            "--configfile",
            type=argparse.FileType('r', encoding='utf-8'),
            default=None,
        )

        parser.add_argument(
            "--logfile",
            type=argparse.FileType('a', encoding='utf-8'),
            default=None,
        )

        parser.add_argument(
            "--cache_directory",
            default=Config._UNSPECIFIED,
            help=f"{APP_NAME} cache directory \
            (defaults to {confdef['cache_directory']})"
        )

        parser.add_argument(
            "--port",
            type=int,
            default=Config._UNSPECIFIED,
            help=f"listening TCP port (defaults to {confdef['port']})"
        )

        parser.add_argument(
            "--listening-address",
            default=Config._UNSPECIFIED,
            help=f"listening IP address (defaults to \
            {confdef['listening-address']})",
        )

        parser.add_argument(
            "--timezone",
            default=Config._UNSPECIFIED,
            help=f"Timezone for html output -internal dates are UTC \
            (defaults to {confdef['timezone']})",
        )

        return parser.parse_args()
