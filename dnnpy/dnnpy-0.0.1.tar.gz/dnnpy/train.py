import numpy as np
from .utils import split_data, Dataloader


def evaluate(network, metric, data_loader):
    """
    Evaluate a network by computing a metric for specific data.

    Parameters
    ----------
    network : Module
        A module that implements the network.
    metric : callable
        A function that takes logits and labels
        and returns a scalar numpy array.
    data_loader : Dataloader
        The data loader that provides the batches.

    Returns
    -------
    values : ndarray
        The computed values for each batch in the data loader.
    """

    values = []
    loss = []

    network.eval()  # eval mode

    for x, y in data_loader:
        y_hat = network.forward(x)  # forward pass

        y_hat = y_hat.reshape(y.shape)

        values.append(y_hat)

        try:
            loss.append(metric.compute_loss(y_hat, y))
        except:
            loss.append(metric.forward(y_hat, y))

    values = np.array(values)

    loss = np.array(loss)

    return values, loss


def update(network, loss, data_loader, optimiser):
    """
    Update a network by optimising the loss for the given data.

    Parameters
    ----------
    network : Module
        A module that implements the network.
    loss : Module
        Loss function module.
    data_loader : Dataloader
        The data loader that provides the batches.
    optimiser : Optimiser
        Optimisation algorithm to use for the update.

    Returns
    -------
    errors : ndarray
        The computed loss for each batch in the data loader.
    """
    errors = []

    network.train()  # train mode

    for x, y in data_loader:

        y_hat = network.forward(x)  # forward pass

        network.zero_grad()

        y_hat = y_hat.reshape(y.shape)

        l = loss.forward(y_hat, y)  # compute the loss
        dloss = loss.backward()  # derivate the loss wrt the outpout

        if len(y.shape) == 1:
            network.backward(np.expand_dims(dloss, axis=1))
        else:
            network.backward(dloss)  # backward pass

        optimiser.step()

        errors.append(l)

    return np.array(errors)


def train(data, network, loss, optimiser, epochs=1, batch_size=None, val_split=0.75, shuffle=True, show=True):
    """
    Train a neural network with gradient descent.

    Parameters
    ----------
    data : tuple of ndarrays
        Dataset as tuple of input features and target values.
    network : Module
        A module that implements the network.
    loss : Module
        Loss function module.
    optimiser : Optimiser
        Optimisation algorithm.
    epochs : int, optional
        Number of times to iterate the dataset.
    batch_size : int or None, optional
        Number of samples to use simultaneously.
        If None, all samples are fed to the network.
    val_split : float, optional
        Percentage of data to use for updating the model.
        The other part of the data is used for evaluating the model.
    shuffle : bool, optional
        Flag to enable or disable shuffling of the training data.

    Returns
    -------
    train_errors : (epochs + 1, n_batches) ndarray
        Training error for each epoch and each batch.
    valid_errors : (epochs + 1, 1) ndarray
        Validation error for each epoch.
    """
    x, y = data

    train, validation = split_data(x, y, ratio=val_split)  # split data to train and validation

    x_train, y_train = train

    x_valid, y_valid = validation

    data_loader_train = Dataloader(x_train, y_train, batch_size=batch_size, shuffle=shuffle)  # data loader for training
    data_loader_valid = Dataloader(x_valid, y_valid, batch_size=batch_size,
                                   shuffle=shuffle)  # data loader for validation

    train_err = []
    val_err = []
    for i in range(1, epochs + 1):
        train_errors = update(network, loss, data_loader_train, optimiser=optimiser)
        _, valid_errors = evaluate(network, loss, data_loader_valid)
        train_err.append(np.mean(train_errors))
        val_err.append(np.mean(valid_errors))

        if show:
            if i == 1 or i % 5 == 0:
                print(f"Epoch: {i}, train_loss={np.mean(train_errors)}, val_loss={np.mean(valid_errors)}")

    return train_err, val_err
