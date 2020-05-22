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


PROTOCOL_LEVEL = 55


def value_error_string(name, to):
    """Teample for ValueErrors.

    Args:
        name (str): Parameter name.
        to (str): Target data type.

    Returns:
        str

    """
    return (
        f"Invalid value for {name}. "
        f"Tried to convert string to {to}. "
        f"Make sure that the value is a valid {to} string."
    )


def type_error_string(name, type_):
    """Template for TypeErrors.

    Args:
        name (str): Parameter name.
        type_ (str): Type of the assigned value to the parameter.

    Returns:
        str

    """
    return (
        f"Invalid type for {name}. "
        f"Tried to redefine {name}. "
        f"Make sure that the value is of type {type_} or string."
    )


class HighestLevel:
    """Largest level of the knowledge database.

    """
    def __init__(self):
        self.highest_level = 4

    def __get__(self, instance, owner):
        return self.highest_level

    def __set__(self, instance, value):
        if isinstance(value, int):
            self.highest_level = value
        elif isinstance(value, str):
            try:
                self.highest_level = int(value)
            except ValueError:
                raise ValueError(value_error_string("highest_level", "integer"))
        else:
            raise TypeError(type_error_string("highest_level", "int"))


class KernelBandwidth:
    """Controlls the bandwidth of the kernel used during density estimation.

    """
    def __init__(self):
        self.kernel_bandwidth = 0.2

    def __get__(self, instance, owner):
        return self.kernel_bandwidth

    def __set__(self, instance, value):
        if isinstance(value, float):
            self.kernel_bandwidth = value
        elif isinstance(value, str):
            try:
                self.kernel_bandwidth = float(value)
            except ValueError:
                raise ValueError(
                    value_error_string("kernel_bandwidth", "float")
                )
        else:
            raise TypeError(type_error_string("kernel_bandwidth", "float"))


class LearnblockMinimum:
    """Minimum required number of samples per learning block. If learning
    blocks are identified within a drawn block that contain fewer samples,
    these learning blocks are discarded. This value must always be set, a
    default value is not implemented.

    """
    def __init__(self):
        self.learnblock_minimum = 500

    def __get__(self, instance, owner):
        return self.learnblock_minimum

    def __set__(self, instance, value):
        if isinstance(value, int):
            self.learnblock_minimum = value

        elif isinstance(value, str):
            try:
                self.learnblock_minimum = int(value)
            except ValueError:
                raise ValueError(value_error_string("learnblock_minimum",
                                                    "integer"))
        else:
            raise TypeError(type_error_string("learnblock_minimum", "int"))


class MaxCategories:
    """Maximale kategoriale Komplexität.
    Bestimmt innerhalb der konzeptuellen Wissensdomäne die Anzahl der Cluster,
    die mittels Clustering-Verfahren bestimmt werden. Dieser Wert muss immer
    gesetzt werden, ein Default-Wert ist nicht implementiert.

    """
    MIN_VALUE = 2
    MAX_VALUE = 1000

    def __init__(self):
        self.max_categories = 2

    def __get__(self, instance, owner):
        return self.max_categories

    def __set__(self, instance, value):
        if isinstance(value, int):
            if self.valid_range(value):
                self.max_categories = value

        elif isinstance(value, str):
            try:
                int_value = int(value)
                if self.valid_range(int_value):
                    self.max_categories = int_value
            except ValueError:
                raise ValueError(value_error_string("max_categories",
                                                    "integer"))

        else:
            raise TypeError(type_error_string("max_categories", "int"))

    def valid_range(self, value):
        if not self.MIN_VALUE <= value <= self.MAX_VALUE:
            raise ValueError(
                "Invalid value for max_categories. "
                "Tried to redefine max_categories. "
                "Make sure that the value is greater equal two.")
        return True


