from .. import Node
import json
from typing import Dict, Any
from preapp.utils.fileio import file_to_json


class RootNode(Node):
    """ The root node of the preapp application, All required entry point nodes are defined here """

    def __init__(self, preset: str, credentials: str):
        super(RootNode, self).__init__(
            "root", [], children=["metadata", "github", "platform", "output"], serializable=False,
        )
        self.preset = preset
        self.credentials = credentials

    def pre_process(self):
        if self.preset != None:
            for key, value in file_to_json(self.preset).items():
                Node._full_response[key] = value

        if self.credentials != None:
            Node._full_response["github_credentials"] = file_to_json(self.credentials)
