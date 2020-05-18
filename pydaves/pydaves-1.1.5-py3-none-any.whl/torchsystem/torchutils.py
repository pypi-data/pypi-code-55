import os
import torch
from pydaves.utils import PyConfig
from pydaves.utils import datetime_4_directory_string


def count_maxpool(block):
    dict_block = dict(block.named_children())
    n_maxpool = 0
    for key in dict_block.keys():
        # noinspection PyProtectedMember
        if 'MaxPool' in dict_block[key]._get_name():
            n_maxpool += 1
    return n_maxpool


def init_params(element):
    if type(element) in [torch.nn.Conv2d]:
        # initializing weights with kaiming normal distribution
        torch.nn.init.kaiming_normal_(element.weight)

        # initializing biases with normal distribution
        torch.nn.init.normal_(element.bias)


class TorchConfig(PyConfig):
    def __init__(self, file_path: str):
        # calling superclass __init__ method
        super().__init__(file_path=file_path)

        # pre-allocating experiment_settings
        self.__experiment_settings = None
        self.__classification_flag = None
        self.__reproducibility_flag = None
        self.__random_seed = None
        self.__verbose = None

        # pre-allocating path_settings
        self.__path_settings = None
        self.__main_dir = None
        self.__datetime_dir_name = datetime_4_directory_string()
        self.__version = None

        # pre-allocating logger_settings
        self.__logger_settings = None
        self.__console_only_flag = None
        self.__print_timestamp_flag = None

        # pre-allocating loader_settings
        self.__loader_settings = None
        self.__dataset_name = None

        # pre-allocating model_settings
        self.__model_settings = None
        self.__model_name = None

        # pre-allocating activation_settings
        self.__activation_settings = None
        self.__activation_name = None

        # pre-allocating loss_settings
        self.__loss_settings = None
        self.__loss_name = None

        # pre-allocating optimizer_settings
        self.__optimizer_settings = None
        self.__optimizer_name = None

        # pre-allocating lr_scheduler_settings
        self.__lr_scheduler_settings = None
        self.__lr_scheduler_name = None

        # pre-allocating training_settings
        self.__training_settings = None
        self.__n_epochs = None
        self.__batch_size = None
        self.__save_net_every_epochs = None
        self.__resume_flag = None
        self.__use_gpu_flag = None
        self.__gpu_index = None

        # pre-allocating testing_settings
        self.__testing_settings = None

        # setting default structure
        self.__default = {
            "experiment_settings": {
                "classification_flag": [None, bool],
                "reproducibility_flag": [False, bool],
                "random_seed": [2294, int],
                "verbose": [2, int]
                # TODO: add support to channel_first, channel_last
            },
            "path_settings": {
                "main_dir": [os.getcwd(), str],
                "version": ["MyTorchExperiment", str]
            },
            "logger_settings": {
                "console_only_flag": [False, bool],
                "print_timestamp_flag": [True, bool]
            },
            "loader_settings": {},
            "model_settings": {},
            "activation_settings": {
                "activation_name": [None, str]
            },
            "loss_settings": {
                "loss_name": [None, str]
            },
            "optimizer_settings": {
                "optimizer_name": [None, str]
            },
            "lr_scheduler_settings": {
                "lr_scheduler_name": [None, str]
            },
            "training_settings": {
                "n_epochs": [None, int],
                "batch_size": [None, int],
                "save_net_every_epochs": [None, int],
                "resume_flag": [False, bool],
                "use_gpu_flag": [True, bool],
                "gpu_index": [0, int]
            },
            "testing_settings": {}
        }

        # validating configuration
        self._validate_config()

    def __super_validator(self, attr_name, attr_value, attr_type):
        if isinstance(attr_value, attr_type):
            self.__setattr__(f"_TorchConfig__{attr_name}",
                             attr_value)
        else:
            raise TypeError(f"{attr_name} must be of type {attr_type}, "
                            f"got {type(attr_value)} instead")

    def __ismandatory(self, super_key, key=None):
        if key is None:
            # checking if the current super_key is mandatory
            mandatory_flag = False
            for c_key in self.__default[super_key]:
                if self.__ismandatory(super_key, c_key):
                    mandatory_flag = True
                    break
            return mandatory_flag
        elif self.__default[super_key][key][0] is None:
            # if the current default key is None, then an external defined one
            # is required, so the kay is mandatory
            return True
        else:
            return False

    def _validate_config(self):
        for super_key in self.__default:
            if super_key in self.data:
                for key in self.__default[super_key]:
                    if key in self.data[super_key]:
                        self.__super_validator(
                            attr_name=key,
                            attr_value=self.data[super_key][key],
                            attr_type=self.__default[super_key][key][1]
                        )
                    elif self.__ismandatory(super_key, key):
                        raise ValueError(f"Value {super_key}:{key} not found "
                                         "in the configuration file "
                                         f"{self.file_name}.\n"
                                         "            This value is "
                                         "mandatory, you must define it.")
                    else:
                        self.__super_validator(
                            attr_name=key,
                            attr_value=self.__default[super_key][key][0],
                            attr_type=self.__default[super_key][key][1]
                        )
                self.__setattr__(f"_TorchConfig__{super_key}",
                                 self.data[super_key])
            elif self.__ismandatory(super_key):
                raise ValueError(f"Section {super_key} not found "
                                 "in the configuration file "
                                 f"{self.file_name}.\n"
                                 "            This section is "
                                 "mandatory, you must define it.")
            else:
                self.__setattr__(f"_TorchConfig__{super_key}", {})
                for key in self.__default[super_key]:
                    self.__super_validator(
                        attr_name=key,
                        attr_value=self.__default[super_key][key][0],
                        attr_type=self.__default[super_key][key][1]
                    )

    @property
    def experiment_settings(self):
        return self.__experiment_settings

    @property
    def classification_flag(self):
        return self.__classification_flag

    @property
    def reproducibility_flag(self):
        return self.__reproducibility_flag

    @property
    def random_seed(self):
        return self.__random_seed

    @property
    def verbose(self):
        return self.__verbose

    @property
    def path_settings(self):
        return self.__path_settings

    @property
    def main_dir(self):
        return self.__main_dir

    @property
    def version(self):
        return self.__version

    @property
    def work_dir(self):
        return os.path.join(self.main_dir, self.version)

    @property
    def this_dir(self):
        return os.path.join(self.work_dir, self.__datetime_dir_name)

    @property
    def log_path(self):
        return os.path.join(self.this_dir, "log.bin")

    @property
    def logger_settings(self):
        return self.__logger_settings

    @property
    def console_only_flag(self):
        return self.__console_only_flag

    @property
    def print_timestamp_flag(self):
        return self.__print_timestamp_flag

    @property
    def loader_settings(self):
        return self.__loader_settings

    @property
    def model_settings(self):
        return self.__model_settings

    @property
    def activation_settings(self):
        return self.__activation_settings

    @property
    def activation_name(self):
        return self.__activation_name

    @property
    def loss_settings(self):
        return self.__loss_settings

    @property
    def loss_name(self):
        return self.__loss_name

    @property
    def optimizer_settings(self):
        return self.__optimizer_settings

    @property
    def optimizer_name(self):
        return self.__optimizer_name

    @property
    def lr_scheduler_settings(self):
        return self.__lr_scheduler_settings

    @property
    def lr_scheduler_name(self):
        return self.__lr_scheduler_name

    @property
    def training_settings(self):
        return self.__training_settings

    @property
    def n_epochs(self):
        return self.__n_epochs

    @property
    def batch_size(self):
        return self.__batch_size

    @property
    def save_net_every_epochs(self):
        return self.__save_net_every_epochs

    @property
    def resume_flag(self):
        return self.__resume_flag

    @property
    def use_gpu_flag(self):
        return self.__use_gpu_flag

    @property
    def gpu_index(self):
        return self.__gpu_index

    @property
    def testing_settings(self):
        return self.__testing_settings

    def __repr__(self):
        return f"TorchConfig instance pointing to {self.file_name}"

    def __str__(self):
        return self.__repr__()


