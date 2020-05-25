import pprint

import click
import yaml
from click import pass_context
import ce_api
from ce_cli import constants
from ce_cli.pipeline import configure_pipeline
from ce_cli.utils import load_config, assert_exists, save_config, pass_info
from ce_cli.utils import notice, declare, title, confirmation, question
from ce_cli.utils import search_column, api_client, api_call
from standards.standard_experiment import *
import re

# TODO: Figure out a proper solution for this
TRAINER_DETAILS = {
    'ff': {
        'args': {'num_output_units': int,
                 'train_batch_size': int,
                 'eval_batch_size': int,
                 'train_steps': int,
                 'save_checkpoints_steps': int,
                 'optimizer': str,
                 'last_activation': str},
        'template': [
            {'type': 'dense', 'units': 128},
            {'type': 'dense', 'units': 128},
            {'type': 'dense', 'units': 128},
            {'type': 'dense', 'units': 128},
            {'type': 'dense', 'units': 128},
            {'type': 'dense', 'units': 128},
            {'type': 'dense', 'units': 64}
        ]},
    'sequence': {
        'args': {'num_output_units': int,
                 'train_batch_size': int,
                 'eval_batch_size': int,
                 'train_steps': int,
                 'save_checkpoints_steps': int,
                 'optimizer': str,
                 'last_activation': str,
                 'sequence_length': int},
        'template': [
            {'type': "lstm", 'units': 128, 'return_sequences': True},
            {'type': "lstm", 'units': 128, 'return_sequences': True},
            {'type': "lstm", 'units': 128, 'return_sequences': True},
            {'type': "lstm", 'units': 128, 'return_sequences': True},
            {'type': "lstm", 'units': 128, 'return_sequences': True},
            {'type': "lstm", 'units': 128, 'return_sequences': False},
            {'type': 'dense', 'units': 64}
        ]},
    'sequence_ae': {
        'args': {'num_output_units': int,
                 'train_batch_size': int,
                 'eval_batch_size': int,
                 'train_steps': int,
                 'save_checkpoints_steps': int,
                 'optimizer': str,
                 'last_activation': str,
                 'sequence_length': int},
        'template': [
            {'type': "lstm", 'units': 128, 'return_sequences': True},
            {'type': "lstm", 'units': 128, 'return_sequences': True},
            {'type': "lstm", 'units': 128, 'return_sequences': False},
            {'type': 'latent', 'units': 5},
            {'type': "lstm", 'units': 128, 'return_sequences': True},
            {'type': "lstm", 'units': 128, 'return_sequences': True},
            {'type': "lstm", 'units': 128, 'return_sequences': True},
        ]},
    'sequence_vae': {
        'args': {'num_output_units': int,
                 'train_batch_size': int,
                 'eval_batch_size': int,
                 'train_steps': int,
                 'save_checkpoints_steps': int,
                 'optimizer': str,
                 'last_activation': str,
                 'sequence_length': int},
        'template': [
            {'type': "lstm", 'units': 128, 'return_sequences': True},
            {'type': "lstm", 'units': 128, 'return_sequences': True},
            {'type': "lstm", 'units': 128, 'return_sequences': False},
            {'type': 'latent', 'units': 5},
            {'type': "lstm", 'units': 128, 'return_sequences': True},
            {'type': "lstm", 'units': 128, 'return_sequences': True},
            {'type': "lstm", 'units': 128, 'return_sequences': True},
        ]}
}

POSSIBLE_LOSS = {"mse", "categorical_crossentropy", "binary_crossentropy"}

