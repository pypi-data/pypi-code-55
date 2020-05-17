#  C O N S T R U C T I V I S T__ __
#   _____ ____   ____   /  |/  // /
#  / ___// __ \ / __ \ / /|_/ // /
# / /__ / /_/ // / / // /  / // /___
# \___/ \____//_/ /_//_/  /_//_____/
#  M A C H I N E   L E A R N I N G
#
#
# A Project by
# Thomas Schmid | UNIVERSITÄT LEIPZIG
# www.constructivist.ml
#
# Code Author: Dmitrij Denisenko
# Licence: MIT


"""Define single access point to all control parameter.

Every parameter is set to its default value after reading the configuration
file. The default configuration file is located at $HOME/.conML/settings.ini on
Unix like OS and it is read during conML module import by the user.
It is possible to provide another settings.ini path destination.

"""


from itertools import starmap
from dataclasses import dataclass, asdict
from configparser import ConfigParser

from conML.shared.parameter import *
from conML.shared.errors import ConfigurationFileError


class MetaSettings(type):
    """Container for all parameter.

    """
    HIGHEST_LEVEL: int = HighestLevel()
    KERNEL_BANDWIDTH: float = KernelBandwidth()

    LEARN_BLOCK_MINIMUM: int = LearnblockMinimum()
    SIGMA_ZETA_CUTOFF: float = SigmaZetaCutoff()

    MAX_CATEGORIES: int = MaxCategories()
    MIN_CATEGORY_SIZE: int = MinCategorySize()
    MAX_MODEL_TARGETS: int = MaxModelTargets()
    MAX_TARGET_ERROR: float = MaxTargetError()

    MIN_BUILD_MODELS: int = MinBuildModels()
    MAX_FEATURES: int = MaxFeatures()
    MAX_FILTER_X: int = MaxFilterX()
    MAX_FILTER_Y: int = MaxFilterY()
    MAX_MODELS_REDUCTION: bool = MaxModelsReduction()
    MIN_TEST_ACCURACY: float = MinTestAccuracy()
    MAX_TEST_ERROR_AVG: float = MaxTestErrorAvg()
    MAX_TEST_ERROR_MAX: float = MaxTestErrorMax()
    RELIABILITY_SAMPLE: float = ReliabilitySample()
    MIN_RELIABILITY: float = MinReliability()
    REDUCE_MODEL_REDUNDANCY: bool = ReduceModelRedundancy()

    DECONST_STRATEGY: str = DeconstStrategy()
    DECONST_MODE: str = DeconstMode()
    DECONST_MAX_DISTANCE_T: int = DeconstMaxDistanceT()
    DECONST_FULL_TOLERANCE: float = DeconstFullTolerance()
    FORCE_TIME_EXPANSION: bool = ForceTimeExpansion()
    ALLOW_WEAK_RELIABILITY: bool = AllowWeakReliability()


class Settings(metaclass=MetaSettings):
    pass


@dataclass
class GeneralSettings:
    """Influence the global framework.

    """
    highest_level: int = HighestLevel()
    kernel_bandwidth: float = KernelBandwidth()

    def __str__(self):
        return "\n".join([
            "{:<20}: {}".format("Highest level", self.highest_level)
        ])


@dataclass
class BlockProcessingSettings:
    """Influence the block drawing.

    """
    learn_block_minimum: int = LearnblockMinimum()
    sigma_zeta_cutoff: float = SigmaZetaCutoff()
    min_category_size: int = MinCategorySize()

    def __str__(self):
        return "\n".join([
            "{:<20}: {}".format("Learn_block_minimum", self.learn_block_minimum),
            "{:<20}: {}".format("Sigma zeta cutoff", self.sigma_zeta_cutoff),
        ])


@dataclass
class ConstructionSettings:
    """Influence the construction step.

    """
    max_categories: int = MaxCategories()
    min_category_size: int = MinCategorySize()
    max_model_targets: int = MaxModelTargets()
    max_target_error: float = MaxTargetError()

    def __str__(self):
        return "\n".join([
            "{:<20}: {}".format("Max categories", self.max_categories),
            "{:<20}: {}".format("Min category size", self.min_category_size),
            "{:<20}: {}".format("Max model targets", self.max_model_targets),
            "{:<20}: {}".format("Max target error", self.max_target_error),
        ])

    def __repr__(self):
        return ", ".join([
            "{}={}".format("max_categories", self.max_categories),
            "{}={}".format("min_category size", self.min_category_size),
            "{}={}".format("max_model_targets", self.max_model_targets),
            "{}={}".format("max_target_error", self.max_target_error),
        ])


