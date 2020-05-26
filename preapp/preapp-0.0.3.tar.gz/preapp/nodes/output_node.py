from .. import Node, ConfirmQuestion
from typing import Dict, Any
import json
import sys
from preapp.utils.fileio import raw_to_json_file


class OutputNode(Node):
    """Manages the the output of all nodes executed """

    def __init__(self):
        super(OutputNode, self).__init__(
            "output",
            [ConfirmQuestion("save", "Do you want to save these settings as a json file.", True,)],
            priority=sys.maxsize,  # should always occur last
            serializable=False,
            parents=["metadata"],
        )

    def post_process(self, responses):
        if responses["save"]:
            data: Dict[str, Any] = Node.get_full_response()

            print_data: Dict[str, Any] = dict()
            for key, value in data.items():
                if value["serializable"]:
                    del value["serializable"]
                    print_data[key] = value

            project_name: str = self.get_full_response()["metadata"]["name"]
            raw_to_json_file(f"{project_name}/preapp_config.json", print_data)


Node.register(OutputNode())
