import yaml
from standards.standard_experiment import GlobalKeys

REQUIRED = [
    (GlobalKeys.VERSION, """# This is the version of the configuration YAML!"""),
    (GlobalKeys.SPLIT, """
# The key 'split' is utilized to configure the process of splitting the dataset 
# into a training and an eval dataset.
#
#   - categorize_by:    string which specifies the name of a selected 
#                       categorical column
#   - categories:       dictionary which has the keys train and eval. Under 
#                       each key, there must be a list of strings, defining 
#                       which category belongs to which split. Can not be 
#                       used while category_ratio is present
#   - category_ratio:   dictionary which has the keys train and eval. Under each 
#                       key, there is a float value determining the split ratio 
#                       within the categories. Can not be used while categories 
#                       is present
#   - index_by:         string which specifies the name of a selected index 
#                       column
#   - index_ratio:      dictionary which has the keys train and eval. Under each 
#                       key, there is a float value determining the ratio of the 
#                       split (it is based on a sorted index column if index_by is 
#                       specified)
#   - where:            list of strings, which defines additional conditions 
#                       while querying the datasource
#
# for more info: https://docs.maiot.io/docs/developer_guide/pipelines_yaml#main-key-split
"""),
    (GlobalKeys.FEATURES, """
# The main key `features` is used to define which set of features will be used 
# during the training and it allows the users to modify the pre-processing 
# steps filling, transform (and possibly resampling in case of sequential 
# data) for each one of these features.
#
# Structurally, each key under features represents a selected feature. 
# Under each key, the user has the chance to determine a method for each 
# pre-processing step to use. If it is not explicitly defined, the behaviour 
# will be inferred from the defaults based on the data type.
#
# for more info: https://docs.maiot.io/docs/developer_guide/pipelines_yaml#main-key-features
"""),
    (GlobalKeys.LABELS, """
# The main key labels is used to determine which data column will be used 
# as the label during the training. The inner structure of this column is 
# quite similar to the block features, where the keys denote the data columns  
# which are selected and the values include the pre-processing configuration
#
# for more info: https://docs.maiot.io/docs/developer_guide/pipelines_yaml#main-key-labels
"""),
    (GlobalKeys.EVALUATOR, """
# The main key evaluator determines which data columns will be used in the 
# evaluation of the trained model. Structurally, it shares the same 
# structure as the features block.
"""),
    (GlobalKeys.TRAINER, """
# The main key trainer is used to configure the model and the training 
# parameters.
#
#   - architecture:             string value which determines the architecture 
#                               of the model, possible values include 
#                               'feedforward' for feedforward networks, 
#                               'sequence' for LSTM networks and 'sequence_ae' 
#                               for sequence-to-sequence autoencoders
#   - type:                     string value which defines the type of the 
#                               problem at hand, possible selections include 
#                               'regression', 'classification', 'autoencoder'
#   - train_batch_size:         the batch size during the training
#   - eval_batch_size:          the batch size during the eval steps
#   - train_steps:              the number of batches which should be 
#                               processed through the training
#   - save_checkpoints_steps:   the number of training batches, which will 
#                               indicate the frequency of the validation steps
#   - optimizer:                the name of the selected optimizer for the 
#                               training
#   - last_activation:          the name of the last layer in the model
#   - num_output_units:         the number of output units in the last layer
#   - sequence_length:          the length of the sequence in one data point 
#                               (provided only on a sequential problem setting)
#   - layers:                   list of dictionaries, which hold the layer 
#                               configurations
#
# for more info: https://docs.maiot.io/docs/developer_guide/pipelines_yaml#main-key-trainer
"""),
    (GlobalKeys.PREPROCESSING, """
# This is the default preprocess block!
# 
# TODO: fill in later after the doc change
"""),
]

OPTIONAL = [
    (GlobalKeys.TIMESERIES_, """
# This block configures the preprocessing steps specific to time-series 
# datasets. 
#
#   - resampling_rate_in_secs:      defines the resampling rate in seconds 
#                                   and it will be used at the corresponding 
#                                   pre-precessing step
#   - trip_gap_threshold_in_secs:   defines a maximum threshold in seconds in 
#                                   order to split the dataset into trips. 
#                                   Sequential transformations will occur once 
#                                   the data is split into trips based on this value.
#   - process_sequence_w_timestamp: specifies which data column holds the 
#                                   timestamp.
#   - process_sequence_w_category:  is an optional value, which, if provided, 
#                                   will be used to split the data into 
#                                   categories before the sequential processes
#   - sequence_shift:               defines the shift (in datapoints) while 
#                                   extracting sequences from the dataset
#
# for more info: https://docs.maiot.io/docs/developer_guide/pipelines_yaml#main-key-timeseries-optional
""")
]


def generate_comment_block(block, description):
    return """##{filler}##
# {title} #
##{filler}##
{description}
""".format(filler='#' * len(block),
           title=block.upper(),
           description=description)


def generate_config_block(block, config):
    return yaml.dump({block: config[block]}, default_flow_style=False) + '\n'


def save_pretty_yaml(config, output_path, no_docs):
    with open(output_path, "w") as output_file:
        for block, description in REQUIRED:
            if not no_docs:
                comment = generate_comment_block(block, description)
                output_file.writelines(comment)
            block = generate_config_block(block, config)
            output_file.writelines(block)

        for block, description in OPTIONAL:
            if block in config:
                if not no_docs:
                    comment = generate_comment_block(block, description)
                    output_file.writelines(comment)
                block = generate_config_block(block, config)
                output_file.writelines(block)


# if __name__ == '__main__':
#     # For testing purposes
#     input_path = '/home/baris/Maiot/gdp/dota.config.yaml'
#     with open(input_path, 'rt', encoding='utf8') as input_file:
#         config = yaml.load(input_file)
#
#     output_file = open("pretty.yaml", "w")
#
#     for block, description in REQUIRED:
#         comment = generate_comment_block(block, description)
#         block = generate_config_block(block, config)
#
#         output_file.writelines(comment + block)
#
#     for block, description in OPTIONAL:
#         if block in config:
#             comment = generate_comment_block(block, description)
#             block = generate_config_block(block, config)
#
#             output_file.writelines(comment + block)
#
#     output_file.close()