class MinCategorySize:
    """Minimum size of a category. Creates the required number within the
    conceptual domain of knowledge samples per cluster. If this is not used
    by all Clustering of a clustering is achieved, the clustering as a whole
    is discarded. Instead of an integer a decimal value between 0 and 1 is
    also given with which the sample number can be calculated from the
    total number of of the samples of the learning block is calculated. This
    value must always be set, a default value is not implemented.

    """
    MIN_VALUE = 0.0
    MAX_VALUE = 1.0

    def __init__(self):
        self.min_category_size = 0.1

    def __get__(self, instance, owner):
        return self.min_category_size

    def __set__(self, instance, value):
        if isinstance(value, float):
            if self.valid_range(value):
                self.min_category_size = value

        elif isinstance(value, str):
            try:
                float_value = float(value)
                if self.valid_range(float_value):
                    self.min_category_size = float(value)
            except ValueError:
                raise ValueError(value_error_string("min_category_size",
                                                    "float"))

        else:
            raise TypeError(type_error_string("min_category_size", "float"))

    def valid_range(self, value):
        if not self.MIN_VALUE <= value <= self.MAX_VALUE:
            raise ValueError("Invalid value for min_category_size. "
                             "Tried to redefine min_category_size. "
                             "Make sure that the value is between 0.0 and 1.0.")
        return True


class SigmaZetaCutoff:
    """Threshold value for the identification of SigmaZ-related Study blocks.
    Determines which density distribution of the Metadata T in a drawn block
    at least must be achieved in order to achieve a one-dimensional clustering.
    Areas that fall below this threshold are not considered.

    """
    MIN_VALUE = 0.0
    MAX_VALUE = 1.0

    def __init__(self):
        self.sigma_zeta_cutoff = 0.1

    def __get__(self, instance, owner):
        return self.sigma_zeta_cutoff

    def __set__(self, instance, value):
        if isinstance(value, float):
            self.sigma_zeta_cutoff = value
        elif isinstance(value, str):
            try:
                self.sigma_zeta_cutoff = float(value)
            except ValueError:
                raise ValueError(value_error_string("sigma_zeta_cutoff",
                                                    "float"))
        else:
            raise TypeError(type_error_string("sigma_zeta_cutoff", "float"))

    def valid_range(self, value):
        if not self.MIN_VALUE <= value <= self.MAX_VALUE:
            raise ValueError("Invalid value for sigma_zeta_cutoff. "
                             "Tried to redefine sigma_zeta_cutoff. "
                             "Make sure that the value is between 0.0 and 1.0.")
        return True


class MaxModelTargets:
    def __init__(self):
        self.max_model_targets = 10

    def __get__(self, instance, owner):
        return self.max_model_targets

    def __set__(self, instance, value):
        if isinstance(value, int):
            self.max_model_targets = value

        elif isinstance(value, str):
            try:
                self.max_model_targets = int(value)
            except Exception as error:
                print(error)


class MaxTargetError:
    def __init__(self):
        self.max_target_error = 0.8

    def __get__(self, instance, owner):
        return self.max_target_error

    def __set__(self, instance, value):
        if isinstance(value, float):
            self.max_target_error = value

        elif isinstance(value, str):
            try:
                self.max_target_error = float(value)
            except TypeError as error:
                print(error)


class MaxFeatures:
    """Maximum allowable model complexity. With this value defines the
    maximum number of input values a model may have. From MaxFeatures+1
    input values a complexity reduction is carried out.

    """
    def __init__(self):
        self.max_features = 5

    def __get__(self, instance, owner):
        return self.max_features

    def __set__(self, instance, value):
        if isinstance(value, int):
            self.max_features = value
        elif isinstance(value, str):
            try:
                self.max_features = int(value)
            except ValueError:
                raise ValueError(value_error_string("max_features",
                                                    "int"))
        else:
            raise TypeError(type_error_string("max_features", "int"))


class MaxFilterX:
    """Filter limit. This value controls when an embedded feature selection
    procedure and when an filter method is used. If a model contains more
    than MaxFilterX input values, a filter method is used; otherwise an embedded
    procedure. This value must always be set, a default value is not implemented

    """
    def __init__(self):
        self.max_filter_x = 10

    def __get__(self, instance, owner):
        return self.max_filter_x

    def __set__(self, instance, value):
        if isinstance(value, int):
            self.max_filter_x = value
        elif isinstance(value, str):
            try:
                self.max_filter_x = int(value)
            except ValueError:
                raise ValueError(value_error_string("max_filter_x",
                                                    "int"))
        else:
            raise TypeError(type_error_string("max_filter_x", "int"))