@dataclass
class FeatureSelectionSettings:
    """Influence the feature selection step.

    """
    max_features: int = MaxFeatures()
    max_filter_x: int = MaxFilterX()
    max_filter_y: int = MaxFilterY()
    max_model_reduction: bool = MaxModelsReduction()

    def __str__(self):
        return "\n".join([
            "{:<20}: {}".format("Max features", self.max_features),
            "{:<20}: {}".format("Filter X", self.max_filter_x),
            "{:<20}: {}".format("Filter Y", self.max_filter_y),
            "{:<20}: {}".format("Model Reduction", self.max_model_reduction),
            ""
        ])


@dataclass
class ReconstructionSettings:
    """Influence the reconstruction step.

    """
    min_test_accuracy: float = MinTestAccuracy()
    max_test_error_avg: float = MaxTestErrorAvg()
    max_test_error_max: float = MaxTestErrorMax()
    reliability_sample: float = ReliabilitySample()
    min_reliability: float = MinReliability()
    reduce_model_redundancy: bool = ReduceModelRedundancy()
    min_build_models: int = MinBuildModels()

    def __str__(self):
        return "\n".join([
            "{:<20}: {}".format("Min test accuracy", self.min_test_accuracy),
            "{:<20}: {}".format("Max test error avg", self.max_test_error_avg),
            "{:<20}: {}".format("Max test error max", self.max_test_error_max),
            "{:<20}: {}".format("Reliability sample", self.reliability_sample),
            "{:<20}: {}".format("Reliability sample", self.min_reliability),
            "{:<20}: {}".format("Reduce model rudendancy", self.reduce_model_redundancy),
            "{:<20}: {}".format("Min build models", self.min_build_models)
        ])


@dataclass
class DeconstructionSettings:
    """Influence the deconstruction step.

    """
    deconst_strategy: str = DeconstStrategy()
    deconst_mode: str = DeconstMode()
    deconst_max_distance_t: int = DeconstMaxDistanceT()
    deconst_full_tolerance: float = DeconstFullTolerance()
    force_time_expansion: bool = ForceTimeExpansion()
    allow_weak_reliability: bool = AllowWeakReliability()
    learn_block_minimum: int = LearnblockMinimum
    min_reliability: float = MinReliability()

    def __str__(self):
        return "\n".join([
            "{:<20}: {}".format("Deconst strategy", self.deconst_strategy),
            "{:<20}: {}".format("Deconst mode", self.deconst_mode),
            "{:<20}: {}".format("Deconst max distance t", self.deconst_max_distance_t),
            "{:<20}: {}".format("Deconst full tolerance", self.deconst_full_tolerance),
            "{:<20}: {}".format("Force time expansion", self.force_time_expansion),
            "{:<20}: {}".format("Allow weak reliability", self.allow_weak_reliability),
            "{:<20}: {}".format("Learnblock minimum", self.learn_block_minimum),
            "{:<20}: {}".format("Min reliability", self.min_reliability)
        ])

    def as_dict(self):
        return asdict(self)


