import logging
import click
from pkg_resources import iter_entry_points
from click_plugins import with_plugins
from dhm_module_base import __version__
from dhm_module_base import options
from dhm_module_base.helpers import (
    ClickColoredLoggingFormatter,
    ClickLoggingHandler,
)
from dhm_module_base.settings import Configuration


def configure_logging(log_level):
    """Configure logging.

    Args:
        log_level (verbosity): Verbosity defines level of logging
    """
    handler = ClickLoggingHandler()
    handler.formatter = ClickColoredLoggingFormatter("%(name)s: %(message)s")
    logging.basicConfig(level=log_level.upper(), handlers=[handler])


@with_plugins(iter_entry_points("dhm_module_base.plugins"))
@click.group("dhm_module_base")
@click.version_option(version=__version__)
@options.verbosity_arg
@options.configuration_arg
@click.pass_context
def cli(ctx, verbosity, config):
    """dhm_module_base command line interface."""
    ctx.ensure_object(dict)

    if config:
        config = Configuration(path=config.name).config
    else:
        config = Configuration().config

    # Pass the configuration object to the current CLI context
    # This allows plugin or subcommands to retrieve it from the context
    # by passing the click decorator @click.pass_context
    ctx.obj["config"] = config

    if verbosity:
        configure_logging(verbosity)
    else:
        configure_logging(config.get("loglevel"))
