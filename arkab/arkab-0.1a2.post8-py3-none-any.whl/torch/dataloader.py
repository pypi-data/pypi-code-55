"""
Dataloader for torch dataloader
"""

import torch as th
import torch.utils.data as tdata
from torch import Tensor as tensor


def batch_provider(*data: list,
                   batch_size: int = 1,
                   shuffle: bool = True,
                   ignore_last: bool = False) -> tdata.DataLoader:
    """

    Args:
        *data: data, multi list
        batch_size: your batch size
        shuffle: shuffle data when loading
        ignore_last: ignore last or not
    Returns:

    """
    dtensors = tuple(map(tensor, data))  # tensor tuple
    dataset = tdata.TensorDataset(*dtensors)
    loader = tdata.DataLoader(dataset=dataset, batch_size=batch_size,
                              shuffle=shuffle, drop_last=ignore_last)
    return loader


def batch_idx_provider(idx_data: list,
                       batch_size: int = 1,
                       shuffle: bool = True) -> tdata.DataLoader:
    dtensors = th.LongTensor(idx_data)
    dataset = tdata.TensorDataset(dtensors)
    loader = tdata.DataLoader(dataset=dataset, batch_size=batch_size,
                              shuffle=shuffle)
    return loader
