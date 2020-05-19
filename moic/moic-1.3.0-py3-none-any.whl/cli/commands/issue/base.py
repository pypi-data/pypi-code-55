"""
Module for base Moic issue commands
"""
import click

from moic.cli import console, global_settings, logger, settings
from moic.cli.completion import (
    autocomplete_comments,
    autocomplete_issue_types,
    autocomplete_priorities,
    autocomplete_projects,
    autocomplete_transitions,
    autocomplete_users,
)
from moic.cli.utils import get_plugin_command
from moic.cli.validators import (
    validate_comment_id,
    validate_issue_key,
    validate_issue_type,
    validate_project_key,
    validate_user,
)


# TODO: Add change issue type command
# TODO: Manage labels
# TODO: Manage components
@click.group()
def issue():
    """Create, edit, list Jira issues"""
    logger.debug("Execute 'issue' command")
    if not global_settings.get("current_context"):
        console.print("[yellow]No context defined yet[/yellow]")
        console.print("[grey]> Please run '[bold]moic context add[/bold]' to setup configuration[/grey]")
        console.line()
        exit(0)


@issue.command()
@click.argument(
    "issue_key", type=click.STRING, callback=validate_issue_key, required=False,
)
@click.option("--all-projects", default=False, help="Search over all Jira Projects")
@click.option(
    "--project",
    default=settings.get("default_project", None),
    help="Project ID to scope search",
    autocompletion=autocomplete_projects,
    callback=validate_project_key,
)
@click.option("--search", default=None, help="JQL query for searching issues")
@click.option("--oneline", default=False, help="Dislay issue on one line", is_flag=True)
@click.option("--subtasks", default=False, help="Dislay issue subtasks", is_flag=True)
def get(issue_key, all_projects, project, search, oneline, subtasks):
    """
    Get an issue
    """
    logger.debug("Execute 'issue get' command")
    command = get_plugin_command("issue", "get")
    command(issue_key, all_projects, project, search, oneline, subtasks)


@issue.command()
@click.argument(
    "issue-key", type=click.STRING, callback=validate_issue_key,
)
def show(issue_key):
    """
    Show an issue
    """
    logger.debug("Execute 'issue show' command")
    command = get_plugin_command("issue", "show")
    command(issue_key)


# TODO : Add more options : Assignee, epic, sprint, parent
# TODO : Add tests
@issue.command()
@click.argument("summary")
@click.option(
    "--project",
    default=settings.get("default_project", None),
    help="Jira project where create the issue",
    autocompletion=autocomplete_projects,
    callback=validate_project_key,
)
@click.option(
    "--issue-type",
    default="Story",
    help="Jira issue type",
    autocompletion=autocomplete_issue_types,
    callback=validate_issue_type,
)
@click.option("--priority", default="", help="Jira issue priority")
def add(summary, project, issue_type, priority):
    """
    Add an issue
    """
    logger.debug("Execute 'issue add' command")
    command = get_plugin_command("issue", "add")
    command(summary, project, issue_type, priority)


@issue.command()
@click.argument(
    "issue-key", type=click.STRING, callback=validate_issue_key,
)
@click.option("--comment", default=None, help="Comment to add on Jira issue")
def comment(issue_key, comment):
    """
    Comment an issue
    """
    logger.debug("Execute 'issue comment' command")
    command = get_plugin_command("issue", "comment")
    command(issue_key, comment)


@issue.command()
@click.argument(
    "issue-key", type=click.STRING, callback=validate_issue_key,
)
@click.option("--last", default=None, help="Only display the last n comments")
@click.option("--oneline", default=False, help="Dislay comments on one line", is_flag=True)
def list_comments(issue_key, last, oneline):
    """
    List comment of an issue
    """
    logger.debug("Execute 'issue list-comments' command")
    command = get_plugin_command("issue", "list_comments")
    command(issue_key, last, oneline)


@issue.command()
@click.argument(
    "issue-key", type=click.STRING, callback=validate_issue_key,
)
@click.argument("comment-id", type=click.STRING, callback=validate_comment_id, autocompletion=autocomplete_comments)
def edit_comment(issue_key, comment_id):
    """
    List comment of an issue
    """
    logger.debug("Execute 'issue edit-comment' command")
    command = get_plugin_command("issue", "edit_comment")
    command(issue_key, comment_id)


@issue.command()
@click.argument("issue_key", type=click.STRING, callback=validate_issue_key)
@click.argument("assignee", type=click.STRING, autocompletion=autocomplete_users)
def assign(issue_key, assignee):
    """
    Assign an issue to a user
    """
    logger.debug("Execute 'issue assignee' command")
    command = get_plugin_command("issue", "assign")
    command(issue_key, assignee)


@issue.command()
@click.argument(
    "issue-key", type=click.STRING, callback=validate_issue_key,
)
@click.argument("peer", type=click.STRING, autocompletion=autocomplete_users, callback=validate_user)
def set_peer(issue_key, peer):
    """
    Assign a peer on an issue
    """
    logger.debug("Execute 'issue set-peer' command")
    command = get_plugin_command("issue", "set_peer")
    command(issue_key, peer)


@issue.command()
@click.argument(
    "issue-key", type=click.STRING, callback=validate_issue_key,
)
@click.option("--subtask", "-s", type=click.STRING, help="The subtask title", multiple=True)
def add_subtasks(issue_key, subtask):
    """
    Add subtasks an issue
    """
    logger.debug("Execute 'issue add-subtasks' command")
    command = get_plugin_command("issue", "add_subtasks")
    command(issue_key, subtask)


@issue.command()
@click.argument("issue-key", type=click.STRING, callback=validate_issue_key)
@click.argument("transition", type=click.STRING, autocompletion=autocomplete_transitions)
def move(issue_key, transition):
    """
    Apply a transition on an issue
    """
    logger.debug("Execute 'issue move' command")
    command = get_plugin_command("issue", "move")
    command(issue_key, transition)


@issue.command()
@click.argument(
    "issue-key", type=click.STRING, callback=validate_issue_key,
)
@click.argument(
    "priority", type=click.STRING, autocompletion=autocomplete_priorities,
)
def rank(issue_key, priority):
    """
    Change the priority of an issue
    """
    logger.debug("Execute 'issue rank' command")
    command = get_plugin_command("issue", "rank")
    command(issue_key, priority)
