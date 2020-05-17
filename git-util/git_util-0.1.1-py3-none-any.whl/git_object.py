
from git_util.git_repo import GitRepo

import git as git_lib


class Git:

    def __init__(self):
        pass

    @staticmethod
    def clone(repo: GitRepo, path: str):
        result = git_lib.Repo.clone_from(repo.url, path)
        return result