SAMPLE_PREPROCESSING_W_TIMESERIES = {
    'boolean': {'filling': {'method': 'forward', 'parameters': {}},
                'label_tuning': {'method': 'leadup',
                                 'parameters': {'duration': 1,
                                                'event_value': True}},
                'resampling': {'method': 'threshold',
                               'parameters': {'c_value': 0,
                                              'cond': 'greater',
                                              'set_value': 1,
                                              'threshold': 0}},
                'transform': {'method': 'no_transform',
                              'parameters': {}}},
    'float': {'filling': {'method': 'forward', 'parameters': {}},
              'label_tuning': {'method': 'leadup',
                               'parameters': {'duration': 1,
                                              'event_value': 1.0}},
              'resampling': {'method': 'mean', 'parameters': {}},
              'transform': {'method': 'scale_to_z_score',
                            'parameters': {}}},
    'integer': {'filling': {'method': 'forward', 'parameters': {}},
                'label_tuning': {'method': 'leadup',
                                 'parameters': {'duration': 1,
                                                'event_value': 1}},
                'resampling': {'method': 'mean', 'parameters': {}},
                'transform': {'method': 'scale_to_z_score',
                              'parameters': {}}},
    'string': {'filling': {'method': 'forward', 'parameters': {}},
               'label_tuning': {'method': 'leadup',
                                'parameters': {'duration': 1,
                                               'event_value': 'True'}},
               'resampling': {'method': 'mode', 'parameters': {}},
               'transform': {'method': 'compute_and_apply_vocabulary',
                             'parameters': {}}}}

SAMPLE_PREPROCESSING_WO_TIMESERIES = {
    'boolean': {'filling': {'method': 'max', 'parameters': {}},
                'label_tuning': {'method': 'no_tuning', 'parameters': {}},
                'resampling': {'method': 'threshold',
                               'parameters': {'c_value': 0,
                                              'cond': 'greater',
                                              'set_value': 1,
                                              'threshold': 0}},
                'transform': {'method': 'no_transform',
                              'parameters': {}}},
    'float': {'filling': {'method': 'max', 'parameters': {}},
              'label_tuning': {'method': 'no_tuning', 'parameters': {}},
              'resampling': {'method': 'mean', 'parameters': {}},
              'transform': {'method': 'scale_to_z_score',
                            'parameters': {}}},
    'integer': {'filling': {'method': 'max', 'parameters': {}},
                'label_tuning': {'method': 'no_tuning', 'parameters': {}},
                'resampling': {'method': 'mean', 'parameters': {}},
                'transform': {'method': 'scale_to_z_score',
                              'parameters': {}}},
    'string': {
        'filling': {'method': 'custom', 'parameters': {'custom_value': ''}},
        'label_tuning': {'method': 'no_tuning', 'parameters': {}},
        'resampling': {'method': 'mode', 'parameters': {}},
        'transform': {'method': 'compute_and_apply_vocabulary',
                      'parameters': {}}}}


# PROCESSORS
@configure_pipeline.command('sequence')
@click.option('--timestamp_column', required=True, type=str,
              help='the name of the data columnn which holds the timestamp')
@click.option('--resampling_rate', required=True, type=int,
              help='the resampling rate in seconds')
@click.option('--trip_gap', required=True, type=int,
              help='the gap threshold between different trips in the data')
@click.option('--sequence_shift', required=True, type=int,
              help='shift in the time steps while extracting sequences from the dataset')
@click.option('--category_column', default=None, type=str,
              help='if specified, the data will be categorized by this column before the sequential processes')
def processor_sequence(timestamp_column,
                       resampling_rate,
                       trip_gap,
                       sequence_shift,
                       category_column):
    """Configure the timeseries configuration"""

    def config_sequence(config, schema):
        notice('Configuring sequences...')

        result = {}

        # Assert and set
        assert_exists(item=timestamp_column,
                      iterable=schema,
                      error_message="Timestamp column '{}' not in schema "
                                    "{}".format(timestamp_column, schema))

        result[TimeSeriesKeys.PROCESS_SEQUENCE_W_TIMESTAMP] = timestamp_column
        result[TimeSeriesKeys.RESAMPLING_RATE_IN_SECS] = resampling_rate
        result[TimeSeriesKeys.TRIP_GAP_THRESHOLD_IN_SECS] = trip_gap
        result[TimeSeriesKeys.SEQUENCE_SHIFT] = sequence_shift

        if category_column is not None:
            assert_exists(item=category_column,
                          iterable=schema,
                          error_message="Category column '{}' not in schema "
                                        "{}".format(category_column, schema))
            result[TimeSeriesKeys.PROCESS_SEQUENCE_W_CATEGORY_] = \
                category_column

        config[GlobalKeys.TIMESERIES_] = result

        return config

    return config_sequence


@configure_pipeline.command('labels')
@click.option('--label', multiple=True, type=(str, str),
              help='used to define pairs of (name_of_the_label_column, loss_function), can be used multiple times')
