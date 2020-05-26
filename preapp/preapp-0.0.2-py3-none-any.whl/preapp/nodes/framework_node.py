import subprocess
from .. import Node, ListQuestion
from ..utils import commit_and_push, __assets_directory__
from preapp.utils.miscellaneous import bash
from preapp.utils.fileio import copy_file, file_to_text, text_to_file
import os
from preapp.hooks import call_hook


class FrameworkNode(Node):
    """Selects a Framework for the project """

    def __init__(self):
        super(FrameworkNode, self).__init__(
            "framework",
            [],
            parents=[
                "nodejs",
                "python_interpreter",
                "platform",
                "github",
                "github_clone",
                "features",
            ],
        )

    def pre_process(self):
        if "web" in self.get_full_response()["platform"]["software"]:
            self.add_question(
                ListQuestion(
                    "web_frontend", "Select a frontend web framework", ["react", "angular", "vue"],
                ),
            )
            self.add_question(
                ListQuestion("web_backend", "Select a backend web framework", ["python"])
            )

    def post_process(self, responses):
        if "web_frontend" in responses:
            call_hook("framework", "web_frontend", responses["web_frontend"])

        if "web_backend" in responses:
            call_hook("framework", "web_backend", responses["web_backend"])


Node.register(FrameworkNode())
