import base64
import os
from datetime import datetime, timezone
from pathlib import Path
import time
import random
import click

import yaml
from click import pass_context
from tabulate import tabulate

import ce_api
from ce_api.enums import PipelineStatusTypes
from ce_api.models import PipelineCreate, PipelineUpdate
from ce_cli import constants
from ce_cli.cli import cli
from ce_cli.utils import api_client, api_call, download_artifact
from ce_cli.utils import check_login_status, pass_info, save_config, \
    get_workers_cpus_from_env_config, notice, error, declare, confirmation, \
    Spinner, format_uuid, find_closest_uuid


@cli.group()
@pass_info
def pipeline(info):
    """Create, configure and deploy pipeline runs"""
    check_login_status(info)

    user = info[constants.ACTIVE_USER]

    # WORKSPACE AND DATASOURCE
    if constants.ACTIVE_WORKSPACE in info[user]:
        api = ce_api.WorkspacesApi(api_client(info))
        ws = api_call(api.get_workspace_api_v1_workspaces_workspace_id_get,
                      info[user][constants.ACTIVE_WORKSPACE])

        click.echo('You are working on the workspace:')
        declare('ID: {}\nName: {}\n'.format(format_uuid(ws.uuid), ws.name))
    else:
        raise click.ClickException(message=error(
            "You have not set a workspace to work on yet \n"
            "'cengine workspace list' to see the possible options \n"
            "'cengine workspace set' to select a workspace \n"))


@pipeline.group('configure', invoke_without_command=True, chain=True)
@click.option('--input_path', default=None, help='Path to an initial config '
                                                 'file for warm-starting via '
                                                 'subcommands')
@click.option('--output_path', required=True, help='Path to save the config')
@pass_info
@pass_context
def configure_pipeline(context, info, output_path, input_path):
    """Configure pipeline from scratch.

    There are two possible ways of using the `configure` subcommand. You can
    either use:

        `cengine pipeline configure --output_path path_to.yaml

    which will trigger the questionnaire or alternatively, you can use:

        `cengine pipeline configure --input_path warm_start.yaml --output_path
        path_to.yaml [SUBCOMMAND1] [SUMCOMMAND1_OPS] [SUBCOMMAND2] ....`

    For a more detailed explanation, please refer to:

        https://docs.maiot.io/docs/developer_guide/pipelines_configure
    """
    user = info[constants.ACTIVE_USER]
    if constants.ACTIVE_DATASOURCE in info[user]:
        api = ce_api.DatasourcesApi(api_client(info))
        ds = api_call(
            api.get_bigquery_datasource_api_v1_datasources_bigquery_bq_ds_id_get,
            info[user][constants.ACTIVE_DATASOURCE])
        click.echo('You are working on the datasource:')
        declare('ID: {}\nName: {}\n'.format(format_uuid(ds.uuid), ds.name))
    else:
        raise click.ClickException(message=error(
            "You have not set a datasource to work on yet \n"
            "'cengine datasource list' to see the possible options \n"
            "'cengine datasource set' to select a datasource \n"))

    # INTRODUCTION
    notice('\nIn the Core Engine, the creation of a pipeline is achieved '
           'through a configuration file. This function will help you create '
           'such a configuration file and store it locally. '
           'While you push a pipeline, you will be required to provide this '
           'file. \n\nPlease note that, before you push your pipeline, you '
           'can still manually modify it even further according to your '
           'needs.\n')


@pipeline.command('pull')
@click.argument('pipeline_id', type=click.STRING)
@click.option('--output_path',
              default=os.path.join(os.getcwd(), 'ce_config.yaml'),
              help='Path to save the config file, default: working directory')
@click.option('--no_docs', is_flag=True, default=False,
              help='Save file without additional documentation')
@pass_info
def pull_pipeline(info, pipeline_id, output_path, no_docs):
    """Copy the configuration of a registered pipeline"""
    active_user = info[constants.ACTIVE_USER]
    workspace_id = info[active_user][constants.ACTIVE_WORKSPACE]
    api = ce_api.WorkspacesApi(api_client(info))
    all_ps = api_call(
        api.get_workspaces_pipelines_api_v1_workspaces_workspace_id_pipelines_get,
        workspace_id=workspace_id)
    p_uuid = find_closest_uuid(pipeline_id, all_ps)

    declare('Pulling pipeline: {}'.format(p_uuid))

    pp = api_call(
        api.get_workspaces_pipeline_by_id_api_v1_workspaces_workspace_id_pipelines_pipeline_id_get,
        workspace_id=workspace_id,
        pipeline_id=p_uuid)

    # Short term fix for these getting into the exp_config
    c = pp.exp_config
    if 'bq_args' in c:
        c.pop('bq_args')
    if 'ai_platform_training_args' in c:
        c.pop('ai_platform_training_args')

    save_config(c, output_path, no_docs)


