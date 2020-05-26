from preapp.hooks import action_hook
from preapp.node import Node
from preapp.utils.miscellaneous import bash
from preapp.utils.github import commit_and_push
from preapp.utils import __assets_directory__
import os
from preapp.utils.fileio import copy_file, file_to_json, raw_to_json_file


@action_hook("framework", "web_frontend", "angular")
def setup():
    project_name: str = Node.get_full_response()["metadata"]["name"]
    bash("sudo npm install -g @angular/cli")

    if not Node.get_full_response()["github"]["use"]:
        bash(f"ng new {project_name}")
    else:
        github_username: str = Node.get_full_response()["github_credentials"]["username"]
        github_auth: str = ""
        if "password" in Node.get_full_response()["github_credentials"]:
            github_auth = Node.get_full_response()["github_credentials"]["password"]
        if "oauth_token" in Node.get_full_response()["github_credentials"]:
            github_auth = Node.get_full_response()["github_credentials"]["oauth_token"]

        bash(f"cd {project_name} && ng new website")

        commit_and_push(
            "Initialized Angular",
            project_name,
            github_username,
            github_auth,
            directory=project_name,
        )


@action_hook("github_actions", "web_frontend", "angular")
def setup_actions():
    project_name: str = Node.get_full_response()["metadata"]["name"]
    github_username: str = Node.get_full_response()["github_credentials"]["username"]
    github_auth: str = ""
    if "password" in Node.get_full_response()["github_credentials"]:
        github_auth = Node.get_full_response()["github_credentials"]["password"]
    if "oauth_token" in Node.get_full_response()["github_credentials"]:
        github_auth = Node.get_full_response()["github_credentials"]["oauth_token"]

    # add additional library for github actions testing
    bash(f"cd {project_name}/website && npm install puppeteer --save-dev")

    # update karma.conf file
    copy_file(
        f"{__assets_directory__}/angular/karma.conf.js",
        f"{os.getcwd()}/{project_name}/website/karma.conf.js",
    )

    # update package.json
    raw_json: Dict[str, Any] = file_to_json(f"{os.getcwd()}/{project_name}/website/package.json")

    raw_json["scripts"]["clean"] = "rimraf ./dist"
    raw_json["scripts"]["build:prod"] = "ng build --prod"
    raw_json["scripts"]["test"] = "ng test --watch=false --browsers=ChromeHeadlessCustom"
    raw_json["scripts"]["build:ci"] = "npm run clean && npm run test && npm run build:prod"

    raw_to_json_file(f"{os.getcwd()}/{project_name}/website/package.json", raw_json)

    copy_file(
        f"{__assets_directory__}/angular/nodejs.yml",
        f"{os.getcwd()}/{project_name}/.github/workflows/nodejs.yml",
    )

    commit_and_push(
        "Setup Github Actions", project_name, github_username, github_auth, directory=project_name,
    )
