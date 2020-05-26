from ... import InputQuestion, PasswordQuestion, Node
from preapp.utils import get_authenticated_user


class GithubCredentialsNode(Node):
    """Gets github credentials"""

    def __init__(self):
        super(GithubCredentialsNode, self).__init__(
            "github_credentials", [], serializable=False, parents=["github"],
        )

    def pre_process(self):
        if not "oauth_token" in self.get_full_response()["github_credentials"]:
            self.add_question(InputQuestion("username", "Enter your github username"))
            self.add_question(PasswordQuestion("password", "Enter your github password"))

    def post_process(self, responses):
        if "username" in responses and "password" in responses:
            username: str = responses["username"]
            password: str = responses["password"]
            # authenticate the user and cache it
            get_authenticated_user(username, password)
        if "oauth_token" in responses:
            oauth_token: str = responses["oauth_token"]
            get_authenticated_user(oauth_token=oauth_token)


Node.register(GithubCredentialsNode())