def processor_labels(label):
    """Configure the labeling configuration"""

    def config_labels(config, schema):
        notice('Configuring labels...')
        result = {}

        for l in label:
            label_name = l[0]
            loss_function = l[1]

            assert_exists(item=label_name,
                          iterable=schema,
                          error_message="Label '{}' not in schema "
                                        "{}".format(label_name, schema))

            assert_exists(item=loss_function,
                          iterable=POSSIBLE_LOSS,
                          error_message="Loss function '{}' not recognized. "
                                        "Select one of {}".format(
                              loss_function,
                              POSSIBLE_LOSS))

            result[label_name] = {}
            result[label_name]['loss'] = loss_function

            if GlobalKeys.TRAINER not in config:
                result[label_name]['metrics'] = []
            elif config[GlobalKeys.TRAINER][
                TrainerKeys.TYPE] == 'classification':
                result[label_name]['metrics'] = ['accuracy']
            elif config[GlobalKeys.TRAINER][TrainerKeys.TYPE] == 'regression':
                result[label_name]['metrics'] = ['mae']
            elif config[GlobalKeys.TRAINER][TrainerKeys.TYPE] == 'autoencoder':
                result[label_name]['metrics'] = []

        config[GlobalKeys.LABELS] = result
        return config

    return config_labels


@configure_pipeline.command('features')
@click.option('--feature', multiple=True, type=str, default=[],
              help='name of the feature to be included in the training, can be used multiple times')
@click.option('--blacklist', multiple=True, type=str, default=[],
              help='name of the feature to be excluded from the training, can be used multiple times')
@click.option('--remove_labels', is_flag=True, default=False,
              help='if given, automatically removes all the labels from the training feature set')
@click.option('--regex', is_flag=True, default=False,
              help='if given, feature and blacklist will be used as regex pattern while including and excluding')
def processor_features(feature, blacklist, remove_labels, regex):
    """Configure the feature selection for training"""

    def config_features(config, schema):
        notice('Configuring features...')
        result = {}

        # Determining the feature set
        if len(feature) == 0:
            feature_set = set(schema.keys())
        else:
            if regex:
                r = re.compile('|'.join(feature))
                feature_set = set(filter(r.match, list(schema.keys())))
            else:
                feature_set = set(feature)

        # Determining the blacklist
        if blacklist:
            if regex:
                r = re.compile('|'.join(blacklist))
                blacklist_set = set(filter(r.match, list(schema.keys())))
            else:
                blacklist_set = set(blacklist)
        else:
            blacklist_set = set()

        # Putting everything together
        if remove_labels and GlobalKeys.LABELS in config:
            feature_set -= set(config[GlobalKeys.LABELS])

        for f in feature_set:
            assert_exists(item=f,
                          iterable=schema,
                          error_message="Feature '{}' not in schema "
                                        "{}".format(f, schema))

            if f not in blacklist_set:
                result[f] = {}

        config[GlobalKeys.FEATURES] = result

        return config

    return config_features


@configure_pipeline.command('evaluator')
@click.option('--slice', multiple=True, type=str,
              help='name of the data column to slice the data for the evaluation, can be used multiple times')
def processor_evaluator(slice):
    """Configure the feature selection for post-training evaluation"""

    def config_evaluator(config, schema):
        notice('Configuring evaluation slices...')
        result = {}

        for s in slice:
            assert_exists(item=s,
                          iterable=schema,
                          error_message="Slicing column '{}' not in schema "
                                        "{}".format(s, schema))

            result[s] = {}

        config[GlobalKeys.EVALUATOR] = result

        return config

    return config_evaluator


@configure_pipeline.command('split')
@click.option('--ratio', required=True, type=float,
              help='defines the ratio of the train dataset, needs to be between 0 and 1')
@click.option('--sort_by', default=None, type=str,
              help='if specified, the data will be sorted by this column before the split')
@click.option('--category_column', default=None, type=str,
              help='if specified, the data will be categorized by this column before the split')
@click.option('--category_ratio', default=1, type=float,
              help='if specified, the ratio of the categories which will be put in the training dataset')
@click.option('--train_category', multiple=True, type=str, default=[],
              help='name of a category which will be put in the training dataset, can be used multiple times')
@click.option('--eval_category', multiple=True, type=str, default=[],
              help='name of a category which will be put in the eval dataset, can be used multiple times')
