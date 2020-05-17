from pathlib import Path

from git_util.git_object import Git
from git_util.git_repo import GitRepo


def clone(repo_input, host_path):

    git = Git()

    repo = GitRepo.from_repo_input(repo_input)

    repo_path = str(Path(host_path).joinpath(repo.user_name).joinpath(repo.name))

    result = git.clone(repo=repo, path=repo_path)

    return result, repo_path

