import random

import numpy as np
import torch

from ..configuration import SystemConfig, TrainerConfig, DataloaderConfig

def patch_configs(epoch_num_to_set=TrainerConfig.epoch_num, batch_size_to_set=DataloaderConfig.batch_size):
    """ Patches configs if cuda is not available

    Returns:
        returns patched dataloader_config and trainer_config

    """
    # default experiment params
    num_workers_to_set = DataloaderConfig.num_workers

    if torch.cuda.is_available():
        device = "cuda"
    else:
        device = "cpu"
        batch_size_to_set = 16
        num_workers_to_set = 2
        epoch_num_to_set = 1

    dataloader_config = DataloaderConfig(batch_size=batch_size_to_set, num_workers=num_workers_to_set)
    trainer_config = TrainerConfig(device=device, epoch_num=epoch_num_to_set)
    return dataloader_config, trainer_config