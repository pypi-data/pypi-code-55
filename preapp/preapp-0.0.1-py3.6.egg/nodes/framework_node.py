import subprocess
from .. import Node, ListQuestion
from ..utils import commit_and_push, __assets_directory__


class FrameworkNode(Node):
    """Selects a Framework for the project """

    def __init__(self):
        super(FrameworkNode, self).__init__(
            "framework", [], parents=["nodejs", "platform", "github", "github_clone"],
        )

    def pre_process(self):
        if "web" in self.get_full_response()["platform"]["software"]:
            self.add_question(
                ListQuestion("web", "Select a web framework", ["react", "angular", "vue"])
            )

    def post_process(self, responses):
        if "web" in responses and responses["web"] == "react":
            project_name: str = self.get_full_response()["metadata"]["name"]
            if not self.get_full_response()["github"]["use"]:
                process = subprocess.Popen(
                    "npx create-react-app " + project_name, shell=True, stdout=subprocess.PIPE,
                )
                stdout, _ = process.communicate()
            else:
                github_username: str = self.get_full_response()["github_credentials"]["username"]
                github_password: str = self.get_full_response()["github_credentials"]["password"]
                # repo_download_url: str = f"https://github.com/{github_username}/{project_name}.git"
                # process = subprocess.Popen(
                #     f"git clone {repo_download_url} && cd {project_name} && npx create-react-app website",  # && git add . && git commit -m "Initialized React" && git push https://{github_username}:{github_password}@github.com/{github_username}/{project_name}.git',
                #     shell=True,
                #     stdout=subprocess.PIPE,
                # )
                # stdout, _ = process.communicate()

                process = subprocess.Popen(
                    f"cd {project_name} && npx create-react-app website",
                    shell=True,
                    stdout=subprocess.PIPE,
                )
                stdout, _ = process.communicate()

                commit_and_push(
                    "Initialized React",
                    project_name,
                    github_username,
                    github_password,
                    directory=project_name,
                )

        if "web" in responses and responses["web"] == "angular":
            project_name: str = self.get_full_response()["metadata"]["name"]
            # assert that angular is installed
            process = subprocess.Popen(
                "npm install -g @angular/cli", shell=True, stdout=subprocess.PIPE
            )
            stdout, _ = process.communicate()

            if not self.get_full_response()["github"]["use"]:
                process = subprocess.Popen(
                    "ng new " + project_name, shell=True, stdout=subprocess.PIPE,
                )
                stdout, _ = process.communicate()
            else:
                github_username: str = self.get_full_response()["github_credentials"]["username"]
                github_password: str = self.get_full_response()["github_credentials"]["password"]

                process = subprocess.Popen(
                    f"cd {project_name} && ng new website", shell=True, stdout=subprocess.PIPE,
                )
                stdout, _ = process.communicate()

                commit_and_push(
                    "Initialized Angular",
                    project_name,
                    github_username,
                    github_password,
                    directory=project_name,
                )

        if "web" in responses and responses["web"] == "vue":
            project_name: str = self.get_full_response()["metadata"]["name"]
            # assert that vue is installed
            process = subprocess.Popen("npm install -g vue", shell=True, stdout=subprocess.PIPE)
            stdout, _ = process.communicate()

            # assert the vue cli is installed
            process = subprocess.Popen(
                "npm install -g @vue/cli", shell=True, stdout=subprocess.PIPE
            )
            stdout, _ = process.communicate()

            if not self.get_full_response()["github"]["use"]:
                process = subprocess.Popen(
                    "vue create -d " + project_name, shell=True, stdout=subprocess.PIPE,
                )
                stdout, _ = process.communicate()
            else:
                github_username: str = self.get_full_response()["github_credentials"]["username"]
                github_password: str = self.get_full_response()["github_credentials"]["password"]

                process = subprocess.Popen(
                    f"cd {project_name} && vue create -d website",
                    shell=True,
                    stdout=subprocess.PIPE,
                )
                stdout, _ = process.communicate()

                commit_and_push(
                    "Initialized Vue",
                    project_name,
                    github_username,
                    github_password,
                    directory=project_name,
                )


Node.register(FrameworkNode())
