from preapp.question import ConfirmQuestion
import subprocess
from preapp import Node


class GithubCloneNode(Node):
    """Clones a github repository"""

    def __init__(self):
        super(GithubCloneNode, self).__init__(
            "github_clone",
            [],
            parents=["metadata", "github", "github_repository", "github_credentials",],
            serializable=False,
        )

    def pre_process(self):
        project_name: str = self.get_full_response()["metadata"]["name"]
        github_username: str = self.get_full_response()["github_credentials"]["username"]
        repo_download_url: str = f"https://github.com/{github_username}/{project_name}.git"
        process = subprocess.Popen(
            f"git clone {repo_download_url}", shell=True, stdout=subprocess.PIPE,
        )
        stdout, _ = process.communicate()


Node.register(GithubCloneNode())
