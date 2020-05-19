"""
Module for base Moic validator functions
"""
import click
from click.core import Context

from moic.plugins.jira import Instance


def validate_issue_key(ctx: Context, param: list, value: str) -> str:
    """
    Validate a given issue key to check if it exists in Jira

    Args:
        ctx (click.core.Context): click.core.Context of the given command
        args (list): List of commands args
        value (str): String input to validate

    Returns:
        str: Retrive the key if it's validated
    """
    try:
        if value:
            jira = Instance()
            issue = jira.session.issue(value)
            return issue.key
        else:
            return ""
    except Exception:
        raise click.BadParameter("Please provide a valide issue key")


def validate_comment_id(ctx: Context, param: list, value: str) -> str:
    """
    Validate a given comment id to check if it exists in Jira

    Args:
        ctx (click.core.Context): click.core.Context of the given command
        args (list): List of commands args
        value (str): String input to validate

    Returns:
        str: Retrive the id if it's validated
    """
    try:
        if value:
            jira = Instance()
            comment = jira.session.comment(ctx.params["issue_key"], value)
            return comment.id
        else:
            return ""
    except Exception:
        raise click.BadParameter("Please provide a valide issue key")


def validate_project_key(ctx: Context, param: list, value: str) -> str:
    """
    Validate a given project key to check if it exists in Jira

    Args:
        ctx (click.core.Context): click.core.Context of the given command
        args (list): List of commands args
        value (str): String input to validate

    Returns:
        str: Retrive the key if it's validated
    """
    try:
        jira = Instance()
        project = jira.session.project(value)
        return project.key
    except Exception:
        raise click.BadParameter("Please provide a valide project key")


def validate_issue_type(ctx: Context, param: list, value: str) -> str:
    """
    Validate a given issue type name to check if it exists in Jira

    Args:
        ctx (click.core.Context): click.core.Context of the given command
        args (list): List of commands args
        value (str): String input to validate

    Returns:
        str: Retrive the name if it's validated
    """
    try:
        jira = Instance()
        issue_types = jira.session.issue_types()
        if value not in [it.name for it in issue_types]:
            raise Exception()
        return value
    except Exception:
        raise click.BadParameter("Please provide a valide issue type name")


def validate_priority(ctx, param, value):
    """
    Validate a given priority name to check if it exists in Jira

    Args:
        ctx (click.core.Context): click.core.Context of the given command
        args (list): List of commands args
        value (str): String input to validate

    Returns:
        str: Retrive the priority name if it's validated
    """
    try:
        jira = Instance()
        priority = [priority for priority in jira.session.priorities() if priority.name == value][0]
        return priority.name
    except Exception:
        raise click.BadParameter("Please provide a valide priority")


def validate_user(ctx, param, value):
    """
    Validate a given user name to check if it exists in Jira

    Args:
        ctx (click.core.Context): click.core.Context of the given command
        args (list): List of commands args
        value (str): String input to validate

    Returns:
        str: Retrive the user name if it's validated
    """
    try:
        if value:
            jira = Instance()
            user = jira.session.user(value)
            return user.name
        else:
            return ""
    except Exception:
        raise click.BadParameter("Please provide a valide user name")
