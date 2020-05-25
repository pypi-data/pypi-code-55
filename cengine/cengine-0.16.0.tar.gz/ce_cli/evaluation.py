import json
import os
import subprocess
from textwrap import dedent

import click
import nbformat as nbf
import pandas as pd
from pathlib import Path

import ce_api
from ce_cli import constants
from ce_cli.cli import pass_info
from ce_cli.pipeline import pipeline
from ce_cli.utils import api_call, api_client, download_artifact, notice, \
    declare, format_uuid, find_closest_uuid


# TODO: remove hacks from the notebook code

@pipeline.command('evaluate')
@click.argument('pipeline_id', type=click.STRING)
@pass_info
def evaluate(info, pipeline_id):
    """Tool for the in-depth evaluation of a pipeline run"""
    active_user = info[constants.ACTIVE_USER]
    ws = info[active_user][constants.ACTIVE_WORKSPACE]
    api = ce_api.WorkspacesApi(api_client(info))

    # resolve uuid
    all_ps = api_call(
        api.get_workspaces_pipelines_api_v1_workspaces_workspace_id_pipelines_get,
        workspace_id=ws)
    p_uuid = find_closest_uuid(pipeline_id, all_ps)

    notice('Downloading evaluation metrics and tensorboard logs for '
           'pipeline ID {}. This might take some time if the model '
           'resources are significantly large in size.\nYour patience is '
           'much appreciated!'.format(format_uuid(p_uuid)))

    log_dir = get_log_dir(p_uuid, info)
    eval_dir = get_eval_dir(p_uuid, info)

    # generate notebook
    nb = nbf.v4.new_notebook()
    nb['cells'] = [
        nbf.v4.new_code_cell(eval_import_block()),
        nbf.v4.new_code_cell(get_model_block(log_dir)),
        nbf.v4.new_code_cell(get_eval_block(eval_dir)),
    ]

    # write notebook
    final_out_path = (
            Path(click.get_app_dir(constants.APP_NAME)) /
            constants.EVALUATION_NOTEBOOK
    )

    s = nbf.writes(nb)
    if isinstance(s, bytes):
        s = s.decode('utf8')

    # only import tfx when needed
    with open(final_out_path, 'w') as f:
        f.write(s)

    os.system('jupyter notebook "{}"'.format(final_out_path))


# @click.argument('pipeline_id_list', type=click.INT, nargs=-1)
@pipeline.command('compare')
@pass_info
def compare(info):
    """Tool to compare pipeline runs based on defined metrics"""
    notice('Downloading evaluation metrics and tensorboard logs for all run '
           'pipelines in the workspace. This might take some time if there  '
           'are many pipelines.\nYour patience is '
           'much appreciated!')

    temp_info = {
        constants.ACTIVE_USER: info[constants.ACTIVE_USER],
        info[constants.ACTIVE_USER]: info[info[constants.ACTIVE_USER]]
    }

    # generate notebook
    nb = nbf.v4.new_notebook()
    nb['cells'] = [
        nbf.v4.new_code_cell(import_block()),
        nbf.v4.new_code_cell(info_block(temp_info)),
        nbf.v4.new_code_cell(application_block()),
        nbf.v4.new_code_cell(interface_block()),
    ]

    # write notebook
    final_out_path = os.path.join(click.get_app_dir(constants.APP_NAME),
                                  constants.COMPARISON_NOTEBOOK)
    s = nbf.writes(nb)
    if isinstance(s, bytes):
        s = s.decode('utf8')

    with open(final_out_path, 'w') as f:
        f.write(s)

    # serve notebook
    os.system('panel serve "{}" --show'.format(final_out_path))


# IMPORT FUNCTIONS
def parse_metrics(d):
    tmp = d.copy()
    m = tmp.pop('metrics')
    for k, v in m.items():
        tmp['metric_' + k] = v['doubleValue']
    return tmp


def api_get_all_context_info(info):
    user = info[constants.ACTIVE_USER]

    api = ce_api.WorkspacesApi(api_client(info))
    context_dict = api_call(
        api.get_eval_contexts_api_v1_workspaces_workspace_id_contexts_get,
        info[user][constants.ACTIVE_WORKSPACE]
    )
    df = pd.DataFrame(context_dict)

    return df