@pass_info
def processor_splits(info,
                     ratio,
                     sort_by,
                     category_column,
                     category_ratio,
                     train_category,
                     eval_category):
    """Configure the dataset splits"""

    def config_splits(config, schema):
        notice('Configuring splits...')
        result = {}

        if category_column is not None:
            assert_exists(item=category_column,
                          iterable=schema,
                          error_message="Category column '{}' not in schema "
                                        "{}".format(category_column, schema))

            result[SplitKeys.CATEGORIZE_BY_] = category_column

            if len(eval_category) > 0 or len(train_category) > 0:
                result[SplitKeys.CATEGORIES_] = {}

                user = info[constants.ACTIVE_USER]
                datasource_id = info[user][constants.ACTIVE_DATASOURCE]
                api = ce_api.DatasourcesApi(api_client(info))
                category_set = set(api_call(
                    api.get_bigquery_datasource_column_values_api_v1_datasources_bigquery_bq_ds_id_schema_column_name_get,
                    datasource_id,
                    category_column))

                if len(train_category) > 0:
                    for c in train_category:
                        assert_exists(
                            item=c,
                            iterable=category_set,
                            error_message="Categorical value '{}' does not "
                                          "exist in the datasource. Select "
                                          "from {}".format(c,
                                                           category_set))

                    result[SplitKeys.CATEGORIES_]['train'] = list(
                        train_category)

                    if len(eval_category) == 0:
                        result[SplitKeys.CATEGORIES_]['eval'] = \
                            list(category_set - set(train_category))

                if len(eval_category) > 0:
                    for c in eval_category:
                        assert_exists(
                            item=c,
                            iterable=category_set,
                            error_message="Categorical value '{}' does not "
                                          "exist in the datasource. Select "
                                          "from {}".format(c,
                                                           category_set))
                    result[SplitKeys.CATEGORIES_]['eval'] = list(eval_category)

                    if len(train_category) == 0:
                        result[SplitKeys.CATEGORIES_]['train'] = \
                            list(category_set - set(eval_category))

            else:
                assert category_ratio <= 1 or category_ratio >= 0, \
                    "Define a ratio between 0 and 1."

                result[SplitKeys.CATEGORY_RATIO_] = {}
                result[SplitKeys.CATEGORY_RATIO_]['train'] = category_ratio
                result[SplitKeys.CATEGORY_RATIO_]['eval'] = 1 - category_ratio

        if sort_by is not None:
            assert_exists(item=sort_by,
                          iterable=schema,
                          error_message="Column to sort by '{}' not in schema "
                                        "{}".format(sort_by, schema))

            result[SplitKeys.INDEX_BY_] = sort_by

        assert ratio <= 1 or ratio >= 0, \
            "Define a ratio between 0 and 1."
        result[SplitKeys.INDEX_RATIO_] = {}
        result[SplitKeys.INDEX_RATIO_]['train'] = ratio
        result[SplitKeys.INDEX_RATIO_]['eval'] = 1 - ratio

        config[GlobalKeys.SPLIT] = result

        return config

    return config_splits


@configure_pipeline.command('trainer')
@click.option('--trainer_type', required=True, type=str,
              help="determines the architecture of the model, possible values include 'feedforward', 'sequence''sequence_ae'")
@click.option('--trainer_architecture', required=True, type=str,
              help="defines the type of the problem at hand, possible selections include 'regression', 'classification', 'autoencoder'")
@click.option('--sequence_length', default=1, type=int,
              help="the length of the sequence in one data point (provided only on a sequential problem setting)")
@click.option('--num_output_units', default=1, type=int,
              help="the number of output units in the last layer, default=1")
@click.option('--train_batch_size', default=32, type=int,
              help="the batch size during the training, default=32")
@click.option('--eval_batch_size', default=32, type=int,
              help="the batch size during the eval steps, default=32")
@click.option('--train_steps', default=5000, type=int,
              help="the number of batches which should be processed through the training, default=5000")
@click.option('--save_checkpoints_steps', default=200, type=int,
              help="the number of training batches, which will indicate the frequency of the validation steps, default=200")
@click.option('--optimizer', default='adam', type=str,
              help="the name of the selected optimizer for the training, default='adam'")
