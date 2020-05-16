from ..metrics import Metrics
import torch

default_device = "cuda" if torch.cuda.is_available() else "cpu"


class MyBaseModel():
    """ Base model with basic functionality. Other models should inherit from this class adding
    more features. """

    def __init__(self, net, device=None):
        self.net = net
        self.device = device or default_device

    def compile(self, optimizer, loss, metrics=[], scheduler=None, precision=5):
        self.optimizer = optimizer
        self.loss = loss
        self.metrics = metrics
        self.precision = precision
        self.scheduler = scheduler

    def train(self, dataloader, device=None):
        device = device or self.device
        self.net.to(device)
        self.net.train()
        metrics = Metrics(self.metrics, precision=self.precision)
        for batch in dataloader:
            X, y = batch
            X, y = X.to(device), y.to(device)
            self.optimizer.zero_grad()
            y_hat = self.net(X)
            loss = self.loss(y_hat, y)
            loss.backward()
            self.optimizer.step()
            metrics.compute(loss.item(), y_hat, y)
        return metrics.compute_average()

    def eval(self, dataloader, device=None):
        device = device or self.device
        self.net.to(device)
        self.net.eval()
        metrics = Metrics(self.metrics, prefix="eval_",
                          precision=self.precision)
        with torch.no_grad():
            for batch in dataloader:
                X, y = batch
                X, y = X.to(device), y.to(device)
                y_hat = self.net(X)
                loss = self.loss(y_hat, y)
                metrics.compute(loss.item(), y_hat, y)
            return metrics.compute_average()

    def predict(self, dataloader, device=None):
        device = device or self.device
        self.net.to(device)
        self.net.eval()
        with torch.no_grad():
            preds = torch.tensor([]).to(device)
            for batch in dataloader:
                X = batch
                X = X.to(device)
                pred = self.net(X)
                preds = torch.cat([preds, pred])
            return preds
