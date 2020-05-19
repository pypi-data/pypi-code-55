"""
Base module for completion functions
It includes all function used for autocomplete click options and arguments
"""
from click.core import Context
from jira.client import ResultList

from moic.cli import settings
from moic.plugins.jira import Instance
from moic.plugins.jira.utils import get_project_boards


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
    try:
        jira = Instance()
        boards = jira.session.boards(type="scrum")
        return [board.name for board in boards if board.name.lower().startswith(incomplete.lower())]
    except Exception:
        return []


def autocomplete_comments(ctx: Context, args: list, incomplete: str) -> list:
    """
    Get autocompleted comments list

    Args:
        ctx (click.core.Context): click.core.Context of the given command
        args (list): List of commands args
        incomplete (str): String input to autocomplete

    Returns:
       list: List available comments id
    """
    try:
        jira = Instance()
        issue_key = args[-1]
        comments = jira.session.comments(issue_key)
        return [(comment.id, f"{comment.author} {comment.created}") for comment in comments]
    except Exception:
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
    try:
        jira = Instance()
        project = ctx.params["project"] if ctx.params["project"] else settings.get("default_project")
        if ctx.params["board"]:
            board = jira.session.boads(name=ctx.params["board"])
        else:
            board = get_project_boards(project)[0]
        sprints = jira.session.sprints(board.id)
        return [(sprint.id, sprint.name) for sprint in sprints]
    except Exception:
        return []


def autocomplete_users(ctx: Context, args: list, incomplete: str) -> ResultList:
    """
    Get Jira users list completion

    Args:
        ctx (click.core.Context): click.core.Context of the given command
        args (list): List of commands args
        incomplete (str): String input to autocomplete

    Returns:
        jira.client.ResultList: List of users corresponding to the incomplete input
    """
    try:
        jira = Instance()
        users = jira.session.search_users(incomplete)
        return [(user.name, user.displayName) for user in users]
    except Exception:
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
    try:
        jira = Instance()
        return [priority.name for priority in jira.session.priorities() if incomplete.lower() in priority.name.lower()]
    except Exception:
        return []


def autocomplete_transitions(ctx: Context, args: list, incomplete: str) -> list:
    """
    Get Jira translations available for an issue

    Args:
        ctx (click.core.Context): click.core.Context of the given command
        args (list): List of commands args
        incomplete (str): String input to autocomplete

    Returns:
        list: List of translation names corresponding to the incomplete input
    """
    try:
        jira = Instance()
        issue_key = args[-1]
        issue = jira.session.issue(issue_key)
        transitions = jira.session.transitions(issue)
        return [
            (t["name"], t["to"]["description"]) for t in transitions if t["name"].lower().startswith(incomplete.lower())
        ]
    except Exception:
        return []


def autocomplete_projects(ctx: Context, args: list, incomplete: str) -> list:
    """
    Get Jira projects list completion

    Args:
        ctx (click.core.Context): click.core.Context of the given command
        args (list): List of commands args
        incomplete (str): String input to autocomplete

    Returns:
        list: List of project names corresponding to the incomplete input
    """
    try:
        jira = Instance()
        projects = jira.session.projects()
        return [(p.key, p.name) for p in projects if incomplete.lower() in p.key.lower()]
    except Exception:
        return []


def autocomplete_issue_types(ctx: Context, args: list, incomplete: str) -> list:
    """
    Get Jira issue types list completion

    Args:
        ctx (click.core.Context): click.core.Context of the given command
        args (list): List of commands args
        incomplete (str): String input to autocomplete

    Returns:
        list: List of issue types names corresponding to the incomplete input
    """
    try:
        jira = Instance()
        issue_types = jira.session.issue_types()
        return [(i.name, i.description) for i in issue_types if incomplete.lower() in i.name.lower()]
    except Exception:
        return []
