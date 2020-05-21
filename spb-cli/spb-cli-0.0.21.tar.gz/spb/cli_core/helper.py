import os
import rich
import rich.table
import rich.console

from spb.cli_core.commands.project import Project
from spb.cli_core.commands.label_data import LabelData
from spb.cli_core.utils import get_project_config
console = rich.console.Console()

class Helper:
    project = Project()
    label_data = LabelData()

    def set_config(self):
        pass

    def init_project(self, directory_path, project_name):
        return self.project.init_project(directory_path, project_name)

    def describe_projects(self):
        self.project.describe_projects()

    def upload(self, dataset_name, log_file, is_force):
        project_config = self._get_workspace_conf()
        return self.label_data.upload_data_and_label(project_config, dataset_name, log_file, is_force)

    def download(self, log_file):
        project_config = self._get_workspace_conf()
        return self.label_data.download_data_and_label(project_config, log_file)

    def check_project(self, project_name):
        return self.project.check_project(project_name)

    def _get_workspace_conf(self):
        workspace_conf_path = '.workspace'
        if os.path.isfile(workspace_conf_path):
            try:
                f = open(f"{workspace_conf_path}", 'r')
                return get_project_config(f.readline())
            except:
                console.print(f"Error while reading workspace configuration. Try again")
                return None
        else:
            console.print(f"Workspace is not initiated. 'spb init' first.")
            return None