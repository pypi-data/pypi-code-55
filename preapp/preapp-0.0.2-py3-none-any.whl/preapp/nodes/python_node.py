from .. import Node, CheckboxQuestion
import subprocess
import re
from preapp.utils.miscellaneous import bash


class PythonNode(Node):
    """Validates that python is correctly installed on this machine """

    def __init__(self):
        super(PythonNode, self).__init__(
            "python_interpreter", [],
        )

    def add_tool_version_as_attribute(
        self, tool_name: str, download_link: str, regex_str: str
    ) -> None:
        stdout = bash(f"{tool_name} --version")
        for line in stdout.splitlines():
            match = re.search(regex_str, line.decode())

            if not match:
                raise EnvironmentError(
                    f"Error [{line.decode()}]{tool_name} is not installed on this device. You can install {tool_name} here {download_link}"
                )
            else:
                self.add_attribute({tool_name: match.group(0)})
                break

    def pre_process(self):
        self.add_tool_version_as_attribute(
            "python", "https://www.python.org/downloads/", r"\d+\.\d+\.\d+"
        )
        self.add_tool_version_as_attribute(
            "pip", "https://pip.pypa.io/en/stable/installing/", r"\d+\.\d+"
        )


Node.register(PythonNode())