@click.option('--last_activation', default='sigmoid', type=str,
              help="the type of the output layer in the model, default='sigmoid'")
def processor_trainer(trainer_type,
                      trainer_architecture,
                      sequence_length,
                      num_output_units,
                      train_batch_size,
                      eval_batch_size,
                      train_steps,
                      save_checkpoints_steps,
                      optimizer,
                      last_activation):
    """Configure the model creation and training"""

    def config_trainer(config, schema):
        notice('Configuring trainer...')

        result = {}

        tasks = ['regression', 'classification', 'autoencoder']
        assert_exists(item=trainer_type, iterable=tasks,
                      error_message='{} unrecognized. Please select one of '
                                    'the selected trainer types '
                                    '{}'.format(trainer_type, tasks))

        architectures = ['lstm', 'feedforward']
        assert_exists(item=trainer_architecture, iterable=architectures,
                      error_message='{} unrecognized. Please select one of '
                                    'the selected architecture '
                                    '{}'.format(trainer_architecture,
                                                architectures))

        result[TrainerKeys.TYPE] = trainer_type
        result[TrainerKeys.ARCHITECTURE] = trainer_architecture
        result[TrainerKeys.SEQUENCE_LENGTH_] = sequence_length
        result[TrainerKeys.NUM_OUTPUT_UNITS_] = num_output_units
        result[TrainerKeys.TRAIN_BATCH_SIZE] = train_batch_size
        result[TrainerKeys.EVAL_BATCH_SIZE] = eval_batch_size
        result[TrainerKeys.TRAIN_STEPS] = train_steps
        result[TrainerKeys.SAVE_CHECKPOINTS_STEPS] = save_checkpoints_steps
        result[TrainerKeys.OPTIMIZER] = optimizer
        result[TrainerKeys.LAST_ACTIVATION_] = last_activation

        # Obtain the type to get the params
        if result[TrainerKeys.ARCHITECTURE] == 'feedforward':
            t = 'ff'
        elif result[TrainerKeys.ARCHITECTURE] == 'lstm':
            if result[TrainerKeys.TYPE] == 'autoencoder':
                t = 'sequence_ae'
            else:
                t = 'sequence'
        else:
            raise Exception('Unknown architecture for the trainer')
        result[TrainerKeys.LAYERS] = TRAINER_DETAILS[t]['template']

        config[GlobalKeys.TRAINER] = result

        return config

    return config_trainer


@configure_pipeline.command('preprocessing')
@click.option('--defaults_path', default=None, type=click.Path(),
              help="path to a .yaml file which would be used to define the defaults")
def processor_preprocessing(defaults_path):
    def config_preprocessing(config, schema):
        """Configure the default pre-processing behaviour"""
        notice('Configuring the default preprocessing behaviour...')
        if defaults_path is None:
            if GlobalKeys.TIMESERIES_ in config:
                defaults = SAMPLE_PREPROCESSING_W_TIMESERIES
            else:
                defaults = SAMPLE_PREPROCESSING_WO_TIMESERIES
        else:
            with open(defaults_path, 'rt', encoding='utf8') as f:
                defaults = yaml.load(f)

        config[GlobalKeys.PREPROCESSING] = defaults
        return config

    return config_preprocessing


# @configure_pipeline.command('pca')
# @click.option('--num_dimensions', required=True, type=int)
# def processor_pca(num_dimensions):
#     def config_pca(config, schema):
#         config[GlobalKeys.PCA_] = {PCAKeys.NUM_DIMENSIONS: num_dimensions}
#         return config
#
#     return config_pca


@configure_pipeline.resultcallback()
@pass_info
@pass_context
def final_callback(context, info, processors, input_path, output_path):
    active_user = info[constants.ACTIVE_USER]
    ds = info[active_user][constants.ACTIVE_DATASOURCE]

    api = ce_api.DatasourcesApi(api_client(info))
    bq_schema = api.get_bigquery_datasource_schema_api_v1_datasources_bigquery_bq_ds_id_schema_get(
        ds)

    config = load_config(input_path)

    if context.invoked_subcommand is None:
        # Manual workflow
        manual_schema(bq_schema)
        config = manual_splits(info, config, bq_schema)
        config = manual_sequence(config, bq_schema)
        config = manual_trainer(config, bq_schema)
        config = manual_labels(config, bq_schema)
        config = manual_features(config, bq_schema)
        # config = manual_pca(config)
        config = manual_preprocessing(config)
    else:
        # Auto workflow
        for step in processors:
            config = step(config, bq_schema)

    config[GlobalKeys.VERSION] = constants.CONFIG_VERSION

    pretty_s = pprint.PrettyPrinter().pformat(config)
    declare('Final configuration:')
    declare('{} \n'.format(pretty_s))

    save_config(config, output_path, no_docs=True)


