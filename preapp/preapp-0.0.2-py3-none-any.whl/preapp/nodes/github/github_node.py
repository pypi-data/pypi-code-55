from preapp import Node, ConfirmQuestion


class GithubNode(Node):
    """Checks if the user wants to connect their github"""

    def __init__(self):
        super(GithubNode, self).__init__(
            "github", [ConfirmQuestion("use", "Do you want to connect your github?", True)],
        )

    def post_process(self, responses):
        if responses["use"] == True:
            self.add_child("github_credentials")
            self.add_child("github_repository")


Node.register(GithubNode())
