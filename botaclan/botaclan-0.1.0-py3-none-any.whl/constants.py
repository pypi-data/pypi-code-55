from vyper import v
import logging

log = logging.getLogger(__name__)


def set_env():
    v.set_env_prefix("botaclan")
    v.set_env_key_replacer(".", "_")
    v.automatic_env()


def set_env_defaults():
    v.set_config_type("yaml")
    v.set_default("command.prefix", "~b ")
    v.set_default("feature.calendar", True)
    v.set_default("feature.roulette", True)
    v.set_default(
        "googleapi.application.credentials", "/etc/botaclan/google_service_account.json"
    )
    v.set_default("googleapi.calendar.id", "primary")
    v.set_default("log.asyncio.level", "warning")
    v.set_default("log.discord.level", "warning")
    v.set_default("log.level", "info")
    v.set_default("log.websockets.level", "warning")
    v.set_default("sentry.enabled", False)
    v.set_default("timezone", "America/Sao_Paulo")


def log_constants():
    log.debug(f"command.prefix={COMMAND_PREFIX}")
    log.debug(f"discord.guild.id={DISCORD_GUILD_ID}")
    log.debug(f"discord.token={DISCORD_TOKEN}")
    log.debug(f"feature.calendar={FEATURE_CALENDAR}")
    log.debug(f"feature.roulette={FEATURE_ROULETTE}")
    log.debug(f"googleapi.application.credentials={GOOGLEAPI_APPLICATION_CREDENTIALS}")
    log.debug(f"googleapi.calendar.id={GOOGLEAPI_CALENDAR_ID}")
    log.debug(f"log.asyncio.level={LOG_ASYNCIO_LEVEL}")
    log.debug(f"log.discord.level={LOG_DISCORD_LEVEL}")
    log.debug(f"log.level={LOG_LEVEL}")
    log.debug(f"log.websockets.level={LOG_WEBSOCKETS_LEVEL}")
    log.debug(f"sentry.enabled={SENTRY_ENABLED}")
    log.debug(f"sentry.dsn={SENTRY_DSN}")
    log.debug(f"timezone={TIMEZONE}")


set_env()
set_env_defaults()

COMMAND_PREFIX = v.get_string("command.prefix")
DISCORD_GUILD_ID = v.get_int("discord.guild.id")
DISCORD_TOKEN = v.get_string("discord.token")
FEATURE_CALENDAR = v.get_bool("feature.calendar")
FEATURE_ROULETTE = v.get_bool("feature.roulette")
GOOGLEAPI_APPLICATION_CREDENTIALS = v.get_string("googleapi.application.credentials")
GOOGLEAPI_CALENDAR_ID = v.get_string("googleapi.calendar.id")
LOG_ASYNCIO_LEVEL = v.get_string("log.asyncio.level").upper()
LOG_DISCORD_LEVEL = v.get_string("log.discord.level").upper()
LOG_LEVEL = v.get_string("log.level").upper()
LOG_WEBSOCKETS_LEVEL = v.get_string("log.websockets.level").upper()
SENTRY_ENABLED = v.get_string("sentry.enabled")
SENTRY_DSN = v.get_string("sentry.dsn")
TIMEZONE = v.get_string("timezone")