class MaxFilterY:
    """Filter limit. This value controls when an embedded feature selection
    method and when a filtering method is used. If a model contains more
    as MaxFilterY samples, a filter method is used; otherwise an embedded
    procedure. This value must always be set, a default value is not
    implemented.

    """
    def __init__(self):
        self.max_filter_y = 1000

    def __get__(self, instance, owner):
        return self.max_filter_y

    def __set__(self, instance, value):
        if isinstance(value, int):
            self.max_filter_y = value
        elif isinstance(value, str):
            try:
                self.max_filter_y = int(value)
            except ValueError:
                raise ValueError(value_error_string("max_filter_y",
                                                    "int"))
        else:
            raise TypeError(type_error_string("max_filter_y", "int"))


class MaxModelsReduction:
    """Forcing a maximum reduction of complexity.
    If this value is set to true, complexity reduction steps are performed until
    no more features can be removed. Otherwise the complexity reduction is
    aborted as soon as less than MaxFeatures input variables were achieved.

    """
    def __init__(self):
        self.max_models_reduction = False

    def __get__(self, instance, owner):
        return self.max_models_reduction

    def __set__(self, instance, value):
        if isinstance(value, bool):
            self.max_models_reduction = value
        elif isinstance(value, str):
            if value in ("no", "No", "false", "False"):
                self.max_models_reduction = False
            elif value in ("yes", "Yes", "true", "True"):
                self.max_models_reduction = True
            else:
                raise ValueError(value_error_string("max_models_reduction",
                                                    "bool"))
        else:
            raise TypeError(type_error_string("max_models_reduction", "bool"))


class MinTestAccuracy:
    """Accuracy check threshold. Defines within the conceptual domain of
    knowledge which Accuracy value models for predictions of classifications
    must at least be achieved. Will MinTestAccuracy is not reached, the model
    discarded.

    """
    MIN_VALUE = 0.0
    MAX_VALUE = 1.0

    def __init__(self):
        self.min_test_accuracy = 0.8

    def __get__(self, instance, owner):
        return self.min_test_accuracy

    def __set__(self, instance, value):
        if isinstance(value, float):
            self.min_test_accuracy = value
        elif isinstance(value, str):
            try:
                self.min_test_accuracy = float(value)
            except ValueError:
                raise ValueError(value_error_string("min_test_accuracy",
                                                    "float"))
        else:
            raise TypeError(type_error_string("min_test_accuracy", "float"))

    def valid_range(self, value):
        if not self.MIN_VALUE <= value <= self.MAX_VALUE:
            raise ValueError("Invalid value for min_test_accuracy. "
                             "Tried to redefine min_test_accuracy. "
                             "Make sure that the value is between 0.0 and 1.0.")
        return True


class MaxTestErrorAvg:
    """Threshold value for the average prediction error. Defines the maximum
    average percentage deviation from the target value for regression
    predictions within the procedural knowledge domain. Is MaxTestErrorAvg is
    exceeded, the model discarded.

    """
    def __init__(self):
        self.max_test_error_avg = 10

    def __get__(self, instance, owner):
        return self.max_test_error_avg

    def __set__(self, instance, value):
        if isinstance(value, float):
            self.max_test_error_avg = value
        elif isinstance(value, str):
            try:
                self.max_test_error_avg = float(value)
            except TypeError as error:
                print(error)


class MaxTestErrorMax:
    """Threshold value for the maximum prediction error.
    Defines within the procedural knowledge domain, the maximum percentage
    deviation from the target value for regression predictions that may be
    achieved. If MaxTestErrorAvg is exceeded, the model is discarded.

    """
    def __init__(self):
        self.max_test_error_max = 10

    def __get__(self, instance, owner):
        return self.max_test_error_max

    def __set__(self, instance, value):
        if isinstance(value, float):
            self.max_test_error_max = value
        elif isinstance(value, str):
            try:
                self.max_test_error_max = float(value)
            except TypeError as error:
                print(error)