def api_get_all_artifacts(info):
    user = info[constants.ACTIVE_USER]
    api = ce_api.WorkspacesApi(api_client(info))
    artifacts = api_call(
        api.get_eval_artifacts_api_v1_workspaces_workspace_id_artifacts_get,
        info[user][constants.ACTIVE_WORKSPACE]
    )

    artifact_df = pd.DataFrame(api_call(
        api.get_eval_contexts_api_v1_workspaces_workspace_id_contexts_get,
        info[user][constants.ACTIVE_WORKSPACE]
    ))

    ws_id = info[info[constants.ACTIVE_USER]][constants.ACTIVE_WORKSPACE]
    local_dict = {}
    for context_id, component_dict in artifacts.items():
        if 'Evaluator.Evaluator' in component_dict:
            pipeline_id = artifact_df.loc[
                artifact_df['context_id'] == int(
                    context_id), 'pipeline_id'].values[0]
            d_path = os.path.join(click.get_app_dir(constants.APP_NAME),
                                  'compare_workspace',
                                  str(ws_id), str(pipeline_id))

            get_eval_dir(pipeline_id, info, d_path=d_path)
            local_dict[context_id] = {'Evaluator': d_path + '/'}

    return local_dict


def api_get_list_of_executions(c, info):
    user = info[constants.ACTIVE_USER]

    api = ce_api.WorkspacesApi(api_client(info))
    executions = api_call(
        api.get_eval_executions_api_v1_workspaces_workspace_id_context_id_executions_get_with_http_info,
        info[user][constants.ACTIVE_WORKSPACE],
        c
    )
    return executions


def get_log_dir(c, info):
    ws_id = info[info[constants.ACTIVE_USER]][constants.ACTIVE_WORKSPACE]

    api = ce_api.PipelinesApi(api_client(info))
    artifact = api_call(
        api.get_pipeline_artifacts_api_v1_pipelines_pipeline_id_artifacts_component_type_get,
        pipeline_id=c,
        component_type='Trainer')
    d_path = os.path.join(click.get_app_dir(constants.APP_NAME),
                          'eval_trainer', str(ws_id), str(c))

    download_artifact(artifact[0], path=d_path)

    return d_path


def get_eval_dir(c, info, d_path=None):
    ws_id = info[info[constants.ACTIVE_USER]][constants.ACTIVE_WORKSPACE]

    api = ce_api.PipelinesApi(api_client(info))
    artifact = api_call(
        api.get_pipeline_artifacts_api_v1_pipelines_pipeline_id_artifacts_component_type_get,
        pipeline_id=c,
        component_type='Evaluator')

    if d_path is None:
        d_path = os.path.join(click.get_app_dir(constants.APP_NAME),
                              'eval_evaluator', str(ws_id), str(c))
    # TODO: [LOW] artifact[1] hard-coded because of upgrade to 0.21.4
    download_artifact(artifact[1], path=d_path)

    # replace google path with local path
    with open(os.path.join(d_path, 'eval_config.json'), 'r') as f:
        eval_config = json.load(f)

    # now override the google path to local path
    eval_config['modelLocations'][''] = d_path

    with open(os.path.join(d_path, 'eval_config.json'), 'w') as f:
        json.dump(eval_config, f)

    return d_path


# THE REAL STUFF
def import_block():
    block = '''\
        import time
        import param
        import panel as pn
        import pandas as pd
        import plotly.express as px
        import tensorflow_model_analysis as tfma
        import random
        from absl import logging
        from typing import Optional, List, Text

        from tensorflow_model_analysis.view import util as tfma_util

        from ce_cli.evaluation import api_get_all_context_info
        from ce_cli.evaluation import api_get_all_artifacts
        from ce_cli.evaluation import api_get_list_of_executions
        from ce_cli.evaluation import parse_metrics

        pn.extension('plotly')
    '''
    return dedent(block)[:-1]


def info_block(info):
    block = '''\
        info = {}
    '''.format(info)
    return dedent(block)[:-1]


