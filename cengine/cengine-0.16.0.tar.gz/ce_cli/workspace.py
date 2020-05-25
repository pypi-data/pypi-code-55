import click
from tabulate import tabulate

import ce_api
from ce_api.models import WorkspaceCreate
from ce_cli import constants
from ce_cli.cli import cli, pass_info
from ce_cli.utils import check_login_status, api_client, api_call, declare, \
    format_uuid, find_closest_uuid


@cli.group()
@pass_info
def workspace(info):
    """Interaction with workspaces"""
    check_login_status(info)


@workspace.command('list')
@pass_info
def list_workspaces(info):
    """List of all workspaces available to the user"""
    user = info[constants.ACTIVE_USER]

    api = ce_api.WorkspacesApi(api_client(info))
    ws_list = api_call(api.get_loggedin_workspaces_api_v1_workspaces_get)

    if constants.ACTIVE_WORKSPACE in info[user]:
        active_w = info[user][constants.ACTIVE_WORKSPACE]
    else:
        active_w = None

    declare('You have created {count} different '
            'workspace(s). \n'.format(count=len(ws_list)))

    if ws_list:
        table = []
        for w in ws_list:
            table.append({'Selection': '*' if w.uuid == active_w else '',
                          'ID': format_uuid(w.uuid),
                          'Name': w.name})
        click.echo(tabulate(table, headers='keys', tablefmt='presto'))
        click.echo()


@workspace.command('set')
@click.argument("workspace_id", default=None, type=str)
@pass_info
def set_workspace(info, workspace_id):
    """Set workspace to be active"""
    user = info[constants.ACTIVE_USER]

    api = ce_api.WorkspacesApi(api_client(info))
    all_ws = api_call(api.get_loggedin_workspaces_api_v1_workspaces_get)
    ws_uuid = find_closest_uuid(workspace_id, all_ws)

    api_call(api.get_workspace_api_v1_workspaces_workspace_id_get,
             ws_uuid)

    info[user][constants.ACTIVE_WORKSPACE] = ws_uuid
    info.save()
    declare('Active workspace set to id: {id}'.format(id=format_uuid(
        ws_uuid)))


# @workspace.command('delete')
# @click.argument("workspace_id", type=int)
# @pass_info
# def delete_workspace(info, workspace_id):
#     api = ce_api.WorkspacesApi(api_client(info))
#     api_call(api.delete_workspace_api_v1_workspaces_workspace_id_delete,
#              workspace_id)
#
#     users = [u for u in info.keys() if u != constants.ACTIVE_USER]
#     for user in users:
#         if constants.ACTIVE_WORKSPACE in info[user] and \
#                 info[user][constants.ACTIVE_WORKSPACE] == workspace_id:
#             info[user].pop(constants.ACTIVE_WORKSPACE)
#
#     info.save()


@workspace.command('create')
@click.argument("name", type=str)
@pass_info
@click.pass_context
def create_workspace(ctx, info, name):
    """Create a workspace and set it to be active."""
    click.echo('Registering the workspace "{}"...'.format(name))

    api = ce_api.WorkspacesApi(api_client(info))
    ws = api_call(api.create_workspace_api_v1_workspaces_post,
                  WorkspaceCreate(name=name))
    declare('Workspace registered.')
    ctx.invoke(set_workspace, workspace_id=ws.uuid)