@pipeline.command('push')
@click.argument('config_path')
@click.argument('pipeline_name')
@click.option('--workers', required=False, type=int,
              help='Desired number of workers')
@click.option('--cpus_per_worker', required=False, type=int,
              help='Desired number of cpus per worker')
@pass_info
def push_pipeline(info,
                  config_path,
                  pipeline_name,
                  workers,
                  cpus_per_worker):
    """Register a pipeline with the selected configuration"""
    active_user = info[constants.ACTIVE_USER]
    if constants.ACTIVE_DATASOURCE in info[active_user]:
        api = ce_api.DatasourcesApi(api_client(info))
        ds = api_call(
            api.get_bigquery_datasource_api_v1_datasources_bigquery_bq_ds_id_get,
            info[active_user][constants.ACTIVE_DATASOURCE])

        click.echo('You are working on the datasource:')
        declare('ID: {}\nName: {}\n'.format(format_uuid(ds.uuid), ds.name))
    else:
        raise click.ClickException(message=error(
            "You have not set a datasource to work on yet \n"
            "'cengine datasource list' to see the possible options \n"
            "'cengine datasource set' to select a datasource \n"))

    with open(config_path, 'rt', encoding='utf8') as f:
        config = yaml.load(f)

    workspace_id = info[active_user][constants.ACTIVE_WORKSPACE]
    datasource_id = info[active_user][constants.ACTIVE_DATASOURCE]

    if cpus_per_worker is None and workers is None:
        notice("No pipeline configuration provided. Automagically configuring "
               "the best settings based on your datasource.\n")
    elif cpus_per_worker is None and workers is None:
        pass
    else:
        error("Please set either both of `cpus_per_worker` and `workers` or "
              "none of them.")

    api = ce_api.PipelinesApi(api_client(info))
    p = api_call(api.create_pipeline_api_v1_pipelines_post,
                 PipelineCreate(name=pipeline_name,
                                workers=workers,
                                cpus_per_worker=cpus_per_worker,
                                exp_config=config,
                                datasource_uuid=datasource_id,
                                workspace_uuid=workspace_id))
    declare('Pipeline {id} pushed successfully!'.format(id=format_uuid(
        p.uuid)))

    workers, cpus_per_worker = get_workers_cpus_from_env_config(p.env_config)

    declare('The pipeline has been configured to run with {} workers at {} '
            'cpus per worker. \nTo change, please run '
            '`cengine pipeline update {} --workers [NEW_NUM_WORKERS] '
            '--cpus_per_worker [NEW_NUM_CPUS]`\n'.format(
        workers,
        cpus_per_worker,
        format_uuid(p.uuid),
    ))
    declare("Use `cengine pipeline run {}` to run the pipeline!".format(
        format_uuid(p.uuid)))


@pipeline.command('run')
@click.argument('pipeline_id', type=click.STRING)
@click.option('-f', '--force', is_flag=True, default=False,
              help='Force run pipeline with no prompts')