class R2Score(object):
    """
        Calculates the R-Squared, the coefficient of determination
        <https://en.wikipedia.org/wiki/Coefficient_of_determination>

        - update method must receive output of the form (y_pred, y_true) or
        {'y_pred': y_pred, 'y_true': y_true}.
        - y and y_pred must be of same shape (N, ) or (N, 1) and of type
    """

    # FIXME: does not work (returns values > 1)

    def __init__(self):
        self._num_examples = 0
        self._sum_of_errors = 0
        self._y_sq_sum = 0
        self._y_sum = 0

    def reset(self):
        self._num_examples = 0
        self._sum_of_errors = 0
        self._y_sq_sum = 0
        self._y_sum = 0

    def update(self, output):
        y_pred, y_true = output
        self._num_examples += y_true.shape[0]
        self._sum_of_errors += torch.sum(torch.pow(y_pred - y_true, 2)).item()

        self._y_sum += torch.sum(y_true).item()
        self._y_sq_sum += torch.sum(torch.pow(y_true, 2)).item()

    def compute(self):
        if self._num_examples == 0:
            raise RuntimeError('R2Score must have at least one example '
                               'before it can be computed.')
        return 1 - self._sum_of_errors / (
                self._y_sq_sum - (self._y_sum ** 2) / self._num_examples)


if __name__ == "__main__":
    config = TorchConfig("config_example.yml")
    print(config)
