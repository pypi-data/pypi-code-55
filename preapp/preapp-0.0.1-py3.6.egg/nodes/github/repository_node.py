from ... import Node, ConfirmQuestion
from github import Github


class GithubRepositoryNode(Node):
    """Creates a github repo"""

    def __init__(self):
        super(GithubRepositoryNode, self).__init__(
            "github_repository",
            [ConfirmQuestion("create", "Do you want to create a github repository?", True)],
            parents=["github", "github_credentials"],
        )

    def post_process(self, responses):
        if responses["create"] == True:
            github_username: str = self.get_full_response()["github_credentials"]["username"]
            github_password: str = self.get_full_response()["github_credentials"]["password"]

            github_object = Github(github_username, github_password)

            repo_name: str = self.get_full_response()["metadata"]["name"]
            repo_description: str = self.get_full_response()["metadata"]["description"]

            # parse the repo string. currently in format "[key]: name" where <key> is the
            # parameter that should be passed to github
            repo_license: str = self.get_full_response()["metadata"]["license"][1:]
            repo_license = repo_license.partition("]")[0]

            github_object.get_user().create_repo(
                name=repo_name,
                description=repo_description,
                license_template=repo_license,
                auto_init=True,
            )

            # allow for github actions to be added
            self.add_child("github_actions")
            self.add_child("github_labels")


Node.register(GithubRepositoryNode())