@pass_info
def run_pipeline(info, pipeline_id, force):
    """Initiate the run of a selected pipeline"""
    active_user = info[constants.ACTIVE_USER]
    ws_id = info[active_user][constants.ACTIVE_WORKSPACE]
    ds_id = info[active_user][constants.ACTIVE_DATASOURCE]

    # resolve uuid
    w_api = ce_api.WorkspacesApi(api_client(info))
    p_api = ce_api.PipelinesApi(api_client(info))

    all_ps = api_call(
        w_api.get_workspaces_pipelines_api_v1_workspaces_workspace_id_pipelines_get,
        workspace_id=ws_id)
    p_uuid = find_closest_uuid(pipeline_id, all_ps)

    # get pipeline
    pp = api_call(
        w_api.get_workspaces_pipeline_by_id_api_v1_workspaces_workspace_id_pipelines_pipeline_id_get,
        workspace_id=ws_id,
        pipeline_id=p_uuid)

    # get datasource
    ds_api = ce_api.DatasourcesApi(api_client(info))
    ds = api_call(ds_api.get_datasource_api_v1_datasources_ds_id_get,
                  ds_id)

    # get config
    workers, cpus_per_worker = get_workers_cpus_from_env_config(
        pp.env_config)

    declare('Using datasource ID: {}\nName: {}\n'.format(format_uuid(ds.uuid),
                                                         ds.name))
    declare(
        'Setting up your pipeline {} with {} workers at {} cpus per '
        'worker.\n'.format(
            p_uuid, workers, cpus_per_worker))

    if not force:
        if workers * cpus_per_worker > 100:
            confirmation('This configuration might incur significant charges, '
                         'and you will not be able to cancel the pipeline once'
                         ' its triggered. Are you sure you want to continue?',
                         abort=True)
        else:
            confirmation('You will not be able to cancel the pipeline once '
                         'its triggered. Are you sure you want to continue?',
                         abort=True)

    notice('Provisioning the required resources. '
           'This might take a few minutes..')
    api_call(p_api.run_pipeline_api_v1_pipelines_pipeline_id_run_post,
             p_uuid)
    declare('Pipeline {id} is now running!\n'.format(id=format_uuid(
        p_uuid)))
    declare("Use 'cengine pipeline status --pipeline_id {}' to check on its "
            "status".format(format_uuid(p_uuid)))


@pipeline.command('list')
@pass_info
def list_pipelines(info):
    """List of registered pipelines"""
    notice('Fetching pipeline(s). This might take a few seconds..')
    active_user = info[constants.ACTIVE_USER]
    ws = info[active_user][constants.ACTIVE_WORKSPACE]
    api = ce_api.WorkspacesApi(api_client(info))
    pipelines = api_call(
        api.get_workspaces_pipelines_api_v1_workspaces_workspace_id_pipelines_get,
        ws)
    pipelines.sort(key=lambda x: x.id)  # sorting by IDs, not UUIDs
    statuses = {}
    for count, p in enumerate(pipelines):
        statuses[p.uuid] = {
            'name': p.name,
        }

    declare('Currently, you have {count} different pipeline(s) in '
            'workspace {ws}.\n'.format(count=len(statuses), ws=ws))

    if len(statuses) > 0:
        table = []
        for k, v in statuses.items():
            table.append({
                'ID': format_uuid(k),
                'Name': v['name'],
            })
        click.echo(tabulate(table, headers='keys', tablefmt='presto'))
        click.echo()


# TODO: [LOW] Add saved time
@pipeline.command('status')
@click.option('--pipeline_id', required=False, type=click.STRING,
              help='Pipeline ID of the selected pipeline')
