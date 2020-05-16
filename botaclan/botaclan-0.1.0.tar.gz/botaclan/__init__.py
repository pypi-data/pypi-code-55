from importlib_metadata import version
import botaclan.constants
import coloredlogs
import logging
import sentry_sdk
import sys

__version__ = version(__package__)

root_log = logging.getLogger()
root_log.setLevel(botaclan.constants.LOG_LEVEL)
coloredlogs.install(
    logger=root_log, stream=sys.stdout, level=botaclan.constants.LOG_LEVEL
)
logging.Formatter("%(asctime)s | %(name)s | %(levelname)s | %(message)s")
logging.getLogger("asyncio").setLevel(botaclan.constants.LOG_ASYNCIO_LEVEL)
logging.getLogger("discord").setLevel(botaclan.constants.LOG_DISCORD_LEVEL)
logging.getLogger("websockets").setLevel(botaclan.constants.LOG_WEBSOCKETS_LEVEL)
logging.getLogger(__name__)

if botaclan.constants.SENTRY_ENABLED:
    sentry_sdk.init(dsn=botaclan.constants.SENTRY_DSN)

botaclan.constants.log_constants()
