from preapp import Node, ConfirmQuestion
from preapp.utils.fileio import file_to_json, get_all_assets
from preapp.question import CheckboxQuestion, ListQuestion
from preapp.utils.github import get_authenticated_user
import github


class AccountsNode(Node):
    """Allows users to select accounts related features"""

    def __init__(self):
        super(AccountsNode, self).__init__(
            "accounts", [], parents=["metadata", "github_credentials", "features"]
        )
        self.account_features_data = {}

    def pre_process(self):
        # get all json files in assets/features
        self.accounts_features_data = file_to_json(get_all_assets("features", "accounts.json")[0])
        # create questions
        self.add_question(
            CheckboxQuestion(
                "functions",
                "Select all the functionality you want for accounts",
                list(map(lambda x: x["name"], self.accounts_features_data["functions"])),
            )
        )

    def post_process(self, responses):
        for account_function in responses["functions"]:
            github_user: github.AuthenticatedUser = get_authenticated_user()
            project_name: str = Node.get_full_response()["metadata"]["name"]
            github_repo: github.Repository = github_user.get_repo(project_name)
            user_story = list(
                filter(
                    lambda x: x["name"] == account_function,
                    self.accounts_features_data["functions"],
                )
            )[0]["user_story"]
            github_repo.create_issue(
                f"add support for account {account_function}", f"{user_story}",
            )


Node.register(AccountsNode())