@pass_info
def get_pipeline_status(info, pipeline_id):
    """Get status of started pipelines"""
    notice('Fetching pipelines. This might take a few seconds..')
    active_user = info[constants.ACTIVE_USER]
    ws = info[active_user][constants.ACTIVE_WORKSPACE]
    p_api = ce_api.PipelinesApi(api_client(info))
    api = ce_api.WorkspacesApi(api_client(info))
    billing_api = ce_api.BillingApi(api_client(info))

    if pipeline_id:
        # resolve uuid
        all_ps = api_call(
            api.get_workspaces_pipelines_api_v1_workspaces_workspace_id_pipelines_get,
            workspace_id=ws)
        p_uuid = find_closest_uuid(pipeline_id, all_ps)
        declare('Pipeline ID: {}'.format(p_uuid))

        p = api_call(
            api.get_workspaces_pipeline_by_id_api_v1_workspaces_workspace_id_pipelines_pipeline_id_get,
            workspace_id=ws,
            pipeline_id=p_uuid)
        if p.pipeline_run is None or p.pipeline_run.status == \
                PipelineStatusTypes.NotStarted.name:
            error("Please run this pipeline first!")
        pipelines = [p]
    else:
        pipelines = api_call(
            api.get_workspaces_pipelines_api_v1_workspaces_workspace_id_pipelines_get,
            workspace_id=ws)
        pipelines.sort(key=lambda x: x.id)  # sorting by ID, not UUID

    statuses = {}
    with click.progressbar(
            label='Fetching pipeline statuses',
            length=len(pipelines)) as bar:
        for count, p in enumerate(pipelines):
            # if its not started, then don't call the metrics API
            if p.pipeline_run is None or p.pipeline_run.status == \
                    PipelineStatusTypes.NotStarted.name:
                continue

            run = api_call(
                p_api.get_pipeline_run_api_v1_pipelines_pipeline_id_run_get,
                pipeline_id=p.uuid)

            if run.status != PipelineStatusTypes.Running.name:
                billing = api_call(
                    billing_api.get_pipeline_billing_api_v1_billing_pipeline_id_get,
                    p.uuid,
                )
                compute_cost = billing.compute_cost
                train_cost = billing.training_cost
                saved_cost = billing.saved_cost
            else:
                compute_cost = 0
                train_cost = 0
                saved_cost = 0
            bar.update(count)

            statuses[p.uuid] = {
                'pipeline_status': run.status,
                'name': p.name,
                'compute_cost': compute_cost,
                'training_cost': train_cost,
                'total_cost': compute_cost + train_cost,
                'saved_cost': saved_cost,
            }
            if len(run.components_status):
                total_components = len(run.components_status)
            else:
                total_components = 1  # avoid zero division error
            n_successful_components = \
                len([c for c in run.components_status if
                     c['status'] == PipelineStatusTypes.Succeeded.name])
            statuses[p.uuid]['completion'] = round(
                n_successful_components / total_components * 100)
            if run.kubeflow_end_time:
                statuses[p.uuid]['time'] = run.kubeflow_end_time - \
                                           run.run_time
            else:
                statuses[p.uuid]['time'] = datetime.now(timezone.utc) - \
                                           run.run_time
            statuses[p.uuid]['start_time'] = run.run_time
            statuses[p.uuid]['end_time'] = run.kubeflow_end_time
        bar.update(len(pipelines))

    declare('Currently, you have run {count} different '
            'pipeline(s).\n'.format(count=len(statuses)))

    if len(statuses) > 0:
        table = []
        for k, v in statuses.items():
            table.append({
                'ID': format_uuid(k),
                'Name': v['name'],
                'Pipeline Status': v['pipeline_status'],
                'Completion': str(v['completion']) + '%',
                'Compute Cost (€)': round(v['compute_cost'], 4),
                'Training Cost (€)': round(v['training_cost'], 4),
                'Total Cost (€)': round(v['total_cost'], 4),
                'Execution Time': v['time'],
            })
        click.echo(tabulate(table, headers='keys', tablefmt='presto'))
        click.echo()


@pipeline.command('statistics')
@click.argument('pipeline_id', type=click.STRING)
@pass_info
def statistics_pipeline(info, pipeline_id):
    """Serve the statistics of a pipeline run"""
    import panel as pn
    import tensorflow as tf
    from tensorflow_metadata.proto.v0 import statistics_pb2

    ws_id = info[info[constants.ACTIVE_USER]][constants.ACTIVE_WORKSPACE]

    api = ce_api.WorkspacesApi(api_client(info))
    all_ps = api_call(
        api.get_workspaces_pipelines_api_v1_workspaces_workspace_id_pipelines_get,
        workspace_id=ws_id)
    p_uuid = find_closest_uuid(pipeline_id, all_ps)

    notice('Generating statistics for the pipeline '
           'ID {}. If your browser opens up to a blank window, please refresh '
           'the page once.'.format(format_uuid(p_uuid)))

    api = ce_api.PipelinesApi(api_client(info))
    artifact = api_call(
        api.get_pipeline_artifacts_api_v1_pipelines_pipeline_id_artifacts_component_type_get,
        pipeline_id=p_uuid,
        component_type='MainStatistics')

    path = Path(click.get_app_dir(constants.APP_NAME), 'statistics',
                str(ws_id), p_uuid)

    result = {}
    for split in ['train', 'eval']:
        d_path = os.path.join(path, split)

        for a in artifact:
            if a['children'] and split in a['children'][0]['signed_url']:
                download_artifact(artifact_json=a, path=d_path)

        stats_path = os.path.join(d_path, 'stats_tfrecord')

        serialized_stats = next(tf.compat.v1.io.tf_record_iterator(stats_path))
        stats = statistics_pb2.DatasetFeatureStatisticsList()
        stats.ParseFromString(serialized_stats)

        dataset_list = statistics_pb2.DatasetFeatureStatisticsList()
        for i, d in enumerate(stats.datasets):
            if d.name == 'All Examples':
                d.name = split
                dataset_list.datasets.append(d)
        result[split] = dataset_list

    h = get_statistics_html(result['train'], result['eval'], 'train', 'eval')

    pn.serve(panels=pn.pane.HTML(h, width=1200), show=True)