# MANUAL FUNCTIONS
def manual_schema(s):
    title('schema')
    if len(s) > 30:
        if confirmation('The schema has more than 30 features, Would you '
                        'still like print it?'):
            pretty_s = pprint.PrettyPrinter().pformat(s)
            declare('{} \n'.format(pretty_s))
    else:
        pretty_s = pprint.PrettyPrinter().pformat(s)
        declare('{} \n'.format(pretty_s))


def manual_sequence(config, s):
    title('SEQUENCES')

    if confirmation('Would you like to apply sequential processes such'
                    ' as resampling and filling?'):
        results = {}

        seq_col = search_column(message='Which column defines the sequential '
                                        'index in your data', schema=s)

        if seq_col is None:
            declare('You have selected to work on non-sequential data \n')
            return config

        results[TimeSeriesKeys.PROCESS_SEQUENCE_W_TIMESTAMP] = seq_col

        resampling_rate = question(
            text='What is the desired resampling rate in seconds?',
            type=float, default=5, show_default=True)
        results[TimeSeriesKeys.RESAMPLING_RATE_IN_SECS] = resampling_rate

        trip_gap = question(
            text='What is the desired trip threshold in seconds? default',
            type=float, default=30, show_default=True)
        results[TimeSeriesKeys.TRIP_GAP_THRESHOLD_IN_SECS] = trip_gap

        sequence_shift = question(
            text='What is the sequence shift in the data points?',
            type=int, default=1, show_default=True)
        results[TimeSeriesKeys.SEQUENCE_SHIFT] = sequence_shift

        if confirmation('Would you like to apply these processing within '
                        'the bounds of a specific category?'):
            cat_col = search_column(message='Which column should '
                                            'define the category',
                                    schema=s)
            if cat_col is not None:
                results[TimeSeriesKeys.PROCESS_SEQUENCE_W_CATEGORY_] = cat_col

        # SUMMARY
        summary = '{col} is selected as the sequential index. \n' \
                  'The resampling rate is {rr} seconds. \n' \
                  'The trip gap threshold is {tg} seconds. \n' \
                  'The sequence shift is {ss}. \n' \
            .format(col=seq_col, rr=resampling_rate,
                    tg=trip_gap, ss=sequence_shift)

        config[GlobalKeys.TIMESERIES_] = results
        declare(summary)
    else:
        declare('You have selected to work on non-sequential data \n')

    return config


def manual_labels(config, s):
    title('labels')

    result = {}

    while True:
        if confirmation('Would you like to add any other labels?'):
            label_column = search_column(message='Name of the label column',
                                         schema=s)

            if label_column is None:
                break

            result[label_column] = {}

            # TODO: force possible selections
            loss = question('What is the loss function associated with '
                            'this label?', type=str)

            result[label_column]['loss'] = loss

            if GlobalKeys.TRAINER not in config:
                result[label_column]['metrics'] = []
            elif config[GlobalKeys.TRAINER][
                TrainerKeys.TYPE] == 'classification':
                result[label_column]['metrics'] = ['accuracy']
            elif config[GlobalKeys.TRAINER][TrainerKeys.TYPE] == 'regression':
                result[label_column]['metrics'] = ['mae']
            elif config[GlobalKeys.TRAINER][TrainerKeys.TYPE] == 'autoencoder':
                result[label_column]['metrics'] = []
        else:
            break

    config[GlobalKeys.LABELS] = result
    declare('You have selected {} as your label(s). \n'.format(
        list(config[GlobalKeys.LABELS].keys())))

    return config


