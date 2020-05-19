"""
Module for base Moic sprint commands
"""
import concurrent.futures
from datetime import datetime

import click
from rich.progress import track

from moic.cli import COLOR_MAP, SPRINT_STATUS_COLORS, console, global_settings, settings
from moic.cli.completion import autocomplete_boards, autocomplete_projects, autocomplete_sprints
from moic.cli.utils import print_issue, print_status
from moic.plugins.jira import Instance
from moic.plugins.jira.core import JiraIssue, JiraStatus
from moic.plugins.jira.utils import get_board_sprints, get_project_boards, get_sprint_issues, get_sprint_story_points

STEPS = ["new", "indeterminate", "done"]

# TODO: Add 'add' and 'remove' from sprint
# TODO: Deal with Jira custom fields
# TODO: Deal with Jira Board mechanism
@click.group()
def sprint():
    """Create, edit, list Jira Sprints"""
    if not global_settings.get("current_context"):
        console.print("[yellow]No context defined yet[/yellow]")
        console.print("[grey]> Please run '[bold]moic context add[/bold]' to setup configuration[/grey]")
        console.line()
        exit(0)
    if not settings.get("custom_fields.story_points"):
        Instance().custom_config(settings.get("default_project"))
        return


@sprint.command()
@click.option(
    "--board", type=click.STRING, default=None, help="Specify Jira Board name", autocompletion=autocomplete_boards
)
@click.option(
    "--project",
    default=settings.get("default_project", None),
    help="Specify a project key",
    autocompletion=autocomplete_projects,
)
@click.option("--closed", type=click.BOOL, default=False, help="Dislay closed sprints", is_flag=True)
@click.option("--oneline", type=click.BOOL, default=False, help="Display sprint on oneline", is_flag=True)
def list(board, project, closed, oneline):
    """List Jira Sprints"""
    try:
        jira = Instance()
        if not board:
            if project and project != "all":
                # This function is used waiting the 3.0.0 release of Python Jira
                # which include it built-in
                # jira_boards = jira.session.boards(type="scrum", projectKeyOrID=project)
                jira_boards = get_project_boards(project)
            else:
                jira_boards = jira.session.boards(type="scrum")
        else:
            jira_boards = jira.session.boards(name=board)

        data = {}
        output = ""

        # Building data
        for jira_board in track(jira_boards, description="Building output..."):
            # Get board sprints
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = [executor.submit(get_board_sprints, jira_board.id, closed) for jira_board in jira_boards]

                for idx, future in enumerate(concurrent.futures.as_completed(futures, timeout=180.0)):
                    res = future.result()
                    data[res["board_id"]] = {
                        "board": [jb for jb in jira_boards if jb.id == res["board_id"]][0],
                        "sprints": res["sprints"],
                    }

            # Get sprint points
            points = {}
            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                futures = [executor.submit(get_sprint_story_points, js.id) for js in data[jira_board.id]["sprints"]]
                for idx, future in enumerate(concurrent.futures.as_completed(futures, timeout=180.0)):
                    res = future.result()
                    points[res["sprint_id"]] = res["points"]

            output = output + f"[blue]{jira_board.name}[/blue] [grey70]({jira_board.id})[/grey70]\n"
            for jira_sprint in data[jira_board.id]["sprints"]:
                prefix = " └─ " if jira_sprint == data[jira_board.id]["sprints"][-1] else " ├─ "
                detail_prefix = "    " if jira_sprint == data[jira_board.id]["sprints"][-1] else " │  "
                goal = jira_sprint.goal if hasattr(jira_sprint, "goal") else ""
                startDate = (
                    datetime.strptime(jira_sprint.startDate.split(".")[0], "%Y-%m-%dT%H:%M:%S").strftime("%m/%d/%Y")
                    if hasattr(jira_sprint, "startDate")
                    else ""
                )
                endDate = (
                    datetime.strptime(jira_sprint.endDate.split(".")[0], "%Y-%m-%dT%H:%M:%S").strftime("%m/%d/%Y")
                    if hasattr(jira_sprint, "endDate")
                    else ""
                )
                sprint_color = COLOR_MAP[SPRINT_STATUS_COLORS[jira_sprint.state]]
                points_values = f"( {points[jira_sprint.id]['done']} / {points[jira_sprint.id]['done'] + points[jira_sprint.id]['todo']} )"
                if oneline:
                    output = (
                        output
                        + f"{prefix}[grey70]({jira_sprint.id})[/grey70] [{sprint_color}]{jira_sprint.name}[/{sprint_color}] {points_values} - [grey70]{startDate} - {endDate}[/grey70]\n"
                    )
                else:
                    output = (
                        output
                        + f"{prefix}[grey70]({jira_sprint.id})[/grey70] [{sprint_color}]{jira_sprint.name}[/{sprint_color}] {points_values}\n"
                    )
                    output = output + f"{detail_prefix}Goal  : {goal}\n"
                    output = output + f"{detail_prefix}Dates : [grey70]{startDate} - {endDate}[/grey70]\n"

        console.print(output)

    except Exception as e:
        console.print(f"[red]Something goes wrong {e}[/red]")


