import os
import torch
import torchnet
import traceback
import numpy as np
from pydaves.utils import PyLogger
from pydaves.utils import touch_dir
from pydaves.torchsystem.torchutils import R2Score
from pydaves.torchsystem.torchutils import TorchConfig
from torch.utils.data.dataloader import DataLoader


class TorchExperiment(object):
    def __init__(self,
                 config: TorchConfig,
                 loader_fun, model_class,
                 loader_args=(), model_args=()):
        # validating inputs
        self.__config, \
        self.__loader_fun, self.__model_class, \
        self.__loader_args, self.__model_args = \
            self._validate_inputs(
                config,
                loader_fun, model_class,
                loader_args, model_args
            )

        # managing reproducibility
        if self.reproducibility_flag:
            # torch.manual_seed(self.random_seed)
            # np.random.seed(self.random_seed)
            # FIXME: modifying random_seed means weird results in training
            pass

        # managing paths
        touch_dir(self.work_dir)
        touch_dir(self.this_dir)

        # creating a logger instance
        self.__logger = PyLogger(
            log_path=self.log_path,
            console_only_flag=self.console_only_flag,
            print_timestamp_flag=self.print_timestamp_flag
        )

        # creating a device instance
        self.__device = self._validate_gpu()

        # creating loaders
        if self.classification_flag:
            self.__train_loader, self.__valid_loader, self.__test_loader, \
            self.__input_shape, self.__classes = self.loader_fun(
                self, *loader_args)
        else:
            self.__train_loader, self.__valid_loader, self.__test_loader, \
            self.__input_shape = self.loader_fun(
                self, *loader_args)
            self.__classes = ()

        # creating activation and loss
        self.__activation = self._get_torch_activation()
        self.__loss = self._get_torch_loss()

        # creating a model instance
        self._model = self.model_class(
            self, *model_args)

        # creating optimizer and lr_scheduler
        self.__optimizer = self._get_torch_optimizer()
        self.__lr_scheduler = self._get_torch_lr_scheduler()

        # creating a trainer instance
        self.__trainer = _TorchTrainer(experiment=self)

    @staticmethod
    def _validate_inputs(config: TorchConfig,
                         loader_fun, model_class,
                         loader_args: tuple, model_args: tuple):
        if not isinstance(config, TorchConfig):
            raise TypeError("Input 'config' must be of type 'TorchConfig', "
                            f"got {type(config)} instead.")
        if not callable(loader_fun):
            raise TypeError("Input 'loader_fun' must be callable.")
        if not callable(model_class):
            raise TypeError("Input 'model_class' must be callable.")
        if not isinstance(loader_args, tuple):
            raise TypeError("Input 'loader_args' must be of type 'tuple', "
                            f"got {type(loader_args)} instead.")
        if not isinstance(model_args, tuple):
            raise TypeError("Input 'model_args' must be of type 'tuple', "
                            f"got {type(model_args)} instead.")
        return config, loader_fun, model_class, loader_args, model_args

    def _validate_gpu(self):
        # checking if the selected gpu is available
        if self.use_gpu_flag:
            if torch.cuda.is_available():
                if self.gpu_index < torch.cuda.device_count():
                    # enabling the chosen gpu
                    os.environ["CUDA_VISIBLE_DEVICES"] = str(self.gpu_index)

                    # creating a torch.device instance for the chosen gpu
                    device = torch.device(f"cuda:{self.gpu_index}")
                else:
                    raise ValueError(f"Invalid gpu index ({self.gpu_index}).")
            else:
                raise ValueError("CUDA not available.")
        else:
            # creating device for cpu
            device = torch.device("cpu")
        return device

    def _get_torch_activation(self):
        # getting activation_name
        activation_name = self.activation_name.lower()

        # selecting activation
        # TODO: add here a routine for each Torch activation
        if activation_name == "tanh":
            return torch.nn.Tanh()
        elif activation_name == "elu":
            if "alpha" not in self.activation_settings:
                self.set(
                    keys=("activation_settings", "alpha"),
                    value=1.0
                )
            if "inplace" not in self.activation_settings:
                self.set(
                    keys=("activation_settings", "inplace"),
                    value=False
                )
            return torch.nn.ELU(
                alpha=self.activation_settings["alpha"],
                inplace=self.activation_settings["inplace"]
            )
        else:
            raise ValueError(f"Unrecognized activation_name "
                             f"{self.activation_name}.")

    def _get_torch_loss(self):
        # getting loss_name
        loss_name = self.loss_name.lower()

        # selecting loss
        # TODO: add here a routine for each Torch loss
        if loss_name == "crossentropyloss":
            if "ignore_index" not in self.loss_settings:
                self.set(
                    keys=("loss_settings", "ignore_index"),
                    value=-100
                )
            if "reduction" not in self.loss_settings:
                self.set(
                    keys=("loss_settings", "reduction"),
                    value="mean"
                )
            return torch.nn.CrossEntropyLoss(
                ignore_index=self.loss_settings["ignore_index"],
                reduction=self.loss_settings["reduction"]
            )
        elif loss_name == "mseloss":
            if "reduction" not in self.loss_settings:
                self.set(
                    keys=("loss_settings", "reduction"),
                    value="mean"
                )
            return torch.nn.MSELoss(
                reduction=self.loss_settings["reduction"]
            )
        else:
            raise ValueError(f"Unrecognized loss_name "
                             f"{self.loss_name}.")

    # noinspection DuplicatedCode
    def _get_torch_optimizer(self):
        # getting optimizer_name
        optimizer_name = self.optimizer_name.lower()

        # selecting optimizer
        # TODO: add here a routine for each Torch optimizer
        if optimizer_name == "adam":
            if "lr" not in self.optimizer_settings:
                self.set(
                    keys=("optimizer_settings", "lr"),
                    value=0.001
                )
            if "betas" not in self.optimizer_settings:
                self.set(
                    keys=("optimizer_settings", "betas"),
                    value=(0.9, 0.999)
                )
            if "eps" not in self.optimizer_settings:
                self.set(
                    keys=("optimizer_settings", "eps"),
                    value=1e-08
                )
            if "weight_decay" not in self.optimizer_settings:
                self.set(
                    keys=("optimizer_settings", "weight_decay"),
                    value=0
                )
            if "amsgrad" not in self.optimizer_settings:
                self.set(
                    keys=("optimizer_settings", "amsgrad"),
                    value=False
                )
            return torch.optim.Adam(
                params=self.model.parameters(),
                lr=self.optimizer_settings["lr"],
                betas=self.optimizer_settings["betas"],
                eps=self.optimizer_settings["eps"],
                weight_decay=self.optimizer_settings["weight_decay"],
                amsgrad=self.optimizer_settings["amsgrad"]
            )
        elif optimizer_name == "adamax":
            if "lr" not in self.optimizer_settings:
                self.set(
                    keys=("optimizer_settings", "lr"),
                    value=0.002
                )
            if "betas" not in self.optimizer_settings:
                self.set(
                    keys=("optimizer_settings", "betas"),
                    value=(0.9, 0.999)
                )
            if "eps" not in self.optimizer_settings:
                self.set(
                    keys=("optimizer_settings", "eps"),
                    value=1e-08
                )
            if "weight_decay" not in self.optimizer_settings:
                self.set(
                    keys=("optimizer_settings", "weight_decay"),
                    value=0
                )
            # noinspection PyUnresolvedReferences
            return torch.optim.Adamax(
                params=self.model.parameters(),
                lr=self.optimizer_settings["lr"],
                betas=self.optimizer_settings["betas"],
                eps=self.optimizer_settings["eps"],
                weight_decay=self.optimizer_settings["weight_decay"],
            )
        elif optimizer_name == "sgd":
            if "lr" not in self.optimizer_settings:
                self.set(
                    keys=("optimizer_settings", "lr"),
                    value=0.01
                )
            if "momentum" not in self.optimizer_settings:
                self.set(
                    keys=("optimizer_settings", "momentum"),
                    value=0
                )
            if "dampening" not in self.optimizer_settings:
                self.set(
                    keys=("optimizer_settings", "dampening"),
                    value=0
                )
            if "weight_decay" not in self.optimizer_settings:
                self.set(
                    keys=("optimizer_settings", "weight_decay"),
                    value=0
                )
            if "nesterov" not in self.optimizer_settings:
                self.set(
                    keys=("optimizer_settings", "nesterov"),
                    value=False
                )
            return torch.optim.SGD(
                params=self.model.parameters(),
                lr=self.optimizer_settings["lr"],
                momentum=self.optimizer_settings["momentum"],
                dampening=self.optimizer_settings["dampening"],
                weight_decay=self.optimizer_settings["weight_decay"],
                nesterov=self.optimizer_settings["nesterov"]
            )
        else:
            raise ValueError(f"Unrecognized optimizer_name "
                             f"{self.optimizer_name}.")

    def _get_torch_lr_scheduler(self):
        # getting lr_scheduler_name
        lr_scheduler_name = self.lr_scheduler_name.lower()

        # selecting lr_scheduler
        # TODO: add here a routine for each Torch lr_scheduler
        # noinspection SpellCheckingInspection
        if lr_scheduler_name == "reducelronplateau":
            if "mode" not in self.lr_scheduler_settings:
                self.set(
                    keys=("lr_scheduler_settings", "mode"),
                    value="min"
                )
            if "factor" not in self.lr_scheduler_settings:
                self.set(
                    keys=("lr_scheduler_settings", "factor"),
                    value=0.1
                )
            if "patience" not in self.lr_scheduler_settings:
                self.set(
                    keys=("lr_scheduler_settings", "patience"),
                    value=10
                )
            if "verbose" not in self.lr_scheduler_settings:
                self.set(
                    keys=("lr_scheduler_settings", "verbose"),
                    value=False
                )
            if "threshold" not in self.lr_scheduler_settings:
                self.set(
                    keys=("lr_scheduler_settings", "threshold"),
                    value=1e-4
                )
            if "threshold_mode" not in self.lr_scheduler_settings:
                self.set(
                    keys=("lr_scheduler_settings", "threshold_mode"),
                    value="rel"
                )
            if "cooldown" not in self.lr_scheduler_settings:
                self.set(
                    keys=("lr_scheduler_settings", "cooldown"),
                    value=0
                )
            if "min_lr" not in self.lr_scheduler_settings:
                self.set(
                    keys=("lr_scheduler_settings", "min_lr"),
                    value=0
                )
            if "eps" not in self.lr_scheduler_settings:
                self.set(
                    keys=("lr_scheduler_settings", "eps"),
                    value=1e-8
                )
            return torch.optim.lr_scheduler.ReduceLROnPlateau(
                optimizer=self.optimizer,
                mode=self.lr_scheduler_settings["mode"],
                factor=self.lr_scheduler_settings["factor"],
                patience=self.lr_scheduler_settings["patience"],
                verbose=self.lr_scheduler_settings["verbose"],
                threshold=self.lr_scheduler_settings["threshold"],
                threshold_mode=self.lr_scheduler_settings["threshold_mode"],
                cooldown=self.lr_scheduler_settings["cooldown"],
                min_lr=self.lr_scheduler_settings["min_lr"],
                eps=self.lr_scheduler_settings["eps"]
            )
        else:
            raise ValueError(
                "<< {} >> lr_scheduler is not a valid one.".format(
                    self.lr_scheduler))

    @property
    def config(self) -> TorchConfig:
        return self.__config

    @property
    def loader_fun(self):
        return self.__loader_fun

    @property
    def model_class(self):
        return self.__model_class

    @property
    def loader_args(self) -> tuple:
        return self.__loader_args

    @property
    def model_args(self) -> tuple:
        return self.__model_args

    @property
    def logger(self) -> PyLogger:
        return self.__logger

    @property
    def device(self) -> torch.device:
        return self.__device

    @property
    def train_loader(self) -> DataLoader:
        return self.__train_loader

    @property
    def valid_loader(self) -> DataLoader:
        return self.__valid_loader

    @property
    def test_loader(self) -> DataLoader:
        return self.__test_loader

    # noinspection PyUnresolvedReferences
    @property
    def n_batches_train(self) -> int:
        return len(self.train_loader)

    @property
    def n_batches_valid(self) -> int:
        if self.valid_loader is None:
            return 0
        else:
            return len(self.valid_loader)

    @property
    def n_batches_test(self) -> int:
        return len(self.test_loader)

    @property
    def input_shape(self) -> tuple:
        return self.__input_shape

    @property
    def input_height(self) -> int:
        return self.input_shape[0]

    @property
    def input_width(self) -> int:
        return self.input_shape[1]

    @property
    def input_depth(self) -> int:
        return self.input_shape[2]

    @property
    def input_n_rows(self) -> int:
        return self.input_shape[0]

    @property
    def input_n_cols(self) -> int:
        return self.input_shape[1]

    @property
    def input_n_channels(self) -> int:
        return self.input_shape[2]

    @property
    def classes(self) -> tuple:
        return self.__classes

    @property
    def n_classes(self) -> int:
        return len(self.classes)

    @property
    def model(self):
        return self._model

    @property
    def model_name(self) -> str:
        return type(self.model).__name__

    @property
    def activation(self):
        return self.__activation

    @property
    def loss(self):
        return self.__loss

    @property
    def optimizer(self):
        return self.__optimizer

    @property
    def lr_scheduler(self):
        return self.__lr_scheduler

    @property
    def trainer(self):
        return self.__trainer

    @property
    def experiment_settings(self) -> dict:
        return self.__config.experiment_settings

    @property
    def classification_flag(self) -> bool:
        return self.__config.classification_flag

    @property
    def reproducibility_flag(self) -> bool:
        return self.__config.reproducibility_flag

    @property
    def random_seed(self) -> int:
        return self.__config.random_seed

    @property
    def verbose(self) -> int:
        return self.__config.verbose

    @property
    def path_settings(self) -> dict:
        return self.__config.path_settings

    @property
    def main_dir(self) -> str:
        return self.__config.main_dir

    @property
    def version(self) -> str:
        return self.__config.version

    @property
    def work_dir(self) -> str:
        return self.__config.work_dir

    @property
    def this_dir(self) -> str:
        return self.__config.this_dir

    @property
    def log_path(self) -> str:
        return self.__config.log_path

    @property
    def logger_settings(self) -> dict:
        return self.__config.logger_settings

    @property
    def console_only_flag(self) -> bool:
        return self.__config.console_only_flag

    @property
    def print_timestamp_flag(self) -> bool:
        return self.__config.print_timestamp_flag

    @property
    def loader_settings(self) -> dict:
        return self.__config.loader_settings

    @property
    def model_settings(self):
        return self.__config.model_settings

    @property
    def activation_settings(self):
        return self.__config.activation_settings

    @property
    def activation_name(self) -> str:
        return self.__config.activation_name

    @property
    def loss_settings(self) -> dict:
        return self.__config.loss_settings

    @property
    def loss_name(self) -> str:
        return self.__config.loss_name

    @property
    def optimizer_settings(self) -> dict:
        return self.__config.optimizer_settings

    @property
    def optimizer_name(self) -> str:
        return self.__config.optimizer_name

    @property
    def lr_scheduler_settings(self) -> dict:
        return self.__config.lr_scheduler_settings

    @property
    def lr_scheduler_name(self) -> str:
        return self.__config.lr_scheduler_name

    @property
    def training_settings(self) -> dict:
        return self.__config.training_settings

    @property
    def n_epochs(self) -> int:
        return self.__config.n_epochs

    @property
    def batch_size(self) -> int:
        return self.__config.batch_size

    @property
    def save_net_every_epochs(self) -> int:
        return self.__config.save_net_every_epochs

    @property
    def resume_flag(self) -> bool:
        return self.__config.resume_flag

    @property
    def use_gpu_flag(self) -> bool:
        return self.__config.use_gpu_flag

    @property
    def gpu_index(self) -> int:
        return self.__config.gpu_index

    @property
    def testing_settings(self) -> dict:
        return self.__config.testing_settings

    # noinspection PyProtectedMember
    def set(self, keys, value):
        if not isinstance(keys, tuple):
            raise TypeError("Input 'keys' must be of type 'tuple', "
                            f"got {type(keys)} instead.")
        elif len(keys) != 2:
            raise ValueError("Lenght of input 'keys' must be 2.")

        # checking the super_key existance
        if keys[0] not in self.config.data:
            self.config._data[keys[0]] = {}

        # assigning the key value
        self.config._data[keys[0]][keys[1]] = value

        # running again _validating_config routine
        self.config._validate_config()

    def print_summary(self):
        # summary preamble
        self.logger.print("EXPERIMENT SETTINGS:", style="d")

        # getting properties list
        prop_list = dir(self)

        # removing some properties from the list
        prop_list.remove("print_summary")
        prop_list.remove("run")
        prop_list.remove("set")

        for current_prop in prop_list:
            if current_prop[0] is not "_":
                self.logger.print("{} = {}".format(
                    current_prop, getattr(self, current_prop)),
                    timestamp_flag=False)

    def run(self):
        # the following try clause contains all the algorithm
        # noinspection PyBroadException
        try:
            if self.verbose >= 1:
                # noinspection SpellCheckingInspection
                self.logger.print(
                    "TORCHEXPERIMENT STARTED",
                    style="ud",
                    timestamp_flag=False
                )

            if self.verbose >= 2:
                self.print_summary()

            # sending model to the right device
            self.model.to(self.device)

            # training
            self.trainer.train()

            # test
            self.trainer.test()
        except Exception:
            self.logger.print(traceback.format_exc())

        # stopping the logger object
        self.logger.stop()

    def __repr__(self):
        return f"TorchExperiment to train {self.model_name}"

    def plot(self):
        import matplotlib as mpl
        from matplotlib import pyplot as plt
        from pydaves.utils import set_fontsize
        x = np.arange(start=1, stop=self.n_epochs + 1).astype(int)

        # LOSS
        # figure and ax
        fig1 = plt.figure(figsize=(12.8, 7.2))
        ax1 = fig1.add_subplot()
        # plot
        ax1.plot(
            x, self.trainer.train_results["loss_list"],
            color="red", linewidth=5, label="train"
        )
        if self.n_batches_valid > 0:
            ax1.plot(
                x, self.trainer.valid_results["loss_list"],
                color="blue", linewidth=5, label="valid"
            )
        # ylabel
        ax1.set_ylabel("Loss")
        # xlabel
        ax1.set_xlabel("Epochs")
        # noinspection PyUnresolvedReferences
        ax1.get_xaxis().set_major_locator(
            mpl.ticker.MaxNLocator(integer=True)
        )
        # legend
        ax1.legend(fontsize=20)
        # fontsize
        set_fontsize(ax1, fontsize=20)
        # grid
        ax1.grid()
        # show
        fig1.show()

        # ACC or R2
        # figure and ax
        fig2 = plt.figure(figsize=(12.8, 7.2))
        ax2 = fig2.add_subplot()
        if self.classification_flag:
            # plot
            ax2.plot(
                x, self.trainer.train_results["acc_list"],
                color="red", linewidth=5, label="train"
            )
            if self.n_batches_valid > 0:
                ax2.plot(
                    x, self.trainer.valid_results["acc_list"],
                    color="blue", linewidth=5, label="valid"
                )
            # y_label
            ax2.set_ylabel("Accuracy")
        else:
            # plot
            ax2.plot(
                x, self.trainer.train_results["r2_list"],
                color="red", linewidth=5, label="train"
            )
            if self.n_batches_valid > 0:
                ax2.plot(
                    x, self.trainer.valid_results["r2_list"],
                    color="blue", linewidth=5, label="valid"
                )
            # y_label
            ax2.set_ylabel("R2 Score")
        # xlabel
        ax2.set_xlabel("Epochs")
        # noinspection PyUnresolvedReferences
        ax2.get_xaxis().set_major_locator(
            mpl.ticker.MaxNLocator(integer=True)
        )
        # legend
        ax2.legend(fontsize=20)
        # fontsize
        set_fontsize(ax2, fontsize=20)
        # grid
        ax2.grid()
        # show
        fig2.show()