def application_block():
    block = '''\
        class Application(param.Parameterized):

            context_df = param.DataFrame() # 1

            pipeline_run_selector = param.ListSelector(default=[], objects=[
            ]) # 2
            hyperparameter_selector = param.ListSelector(default=[], 
            objects=[]) # 3 

            slicing_metric_selector = param.ObjectSelector(default='', 
            objects=['']) # 4 
            performance_metric_selector = param.ObjectSelector(objects=[]) # 5 


            def __init__(self, **params):
                super(Application, self).__init__(**params)

                context_info = api_get_all_context_info(info)

                result_list = []
                artifacts = api_get_all_artifacts(info)
                for context_id, component_dict in artifacts.items():
                    eval_path = component_dict['Evaluator']
                    evaluation = tfma.load_eval_result(eval_path)
                    for s, m in evaluation.slicing_metrics:
                        result_list.append(dict([('context_id', 
                        int(context_id)), 
                                                 ('slice_name', s[0][0] if s 
                                                 else ''), 
                                                 ('slice_value', s[0][1] if 
                                                 s else ''), 
                                                 ('metrics', m[''][''])]))
                result_info = pd.DataFrame([parse_metrics(r) for r in 
                result_list])

                self.results = pd.merge(result_info, context_info, 
                on='context_id', how='inner')
                self.param.pipeline_run_selector.objects = self.results[
                'pipeline_name'].unique()

                c_df = context_info[context_info['context_id'].isin(
                result_info['context_id'].unique())]
                c_df = c_df.drop(['run_id', 'context_id', 'context_name'], 
                axis=1)
                c_df = c_df.reindex(['pipeline_id', 'pipeline_name'], axis=1)
                self.param.context_df.default = c_df
                self.context_df = c_df


            def extract_param_list(self, context_list):
                param_set = set()
                for c in context_list:
                    for e in api_get_list_of_executions(int(c), info)[0]:
                        component_id = e['properties']['component_id'][
                        'stringValue']
                        for p in e['properties']:
                            if e['properties'][p]['stringValue'].isnumeric():
                                param_set.add(component_id+":"+ p)
                            else:
                                param_set.discard(component_id+":"+ p)
                return list(param_set)


            def generate_results_with_additional_params(self, df, 
            track_list, pipeline_run_selector):
                print('Generating results...')
                tracking_dict = dict()
                for key in track_list:
                    component, parameter = key.split(':')
                    if component in tracking_dict:
                        tracking_dict[component].append(parameter)
                    else:
                        tracking_dict[component] = [parameter]

                context_list = list(self.results[self.results[
                'pipeline_name'].isin(pipeline_run_selector)][
                'context_id'].unique())
                for c in context_list:
                    for e in api_get_list_of_executions(int(c), info)[0]:
                        component_id = e['properties']['component_id'][
                        'stringValue']
                        if component_id in tracking_dict:
                            parameter_list = tracking_dict[component_id]
                            for p in parameter_list:
                                param_name = ':'.join([component_id, p])
                                param_value = e['properties'][p]['stringValue']
                                df.loc[df['context_id'] == c, param_name] = 
                                float(param_value)

                return df


            @param.depends('pipeline_run_selector', watch=True)
            def _updated_context(self):
                print('Context list updated!')
                df = self.results[self.results['pipeline_name'].isin(
                self.pipeline_run_selector)]
                df = df.dropna(axis=1, how='all')

                slicing_metric_list = sorted(list(df['slice_name'].unique()))

                performance_metric_set = {c for c in df.columns if 
                c.startswith('metric_')}
                performance_metric_list = [None] + sorted(list(
                performance_metric_set))

                context_list = list(self.results[self.results[
                'pipeline_name'].isin(self.pipeline_run_selector)][
                'context_id'].unique())
                parameter_list = self.extract_param_list(context_list)

                self.param['slicing_metric_selector'].objects = 
                slicing_metric_list
                self.param['performance_metric_selector'].objects = 
                performance_metric_list
                self.param['hyperparameter_selector'].objects = parameter_list

                self.slicing_metric_selector = ''
                self.performance_metric_selector = None


            @param.depends('slicing_metric_selector', 
            'performance_metric_selector', watch=True)
            def performance_graph(self): 
                print('One of the metrics updated!') 
                if self.performance_metric_selector:
                    df = self.results[(self.results['pipeline_name'].isin(
                    self.pipeline_run_selector)) & 
                                      (self.results['slice_name'] == 
                                      self.slicing_metric_selector)]
                    fig = px.scatter(df,
                                     x='pipeline_name',
                                     y=self.performance_metric_selector,
                                     color='slice_value',
                                     width=1100,
                                     title='Pipeline Comparison')

                    fig = fig.update_traces(mode='lines+markers')

                else:
                    fig = px.scatter(pd.DataFrame(),
                                     marginal_y='rug',
                                     width=1100,
                                     title='Pipeline Comparison')

                return fig


            @param.depends('performance_metric_selector', 
            'hyperparameter_selector', watch=True)
            def parameter_graph(self): 
                if self.performance_metric_selector and len(
                self.hyperparameter_selector) > 0:
                    df = self.results[(self.results['pipeline_name'].isin(
                    self.pipeline_run_selector)) & 
                                      (self.results['slice_name'] == '')]

                    extra_df = self.generate_results_with_additional_params(
                    df, 
                                                                           self.hyperparameter_selector, 
                                                                           self.pipeline_run_selector)

                    dimensions = ['pipeline_name'] + 
                    self.hyperparameter_selector + [
                    self.performance_metric_selector]

                    fig = px.parallel_coordinates(extra_df, 
                                                  color=self.performance_metric_selector, 
                                                  dimensions=dimensions, 
                                                  color_continuous_scale=[
                                                  'red', 'blue', 'green'],
                                                  width=1100,
                                                  title='Hyperparameter 
                                                  Comparison')
                else:
                    fig = px.scatter(pd.DataFrame(),
                                     marginal_y='rug',
                                     width=1100,
                                     title='Hyperparameter Comparison')

                return fig
    '''
    return dedent(block)[:-1]