def specific_settings_factory(settings_type):
    """Factory method for specific settings objects.

    Returns:
         One of the settings objects.

    """
    factory = {
        "general": starmap(
            GeneralSettings, [(Settings.HIGHEST_LEVEL,
                               Settings.KERNEL_BANDWIDTH)]),

        "block_processing": starmap(
            BlockProcessingSettings, [(Settings.LEARN_BLOCK_MINIMUM,
                                       Settings.SIGMA_ZETA_CUTOFF,
                                       Settings.MIN_CATEGORY_SIZE)]),

        "construction": starmap(
            ConstructionSettings, [(Settings.MAX_CATEGORIES,
                                    Settings.MIN_CATEGORY_SIZE,
                                    Settings.MAX_MODEL_TARGETS,
                                    Settings.MAX_TARGET_ERROR)]),

        "feature_selection": starmap(
            FeatureSelectionSettings, [(Settings.MAX_FEATURES,
                                        Settings.MAX_FILTER_X,
                                        Settings.MAX_FILTER_Y,
                                        Settings.MAX_MODELS_REDUCTION)]),

        "reconstruction": starmap(
            ReconstructionSettings, [(Settings.MIN_TEST_ACCURACY,
                                      Settings.MAX_TEST_ERROR_AVG,
                                      Settings.MAX_TEST_ERROR_MAX,
                                      Settings.RELIABILITY_SAMPLE,
                                      Settings.MIN_RELIABILITY,
                                      Settings.REDUCE_MODEL_REDUNDANCY,
                                      Settings.MIN_BUILD_MODELS)]),

        "deconstruction": starmap(
            DeconstructionSettings, [(Settings.DECONST_STRATEGY,
                                      Settings.DECONST_MODE,
                                      Settings.DECONST_MAX_DISTANCE_T,
                                      Settings.DECONST_FULL_TOLERANCE,
                                      Settings.FORCE_TIME_EXPANSION,
                                      Settings.ALLOW_WEAK_RELIABILITY,
                                      Settings.LEARN_BLOCK_MINIMUM,
                                      Settings.MIN_RELIABILITY)])
    }

    return next(factory[settings_type])


def read_settings(path):
    """Read settings from configuration file and assign their values
    to the global Settings object.

    Args:
        path (str): Path to the configuration file.

    raises:
        ConfigurationFileError:
            Settings from the configuration file cannot be read.

    """
    try:
        config = ConfigParser()
        config.read(path)
        configure_main_settings_class(config)

    except AttributeError as e:
        raise ConfigurationFileError(
            "Error during reading the configuration file."
            "Tried read the configuration file."
            "Make sure that all parameters are in the configuration file."
        )


def configure_main_settings_class(config):
    """Assign the values from the configuration file to the global
    Settings object.

    Args:
        config (dict): Read configuration file.

    """
    default = config["GENERAL"]
    Settings.HIGHEST_TIER = default["highest_level"]

    block_processing = config["BLOCK_PROCESSING"]
    Settings.LEARN_BLOCK_MINIMUM = block_processing["learn_block_minimum"]
    Settings.SIGMA_ZETA_CUTOFF = block_processing["sigma_zeta_cutoff"]

    construction = config["CONSTRUCTION"]
    Settings.MAX_TARGET_ERROR = construction["max_target_error"]
    Settings.MAX_MODEL_TARGETS = construction["max_model_targets"]
    Settings.MAX_CATEGORIES = construction["max_categories"]
    Settings.MIN_CATEGORY_SIZE = construction["min_category_size"]

    feature_selection = config["FEATURE_SELECTION"]
    Settings.MAX_FEATURES = feature_selection["max_features"]
    Settings.MAX_FILTER_X = feature_selection["max_filter_x"]
    Settings.MAX_FILTER_Y = feature_selection["max_filter_y"]
    Settings.MAX_MODELS_REDUCTION = feature_selection["max_model_reduction"]

    reconstruction = config["RECONSTRUCTION"]
    Settings.MIN_TEST_ACCURACY = reconstruction["min_test_accuracy"]
    Settings.MAX_TEST_ERROR_AVG = reconstruction["max_test_error_avg"]
    Settings.MAX_TEST_ERROR_MAX = reconstruction["max_test_error_max"]
    Settings.RELIABILITY_SAMPLE = reconstruction["reliability_sample"]
    Settings.MIN_RELIABILITY = reconstruction["min_reliability"]
    Settings.REDUCE_MODEL_REDUNDANCY = reconstruction["reduce_model_redundancy"]
    Settings.MIN_BUILD_MODELS = reconstruction["min_build_models"]

    deconstruction = config["DECONSTRUCTION"]
    Settings.DECONST_STRATEGY = deconstruction["deconst_strategy"]
    Settings.DECONST_MODE = deconstruction["deconst_mode"]
    Settings.DECONST_MAX_DISTANCE_T = deconstruction["deconst_max_distance_t"]
    Settings.DECONST_FULL_TOLERANCE = deconstruction["deconst_full_tolerance"]
    Settings.FORCE_TIME_EXPANSION = deconstruction["force_time_expansion"]
    Settings.ALLOW_WEAK_RELIABILITY = deconstruction["allow_weak_reliability"]
