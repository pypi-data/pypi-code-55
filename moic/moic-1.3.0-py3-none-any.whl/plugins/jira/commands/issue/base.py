"""
Module for base Moic issue commands
"""
import os

import click

from moic.cli import COLOR_MAP, PRIORITY_COLORS, console, settings
from moic.cli.utils import get_template, print_comments, print_issue, print_issues
from moic.plugins.jira import Instance
from moic.plugins.jira.core import JiraComment, JiraIssue
from moic.plugins.jira.utils.parser import JiraDocument


def get(id, all, project, search, oneline, subtasks):
    """Get a Jira issue"""
    if not id and not search:
        return console.print("You must specify an issue ID or a search query")
    try:
        jira = Instance()
        if search:
            if project and not all and "project" not in search:
                search = f"{search} AND project = {project}"

            issues = jira.session.search_issues(search)
        else:
            issues = [jira.session.issue(id)]
        issues = [JiraIssue(i) for i in issues]
        print_issues(issues, prefix="", oneline=oneline, subtasks=subtasks)
    except Exception as e:
        console.print(f"[red]Something goes wrong {e}[/red]")


def show(issue_key):
    """Show a Jira Issue description"""
    try:
        jira = Instance()
        issue = jira.session.issue(issue_key)
        jd = JiraDocument(issue.fields.description)
        for element in jd.elements:
            console.print(element.rendered)
    except Exception as e:
        console.print(f"[red]Something goes wrong {e}[/red]")


def add(summary, project, issue_type, priority):
    """Create new issue"""
    tpl = get_template(project, issue_type)
    if tpl:
        tpl_name = tpl.split("/")[-1:][0]
        tpl_project_target = tpl_name.split("_")[1] if tpl_name.split("_")[1] != "all" else "default"
        tpl_issue_target = tpl_name.split("_")[0]

        console.print(
            f"Using [green]{tpl_project_target}[/green] template of [green]{tpl_issue_target}[/green] project [grey70]({tpl})[/grey70]",
            highlight=False,
        )
        with open(os.path.expanduser(tpl), "r") as tpl_file:
            default_description = tpl_file.read()
    else:
        default_description = "h1. Description\n"

    description = click.edit(default_description)

    if description:
        try:
            jira = Instance()
            new_issue = jira.session.create_issue(
                project=project,
                summary=summary,
                description=JiraDocument(description).raw,
                issuetype={"name": issue_type},
            )
            print_issue(JiraIssue(new_issue), oneline=False)
        except Exception as e:
            console.print(f"[red]Something goes wrong {e}[/red]")


def comment(issue_key, comment):
    """Add a comment on an issue"""
    if not comment:
        comment = click.edit("")
    try:
        jira = Instance()
        jira.session.add_comment(issue_key, JiraDocument(comment).raw)
    except Exception as e:
        console.print(f"[red]Something goes wrong {e}[/red]")


def edit_comment(issue_key, comment_id):
    """Edit a comment on an issue"""
    try:
        jira = Instance()
        comment = jira.session.comment(issue_key, comment_id)
        comment.update(body=click.edit(comment.body))
        console.print(f"[green]Comment updated![/green]")
    except Exception as e:
        console.print(f"[red]Something goes wrong {e}[/red]")


def list_comments(issue_key, last, oneline):
    """List comments on an issue"""
    try:
        jira = Instance()
        issue = jira.session.issue(issue_key)
        comments = jira.session.comments(issue)
        if last:
            comments = comments[len(comments) - int(last) :]
        print_comments([JiraComment(c) for c in comments], "", oneline)

    except Exception as e:
        console.print(f"[red]Something goes wrong {e}[/red]")


def assign(issue_key, assignee):
    """Assign a Jira issue"""
    try:
        jira = Instance()
        issue = jira.session.issue(issue_key)
        issue.update(assignee={"name": assignee})
        console.print(
            f"Assigned [green]{assignee}[/green] on [blue]{issue_key}[/blue]", highlight=False,
        )
    except Exception as e:
        console.print(f"[red]Something goes wrong {e}[/red]")


def set_peer(issue_key, peer):
    """Define the peer user on a Jira issue"""
    try:
        jira = Instance()
        issue = jira.session.issue(issue_key)
        peer_user = jira.session.search_users(peer)
        if peer_user:
            issue.update(fields={settings.get("custom_fields.peer"): {"name": peer}})
        console.print(
            f"Peer [green]{peer}[/green] added on [blue]{issue_key}[/blue]", highlight=False,
        )
    except Exception as e:
        console.print(f"[red]Something goes wrong {e}[/red]")


def add_subtasks(issue_key, subtask):
    """Add subtasks to a Jira issue"""
    try:
        jira = Instance()

        issue = jira.session.issue(issue_key)
        if not subtask:
            description = "# Creates one subtask per line (separate summary and description with '|'"
            subtasks_list = click.edit(description).split("\n")
            subtask = [sub for sub in subtasks_list if not sub.startswith("#")]

        for sub in subtask:
            summary = sub
            description = ""
            if "|" in sub:
                summary, description = sub.split("|")
            new_subtask = jira.session.create_issue(
                project={"key": issue.fields.project.key},
                summary=summary,
                description=JiraDocument(description).raw,
                issuetype={"name": "Sub-task"},
                parent={"key": issue.key},
            )
            print_issue(JiraIssue(new_subtask), oneline=True)
            console.line()

    except Exception as e:
        console.print(f"[red]Something goes wrong {e}[/red]")


def move(issue_key, transition):
    """Apply a transition on a Jira issue"""
    try:
        jira = Instance()
        issue = jira.session.issue(issue_key)
        transitions = jira.session.transitions(issue)
        transition = [t for t in transitions if t["name"] == transition]
        if transition:
            transition = transition[0]
            jira.session.transition_issue(issue, transition["id"])
            console.print(
                f"Moved [green]{issue_key}[/green] to [{COLOR_MAP[transition['to']['statusCategory']['colorName']]}]{transition['name']}[/{COLOR_MAP[transition['to']['statusCategory']['colorName']]}] status",
                highlight=False,
            )
        else:
            console.print(f"[yellow]No transition available for {issue_key}[/yellow]")

    except Exception as e:
        console.print(f"[red]Something goes wrong {e}[/red]")


def rank(issue_key, priority):
    """Change the priority of a Jira issue"""
    try:
        jira = Instance()
        issue = jira.session.issue(issue_key)
        issue.update(fields={"priority": {"name": priority}})
        console.print(f"[green]{issue_key}[/green] ranked to [{PRIORITY_COLORS[priority]}]{priority}[/]")
    except Exception as e:
        console.print(f"[red]Something goes wrong {e}[/red]")