class MinBuildModels:
    """Minum of successful trained supervised machine learning models to
    continue the reconstruction process.

    """
    MIN_VALUE = 2

    def __init__(self):
        self.min_build_models = self.MIN_VALUE

    def __get__(self, instance, owner):
        return self.min_build_models

    def __set__(self, instance, value):
        if isinstance(value, int):
            self.min_build_models = value
        elif isinstance(value, str):
            try:
                self.min_build_models = int(value)
            except ValueError:
                raise ValueError(value_error_string("min_build_models",
                                                    "int"))
        else:
            raise TypeError(type_error_string("min_build_models", "int"))


class ReliabilitySample:
    """Sample size for reliability testing. Determines the Proportion of
    samples used to determine the reliability coefficient of a model. The
    specified value must be between 0 and 1.

    """
    MIN_VALUE = 0.0
    MAX_VALUE = 1.0

    def __init__(self):
        self.reliability_sample = 0.2

    def __get__(self, instance, owner):
        return self.reliability_sample

    def __set__(self, instance, value):
        if isinstance(value, float):
            self.reliability_sample = value
        elif isinstance(value, str):
            try:
                self.reliability_sample = float(value)
            except ValueError:
                raise ValueError(value_error_string("reliability_sample",
                                                    "float"))
        else:
            raise TypeError(type_error_string("reliability_sample", "float"))

    def valid_range(self, value):
        if not self.MIN_VALUE <= value <= self.MAX_VALUE:
            raise ValueError("Invalid value for reliability_sample. "
                             "Tried to redefine reliability_sample. "
                             "Make sure that the value is between 0.0 and 1.0.")
        return True


class MinReliability:
    """Threshold value for reliability testing. Determines from which value
    of the interreliability coefficient a agreement is assumed.

    """
    MIN_VALUE = 0.0
    MAX_VALUE = 1.0

    def __init__(self):
        self.min_reliability = 0.1

    def __get__(self, instance, owner):
        return self.min_reliability

    def __set__(self, instance, value):
        if isinstance(value, float):
            self.min_reliability = value
        elif isinstance(value, str):
            try:
                self.min_reliability = float(value)
            except ValueError:
                raise ValueError(value_error_string("min_reliability",
                                                    "float"))
        else:
            raise TypeError(type_error_string("min_reliability", "float"))

    def valid_range(self, value):
        if not self.MIN_VALUE <= value <= self.MAX_VALUE:
            raise ValueError("Invalid value for reliability_sample. "
                             "Tried to redefine reliability_sample. "
                             "Make sure that the value is between 0.0 and 1.0.")
        return True


class ReduceModelRedundancy:
    def __init__(self):
        self.reduce_model_redundancy = False

    def __get__(self, instance, owner):
        return self.reduce_model_redundancy

    def __set__(self, instance, value):
        if isinstance(value, bool):
            self.reduce_model_redundancy = value

        elif isinstance(value, str):
            if value in ("False", "no", "false"):
                self.reduce_model_redundancy = False
            elif value in ("True", "yes", "true"):
                self.reduce_model_redundancy = True
            else:
                raise ValueError(value_error_string("reduce_model_redundancy",
                                                    "bool"))
        else:
            raise TypeError(type_error_string("reduce_model_redundancy",
                                              "bool"))


class DeconstStrategy:
    """Dealing with new models. Determines whether new successfully
    deconstructed models are included in the knowledge domain.

    """
    def __init__(self):
        self.deconst_strategy = "conservative"

    def __get__(self, instance, owner):
        return self.deconst_strategy

    def __set__(self, instance, value):
        if value in ("conservative", "integrative", "oppurtunistic"):
            self.deconst_strategy = value
        else:
            raise ValueError(
                f"Invalid value for deconst_strategy. "
                f"Tried to redefine deconst_strategy. "
                f"Make sure that the value is either 'conservative', "
                f"'integrative', 'oppurtunistic'."
            )


class DeconstMode:
    """Termination condition. The deconstruction process is either aborted
    as soon as a complete, a SigmaZ, a TZ or a TSigma deconstruction was
    successful (minimal) or only when no more pragmatically related models
    can be identified (full).

    """
    def __init__(self):
        self.deconst_mode = "minimal"

    def __get__(self, instance, owner):
        return self.deconst_mode

    def __set__(self, instance, value):
        if value in ("minimal", "full"):
            self.deconst_mode = value
        else:
            raise ValueError(
                f"Invalid valid for deconst_mode. " 
                f"Tried to redefine deconst_mode. "
                f"Make sure that the value is either 'full' or 'minimal'."
            )


