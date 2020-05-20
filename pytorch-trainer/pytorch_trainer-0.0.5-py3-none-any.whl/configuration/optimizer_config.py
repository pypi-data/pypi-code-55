from typing import Iterable
from dataclasses import dataclass

@dataclass
class OptimizerConfig:
    learning_rate: float = 1e-3
    momentum: float = 0.9
    weight_decay: float = 1e-4
    lr_step_milestones: Iterable = (30, 40)
    lr_gamma: float = 0.1
    