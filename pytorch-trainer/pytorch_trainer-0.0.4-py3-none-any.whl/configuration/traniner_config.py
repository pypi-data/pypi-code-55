from dataclasses import  dataclass

@dataclass
class TrainerConfig:
    model_dir: str = "checkpoints"  # directory to save model states
    model_save_best: bool = True  # save model with best accuracy
    model_saving_frequency: int = 1  # frequency of model state savings per epochs
    device: str = "cpu"  # device to use for training.
    epoch_num: int = 50  # number of times the whole dataset will be passed through the network
    progress_bar: bool = False  # enable progress bar visualization during train process