class DeconstMaxDistanceT:
    """Temporal expansion tolerance. Defines the maximum size of the temporal
    gap between SigmaZ-related models for expansion to be tested. If this value
    is set to 1, the check is always performed. If it is set to 0, the check
    only checks if there is an overlap. Otherwise, the temporal gap must not
    exceed the size of the part of the total span defined by the set value.

    """
    MIN_VALUE = 0.0
    MAX_VALUE = 1.0

    def __init__(self):
        self.deconst_max_distance_t = 0.1

    def __get__(self, instance, owner):
        return self.deconst_max_distance_t

    def __set__(self, instance, value):
        if isinstance(value, float):
            self.deconst_max_distance_t = value

        elif isinstance(value, str):
            try:
                self.deconst_max_distance_t = float(value)
            except ValueError:
                raise ValueError(value_error_string("deconst_max_distance_t",
                                                    "float"))

        else:
            raise TypeError(type_error_string("deconst_max_distance_t",
                                              "float"))

    def valid_range(self, value):
        if not self.MIN_VALUE <= value <= self.MAX_VALUE:
            raise ValueError("Invalid value for deconst_max_distance_t. "
                             "Tried to redefine deconst_max_distance_t. "
                             "Make sure that the value is between 0.0 and 1.0.")
        return True


class DeconstFullTolerance:
    """Temporal tolerance with complete kinship. Defines the proportion by
    which the time interval T can be extended to constitute a relationship.

    """
    MIN_VALUE = 0.0
    MAX_VALUE = 1.0

    def __init__(self):
        self.deconst_full_tolerance = 0.1

    def __get__(self, instance, owner):
        return self.deconst_full_tolerance

    def __set__(self, instance, value):
        if isinstance(value, float):
            self.deconst_full_tolerance = value

        elif isinstance(value, str):
            try:
                self.deconst_full_tolerance = float(value)

            except ValueError:
                raise ValueError(value_error_string("deconst_full_tolerance",
                                                    "float"))

        else:
            raise TypeError(type_error_string("deconst_full_tolerance",
                                              "float"))

    def valid_range(self, value):
        if not self.MIN_VALUE <= value <= self.MAX_VALUE:
            raise ValueError("Invalid value for deconst_full_tolerance. "
                             "Tried to redefine deconst_full_tolerance. "
                             "Make sure that the value is between 0.0 and 1.0.")
        return True


class ForceTimeExpansion:
    """Association of SigmaZ-related models. If True, SigmaZ-related models
    are treated preferentially or unified.

    """
    def __init__(self):
        self.force_time_expansion = True

    def __get__(self, instance, owner):
        return self.force_time_expansion

    def __set__(self, instance, value):
        if isinstance(value, bool):
            self.force_time_expansion = value

        elif isinstance(value, str):
            if value in ("False", "no"):
                self.force_time_expansion = False
            elif value in ("True", "yes"):
                self.force_time_expansion = True
            else:
                raise ValueError(value_error_string("force_time_expansion",
                                                    "bool"))
        else:
            raise TypeError("Invalid value for force_time_expansion. "
                            "Tried to redefine force_time_expansion. "
                            "Make sure that the value is a bool.")


class AllowWeakReliability:
    def __init__(self):
        self.allow_weak_reliability = False

    def __get__(self, instance, owner):
        return self.allow_weak_reliability

    def __set__(self, instance, value):
        if isinstance(value, bool):
            self.allow_weak_reliability = value

        elif isinstance(value, str):
            if value in ("False", "no"):
                self.allow_weak_reliability = False
            elif value in ("True", "yes"):
                self.allow_weak_reliability = True
            else:
                raise ValueError(value_error_string("allow_weak_reliability",
                                                    "bool"))

        else:
            raise TypeError("Invalid value for the allow_weak_reliability. ",
                            "Tried to redefine allow_weak_reliability. "
                            "Make sure that the value is a bool.")
