from preapp import Node, ListQuestion
from github import Github
from preapp.utils import __assets_directory__, get_authenticated_user
from typing import Dict, Any
import json
from preapp.utils.fileio import file_to_json


class GithubLabelsNode(Node):
    """Gives the users an option to change the label presets for their repository"""

    def __init__(self):
        super(GithubLabelsNode, self).__init__(
            "github_labels",
            [
                ListQuestion(
                    "organization",
                    "Select the label organization for your repository?",
                    ["default", "PST"],
                )
            ],
            parents=["metadata", "github_credentials", "github_repository"],
        )

    def post_process(self, responses):
        if responses["organization"] == "PST":
            repo_name: str = self.get_full_response()["metadata"]["name"]

            remove_all_labels(repo_name)

            github_user: AuthenticatedUser = get_authenticated_user()
            repo_object = github_user.get_repo(repo_name)

            for item in file_to_json(f"{__assets_directory__}/github/labels/pst.json"):
                repo_object.create_label(item["name"], item["color"], item["description"])


Node.register(GithubLabelsNode())


def remove_all_labels(repository_name: str) -> None:
    github_user: AuthenticatedUser = get_authenticated_user()

    for label in github_user.get_repo(repository_name).get_labels():
        label.delete()
