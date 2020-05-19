"""
Moic cli definition base module
"""
import click

from moic.cli import logger, settings
from moic.cli.commands.context import context
from moic.cli.commands.issue import issue
from moic.cli.commands.rabbit import rabbit
from moic.cli.commands.resources import resources
from moic.cli.commands.template import template
from moic.cli.commands.version import version
from moic.cli.utils import check_instance_is_up, get_plugin_custom_commands


@click.group()
@click.pass_context
def cli(ctx):
    """
    Main MOIC cli command group
    """
    if settings.get("instance"):
        check_instance_is_up()


# Register configs commands
logger.debug("Loading commands:")
logger.debug(" - template")
cli.add_command(template)
logger.debug(" - context")
cli.add_command(context)
# Register buitlin commands
logger.debug(" - rabbit")
cli.add_command(rabbit)
logger.debug(" - version")
cli.add_command(version)
# Register default commands
logger.debug(" - issue")
cli.add_command(issue)
logger.debug(" - resources")
cli.add_command(resources)

# Register custom commands
if settings.get("plugin"):
    logger.debug(f"Loading {settings.get('plugin')} plugin custom commands:")
    for c in get_plugin_custom_commands(settings.get("plugin")):
        logger.debug(f" - {c.name}")
        cli.add_command(c)


def run():
    """
    Run the cli application
    """

    cli()
