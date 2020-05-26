from preapp.hooks import action_hook
from preapp.node import Node
from preapp.utils.miscellaneous import bash
from preapp.utils.github import commit_and_push
from preapp.utils import __assets_directory__
import os
from preapp.utils.fileio import copy_file, file_to_text, text_to_file


@action_hook("framework", "web_backend", "python")
def setup_module():
    project_name: str = Node.get_full_response()["metadata"]["name"]

    bash(f"cd {project_name} && mkdir backend")
    copy_file(
        f"{__assets_directory__}/python/module/requirements.txt",
        f"{os.getcwd()}/{project_name}/backend/requirements.txt",
    )
    copy_file(
        f"{__assets_directory__}/python/module/setup.py",
        f"{os.getcwd()}/{project_name}/backend/setup.py",
    )

    source: str = file_to_text(f"{os.getcwd()}/{project_name}/backend/setup.py")
    source = source.replace("__NAME__", Node.get_full_response()["metadata"]["name"])
    source = source.replace("__VERSION__", Node.get_full_response()["metadata"]["version"])
    source = source.replace("__DESCRIPTION__", Node.get_full_response()["metadata"]["description"])
    source = source.replace("__AUTHOR__", Node.get_full_response()["metadata"]["owner"])
    source = source.replace("__EMAIL__", Node.get_full_response()["metadata"]["owner_email"])
    source = source.replace(
        "__LICENSE__",
        Node.get_full_response()["metadata"]["license"][1:].partition("]")[0].upper(),
    )

    text_to_file(source, f"{os.getcwd()}/{project_name}/backend/setup.py")

    copy_file(
        f"{__assets_directory__}/python/module/noxfile.py",
        f"{os.getcwd()}/{project_name}/backend/noxfile.py",
    )

    # backend/<project_name> directory
    bash(f"cd {project_name}/backend && mkdir {project_name}")
    bash(f'cd {project_name}/backend/{project_name} && echo "" > __init__.py')
    copy_file(
        f"{__assets_directory__}/python/module/__main__.py",
        f"{os.getcwd()}/{project_name}/backend/{project_name}/__main__.py",
    )

    # backend/tests directory
    bash(f"cd {project_name}/backend && mkdir tests")
    copy_file(
        f"{__assets_directory__}/python/module/__test_util.py",
        f"{os.getcwd()}/{project_name}/backend/tests/test_util.py",
    )

    # setup the virtual environment
    bash(f"cd {project_name}/backend && python -m venv {project_name}-env")
    bash(f"cd {project_name}/backend && python -m pip install nox")

    github_username: str = Node.get_full_response()["github_credentials"]["username"]
    github_auth: str = ""
    if "password" in Node.get_full_response()["github_credentials"]:
        github_auth = Node.get_full_response()["github_credentials"]["password"]
    if "oauth_token" in Node.get_full_response()["github_credentials"]:
        github_auth = Node.get_full_response()["github_credentials"]["oauth_token"]

    commit_and_push(
        "Initialized Python backend",
        project_name,
        github_username,
        github_auth,
        directory=project_name,
    )
