from pobject import I
from url_util import URL


class GitRepo:

    def __init__(self, url):
        self._url = url

    @property
    def url(self):
        return self._url

    @property
    def user_name(self):
        user_name = URL(self.url).first_path_part
        return user_name

    @property
    def name(self):
        name = URL(self.url).second_path_part
        return name

    @classmethod
    def from_repo_input(cls, repo_input) -> 'GitRepo':

        if I(repo_input).is_url:
            return GitRepo(url=repo_input)

        else:
            raise NotImplementedError


