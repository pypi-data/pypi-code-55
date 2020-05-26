from preapp import Node, ConfirmQuestion
from typing import List, Dict, Any
import subprocess
import os
from preapp.utils import commit_and_push
import json
from preapp.utils.fileio import copy_file, file_to_json, raw_to_json_file
from preapp.utils.miscellaneous import bash
from preapp.hooks import call_hook


class GithubActionsNode(Node):
    """Checks if the user wants to use github actions"""

    def __init__(self):
        super(GithubActionsNode, self).__init__(
            "github_actions",
            [ConfirmQuestion("use", "Do you want to add github actions?", True)],
            parents=["github", "github_repository", "github_credentials", "framework",],
        )

    def post_process(self, responses):
        if responses["use"] == True:
            frameworks: Dict[str, Any] = self.get_full_response()["framework"]
            if "web_frontend" in frameworks:
                project_name: str = self.get_full_response()["metadata"]["name"]

                bash(f"cd {project_name} && mkdir .github && cd .github && mkdir workflows")

                call_hook("github_actions", "web_frontend", frameworks["web_frontend"])


Node.register(GithubActionsNode())


def commit_actions_file(
    actions_filepath: str, project_name: str, github_username: str, github_password: str
) -> None:
    copy_file(actions_filepath, f"{os.getcwd()}/{project_name}/.github/workflows/nodejs.yml")

    commit_and_push(
        "Setup Github Actions",
        project_name,
        github_username,
        github_password,
        directory=project_name,
    )
