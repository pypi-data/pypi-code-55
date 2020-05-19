"""
Module for base Moic configuration commands
"""
import click

from moic.cli import CONF_DIR, PLUGINS, CustomSettings, MoicInstance, console, global_settings, logger
from moic.cli.completion import autocomplete_contexts, autocomplete_plugins
from moic.cli.utils import get_plugin_instance


@click.group()
def context():
    """
    Command to list, add and delete configuration contexts
    """
    if not global_settings.get("contexts"):
        MoicInstance()
    pass


@context.command()
def list():
    """
    List existing contexts
    """
    logger.debug("Execute 'context list' command")
    contexts = global_settings.get("contexts")
    if not contexts:
        console.print("[yellow]No context defined yet[/yellow]")
        console.print("[grey]> Please run '[bold]moic context add[/bold]' to setup configuration[/grey]")
        console.line()
        exit(0)
    for ctx in contexts:
        context_color = "green" if ctx.get("name") == global_settings.get("current_context") else "blue"
        prefix = "✓" if ctx.get("name") == global_settings.get("current_context") else "•"
        console.print(
            f"[{context_color}]{prefix} {ctx.get('name').ljust(20)}[/]: [grey70]{ctx.get('description')}[/grey70]"
        )


@context.command()
@click.argument("plugin", type=click.STRING, autocompletion=autocomplete_plugins)
@click.option("--name", type=click.STRING, default=None, help="The context name")
@click.option("--description", type=click.STRING, default=None, help="The context description")
def add(plugin, name, description):
    """
    Add a new context in the configuration
    """
    logger.debug("Execute 'context add' command")
    if plugin not in PLUGINS:
        console.print(f"[yellow]unsupported plugin {plugin}[/]")

    name = click.prompt("name") if not name else name
    if not name:
        name = f"default-{plugin}"
    if not description:
        description = click.prompt("description", default=f"{plugin} default context")

    if name in [ctx["name"] for ctx in global_settings.get("contexts")]:
        console.print(f"[red]Context '{name}' already definded[/red]")
        exit(1)

    InstanceClass = get_plugin_instance(plugin)
    ic = InstanceClass()
    context = ic.add_context(name, force=True)
    context["plugin"] = plugin
    context["name"] = name
    context["description"] = description
    config = {"default": {"contexts": [context]}}
    ic.update_config(config)
    # Reload configuration
    CustomSettings.reload()
    ic.set_current_context(name)
    CustomSettings.reload()

    # If the plugin provide a custom_config method ask user if he want to use it
    if hasattr(ic, "custom_config"):
        set_custom = click.confirm(ic.custom_config_label)
        if set_custom:
            ic.custom_config(project=context["default_project"], force=True)
    console.print(f"[grey70] > Configuration stored in {CONF_DIR}/config.yaml[/grey70]")


@context.command()
@click.argument("context_name", type=click.STRING, autocompletion=autocomplete_contexts)
def set(context_name):
    """
    Set the current context to use
    """
    MoicInstance().set_current_context(context_name)
    console.print(f"Context swithed to [green]{context_name}[/green]")


@context.command()
@click.argument("context_name", type=click.STRING, autocompletion=autocomplete_contexts)
def delete(context_name):
    """
    Delete the given context
    """
    MoicInstance().delete_context(context_name)
    console.print(f"Context [red]{context_name}[/red] deleted")
