"""
Module for base Moic cli utils function
"""
import json

import requests
from jira.client import ResultList

from moic.cli import settings
from moic.plugins.jira import Instance


class Board:
    """
    Class representing a Jira Board
    """

    def __init__(self, json_board: dict):
        """
        Init a board

        Args:
            json_board (dict): Json representation of the board
        """
        self.raw = json_board
        self.id = json_board["id"]
        self.name = json_board["name"]
        self.type = json_board["type"]


def sort_issue_per_status(issues: list, project: str = settings.get("default_project", None)) -> list:
    """
    Sort an issue liste based on the project defined workflow

    Args:
        issues (list): The list of Jira issues to sort
        project (str): The Jira project key

    Returns:
        list: The sorted Jira issues list
    """
    sorted_i = []
    w = settings.get(f"projects.{project}.workflow")
    for step in ["new", "indeterminate", "done"]:
        for s in w[step]:
            sorted_i.extend([i for i in issues if i.status.id == s])

    return sorted_i


def get_board_sprints(board_id: str, closed: bool = False) -> dict:
    """
    Return le sprint list of a board

    Args:
        board_id (str): The Jira Board ID
        closed (bool): Indicate if we should returned only opened sprints

    Returns:
        dict: Dict {"board_id": id, "sprints": list} of sprints
    """
    sprints = Instance().session.sprints(board_id)
    if not closed:
        sprints = [jira_sprint for jira_sprint in sprints if jira_sprint.state != "closed"]
    ret = {"board_id": board_id, "sprints": sprints}
    return ret


def get_sprint_story_points(sprint_id: str) -> dict:
    """
    Return the detailled list of story points for a given sprint Id
    Splitted between done points and todo points

    Args:
        sprint_id (str): Jira Sprint ID

    Returns:
        dict: {"sprint_id": id, "points": {"todo": float, "done": float}}
    """

    jira = Instance()
    issues = [
        issue
        for issue in jira.session.search_issues(f"Sprint = {sprint_id}")
        if settings.get("custom_fields.story_points") in issue.raw["fields"].keys()
    ]

    done = [issue for issue in issues if issue.fields.status.statusCategory.key == "done"]
    todo = [issue for issue in issues if issue not in done]

    ret = {
        "sprint_id": sprint_id,
        "points": {
            "done": float(
                sum(
                    [
                        float(
                            0
                            if issue.raw["fields"][settings.get("custom_fields.story_points")] is None
                            else issue.raw["fields"][settings.get("custom_fields.story_points")]
                        )
                        for issue in done
                    ]
                )
            ),
            "todo": float(
                sum(
                    [
                        float(
                            0
                            if issue.raw["fields"][settings.get("custom_fields.story_points")] is None
                            else issue.raw["fields"][settings.get("custom_fields.story_points")]
                        )
                        for issue in todo
                    ]
                )
            ),
        },
    }
    return ret


def get_sprint_issues(sprint_id: str) -> ResultList:
    """
    Returns list of Jira Issues linked to a given Jira Sprint

    Args:
        sprint_id (str): Jira Sprint ID

    Returns
        ResultList: List Jira Issues contained into the sprint
    """
    jira = Instance()
    return jira.session.search_issues(f"sprint = {sprint_id}")


def get_project_boards(project_key: str) -> list:
    """
    Get the board list of a given project

    This function is used waiting the 3.0.0 release of Python Jira
    which include it built-in

    Args:
        project_Key (str): The Jira project Key used to filtered

    Returns:
        list: A list of boards dict
    """

    r_boards = requests.get(
        f'{settings.get("instance")}/rest/agile/latest/board/?type=scrum&projectKeyOrId={project_key}',
        auth=(settings.get("login"), settings.get("password")),
    )

    if r_boards.status_code == 200:
        boards = json.loads(r_boards.content)["values"]
        return [Board(board) for board in boards]
    else:
        return []