@sprint.command()
@click.option(
    "--board", type=click.STRING, default=None, help="Specify Jira Board name", autocompletion=autocomplete_boards
)
@click.option(
    "--sprint", type=click.STRING, default=None, help="Specify Jira Sprint id", autocompletion=autocomplete_sprints
)
@click.option(
    "--project",
    default=settings.get("default_project", None),
    help="Specify a project key",
    autocompletion=autocomplete_projects,
)
@click.option("--subtasks", default=False, help="Display story subtask", is_flag=True)
def get(board, sprint, project, subtasks):
    """Get Jira sprints link to a board"""
    if not settings.get(f"projects.{project}.workflow"):
        Instance().configure_agile(project)

    jira = Instance()
    if not board:
        # This function is used waiting the 3.0.0 release of Python Jira
        # which include it built-in
        # jira_boards = jira.session.boards(type="scrum", projectKeyOrID=project)[0]
        boards = get_project_boards(project)
        if not boards:
            console.print("[yellow]No board found[/yellow]")
            exit(1)
        board = boards[0]
    else:
        board = jira.session.boards(name=board)[0]
    if not sprint:
        sprints = jira.session.sprints(board.id, state="active")
    else:
        sprints = [jira.session.sprint(sprint)]

    jira_statuses = jira.session.statuses()
    if sprints:
        for sprint in sprints:
            if hasattr(sprint, "goal"):
                sprint_goal = sprint.goal
            else:
                sprint_goal = ""
            console.print()
            console.print(f"[grey70]({sprint.id})[/grey70] {sprint.name} : {sprint_goal}")
            console.print()
            issues = get_sprint_issues(sprint.id)

            workflow = settings.get(f"projects.{project}.workflow")

            for step in STEPS:
                statuses = workflow.get(step).to_list()
                for status_id in statuses:
                    if "," not in status_id:
                        status = [s for s in jira_statuses if s.id == status_id][0]
                        issues_to_display = [
                            issue
                            for issue in issues
                            if issue.fields.status.name == status.name and issue.fields.issuetype.name == "Story"
                        ]
                        if issues_to_display:
                            print_status([JiraStatus(status)])
                            for i in issues_to_display:
                                i = JiraIssue(i)
                                last = True if i.key == issues_to_display[-1].key else False
                                prefix = " └─ " if last else " ├─ "
                                print_issue(i, prefix=prefix, oneline=True, subtasks=subtasks, last=last)
                    else:
                        status_for_step = [s for s in jira_statuses if s.id in status_id.split(",")]
                        issues_to_display = [
                            issue
                            for issue in issues
                            if issue.fields.status.name in [status.name for status in status_for_step]
                            and issue.fields.issuetype.name == "Story"
                        ]
                        if issues_to_display:
                            print_status([JiraStatus(s) for s in status_for_step])
                            for i in issues_to_display:
                                i = JiraIssue(i)
                                last = True if i.key == issues_to_display[-1].key else False
                                prefix = " └─ " if last else " ├─ "
                                print_issue(i, prefix=prefix, oneline=True, subtasks=subtasks, last=last)
    else:
        console.print("[yellow]No sprint found[/yellow]")
