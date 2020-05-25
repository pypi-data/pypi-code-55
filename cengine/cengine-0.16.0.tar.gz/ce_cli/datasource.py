import json

import click
from tabulate import tabulate

import ce_api
from ce_api.models import DatasourceBQCreate, DatasourceImageCreate
from ce_cli import constants
from ce_cli.cli import cli, pass_info
from ce_cli.utils import check_login_status, api_client, api_call, declare, \
    format_uuid, find_closest_uuid


@cli.group()
@pass_info
def datasource(info):
    """Interaction with datasources"""
    check_login_status(info)


@datasource.group("list", invoke_without_command=True, )
@pass_info
@click.pass_context
def list_datasources(context, info):
    """List all datasources"""
    if context.invoked_subcommand is None:
        """List of all the available datasources"""
        user = info[constants.ACTIVE_USER]

        api = ce_api.DatasourcesApi(api_client(info))
        ds_list = api_call(api.get_datasources_api_v1_datasources_get)

        if constants.ACTIVE_DATASOURCE in info[user]:
            active_datasource = info[user][constants.ACTIVE_DATASOURCE]
        else:
            active_datasource = None

        declare('You have created {count} different '
                'datasource(s).\n'.format(count=len(ds_list)))

        if ds_list:
            table = []
            for ds in ds_list:
                table.append({
                    'Selection': '*' if ds.uuid == active_datasource else '',
                    'ID': format_uuid(ds.uuid),
                    'Name': ds.name,
                    'Type': ds.datasource_type.replace("datasource", "")
                })
            click.echo(tabulate(table, headers='keys', tablefmt='presto'))
            click.echo()
    else:
        pass


@list_datasources.command('bq')
@pass_info
def list_bq_datasources(info):
    """List of all the available datasources"""
    user = info[constants.ACTIVE_USER]

    api = ce_api.DatasourcesApi(api_client(info))
    ds_list = api_call(
        api.get_bigquery_datasources_api_v1_datasources_bigquery_get)

    if constants.ACTIVE_DATASOURCE in info[user]:
        active_datasource = info[user][constants.ACTIVE_DATASOURCE]
    else:
        active_datasource = None

    declare('You have created {count} different '
            'datasource(s).\n'.format(count=len(ds_list)))

    if ds_list:
        table = []
        for ds in ds_list:
            table.append({
                'Selection': '*' if ds.uuid == active_datasource else '',
                'ID': format_uuid(ds.uuid),
                'Name': ds.name,
                'Rows': ds.n_rows,
                'Cols': ds.n_columns,
                'Size (MB)': round(ds.n_bytes / (1024 * 1024)),
            })
        click.echo(tabulate(table, headers='keys', tablefmt='presto'))
        click.echo()


@list_datasources.command('images')
@pass_info
def list_image_datasources(info):
    """List of all the available datasources"""
    user = info[constants.ACTIVE_USER]
    api = ce_api.DatasourcesApi(api_client(info))
    ds_list = api_call(
        api.get_image_datasources_api_v1_datasources_images_get)

    if constants.ACTIVE_DATASOURCE in info[user]:
        active_datasource = info[user][constants.ACTIVE_DATASOURCE]
    else:
        active_datasource = None

    declare('You have created {count} different '
            'datasource(s).\n'.format(count=len(ds_list)))

    if ds_list:
        table = []
        for ds in ds_list:
            table.append({
                'Selection': '*' if ds.uuid == active_datasource else '',
                'ID': format_uuid(ds.uuid),
                'Name': ds.name,
                'Origin Path': ds.client_storage_path,
                'Samples': ds.n_samples,
            })
        click.echo(tabulate(table, headers='keys', tablefmt='presto'))
        click.echo()


@datasource.command('set')
@click.argument("datasource_id", default=None, type=str)
@pass_info
def set_datasource(info, datasource_id):
    """Set datasource to be active"""
    user = info[constants.ACTIVE_USER]

    api = ce_api.DatasourcesApi(api_client(info))
    # get DS type

    # if DS type == images:

    # if DS type == bigquery:
    all_ds = api_call(api.get_datasources_api_v1_datasources_get)
    ds_uuid = find_closest_uuid(datasource_id, all_ds)

    ds = api_call(
        api.get_datasource_api_v1_datasources_ds_id_get, ds_uuid)

    info[user][constants.ACTIVE_DATASOURCE] = ds.uuid
    info.save()
    declare('Active datasource set to id: {id}'.format(id=format_uuid(
        ds_uuid
    )))


