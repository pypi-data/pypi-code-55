"""
This module represents the the Jira Instance class
"""
import json

import click
import keyring
from jira import JIRA

from moic.cli import MoicInstance, console, global_settings, settings
from moic.plugins.jira.api import get_project_story_status

# Define plugin custom commands
custom_commands = ["sprint.sprint"]


# Defin plugin Instance
class Instance(MoicInstance):
    """
    Instance class which allow you to access Jira's API using basic auth credentials
    It allows to setup several configuration such as:
    - Default project, custom fields, sprint workflow etc...
    """

    instance = None
    custom_config_label = "Would you like to configure Jira Agile"

    @property
    def session(self) -> JIRA:
        """
        Session object which represents a JIRA API session

        Returns:
            JIRA: A Jira API session
        """
        if not Instance.instance:
            self.create_session_instance()
        return Instance.instance

    def create_session_instance(self) -> None:
        """
        Setup the instance if it doesn't exist yet

        Returns:
            None
        """
        try:
            Instance.instance = JIRA(
                settings.get("instance"),
                basic_auth=(settings.get("login"), settings.get("password"),),
                options={"agile_rest_path": "agile", "rest_api_version": "latest", "agile_rest_api_version": "latest"},
            )
        except Exception as e:
            console.print(f"[red]Something goes wrong {e.status_code}[/red]")
            exit(1)

    def add_context(self, name: str, force: bool = False) -> dict:
        """
        Setup the main configuration and saved it:
        Instance, credentials and default project

        Args:
            force (bool): Force configuration to be setup even if it exists

        Returns:
            None
        """
        instance = click.prompt("Your Jira Instance").lower()

        if instance.endswith("/"):
            instance = instance[:-1]

        login = click.prompt("login")
        password = click.prompt("password", hide_input=True)
        default_project = click.prompt("Default project id")
        console.print("")
        persist = click.confirm("Would you like to persist the credentials to the local keyring?")
        if persist:
            keyring.set_password(f"moic-{name}", login, password)

        try:
            Instance.instance = JIRA(
                instance,
                basic_auth=(login, password),
                options={"agile_rest_path": "agile", "rest_api_version": "latest", "agile_rest_api_version": "latest"},
            )
        except Exception:
            console.print(f"[red]Something goes wrong with your Jira configuration[/red]")
            exit(1)

        conf = {
            "instance": instance,
            "login": login,
            "default_project": default_project,
        }
        return conf

    def custom_config(self, project: str, force: bool = False) -> None:
        """
        Configure the agile settings
        It configured several custom fields:
        * Story point custom field
        * Peer custom field

        Args:
            project (str): Jira Project key which should be configured
            force (bool): Force configuration to be setup even if it exists

        Returns:
            None
        """
        if not settings.get("custom_fields.peer") or force:
            console.print("\n[yellow]Agile configuration: custom fields for peer is not set[/yellow]")
            fields = self.session.fields()
            candidates = [field for field in fields if "Peer" in field["name"]]
            if candidates:
                for candidate in candidates:
                    console.print(f" - [blue]{candidate['id'].ljust(20)}[/blue]: [grey70]{candidate['name']}[/grey70]")
            else:
                for field in fields:
                    console.print(f" - [blue]{field['id'].ljust(20)}[/blue]: [grey70]{field['name']}[/grey70]")
            choice = click.prompt("\nWhich custom fields correspond to the Peer value? (id)")
            if not [field for field in fields if field["id"] == choice]:
                console.print("[red]Wrong value provided, you must specify a field ID[/red]")
                exit()
            self.update_config(
                {
                    "default": {
                        "contexts": [
                            {"name": global_settings.get("current_context"), "custom_fields": {"peer": choice}}
                        ]
                    }
                }
            )

        if not settings.get("custom_fields.story_points") or force:
            console.print("\n[yellow]Agile configuration: custom fields for story points is not set[/yellow]")
            fields = self.session.fields()
            candidates = [field for field in fields if "Story Points" in field["name"]]
            if candidates:
                for candidate in candidates:
                    console.print(f" - [blue]{candidate['id'].ljust(20)}[/blue]: [grey70]{candidate['name']}[/grey70]")
            else:
                for field in fields:
                    console.print(f" - [blue]{field['id'].ljust(20)}[/blue]: [grey70]{field['name']}[/grey70]")
            choice = click.prompt("\nWhich custom fields correspond to the Story Point value? (id)")
            if not [field for field in fields if field["id"] == choice]:
                console.print("[red]Wrong value provided, you must specify a field ID[/red]")
                exit()
            self.update_config(
                {
                    "default": {
                        "contexts": [
                            {"name": global_settings.get("current_context"), "custom_fields": {"story_points": choice}}
                        ]
                    }
                }
            )

        if not settings.get(f"projects.{project}.workflow") or force:
            console.print("\n[yellow]Agile configuration:  workflow is not set[/yellow]")
            # Get Status for the project
            statuses = get_project_story_status(
                project, url=settings.get("instance"), login=settings.get("login"), password=settings.get("password"),
            )
            suggest = """# You can configure the sprint command output
# Choosing the order of the issue status inside the main classes : new, inderminate, done
#
# Provide the orderd configuration you want such as this example:
#
#
# {'new': ['1', '4'], 'indeterminate': ['3', '5,6', '9'], 'done': ['8', '7']}
#
# note : use ',' to group status
#
"""
            default = {}
            for sc in ["new", "indeterminate", "done"]:
                default_status = []
                suggest = suggest + f"# {sc}\n"
                for status in statuses:
                    if status["statusCategory"]["key"] == sc:
                        suggest = suggest + f"#  - ({status['id']}) {status['name']}\n"
                        default_status.append(status["id"])
                default[sc] = default_status
            suggest = suggest + "\n" + str(default)
            response = click.edit(suggest, require_save=False)
            workflow = [line for line in response.split("\n") if not line.startswith("#") and line != ""]
            if workflow:
                workflow_config = json.loads(workflow[0].replace("'", '"'))
                self.update_config(
                    {
                        "default": {
                            "contexts": [
                                {
                                    "name": global_settings.get("current_context"),
                                    "projects": {project: {"workflow": workflow_config}},
                                }
                            ]
                        }
                    }
                )
                console.print(workflow_config)

        console.line()
        console.print("[green]Agile workflow saved![/green]")
