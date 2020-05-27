import os
import click
import rich
import rich.table
import rich.console

import spb
from spb.cli_core.utils import get_project_config

console = rich.console.Console()

class Project():
    def describe_projects(self):
        projects = self._get_projects()

        table = rich.table.Table(show_header=True, header_style="bold magenta")
        table.add_column("NAME", width=20)
        table.add_column("LABELS")
        table.add_column("PROGRESS", justify="right")

        for item in projects:
            table.add_row(item.name, f"{item.label_count}", f"{item.progress}%")

        console.print(table)

    def check_project(self, project_name):
        projects = self._get_projects()
        for project in projects:
            if project.name == project_name:
                return True
        return False

    def init_project(self, directory_path, project_name):
        if os.path.isdir(directory_path):
            console.print(f"Error whilte initiating project. directory already exists. Try again")
            return
        os.mkdir(directory_path)

        projects = self._get_projects()
        project_id = None
        for project in projects:
            if project.name == project_name:
                project_id = project.id
                break
        if project_id is None:
            console.print(f"Error while loading project definition. Check project name.")
            return

        f = open(f"{directory_path}/.workspace", 'w')
        f.write(f"{project_name}\t{project_id}")
        f.close()
        console.print(f"Workspace '{directory_path}' for project '{project_name}' has been created.")

    def _get_projects(self):
        spb.client()
        command = spb.Command(type='describe_project')
        return spb.run(command=command)