# @datasource.command('delete')
# @click.argument("datasource_id", type=str)
# @pass_info
# def delete_datasource(info, datasource_id):
#     api = ce_api.DatasourcesApi(api_client(info))
#     api_call(
#         api.delete_bigquery_datasource_api_v1_datasources_bigquery_bq_ds_id_delete,
#         datasource_id)
#
#     users = [u for u in info.keys() if u != constants.ACTIVE_USER]
#     for user in users:
#         if constants.ACTIVE_DATASOURCE in info[user] and \
#                 info[user][constants.ACTIVE_DATASOURCE] == datasource_id:
#             info[user].pop(constants.ACTIVE_DATASOURCE)
#
#     info.save()


@datasource.group('create')
@pass_info
def create_datasource(info):
    """Create a datasource"""
    pass


@create_datasource.command('images')
@click.option("--name", required=True, help='Name of the datasource')
@click.option("--storage_path", required=True,
              help='Path to Google Storage Bucket')
@click.option("--service_account", required=True,
              help='Path to the service account')
@pass_info
@click.pass_context
def create_images_datasource(ctx, info, name, storage_path, service_account):
    """Create Image datasource and set it to be active"""
    click.echo(
        'Creating Image datasource from {}...'.format(storage_path))

    with open(service_account, 'rt', encoding='utf8') as f:
        account = json.load(f)

    api = ce_api.DatasourcesApi(api_client(info))
    ds = api_call(
        api.create_datasource_images_api_v1_datasources_images_post,
        DatasourceImageCreate(name=name,
                              client_storage_path=storage_path,
                              service_account=account))
    declare('Datasource registered.')
    ctx.invoke(set_datasource, datasource_id=ds.uuid)


@create_datasource.command('bq')
@click.option("--name", required=True, help='Name of the datasource')
@click.option("--project", required=True, help='Project of the BQ table')
@click.option("--dataset", required=True, help='Dataset of the BQ table')
@click.option("--table", required=True, help='Name of the BQ table')
@click.option("--table_type", required=True,
              help='Type of the BQ table, public or private')
@click.option("--service_account", required=False,
              help='Path to the service account')
@pass_info
@click.pass_context
def create_bq_datasource(ctx, info, name, project, dataset, table, table_type,
                         service_account):
    """Create BigQuery datasource and set it to be active"""
    click.echo(
        'Registering the BQ table {}:{}:{}...'.format(project, dataset, table))

    account = None
    if service_account is not None:
        with open(service_account, 'rt', encoding='utf8') as f:
            account = json.load(f)

    api = ce_api.DatasourcesApi(api_client(info))
    ds = api_call(
        api.create_datasource_bigquery_api_v1_datasources_bigquery_post,
        DatasourceBQCreate(name=name,
                           client_project=project,
                           client_dataset=dataset,
                           client_table=table,
                           bigquery_type=table_type,
                           service_account=account))
    declare('Datasource registered.')
    ctx.invoke(set_datasource, datasource_id=ds.uuid)


@datasource.command('peek')
@click.argument("datasource_id", default=None, type=str)
@click.option("--sample_size", default=10, help='Number of samples to peek at')
@pass_info
def peek_datasource(info, datasource_id, sample_size):
    """Randomly sample datasource and print to console."""
    api = ce_api.DatasourcesApi(api_client(info))
    all_ds = api_call(api.get_datasources_api_v1_datasources_get)
    ds_uuid = find_closest_uuid(datasource_id, all_ds)

    declare('Randomly generating {} samples from datasource {}'.format(
        sample_size,
        format_uuid(ds_uuid)
    ))

    data = api_call(
        api.get_bigquery_datasource_column_values_api_v1_datasources_bigquery_bq_ds_id_data_get,
        sample_size=sample_size,
        bq_ds_id=ds_uuid)

    click.echo(tabulate(data, headers='keys', tablefmt='presto'))
