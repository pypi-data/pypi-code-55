from .. import Node
from .. import CheckboxQuestion
import sys
from typing import Dict, Any
import json
from preapp.question import ListQuestion
import subprocess


class PlatformNode(Node):
    """ Selects a target platform(s) """

    def __init__(self):
        super(PlatformNode, self).__init__(
            "platform",
            [
                CheckboxQuestion(
                    "software",
                    "Select the software platforms to target",
                    ["mobile", "desktop", "web", "wearable"],
                ),
                CheckboxQuestion(
                    "hardware",
                    "Select the hardware platforms to target",
                    ["IOS", "Android", "Mac", "Linux", "Windows"],
                ),
            ],
        )

    def pre_process(self):
        self.add_child("framework")


Node.register(PlatformNode())
