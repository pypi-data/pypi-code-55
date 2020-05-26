from torch import Tensor, nn


class BayesianBaseLayer(nn.Module):
    def sample_parameters(self) -> None:
        raise NotImplementedError()

    def set_to_best_prediction(self) -> None:
        raise NotImplementedError()

    @property
    def weights(self) -> Tensor:
        raise NotImplementedError()

    @property
    def kl_loss(self) -> Tensor:
        raise NotImplementedError()
