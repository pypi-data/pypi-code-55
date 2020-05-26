from .. import Node, CheckboxQuestion
import subprocess
import re
from preapp.utils.miscellaneous import bash


class NodeJSNode(Node):
    """Validates that nodejs is correctly installed on this machine """

    def __init__(self):
        super(NodeJSNode, self).__init__(
            "nodejs", [],
        )

    def add_tool_version_as_attribute(self, tool_name: str) -> None:
        stdout = bash(f"{tool_name} -v")
        for line in stdout.splitlines():
            match = re.search(r"\d+\.\d+\.\d+", line.decode())

            if not match:
                print(
                    "Error "
                    + tool_name
                    + " is not installed on this device. You can install node here https://nodejs.org/en/download/"
                )
                exit(0)
            else:
                self.add_attribute({tool_name: match.group(0)})

    def pre_process(self):
        self.add_tool_version_as_attribute("node")
        self.add_tool_version_as_attribute("npm")


Node.register(NodeJSNode())
