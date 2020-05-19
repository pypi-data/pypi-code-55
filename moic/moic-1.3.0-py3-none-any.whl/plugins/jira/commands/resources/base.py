"""
Module for base Moic resources commands
"""
from moic.cli import COLOR_MAP, console
from moic.plugins.jira import Instance


def projects():
    """List Jira Projects"""
    jira = Instance()
    projects = jira.session.projects()
    for p in projects:
        console.print(
            f"[grey70]{p.name.ljust(20)}[/grey70] : [magenta]{p.key}[/magenta]", highlight=False,
        )


def issue_type():
    """List Jira Issue Type"""
    jira = Instance()
    issue_types = jira.session.issue_types()
    for i in issue_types:
        console.print(
            f"[grey70]{i.name.ljust(20)}[/grey70] : [green]{i.description}[/green]", highlight=False,
        )


def priorities():
    """List Jira Priorities"""
    jira = Instance()
    priorities = jira.session.priorities()
    for p in priorities:
        console.print(
            f"[grey70]{p.name.ljust(10)}[/grey70] : [green]{p.description}[/green]", highlight=False,
        )


def status():
    """List Jira status"""
    jira = Instance()
    statuses = jira.session.statuses()
    for s in statuses:
        color_name = COLOR_MAP[s.raw["statusCategory"]["colorName"]]
        console.print(
            f"[{color_name}]{s.name.ljust(25)}[/{color_name}] : [grey70]{s.description}[/grey70]", highlight=False,
        )
