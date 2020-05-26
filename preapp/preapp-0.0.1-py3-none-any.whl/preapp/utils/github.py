import subprocess
import github


_CACHED_AUTHENTICATED_USER: github.AuthenticatedUser = None


def get_authenticated_user(
    username: str = None, password: str = None, oauth_token: str = None
) -> github.AuthenticatedUser:
    global _CACHED_AUTHENTICATED_USER

    if oauth_token != None:
        _CACHED_AUTHENTICATED_USER = github.Github(oauth_token).get_user()
    if username != None and password != None:
        _CACHED_AUTHENTICATED_USER = github.Github(username, password).get_user()

    if _CACHED_AUTHENTICATED_USER == None:
        raise PermissionError("No user has been authenticated")

    return _CACHED_AUTHENTICATED_USER


def clone(project_owner: str, project_name: str) -> None:
    repo_download_url: str = f"https://github.com/{project_owner}/{project_name}.git"
    process = subprocess.Popen(
        f"git clone {repo_download_url}", shell=True, stdout=subprocess.PIPE,
    )
    stdout, _ = process.communicate()


def commit_and_push(
    commit_message: str,
    project_name: str,
    username: str,
    password: str,
    project_owner: str = "",
    directory: str = ".",
) -> None:

    if project_owner == "":
        project_owner = username

    process = subprocess.Popen(
        f'cd {directory} && git add . && git commit -m "{commit_message}" && git push https://{username}:{password}@github.com/{project_owner}/{project_name}.git',
        shell=True,
        stdout=subprocess.PIPE,
    )
    stdout, _ = process.communicate()