def manual_features(config, s):
    title('features for training and evaluation')
    feature_set = set(s.keys())

    if GlobalKeys.FEATURES not in config:
        config[GlobalKeys.FEATURES] = {}
    if GlobalKeys.EVALUATOR not in config:
        config[GlobalKeys.EVALUATOR] = {}

    declare('By default, all of the features are set to be used for training. '
            'In addition, each feature which plays a role in the training is '
            'inherently used in the evaluation.')

    if GlobalKeys.LABELS in config:
        notice('Current feature set: {}'.format(feature_set))
        if confirmation(
                'First, would you like to remove the label columns {} from '
                'the feature set?'.format(set(config[GlobalKeys.LABELS]))):
            feature_set -= set(config[GlobalKeys.LABELS])

    while True:
        notice('\nCurrent feature set: {}'.format(feature_set))
        if confirmation('Would you like to remove any features from '
                        'the training feature set?'):
            feature = search_column(message='Please name feature you want to '
                                            'remove',
                                    schema=feature_set)

            if feature is None:
                break

            feature_set -= {feature}
            if confirmation('{} is removed from the feature set. Would you '
                            'still like to use it as a splittig_feature for the '
                            'evaluation?'.format(feature)):
                config[GlobalKeys.EVALUATOR][feature] = {}
        else:
            break
    for f in feature_set:
        config[GlobalKeys.FEATURES][f] = {}

    declare('{f} will be used both during training and evaluation, while '
            '{e} will just be used for evaluation \n'
            .format(f=set(config[GlobalKeys.FEATURES].keys()),
                    e=set(config[GlobalKeys.EVALUATOR].keys())))

    return config


def manual_splits(info, config, s):
    title('splits')
    result = {}

    notice('When it comes to splitting your data into a train and eval '
           'dataset, the Core Engine allows the user to define more than '
           'just a random split.\n')

    notice('Imagine that you gather data from different assets in the field'
           ' for ten days and your data is timestamped. You want to split '
           'your data in a way that the respective last three days of each '
           'asset are in the eval set, while the first seven are in the '
           'training dataset. For such a scenario, the data needs to be both '
           'sorted (according to the timestamp) and categorized (according '
           'to the id of the asset) because the time interval for each '
           'asset may not align in terms of time.\n')

    notice('In order to handle situations similar to this example, the Core '
           'Engine allows its users to define 1 categorical column and 1 '
           'indexed column for splitting.\n')

    notice('You can use the categorical column to group the data before the '
           'split or even to specify which category goes to which split.\n')

    notice('As for the indexed column, you can use it sort your data before '
           'the split. \n')

    if confirmation('Would you like to specify a categorical column?'):
        cat_col = search_column(message='Provide the name of the categorical '
                                        'column',
                                schema=s)

        if cat_col is not None:
            user = info[constants.ACTIVE_USER]
            datasource_id = info[user][constants.ACTIVE_DATASOURCE]
            api = ce_api.DatasourcesApi(api_client(info))
            category_set = set(api_call(
                api.get_bigquery_datasource_column_values_api_v1_datasources_bigquery_bq_ds_id_schema_column_name_get,
                datasource_id,
                cat_col))

            train_category_set = category_set
            eval_category_set = set()

            result[SplitKeys.CATEGORIZE_BY_] = cat_col
            notice('In this column, you have the following categories: '
                   '{}'.format(list(train_category_set)))

            if confirmation('Would you like to manually specify which '
                            'categories belong to which split?'):

                while True:
                    notice('Right now, {t} are in the training dataset.\n'
                           '{e} are in the eval dataset.\n'
                           .format(t=list(train_category_set),
                                   e=list(eval_category_set)))
                    if confirmation('Would you like to move any (other) '
                                    'categories to eval dataset?'):
                        cat = search_column(
                            message='Which category should be completely '
                                    'moved to the eval dataset?',
                            schema=train_category_set)

                        if cat is not None:
                            train_category_set.remove(cat)
                            eval_category_set.add(cat)
                        else:
                            break
                    else:
                        break

                result[SplitKeys.CATEGORIES_] = {
                    'train': list(train_category_set),
                    'eval': list(eval_category_set)}

                declare('Categories set!\n'
                        '{t} are in the training dataset.\n'
                        '{e} are in the eval dataset.\n '.format(
                    t=list(train_category_set),
                    e=list(eval_category_set)))

            elif confirmation('Would you like to specify a train ratio? Note: '
                              'This ratio will only be used among categories! '
                              'The question regarding the ratio within the '
                              'each category will soon follow.'):
                train_ratio = question('Please define a train dataset ratio '
                                       'between 0 and 1', type=float)

                while train_ratio > 1 or train_ratio < 0:
                    train_ratio = question('Please define a train dataset '
                                           'ratio between 0 and 1', type=float)

                result[SplitKeys.CATEGORY_RATIO_] = {
                    'train': train_ratio,
                    'eval': 1 - train_ratio}
                declare('The train ratio among categories is {t}.\n'
                        'The eval ratio among categories is {e}.\n'.format(
                    t=round(train_ratio, 2), e=round(1 - train_ratio, 2)))

            else:
                declare('Nonetheless, the data will be categorized according '
                        'to {} and the split will happen in each category '
                        'separately.\n'.format(cat_col))

    if confirmation('Would you like to specify a indexed column to sort the '
                    'data before splitting?'):
        idx_col = search_column(message='Provide the name of the indexed '
                                        'column',
                                schema=s)
        result[SplitKeys.INDEX_BY_] = idx_col
        declare('The data will be sorted and split according to {}.'.format(
            idx_col))

    declare('\nLastly, you need define a train ratio between 0 and 1'
            ' for the split. If categories are given, this ratio will be '
            'applied to data within each category. If there are no '
            'categories, it will be applied to the whole dataset.')

    ratio = question('Please define a train dataset ratio between '
                     '0 and 1', type=float)

    while ratio > 1 or ratio < 0:
        ratio = question('Please define a train dataset ratio between '
                         '0 and 1', type=float)

    result[SplitKeys.INDEX_RATIO_] = {
        'train': ratio,
        'eval': 1 - ratio}
    declare('The train ratio is {t}.\n'
            'The eval ratio is {e}.\n'.format(t=round(ratio, 2),
                                              e=round(1 - ratio, 2)))

    config[GlobalKeys.SPLIT] = result
    return config


