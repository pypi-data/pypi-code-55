from preapp import Node, ListQuestion
from github import Github
from preapp.utils import __assets_directory__
from typing import Dict, Any
import json


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
            github_username: str = self.get_full_response()["github_credentials"]["username"]
            github_password: str = self.get_full_response()["github_credentials"]["password"]
            repo_name: str = self.get_full_response()["metadata"]["name"]

            remove_all_labels(github_username, github_password, repo_name)

            pst_src: TextIOWrapper = open(f"{__assets_directory__}/github/labels/pst.json", "r")
            pst_data = json.load(pst_src)
            pst_src.close()

            github_object = Github(github_username, github_password)
            repo_object = github_object.get_user().get_repo(repo_name)

            for item in pst_data:
                repo_object.create_label(item["name"], item["color"], item["description"])


Node.register(GithubLabelsNode())


def remove_all_labels(github_username: str, github_password: str, repository_name: str) -> None:
    github_object = Github(github_username, github_password)
    for label in github_object.get_user().get_repo(repository_name).get_labels():
        label.delete()
