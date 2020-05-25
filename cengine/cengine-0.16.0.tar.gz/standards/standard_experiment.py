from standards.utils import ConfigKeys


class GlobalKeys(ConfigKeys):
    VERSION = 'version'
    # bq_args key is MANUALLY added to the exp_config during pipeline creation
    BQ_ARGS = 'bq_args'
    SPLIT = 'split'
    FEATURES = 'features'
    LABELS = 'labels'
    TRAINER = 'trainer'
    EVALUATOR = 'evaluator'
    PREPROCESSING = 'preprocessing'
    TIMESERIES_ = 'timeseries'
    PCA_ = 'pca'


class BQArgsKeys(ConfigKeys):
    PROJECT = 'project'
    DATASET = 'dataset'
    TABLE = 'table'


class TimeSeriesKeys:
    RESAMPLING_RATE_IN_SECS = 'resampling_rate_in_secs'
    TRIP_GAP_THRESHOLD_IN_SECS = 'trip_gap_threshold_in_secs'

    PROCESS_SEQUENCE_W_TIMESTAMP = 'process_sequence_w_timestamp'
    PROCESS_SEQUENCE_W_CATEGORY_ = 'process_sequence_w_category'

    SEQUENCE_SHIFT = 'sequence_shift'


class SplitKeys(ConfigKeys):
    CATEGORIZE_BY_ = 'categorize_by'
    CATEGORIES_ = 'categories'
    CATEGORY_RATIO_ = 'category_ratio'

    INDEX_BY_ = 'index_by'
    INDEX_RATIO_ = 'index_ratio'

    WHERE_ = 'where'


class PCAKeys(ConfigKeys):
    NUM_DIMENSIONS = 'num_dimensions'


class TrainerKeys(ConfigKeys):
    ARCHITECTURE = 'architecture'
    TYPE = 'type'

    TRAIN_BATCH_SIZE = 'train_batch_size'
    EVAL_BATCH_SIZE = 'eval_batch_size'

    TRAIN_STEPS = 'train_steps'
    SAVE_CHECKPOINTS_STEPS = 'save_checkpoints_steps'
    OPTIMIZER = 'optimizer'

    LAYERS = 'layers'

    LAST_ACTIVATION_ = 'last_activation'
    SEQUENCE_LENGTH_ = 'sequence_length'
    NUM_OUTPUT_UNITS_ = 'num_output_units'


class DefaultKeys(ConfigKeys):
    STRING = 'string'
    INTEGER = 'integer'
    BOOLEAN = 'boolean'
    FLOAT = 'float'


class PreProcessKeys(ConfigKeys):
    RESAMPLING = 'resampling'
    FILLING = 'filling'
    TRANSFORM = 'transform'
    LABEL_TUNING = 'label_tuning'


class MethodKeys(ConfigKeys):
    METHOD = 'method'
    PARAMETERS = 'parameters'