def get_statistics_html(lhs_statistics,
                        rhs_statistics=None,
                        lhs_name='lhs_statistics',
                        rhs_name='rhs_statistics'):
    from tensorflow_metadata.proto.v0 import statistics_pb2

    if not isinstance(lhs_statistics,
                      statistics_pb2.DatasetFeatureStatisticsList):
        raise TypeError(
            'lhs_statistics is of type %s, should be '
            'a DatasetFeatureStatisticsList proto.' % type(
                lhs_statistics).__name__)

    if len(lhs_statistics.datasets) != 1:
        raise ValueError(
            'lhs_statistics proto contains multiple datasets. Only '
            'one dataset is currently supported.')

    if lhs_statistics.datasets[0].name:
        lhs_name = lhs_statistics.datasets[0].name

    # Add lhs stats.
    combined_statistics = statistics_pb2.DatasetFeatureStatisticsList()
    lhs_stats_copy = combined_statistics.datasets.add()
    lhs_stats_copy.MergeFrom(lhs_statistics.datasets[0])

    if rhs_statistics is not None:
        if not isinstance(rhs_statistics,
                          statistics_pb2.DatasetFeatureStatisticsList):
            raise TypeError('rhs_statistics is of type %s, should be a '
                            'DatasetFeatureStatisticsList proto.'
                            % type(rhs_statistics).__name__)
        if len(rhs_statistics.datasets) != 1:
            raise ValueError(
                'rhs_statistics proto contains multiple datasets. Only '
                'one dataset is currently supported.')

        if rhs_statistics.datasets[0].name:
            rhs_name = rhs_statistics.datasets[0].name

        # If we have same name, revert to default names.
        if lhs_name == rhs_name:
            lhs_name, rhs_name = 'lhs_statistics', 'rhs_statistics'

        # Add rhs stats.
        rhs_stats_copy = combined_statistics.datasets.add()
        rhs_stats_copy.MergeFrom(rhs_statistics.datasets[0])
        rhs_stats_copy.name = rhs_name

    # Update lhs name.
    lhs_stats_copy.name = lhs_name

    protostr = base64.b64encode(
        combined_statistics.SerializeToString()).decode('utf-8')

    html_template = """<iframe id='facets-iframe' width="100%" 
    height="500px"></iframe>
        <script>
        facets_iframe = document.getElementById('facets-iframe');
        facets_html = '<script 
        src="https://cdnjs.cloudflare.com/ajax/libs/webcomponentsjs/1.3.3
        /webcomponents-lite.js"><\/script><link rel="import" 
        href="https://raw.githubusercontent.com/PAIR-code/facets/master
        /facets-dist/facets-jupyter.html"><facets-overview 
        proto-input="protostr"></facets-overview>';
        facets_iframe.srcdoc = facets_html;
         facets_iframe.id = "";
         setTimeout(() => {
           facets_iframe.setAttribute('height', 
           facets_iframe.contentWindow.document.body.offsetHeight + 'px')
         }, 1500)
         </script>"""

    html = html_template.replace('protostr', protostr)
    return html


@pipeline.command('model')
@click.argument('pipeline_id', type=click.STRING)
@click.option('--output_path', required=True, help='Path to save the model')
@pass_info
def model_pipeline(info, pipeline_id, output_path):
    """Download the trained model to a specified location"""
    if os.path.exists(output_path) and os.path.isdir(output_path):
        if not [f for f in os.listdir(output_path) if
                not f.startswith('.')] == []:
            error("Output path must be an empty directory!")
    if os.path.exists(output_path) and not os.path.isdir(output_path):
        error("Output path must be an empty directory!")
    if not os.path.exists(output_path):
        "Creating directory {}..".format(output_path)

    ws_id = info[info[constants.ACTIVE_USER]][constants.ACTIVE_WORKSPACE]
    api = ce_api.WorkspacesApi(api_client(info))
    all_ps = api_call(
        api.get_workspaces_pipelines_api_v1_workspaces_workspace_id_pipelines_get,
        workspace_id=ws_id)
    p_uuid = find_closest_uuid(pipeline_id, all_ps)

    notice('Downloading the trained model from pipeline '
           'ID {}. This might take some time if the model '
           'resources are significantly large in size.\nYour patience is '
           'much appreciated!'.format(format_uuid(p_uuid)))

    api = ce_api.PipelinesApi(api_client(info))
    artifact = api_call(
        api.get_pipeline_artifacts_api_v1_pipelines_pipeline_id_artifacts_component_type_get,
        pipeline_id=p_uuid,
        component_type='Deployer')

    # TODO: maybe add a progress bar here for the download
    if len(artifact) == 1:
        download_artifact(artifact_json=artifact[0],
                          path=output_path)
    else:
        error('Something unexpected happened! Please contact '
              'core@maiot.io to get further information.')

    declare('Model downloaded to: {}'.format(output_path))
    # TODO: [LOW] Make the Tensorflow version more dynamic
    declare('Please note that the model is saved as a SavedModel Tensorflow '
            'artifact, trained on Tensoflow 2.1.0.')


