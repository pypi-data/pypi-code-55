"""
Base module for completion functions
It includes all function used for autocomplete click options and arguments
"""
from click.core import Context

from moic.cli import PLUGINS, global_settings
from moic.cli.utils import get_plugin_autocomplete


def autocomplete_plugins(ctx: Context, args: list, incomplete: str) -> list:
    """
    Get autocompleted plugins list

    Args:
        ctx (click.core.Context): click.core.Context of the given command
        args (list): List of commands args
        incomplete (str): String input to autocomplete

    Returns:
       list: List available plugins autocompleted
    """
    return [plugin for plugin in PLUGINS if plugin.lower().startswith(incomplete.lower())]


def autocomplete_comments(ctx: Context, args: list, incomplete: str) -> list:
    """
    Get autocompleted comments list

    Args:
        ctx (click.core.Context): click.core.Context of the given command
        args (list): List of commands args
        incomplete (str): String input to autocomplete

    Returns:
       list: List available comments name
    """
    command = get_plugin_autocomplete("comments")
    if command:
        return command(ctx, args, incomplete)
    return []


def autocomplete_boards(ctx: Context, args: list, incomplete: str) -> list:
    """
    Get autocompleted boards list

    Args:
        ctx (click.core.Context): click.core.Context of the given command
        args (list): List of commands args
        incomplete (str): String input to autocomplete

    Returns:
       list: List available boards name
    """
    command = get_plugin_autocomplete("boards")
    if command:
        return command(ctx, args, incomplete)
    return []


def autocomplete_sprints(ctx: Context, args: list, incomplete: str) -> list:
    """
    Get autocompleted sprints list

    Args:
        ctx (click.core.Context): click.core.Context of the given command
        args (list): List of commands args
        incomplete (str): String input to autocomplete

    Returns:
       list: List available sprints name
    """
    command = get_plugin_autocomplete("sprints")
    if command:
        return command(ctx, args, incomplete)
    return []


def autocomplete_contexts(ctx: Context, args: list, incomplete: str) -> list:
    """
    Get autocompleted contexts list from configuration

    Args:
        ctx (click.core.Context): click.core.Context of the given command
        args (list): List of commands args
        incomplete (str): String input to autocomplete

    Returns:
       list: List available issuersautocompleted
    """
    return [
        (context["name"], context["description"])
        for context in global_settings["contexts"]
        if context["name"].lower().startswith(incomplete.lower())
    ]


def autocomplete_users(ctx: Context, args: list, incomplete: str) -> list:
    """
    Get users list completion

    Args:
        ctx (click.core.Context): click.core.Context of the given command
        args (list): List of commands args
        incomplete (str): String input to autocomplete

    Returns:
        list: jira.client.ResultList: List of users corresponding to the incomplete input
    """
    command = get_plugin_autocomplete("users")
    if command:
        return command(ctx, args, incomplete)
    return []


def autocomplete_priorities(ctx: Context, args: list, incomplete: str) -> list:
    """
    Get Jira priorities name list completion

    Args:
        ctx (click.core.Context): click.core.Context of the given command
        args (list): List of commands args
        incomplete (str): String input to autocomplete

    Returns:
        list: List of priorities name corresponding to the incomplete input
    """
    command = get_plugin_autocomplete("priorities")
    if command:
        return command(ctx, args, incomplete)
    return []


def autocomplete_transitions(ctx: Context, args: list, incomplete: str) -> list:
    """
    Get transitions available for an issue

    Args:
        ctx (click.core.Context): click.core.Context of the given command
        args (list): List of commands args
        incomplete (str): String input to autocomplete

    Returns:
        list: List of translation names corresponding to the incomplete input
    """
    command = get_plugin_autocomplete("transitions")
    if command:
        return command(ctx, args, incomplete)
    return []


def autocomplete_projects(ctx: Context, args: list, incomplete: str) -> list:
    """
    Get projects list completion

    Args:
        ctx (click.core.Context): click.core.Context of the given command
        args (list): List of commands args
        incomplete (str): String input to autocomplete

    Returns:
        list: List of project names corresponding to the incomplete input
    """
    command = get_plugin_autocomplete("projects")
    if command:
        return command(ctx, args, incomplete)
    return []


def autocomplete_issue_types(ctx: Context, args: list, incomplete: str) -> list:
    """
    Get issue types list completion

    Args:
        ctx (click.core.Context): click.core.Context of the given command
        args (list): List of commands args
        incomplete (str): String input to autocomplete

    Returns:
        list: List of issue types names corresponding to the incomplete input
    """
    command = get_plugin_autocomplete("issue_types")
    if command:
        return command(ctx, args, incomplete)
    return []