class _TorchTrainer(object):
    """
    Private Class, only TorchExperiment can use it.
    """

    def __init__(self, experiment: TorchExperiment):
        # assigning experiment
        self.experiment = experiment

        # pre-allocating result values
        if self.experiment.classification_flag:
            self.train_results = {
                "loss_list": [],
                "acc_list": [],
                "cm_list": [],
                "last_loss": float("inf"),
                "last_acc": 0.,
                "best_loss": float("inf"),
                "best_acc": 0.,
                "best_epoch_for_loss": 0,
                "best_epoch_for_acc": 0
            }
            self.valid_results = {
                "loss_list": [],
                "acc_list": [],
                "cm_list": [],
                "lr_list": [],
                "last_loss": float("inf"),
                "last_acc": 0.,
                "best_loss": float("inf"),
                "best_acc": 0.,
                "best_epoch_for_loss": 0,
                "best_epoch_for_acc": 0
            }
            self.test_results = {
                "loss": None,
                "acc": None,
                "cm": None
            }
        else:
            self.train_results = {
                "loss_list": [],
                "r2_list": [],
                "last_loss": float("inf"),
                "last_r2": 0.,
                "best_loss": float("inf"),
                "best_r2": 0.,
                "best_epoch_for_loss": 0,
                "best_epoch_for_r2": 0
            }
            self.valid_results = {
                "loss_list": [],
                "r2_list": [],
                "lr_list": [],
                "last_loss": float("inf"),
                "last_r2": 0.,
                "best_loss": float("inf"),
                "best_r2": 0.,
                "best_epoch_for_loss": 0,
                "best_epoch_for_r2": 0
            }
            self.test_results = {
                "loss": None,
                "r2": None
            }

    def __repr__(self):
        return f"TorchTrainer instance to train {self.experiment.model_name}"

    def __str__(self):
        return self.__repr__()

    def _init_training(self):
        self.__init__(self.experiment)

    def run(self):
        self.train()
        self.test()

    def train(self):
        # initializing training
        self._init_training()

        # main loop
        for epoch in range(self.experiment.n_epochs):
            # printing this epoch
            self.experiment.logger.print(
                'EPOCH {}/{}'.format(epoch + 1, self.experiment.n_epochs),
                style="ud", up_extra_lines=1)

            # running training
            self._loop(mode=0)

            if self.experiment.n_batches_valid > 0:
                # running validation
                self._loop(mode=1)

            # saving last values if best training loss
            if self.train_results["last_loss"] >= \
                    self.train_results["best_loss"]:
                self.train_results["best_loss"] = \
                    self.train_results["last_loss"]
                self.train_results["best_epoch_for_loss"] = epoch

            if self.experiment.classification_flag:
                # saving last values if best training acc
                if self.train_results["last_acc"] >= \
                        self.train_results["best_acc"]:
                    self.train_results["best_acc"] = \
                        self.train_results["last_acc"]
                    self.train_results["best_epoch_for_acc"] = epoch
            else:
                # saving last values if best training r2
                if self.train_results["last_r2"] >= \
                        self.train_results["best_r2"]:
                    self.train_results["best_r2"] = \
                        self.train_results["last_r2"]
                    self.train_results["best_epoch_for_r2"] = epoch

            # saving last net
            torch.save(
                self.experiment.model.state_dict(),
                os.path.join(self.experiment.this_dir,
                             'Net_last_update.pt')
            )

            # saving net if the epoch x has come
            if (epoch + 1) % self.experiment.save_net_every_epochs == 0:
                torch.save(
                    self.experiment.model.state_dict(),
                    os.path.join(self.experiment.this_dir,
                                 f"Net_at_epoch_{epoch + 1}.pt")
                )

            # saving last net and values if best validation loss
            if self.valid_results["last_loss"] <= \
                    self.valid_results["best_loss"]:
                torch.save(
                    self.experiment.model.state_dict(),
                    os.path.join(self.experiment.this_dir,
                                 'Net_best_loss.pt')
                )
                self.valid_results["best_loss"] = \
                    self.valid_results["last_loss"]
                self.valid_results["best_epoch_for_loss"] = epoch

            if self.experiment.classification_flag:
                # saving last net and values if best validation acc
                if self.valid_results["last_acc"] >= \
                        self.valid_results["best_acc"]:
                    torch.save(
                        self.experiment.model.state_dict(),
                        os.path.join(self.experiment.this_dir,
                                     'Net_best_acc.pt')
                    )
                    self.valid_results["best_acc"] = \
                        self.valid_results["last_acc"]
                    self.valid_results["best_epoch_for_acc"] = epoch
            else:
                # saving last net and values if best validation r2
                if abs(1 - self.valid_results["last_r2"]) <= \
                        abs(1 - self.valid_results["best_r2"]):
                    torch.save(
                        self.experiment.model.state_dict(),
                        os.path.join(self.experiment.this_dir,
                                     'Net_best_r2.pt')
                    )
                    self.valid_results["best_r2"] = \
                        self.valid_results["last_r2"]
                    self.valid_results["best_epoch_for_r2"] = epoch

            # TODO: print a summary for this epoch

            # TODO: print if a new best net was found

            # TODO: saving routine for plots

            # saving plot
            # self.save_loss_fig(losses_train, 'loss_val',
            # losses_val=losses_val)
            # self.save_loss_fig(accs_train, 'acc_val', losses_val=accs_val)
            # self.save_loss_fig(lr_epoch, 'learning_rate')

            # self.experiment.logger("")
            # print('== TRAIN ==')
            # print('LOSS: {:.4f}'.format(loss_tr))
            # print('ACC:  {:.4f}'.format(acc_tr))
            # print('CM: \n%s' % cm_tr)
            # print('== VALIDATION ==')
            # print('LOSS: {:.4f}'.format(loss_val))
            # print('ACC:  {:.4f}'.format(acc_val))
            # print('CM: \n%s' % cm_val)
            # print(f'Epoch best loss: {epoch_best}')
            # print(f'Epoch best acc:  {epoch_best_acc}')
            # print('\n')

    # noinspection PyArgumentList
    def _loop(self, mode):
        """
        Private method _loop
        :param mode: 0 for train, 1 for valid, 2 for test
        :return:
        """

        # switch mode
        if mode == 0:  # training
            if self.experiment.verbose > 0:
                self.experiment.logger.print(
                    "TRAINING", style="ud", up_extra_lines=1)
            # turning the model to train mode
            self.experiment.model.train()
            dataset_loader = self.experiment.train_loader
            n_batches = self.experiment.n_batches_train
            mode_str = "TRAINING"
            #
        elif mode == 1:  # validation
            if self.experiment.verbose > 0:
                self.experiment.logger.print(
                    "VALIDATION", style="ud", up_extra_lines=1)
            # turning the model to evaluation mode
            self.experiment.model.eval()
            dataset_loader = self.experiment.valid_loader
            n_batches = self.experiment.n_batches_valid
            mode_str = "VALIDATION"
            #
        elif mode == 2:  # testing
            if self.experiment.verbose > 0:
                self.experiment.logger.print(
                    "TESTING", style="ud", up_extra_lines=1)
            # turning the model to evaluation mode
            self.experiment.model.eval()
            dataset_loader = self.experiment.test_loader
            n_batches = self.experiment.n_batches_test
            mode_str = "TESTING"
            #
        else:
            raise ValueError(f"Unrecognized 'mode' value ({mode}), "
                             f"only 0/1/2 permitted.")

        # pre-allocating batch_loss_list
        batch_loss_list = []

        # creating instances to track accuracy / R2 score evolution
        if self.experiment.classification_flag:
            # confusion matrix if classification
            confusion_matrix = torchnet.meter.ConfusionMeter(
                self.experiment.n_classes)
        else:
            # R2 score if regression
            r2_score = R2Score()

        # batch loop
        for batch_index, batch_samples in enumerate(dataset_loader):
            # getting current X (inputs) and y_true (labels)
            X = batch_samples[0].float()
            y_true = batch_samples[1]

            # sending inputs and labels to the right device
            X = X.to(self.experiment.device)
            y_true = y_true.to(self.experiment.device)

            # clearing gradient buffer (we do not want any gradient from
            # previous epoch, we do not want to cumulate gradients)
            self.experiment.optimizer.zero_grad()

            # computing output
            y_pred = self.experiment.model(X)

            # deleting inputs from memory (if on gpu, releasing memory)
            del X

            # computing loss
            if self.experiment.loss_name.lower() == "mseloss":
                batch_loss = self.experiment.loss(
                    y_pred.float(), y_true.float()
                )
            else:
                batch_loss = self.experiment.loss(
                    y_pred, y_true
                )

            # updating batch loss list
            # noinspection PyTypeChecker
            batch_loss_list.append(float(batch_loss))

            if self.experiment.classification_flag:
                # computing class_pred
                _, classes_pred = torch.max(y_pred, 1)
                classes_true = y_true

                # now, both class_true and class_pred are 1 x batch_size
                # tensors. So, we can compute accuracy
                batch_acc = (classes_pred == classes_true).sum().item() / len(
                    classes_true)

                # updating confusion matrix
                # noinspection PyUnboundLocalVariable
                confusion_matrix.add(classes_pred.int(), classes_true)
            else:
                # adding the current (y_pred, y_true) couple to the R2Score
                # instance
                # noinspection PyUnboundLocalVariable
                r2_score.update(output=(y_pred, y_true))

            # backward + optimize if training
            if mode == 0:
                # back propagating loss
                batch_loss.backward()

                # making a step with the optimizer
                self.experiment.optimizer.step()

            # printing batch information
            if self.experiment.verbose >= 2:
                # noinspection PyTypeChecker
                expression = ">> {} Batch {}/{} | loss: {:.4f}".format(
                    mode_str,
                    str(batch_index + 1).zfill(len(str(n_batches))),
                    n_batches,
                    float(batch_loss)
                )
                if self.experiment.classification_flag:
                    # noinspection PyUnboundLocalVariable
                    expression += ", acc: {:.4f}".format(batch_acc)
                self.experiment.logger.print(expression)

        # ALL BATCHES DONE!!

        # running lr_scheduler if in validation
        if mode == 1:
            if type(self.experiment.lr_scheduler).__name__ == \
                    "ReduceLROnPlateau":
                self.experiment.lr_scheduler.step(np.mean(batch_loss_list))
            else:
                self.experiment.lr_scheduler.step()

        # getting lr
        lr = None
        for param_group in self.experiment.optimizer.param_groups:
            lr = param_group['lr']

        if self.experiment.classification_flag:
            # computing confusion matrix and accuracy
            cm = confusion_matrix.conf
            acc = sum(cm.diagonal()) / np.sum(cm)
        else:
            # computing r2 score
            r2 = r2_score.compute()

        # computing loss
        loss = float(np.mean(batch_loss_list))

        # filling result dictionaries
        if mode == 0:  # training
            self.train_results["loss_list"].append(loss)
            self.train_results["last_loss"] = loss
            if self.experiment.classification_flag:
                # noinspection PyUnboundLocalVariable
                self.train_results["acc_list"].append(acc)
                self.train_results["last_acc"] = acc
                # noinspection PyUnboundLocalVariable
                self.train_results["cm_list"].append(cm)
            else:
                # noinspection PyUnboundLocalVariable
                self.train_results["r2_list"].append(r2)
                self.train_results["last_r2"] = r2
            #
        elif mode == 1:  # validation
            self.valid_results["loss_list"].append(loss)
            self.valid_results["last_loss"] = loss
            self.valid_results["lr_list"].append(lr)
            if self.experiment.classification_flag:
                # noinspection PyUnboundLocalVariable
                self.valid_results["acc_list"].append(acc)
                self.valid_results["last_acc"] = acc
                # noinspection PyUnboundLocalVariable
                self.valid_results["cm_list"].append(cm)
            else:
                # noinspection PyUnboundLocalVariable
                self.valid_results["r2_list"].append(r2)
                self.valid_results["last_r2"] = r2
            #
        elif mode == 2:  # testing
            # noinspection PyTypeChecker
            self.test_results["loss"] = loss
            if self.experiment.classification_flag:
                # noinspection PyUnboundLocalVariable
                self.test_results["acc"] = acc
                # noinspection PyUnboundLocalVariable
                self.test_results["cm"] = cm
            else:
                # noinspection PyUnboundLocalVariable
                self.test_results["r2"] = r2

    def test(self):
        # if there was validation, loading the best model
        if self.experiment.n_batches_valid > 0:
            self.experiment.model.load_state_dict(
                torch.load(
                    os.path.join(self.experiment.this_dir, 'Net_best_loss.pt')
                )
            )
        self._loop(mode=2)
        if self.experiment.verbose >= 1:
            # noinspection PyStringFormat
            expression = "loss: {:.4f}\n".format(self.test_results['loss'])
            if self.experiment.classification_flag:
                # noinspection PyStringFormat
                expression += "accuracy: {:.4f}\n".format(
                    self.test_results['acc'])
                expression += f"conf matrix:\n{self.test_results['cm']}"
            else:
                # noinspection PyStringFormat
                expression += "r2 score: {:.4f}".format(
                    self.test_results['r2'])
            self.experiment.logger.print(
                expression,
                up_extra_lines=1,
                timestamp_flag=False
            )


if __name__ == '__main__':
    # importing MNIST loader and model
    from pydaves.torchsystem.torchloaders import mnist
    from pydaves.torchsystem.torchmodels import Net3Conv1MP2Lin

    # creating a TorchConfig instance
    config = TorchConfig("config_example.yml")

    # creating a TorchExperiment instance
    experiment = TorchExperiment(
        config=config,
        loader_fun=mnist,
        model_class=Net3Conv1MP2Lin
    )

    # running the experiment
    experiment.run()

    # plotting results
    experiment.plot()
