from typing import Any, Dict, List

from forge_template.handler.handler import BaseHandler
from forge_template.tool_info import ToolInfo


class SAReplicationHandler(BaseHandler):
    def __init__(self, config: Dict[str, Any], tool_info: ToolInfo):
        self.name = tool_info.name

        self.paths_to_upload: List[str] = []
        self.existing_paths: List[str] = []
        self.uploaded_paths: List[str] = []

        super().__init__(config=config, tool_info=tool_info)

    def create_preview(self) -> None:
        """
        1. Check if files (listed in paths_to_upload) already exists in GCP
        2. For each file: If it exist add its name to existing_paths
        """
        pass

    def print_preview(self) -> None:
        """
        1. Print the name of the files that will be uploaded (from paths_to_upload)
        2. If file also in existing_paths inform the user that the existing file will be overwritten
        """
        pass

    def rollback(self) -> None:
        """
        Iterate through the files in uploaded_paths and delete them from GCP
        """
        pass

    def delete_all_resources(self):
        """
        Iterate through the files in paths_to_upload and delete them if they exist
        """
        pass

    def setup(self) -> None:
        """
        Upload files from paths_to_upload. If the file is successfully uploaded add it to uploaded_paths
        """
        pass
