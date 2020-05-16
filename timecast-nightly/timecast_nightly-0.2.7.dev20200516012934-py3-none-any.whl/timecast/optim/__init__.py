"""timecast.optim

Todo:
    * Document available optimizers
"""
import flax
from flax.optim import Adagrad
from flax.optim import Adam
from flax.optim import GradientDescent
from flax.optim import LAMB
from flax.optim import LARS
from flax.optim import Momentum
from flax.optim import RMSProp


@flax.struct.dataclass
class _DummyGradHyperParams:
    """DummyGrad hyper parameters"""

    add: float


class DummyGrad(flax.optim.OptimizerDef):
    """Dummy optimizer for testing"""

    def __init__(self, add: float = 0.0):
        """Initialize hyper parameters"""
        super().__init__(_DummyGradHyperParams(add))

    def init_param_state(self, param):
        """Initialize parameter state"""
        return {}

    def apply_param_gradient(self, step, hyper_params, param, state, grad):
        """Apply per-parametmer gradients"""
        new_param = param + hyper_params.add
        return new_param, state


__all__ = ["Adagrad", "Adam", "GradientDescent", "Momentum", "LAMB", "LARS", "RMSProp"]
