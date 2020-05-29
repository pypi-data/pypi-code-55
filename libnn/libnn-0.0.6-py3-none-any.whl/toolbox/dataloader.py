import pickle

import numpy as np
import torch
from torch.utils.data import Dataset
from torchvision import transforms, utils


class Loader(Dataset):
    def __init__(self, file_path = None, transform = None):
        with open(file_path, "rb+") as f:
            data = pickle.load(f)
            self.Xs = data["Xs"]
            self.ys = data["ys"]
            self.transform = transform

    def __len__(self):
        return len(self.Xs)

    def __getitem__(self, idx):
        sample = (self.Xs[idx], self.ys[idx])
        if self.transform:
            sample = self.transform(sample)
        return sample


class ToTensor(object):
    """Convert ndarrays in sample to Tensors."""

    def __call__(self, sample):
        Xs, ys = sample
        ys = np.array(ys)
        # Xs = Xs[np.newaxis, :]
        # ys = ys.reshape(1)
        return (torch.from_numpy(Xs).float(), torch.from_numpy(ys).float())