def interface_block():
    block = '''\
        def generate_interface():

            app = Application()
            handlers = pn.Param(app.param)

            # Summary Page
            summary_page = pn.GridSpec(height = 850, width=1850, max_height 
            = 850, max_width=1850)
            summary_page[0:1, 0:1] = handlers[1]

            # Analysis Page
            analysis_page = pn.GridSpec(height = 850, width=1850, max_height 
            = 850, max_width=1850)
            analysis_page[0:8, 0:2] = handlers[2]
            analysis_page[0:10, 8:10] = handlers[3]
            analysis_page[8:9, 0:2] = handlers[4]
            analysis_page[9:10, 0:2] = handlers[5]
            analysis_page[0:5, 2:8] = app.performance_graph
            analysis_page[5:10, 2:8] = app.parameter_graph

            interface = pn.Tabs(
                ('Summary', summary_page),
                ('Analysis Page', analysis_page),
            )
            return interface

        platform = generate_interface()
        platform.servable()
    '''
    return dedent(block)[:-1]


def eval_import_block():
    block = '''\
        import os
        import tensorflow_model_analysis as tfma
    '''
    return dedent(block)[:-1]


def get_model_block(log_dir):
    block = '''\
    model_path = '"{evaluation}"'
    logdir = os.path.join(model_path, 'serving_model_dir')
    %load_ext tensorboard
    '''.format(evaluation=log_dir)
    block = dedent(block)
    block += '%tensorboard --logdir {logdir}'
    return block


def get_eval_block(eval_dir):
    block = '''\
    # If the visualization does not appear after running this block, please 
    # run the same cell again
    
    evaluation_path = '{evaluation}'
    evaluation = tfma.load_eval_result(output_path=evaluation_path)
    
    # find slicing metrics
    slicing_columns = set([x.feature_keys[0] for x in 
    evaluation.config.slicing_specs if len(x.feature_keys) == 1])
    print("")
    print("Available slicing columns: ")
    print(slicing_columns)
    
    tfma.view.render_slicing_metrics(evaluation)
    
    # in order to view sliced results, pass in the `slicing_column` parameter:
    # tfma.view.render_slicing_metrics(evaluation, slicing_column='col_name')
    '''.format(evaluation=eval_dir)
    return dedent(block)[:-1]
