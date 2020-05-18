"""
torchsystem.loaders

This module contains some loader functions to create data loaders for the
training set and the validation set. If you want to add a new dataset
loader, just create a new function here. The loader function:
- must have an instance of the TorchExperiment as first input;
- can have several inputs; the TorchExperiment class will pass this inputs
  when calling the loader_fun using the loader_args tuple;
- must compute and return the followings:
    * train_loader: torch.utils.data.DataLoader instance for train set
    * valid_loader: torch.utils.data.DataLoader instance for validation set
    * test_loader: torch.utils.data.DataLoader instance for test set
    * input_shape: tuple 1 * 3
        where each element of this tuple means the following:
        (n_rows (height) * n_cols (width) * n_channels (depth))
    * classes: (only if classification experiment) tuple 1 * n_classes
Take a look to the MNIST dataset below for an example.
"""

import os
from torchvision import datasets
from torchvision import transforms
from pydaves.torchsystem.torchsystem import TorchExperiment
from torch.utils.data.dataloader import DataLoader


def mnist(experiment: TorchExperiment):
    # computing dataset path
    root = os.path.join(experiment.work_dir, "datasets")

    # computing transformations to do on dataset once it is loaded.
    # transforms.Compose: compose different transformations
    # transform.ToTensor: convert PIL Image or numpy.ndarray to tensor.
    # transform.Normalize: normalize a tensor image with mean and standard
    # deviation.
    # Given mean: (M1,...,Mn) and std: (S1,..,Sn) for n channels
    # this transform will normalize each channel of the input torch.*Tensor
    # i.e. input[channel] = (input[channel] - mean[channel]) / std[channel]
    transform = transforms.Compose(
        [transforms.ToTensor(),
         transforms.Normalize((0.1307,), (0.3081,))]
    )

    # getting training and validation set
    train_set = datasets.MNIST(
        root=root,
        train=True,
        download=True,
        transform=transform
    )
    test_set = datasets.MNIST(
        root=root,
        train=False,
        download=True,
        transform=transform
    )

    # crating loaders
    train_loader = DataLoader(
        train_set,
        batch_size=experiment.batch_size,
        shuffle=True
    )
    valid_loader = None
    test_loader = DataLoader(
        test_set,
        batch_size=experiment.batch_size,
        shuffle=False
    )

    # creating input_shape and classes
    input_shape = (28, 28, 1)
    classes = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9")

    # TODO: more smart way to pass outputs. Maybe the user does not want to
    #  use validation, or test also. Furthermore, input_shape and classes are
    #  not needed, cause the TorchExperiment instance can compute them using
    #  loaders during the init procedure.

    # returning loaders
    return train_loader, valid_loader, test_loader, input_shape, classes
