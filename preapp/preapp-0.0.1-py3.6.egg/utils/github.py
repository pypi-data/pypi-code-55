import subprocess


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
