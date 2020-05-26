from preapp import Node, ConfirmQuestion
from typing import List, Dict, Any
import subprocess
import os
from preapp.utils import commit_and_push
import json


class GithubActionsNode(Node):
    """Checks if the user wants to use github actions"""

    def __init__(self):
        super(GithubActionsNode, self).__init__(
            "github_actions",
            [ConfirmQuestion("use", "Do you want to add github actions?", True)],
            parents=["github", "github_repository", "github_credentials", "framework",],
        )

    def post_process(self, responses):
        if responses["use"] == True:
            frameworks: List[str] = self.get_full_response()["framework"]
            if "web" in frameworks:
                project_name: str = self.get_full_response()["metadata"]["name"]
                github_username: str = self.get_full_response()["github_credentials"]["username"]
                github_password: str = self.get_full_response()["github_credentials"]["password"]

                process = subprocess.Popen(
                    f"cd {project_name} && mkdir .github && cd .github && mkdir workflows",
                    shell=True,
                    stdout=subprocess.PIPE,
                )
                stdout, _ = process.communicate()
                dirname, _ = os.path.split(os.path.abspath(__file__))

                if frameworks["web"] == "react":
                    commit_actions_file(
                        f"{dirname}/../../assets/nodejs.yml",
                        project_name,
                        github_username,
                        github_password,
                    )

                if frameworks["web"] == "angular":
                    # add additional library for github actions testing
                    process = subprocess.Popen(
                        f"cd {project_name}/website && npm install puppeteer --save-dev",
                        shell=True,
                        stdout=subprocess.PIPE,
                    )
                    stdout, _ = process.communicate()

                    # update karma.conf file
                    dirname, filename = os.path.split(os.path.abspath(__file__))
                    karma_src_file: TextIOWrapper = open(
                        f"{dirname}/../../assets/angular/karma.conf.js", "r"
                    )
                    karma_dest_file: TextIOWrapper = open(
                        f"{os.getcwd()}/{project_name}/website/karma.conf.js", "w",
                    )
                    karma_dest_file.write("".join(karma_src_file.readlines()))
                    karma_src_file.close()
                    karma_dest_file.close()

                    # update package.json
                    package_src: TextIOWrapper = open(
                        f"{os.getcwd()}/{project_name}/website/package.json", "r",
                    )
                    raw_json: Dict[str, Any] = json.load(package_src)
                    package_src.close()

                    raw_json["scripts"]["clean"] = "rimraf ./dist"
                    raw_json["scripts"]["build:prod"] = "ng build --prod"
                    raw_json["scripts"][
                        "test"
                    ] = "ng test --watch=false --browsers=ChromeHeadlessCustom"
                    raw_json["scripts"][
                        "build:ci"
                    ] = "npm run clean && npm run test && npm run build:prod"

                    package_dest: TextIOWrapper = open(
                        f"{os.getcwd()}/{project_name}/website/package.json", "w",
                    )
                    json.dump(raw_json, package_dest, indent=4)
                    package_dest.close()

                    commit_actions_file(
                        f"{dirname}/../../assets/angular/nodejs.yml",
                        project_name,
                        github_username,
                        github_password,
                    )

                if frameworks["web"] == "vue":
                    commit_actions_file(
                        f"{dirname}/../../assets/vue/nodejs.yml",
                        project_name,
                        github_username,
                        github_password,
                    )


Node.register(GithubActionsNode())


def commit_actions_file(
    actions_filepath: str, project_name: str, github_username: str, github_password: str
) -> None:
    dirname, filename = os.path.split(os.path.abspath(__file__))
    actions_src_file: TextIOWrapper = open(actions_filepath, "r")
    actions_dest_file: TextIOWrapper = open(
        f"{os.getcwd()}/{project_name}/.github/workflows/nodejs.yml", "w+",
    )
    actions_dest_file.write("".join(actions_src_file.readlines()))
    actions_src_file.close()
    actions_dest_file.close()

    commit_and_push(
        "Setup Github Actions",
        project_name,
        github_username,
        github_password,
        directory=project_name,
    )
