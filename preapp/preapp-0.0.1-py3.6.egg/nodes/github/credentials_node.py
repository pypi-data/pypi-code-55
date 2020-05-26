from ... import InputQuestion, PasswordQuestion, Node


class GithubCredentialsNode(Node):
    """Gets github credentials"""

    def __init__(self):
        super(GithubCredentialsNode, self).__init__(
            "github_credentials",
            [
                InputQuestion("username", "Enter your github username",),
                PasswordQuestion("password", "Enter your github password",),
            ],
            serializable=False,
            parents=["github"],
        )


Node.register(GithubCredentialsNode())
