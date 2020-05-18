import click

from convisoappsec.flow import api
from convisoappsec.flowcli.context import pass_flow_context
from convisoappsec.flow.version_searchers import SortedByVersioningStyle
from convisoappsec.flowcli import help_option

from convisoappsec.flowcli.deploy.create.with_.tag_tracker.context import (
    pass_tag_tracker_context
)

@click.command()
@click.argument("project-code", required=True)
@click.argument('current-tag', required=False)
@click.option(
    '-i',
    '--ignore-prefix',
    required=False,
    default='v',
    show_default=True,
    help="Prefix to be ignored on parsing to versioning style.",
)
@click.option(
    '-s',
    '--style',
    required=False,
    type=click.Choice(SortedByVersioningStyle.STYLES),
    default=SortedByVersioningStyle.SEMANTIC_VERSIONING_STYLE,
    show_default=True,
    help="Versioning style type used at repository.",
)
@help_option
@pass_tag_tracker_context
@pass_flow_context
def versioning_style(
    flow_context, tag_tracker_context, ignore_prefix, style, project_code, current_tag
):
    try:
        repository_dir = tag_tracker_context.repository_dir

        searcher = SortedByVersioningStyle(
            repository_dir,
            ignore_prefix,
            style,
            current_tag,
        )

        result = searcher.find_current_and_previous_version()

        flow = flow_context.create_flow_api_client()

        flow.deploys.create(
            project_code,
            result.current_version,
            result.previous_version
        )
    except Exception as e:
        raise click.ClickException(str(e)) from e