def manual_trainer(config, s):
    title('trainer')
    result = {}
    tasks = ['classification', 'regression', 'autoencoder']

    task = question('What kind of a task would you like to execute? '
                    'Choose from {}'.format(tasks))
    while task not in tasks:
        task = question(
            'Invalid input for the task. Please select from {}'.format(tasks))
    result[TrainerKeys.TYPE] = task

    if GlobalKeys.TIMESERIES_ in config:
        declare('Since you have selected to work on timeseries data, '
                'Implementing an LSTM network...\n')
        result[TrainerKeys.ARCHITECTURE] = 'lstm'
    else:
        result[TrainerKeys.ARCHITECTURE] = 'feedforward'

    # Obtain the type to get the params
    if result[TrainerKeys.ARCHITECTURE] == 'feedforward':
        trainer_type = 'ff'
    elif result[TrainerKeys.ARCHITECTURE] == 'lstm':
        if result[TrainerKeys.TYPE] == 'autoencoder':
            trainer_type = 'sequence_ae'
        else:
            trainer_type = 'sequence'
    else:
        raise Exception('Unknown architecture for the trainer')

    result[TrainerKeys.LAYERS] = TRAINER_DETAILS[trainer_type]['template']

    trainer_args = TRAINER_DETAILS[trainer_type]['args']

    for arg, t in trainer_args.items():
        value = question(
            'Please provide a value for the parameter, {}'.format(arg),
            type=t)
        result[arg] = value
    click.echo()

    for k, v in result.items():
        declare('The value for {} is {}.'.format(k, v))
    click.echo()
    config[GlobalKeys.TRAINER] = result

    return config


def manual_preprocessing(config):
    declare('\nAdding the preprocessing defaults.')
    if GlobalKeys.TIMESERIES_ in config:
        defaults = SAMPLE_PREPROCESSING_W_TIMESERIES
    else:
        defaults = SAMPLE_PREPROCESSING_WO_TIMESERIES
    config[GlobalKeys.PREPROCESSING] = defaults
    return config

# def manual_pca(config):
#     title('PCA')
#     if confirmation('Would you like to apply PCA to your data?'):
#         num_dimensions = question(
#             text='Please specify the number of desired dimensions for the PCA',
#             type=int, default=2, show_default=True)
#         config[GlobalKeys.PCA_] = {PCAKeys.NUM_DIMENSIONS: num_dimensions}
#
#     return config
