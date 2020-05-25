import shutil
import sys
from enum import Enum, unique
from pathlib import Path
from subprocess import PIPE, call, run
from typing import Optional, Tuple, Union


@unique
class CheckoutType(Enum):
    BRANCH = "branch"
    TAG = "tag"
    COMMIT = "commit"


class CheckoutCommand:
    def __init__(self, type: CheckoutType, value: str):
        self.type = type
        self.value = value


DEFAULT_COMMAND = CheckoutCommand(CheckoutType.BRANCH, "master")


def load_repo(
    path: Union[Path, str],
    repo_url: str,
    branch: str = None,
    tag: str = None,
    commit: str = None,
    use_existing: bool = False,
) -> Optional[str]:
    """
    Load repository from "repo_url" into "path" folder. Only one parameter from "branch", "tag" or "commit" must be
    defined. If no one of these parameters are defined function use default value branch='master'.

    :param path: target folder for repository
    :param repo_url:  repository url
    :param branch: branch name
    :param tag: tag name
    :param commit: commit hash
    :param use_existing: use existing repo
    :return: optional error description
    """

    command, error = _extract_fetch_type(branch, tag, commit)
    if error:
        return error

    path = Path(path).expanduser().absolute()

    if path.exists() and not _dir_is_empty(path):
        if not use_existing:
            return "Use of existing repository is forbidden"

        actual_origin, error = _remote_url(path)
        if error:
            return error
        if actual_origin != repo_url:
            return "Path {} expected to contain {} repo but was {}".format(path, repo_url, actual_origin)

        return checkout_existing_repo(path, command)

    else:
        return checkout_new_repo(path, repo_url, command)


def checkout_existing_repo(path: Path, checkout: CheckoutCommand) -> Optional[str]:
    git_dir = str(path.joinpath(".git"))
    path = str(path)

    code = call(["git", "--git-dir", git_dir, "--work-tree", path, "fetch", "--unshallow"])
    if code:
        code = call(["git", "--git-dir", git_dir, "--work-tree", path, "fetch"])
    if code:
        return "git fetch exited with code {}".format(code)

    if checkout.type is CheckoutType.BRANCH:
        code = call(["git", "--git-dir", git_dir, "--work-tree", path, "checkout", checkout.value])
        if code == 0:
            code = call(["git", "--git-dir", git_dir, "--work-tree", path, "pull"])
    elif checkout.type in [CheckoutType.TAG, CheckoutType.COMMIT]:
        code = call(["git", "--git-dir", git_dir, "--work-tree", path, "checkout", checkout.value])
    else:
        return "Unknown checkout type {}".format(checkout.type)
    if code:
        return "git fetch exited with code {}".format(code)


def checkout_new_repo(path: Path, url: str, checkout: CheckoutCommand) -> Optional[str]:
    path.mkdir(parents=True, exist_ok=True)
    git_dir = str(path.joinpath(".git"))
    path = str(path)

    if checkout.type in [CheckoutType.BRANCH, CheckoutType.TAG]:
        code = call(["git", "clone", "--branch", checkout.value, "--depth", "1", url, path])
        if code:
            return "git clone exited with code {}".format(code)
    elif checkout.type is CheckoutType.COMMIT:
        code = call(["git", "clone", url, path])
        if code:
            return "git clone exited with code {}".format(code)
        code = call(["git", "--git-dir", git_dir, "--work-tree", path, "checkout", checkout.value])
        if code:
            return "git checkout exited with code {}".format(code)
    else:
        return "Unknown checkout type {}".format(checkout.type)


def _extract_fetch_type(branch: str, tag: str, commit: str) -> Tuple[Optional[CheckoutCommand], Optional[str]]:
    values = list(
        filter(
            lambda c: c.value is not None,
            [
                CheckoutCommand(CheckoutType.BRANCH, branch),
                CheckoutCommand(CheckoutType.TAG, tag),
                CheckoutCommand(CheckoutType.COMMIT, commit),
            ],
        )
    )

    if len(values) == 0:
        return DEFAULT_COMMAND, None
    elif len(values) != 1:
        return None, "Too many checkout parameters: {}".format(values)

    return values[0], None


def _remote_url(repo_dir: Path) -> Tuple[Optional[str], Optional[str]]:
    git_dir = str(repo_dir.joinpath(".git"))
    repo_dir = str(repo_dir.as_posix())

    result = run(
        ["git", "--git-dir", git_dir, "--work-tree", repo_dir, "remote", "get-url", "origin"], stdout=PIPE, stderr=PIPE
    )
    if len(result.stderr) == 0 and len(result.stdout) != 0:
        return result.stdout.decode(sys.stdout.encoding).strip("\n "), None
    else:
        return None, result.stderr.decode(sys.stderr.encoding)


def _dir_is_empty(directory: Path) -> bool:
    return next(directory.iterdir(), None) is None


def _git_version() -> Optional[str]:
    if shutil.which("git"):
        result = run(["git", "--version"], stdout=PIPE)
        return result.stdout.decode(sys.stdout.encoding).strip("\n ").split(" ")[-1]
    else:
        return None
