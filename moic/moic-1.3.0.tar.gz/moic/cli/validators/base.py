"""
Module for base Moic validator functions
"""
from click.core import Context

from moic.cli.utils import get_plugin_validator


def validate_issue_key(ctx: Context, param: list, value: str) -> str:
    """
    Validate a given issue key to check if it exists

    Args:
        ctx (click.core.Context): click.core.Context of the given command
        args (list): List of commands args
        value (str): String input to validate

    Returns:
        str: Retrive the key if it's validated
    """
    command = get_plugin_validator("issue_key")
    if command:
        return command(ctx, param, value)
    return value


def validate_comment_id(ctx: Context, param: list, value: str) -> str:
    """
    Validate a given comment id to check if it exists

    Args:
        ctx (click.core.Context): click.core.Context of the given command
        args (list): List of commands args
        value (str): String input to validate

    Returns:
        str: Retrive the id if it's validated
    """
    command = get_plugin_validator("comment_id")
    if command:
        return command(ctx, param, value)
    return value


def validate_project_key(ctx: Context, param: list, value: str) -> str:
    """
    Validate a given project key to check if it exists

    Args:
        ctx (click.core.Context): click.core.Context of the given command
        args (list): List of commands args
        value (str): String input to validate

    Returns:
        str: Retrive the key if it's validated
    """
    command = get_plugin_validator("project_key")
    if command:
        return command(ctx, param, value)
    return value


def validate_issue_type(ctx: Context, param: list, value: str) -> str:
    """
    Validate a given issue type name to check if it exists

    Args:
        ctx (click.core.Context): click.core.Context of the given command
        args (list): List of commands args
        value (str): String input to validate

    Returns:
        str: Retrive the name if it's validated
    """
    command = get_plugin_validator("issue_type")
    if command:
        return command(ctx, param, value)
    return value


def validate_priority(ctx, param, value):
    """
    Validate a given priority name to check if it exists

    Args:
        ctx (click.core.Context): click.core.Context of the given command
        args (list): List of commands args
        value (str): String input to validate

    Returns:
        str: Retrive the priority name if it's validated
    """
    command = get_plugin_validator("piority")
    if command:
        return command(ctx, param, value)
    return value


def validate_user(ctx, param, value):
    """
    Validate a given user name to check if it exists

    Args:
        ctx (click.core.Context): click.core.Context of the given command
        args (list): List of commands args
        value (str): String input to validate

    Returns:
        str: Retrive the user name if it's validated
    """
    command = get_plugin_validator("user")
    if command:
        return command(ctx, param, value)
    return value
