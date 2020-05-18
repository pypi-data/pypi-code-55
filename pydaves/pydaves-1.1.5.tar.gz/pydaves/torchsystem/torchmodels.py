"""
TorchSystem.models

This module contains Neural Network classes.
"""

import torch.nn as nn
from pydaves.torchsystem.torchutils import init_params
from pydaves.torchsystem.torchutils import count_maxpool
from pydaves.torchsystem.torchsystem import TorchExperiment


class Net3Conv1MP2Lin(nn.Module):
    """
    This is a simple Neural Networks with 3 Convolutional layers,
    1 Max Pooling layer and 2 liner layers at the end.
    """

    def __init__(self, experiment: TorchExperiment):
        # calling the superclass init method
        super(Net3Conv1MP2Lin, self).__init__()

        # hard copying other useful parameters
        self.activation = experiment.activation
        self.input_height = experiment.input_height
        self.input_width = experiment.input_width
        self.input_depth = experiment.input_depth
        self.n_channels = self.input_depth
        self.n_filters = experiment.model_settings["n_filters"]
        self.pool_size = experiment.model_settings["pool_size"]
        self.kernel_size = experiment.model_settings["kernel_size"]
        self.n_classes = experiment.n_classes
        self.first_linear_layer_out_size = 50

        # creation of the convolutional part of the neural network
        self.convolutional_layers = nn.Sequential(
            # first convolutional layer
            nn.Conv2d(
                in_channels=self.n_channels,
                out_channels=self.n_channels,
                kernel_size=self.kernel_size,
                padding=(1, 1)
            ),

            # activation for the first convolutional layer
            self.activation,

            # first Max Pooling
            nn.MaxPool2d(
                kernel_size=(self.pool_size, self.pool_size),
                stride=(self.pool_size, self.pool_size)
            ),

            # second convolutional layer
            nn.Conv2d(
                self.n_channels,
                self.n_filters,
                kernel_size=self.kernel_size,
                padding=(1, 1)
            ),

            # activation for the second convolutional layer
            self.activation,

            # third convolutional layer
            nn.Conv2d(
                self.n_filters,
                self.n_filters * 2,
                kernel_size=self.kernel_size,
                padding=(1, 1)
            ),

            # activation for the third convolutional layer
            self.activation
        )

        # counting how many pooling layers
        n_pools = count_maxpool(self.convolutional_layers)

        # computing output size
        height_out = self.input_height // (self.pool_size ** n_pools)
        width_out = self.input_width // (self.pool_size ** n_pools)

        # computing linear layer length
        self.first_linear_layer_in_size = height_out * width_out * \
                                          (self.n_filters * 2)

        # creating the first linear layer;
        # it will reduce the dimensionality to 50
        self.classifier0 = nn.Linear(self.first_linear_layer_in_size,
                                     self.first_linear_layer_out_size)

        # crating the output
        self.classifier = nn.Sequential(
            # activation for the first linear layer
            self.activation,

            # creating the second linear layer
            nn.Linear(self.first_linear_layer_out_size, self.n_classes))

        # Initializing all parameters of the Neural Network using the
        # nn.Module.apply method. This method applies a function recursively
        # to every submodule (as returned by .children()) as well as self.
        self.apply(init_params)

    def forward(self, x):
        # computing the output for the convolutional part of the Neural Network
        x = self.convolutional_layers(x)

        # The view method returns a new tensor with the same data as the self
        # tensor but of a different shape. The size -1 is inferred from
        # other dimensions.
        x = x.view(-1, self.first_linear_layer_in_size)

        # computing the output from the first linear layer
        x0 = self.classifier0(x)

        # computing the final output
        x = self.classifier(x0)

        # returning the final output
        return x
