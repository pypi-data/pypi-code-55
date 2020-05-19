import os
import shutil
from typing import List

import forge_template.util.log_util as log_util
from forge_template.handler.handler import BaseHandler
from forge_template.paths import (
    SCRIPT_OUTPUT_FOLDER,
    SCRIPT_TEMPLATE_FOLDER,
    WORKFLOW_OUTPUT_FOLDER,
    WORKFLOW_TEMPLATE_FOLDER,
)
from forge_template.tool_info import ToolInfo

GITHUB_ACTION_HANDLER_NAME = "github_actions"


class GithubActionsHandler(BaseHandler):
    def __init__(self, tool_info: ToolInfo) -> None:
        self._tool = tool_info.name
        self._paths_to_create = [SCRIPT_OUTPUT_FOLDER, WORKFLOW_OUTPUT_FOLDER]

        self._to_from_paths = [
            (
                os.path.join(SCRIPT_OUTPUT_FOLDER, tool_info.github_actions_script_name),
                os.path.join(SCRIPT_TEMPLATE_FOLDER, tool_info.github_actions_script_name),
            ),
            (
                os.path.join(WORKFLOW_OUTPUT_FOLDER, tool_info.github_actions_template_name),
                os.path.join(WORKFLOW_TEMPLATE_FOLDER, tool_info.github_actions_template_name),
            ),
        ]

        self._created_folders: List[str] = []
        self._copied_files: List[str] = []

        super().__init__(config={}, tool_info=tool_info)

    def create_preview(self) -> None:
        pass

    def print_preview(self) -> None:
        log_util.print_resource_to_add(self._paths_to_create, "Directory")
        log_util.print_resource_to_add(
            [self._to_from_paths[0][0], self._to_from_paths[1][0]], "File",
        )

    def setup(self) -> None:
        self.__create_path()
        self.__copy_files()

    def rollback(self) -> None:
        if self._copied_files:
            log_util.print_rollback("Files")
            for file in self._copied_files:
                self.__delete_path(file)

        if self._created_folders:
            log_util.print_rollback("Folders")
            for folder in self._created_folders:
                self.__delete_path(folder)

    def delete_all_resources(self):
        for path in self._paths_to_create:
            self.__delete_path(path)

    @staticmethod
    def __delete_path(path: str) -> None:
        if os.path.exists(path):
            if os.path.isdir(path):
                os.rmdir(path)
                log_util.print_success_deleted(path, "Directory")
            else:
                os.remove(path)
                log_util.print_success_deleted(path, "File")

    def __create_path(self) -> None:
        for path in self._paths_to_create:
            if not os.path.exists(path):
                os.makedirs(path)
                self._created_folders.append(path)
                log_util.print_success_created(path, "Directory")

    def __copy_files(self) -> None:
        for (to_path, from_path) in self._to_from_paths:
            shutil.copyfile(from_path, to_path)
            self._copied_files.append(to_path)
            file_name = os.path.basename(to_path)
            folder_name = os.path.dirname(to_path)
            log_util.print_success_added(folder_name, "Directory", file_name, "File")

    @property
    def created_folders(self):
        return self._created_folders