@pipeline.command('update')
@click.argument('pipeline_id', type=click.STRING)
@click.option('--workers', required=True, type=int,
              help='Desired number of workers')
@click.option('--cpus_per_worker', required=True, type=int,
              help='Desired number of cpus per worker')
@pass_info
def update_pipeline(info,
                    pipeline_id: str,
                    workers: int,
                    cpus_per_worker: int):
    """Update a pipelines configuration"""
    ws_id = info[info[constants.ACTIVE_USER]][constants.ACTIVE_WORKSPACE]
    api = ce_api.WorkspacesApi(api_client(info))
    all_ps = api_call(
        api.get_workspaces_pipelines_api_v1_workspaces_workspace_id_pipelines_get,
        workspace_id=ws_id)
    p_uuid = find_closest_uuid(pipeline_id, all_ps)

    api = ce_api.PipelinesApi(api_client(info))
    p = api_call(api.update_pipeline_api_v1_pipelines_pipeline_id_put,
                 PipelineUpdate(workers=workers,
                                cpus_per_worker=cpus_per_worker),
                 pipeline_id=p_uuid)
    declare('Pipeline {id} updated successfully!'.format(id=format_uuid(
        p.uuid)))
    workers, cpus_per_worker = get_workers_cpus_from_env_config(p.env_config)
    declare('The pipeline has been configured to run with {} workers at {} '
            'cpus per worker. \nTo change, please run '
            '`cengine pipeline update {} --workers [NEW_NUM_WORKERS] '
            '--cpus_per_worker [NEW_NUM_CPUS]`'.format(
        workers,
        cpus_per_worker,
        format_uuid(p.uuid),
    ))
    declare("Use `cengine pipeline run {}` to run the pipeline!".format(
        format_uuid(p.uuid)))


# @click.argument('pipeline_id', type=click.STRING, required=True)
# @pipeline.command('logs')
# @pass_info
# def logs(info, pipeline_id):
#     """Update a pipelines configuration"""
#     active_user = info[constants.ACTIVE_USER]
#     ws = info[active_user][constants.ACTIVE_WORKSPACE]
#     p_api = ce_api.PipelinesApi(api_client(info))
#     api = ce_api.WorkspacesApi(api_client(info))
#
#     # resolve uuid
#     all_ps = api_call(
#         api.get_workspaces_pipelines_api_v1_workspaces_workspace_id_pipelines_get,
#         workspace_id=ws)
#     p_uuid = find_closest_uuid(pipeline_id, all_ps)
#
#     run = api_call(
#         p_api.get_pipeline_run_api_v1_pipelines_pipeline_id_run_get,
#         pipeline_id=p_uuid)
#
#     old_logs = api_call(
#         p_api.get_pipeline_logs_api_v1_pipelines_pipeline_id_logs_get,
#         pipeline_id=p_uuid)
#     click.echo('\n' + old_logs + '\n')

    # spin = Spinner()
    # spin.start()
    # while run.status != PipelineStatusTypes.Succeeded.name and run.status != \
    #         PipelineStatusTypes.Failed.name:
    #     try:
    #         time.sleep(5)
    #         run = api_call(
    #             p_api.get_pipeline_run_api_v1_pipelines_pipeline_id_run_get,
    #             pipeline_id=p_uuid)
    #         new_logs = api_call(
    #             p_api.get_pipeline_logs_api_v1_pipelines_pipeline_id_logs_get,
    #             pipeline_id=p_uuid)
    #
    #         # just echo the diff
    #         echod = new_logs.replace(old_logs, '')
    #         if echod != '':
    #             click.echo('\n' + echod + '\n')
    #         # now new logs are old logs
    #         old_logs = new_logs
    #     except KeyboardInterrupt:
    #         break

    # spin.stop()

    # while run.status == PipelineStatusTypes.Running.name:
    #
    #     spin.start()
    #     time.sleep(random.randint(2, 5))
    #     spin.stop()
