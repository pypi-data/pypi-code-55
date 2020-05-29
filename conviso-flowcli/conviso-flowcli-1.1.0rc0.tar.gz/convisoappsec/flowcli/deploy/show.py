import click
import json

from convisoappsec.flowcli.context import pass_flow_context
from convisoappsec.flowcli import help_option


@click.command()
@help_option
@click.argument('project-code', required=True)
@click.argument('current-tag', required=True)
@pass_flow_context
def show(flow_context, project_code, current_tag):
    try:
        flow = flow_context.create_flow_api_client()
        deploy = flow.deploys.get(project_code, current_tag)
        deploy_json = json.dumps(deploy, indent=2)
        click.echo(deploy_json)
    except Exception as e:
        raise click.ClickException(str(e)) from e

