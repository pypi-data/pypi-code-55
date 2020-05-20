from typing import Callable, Iterable
from dataclasses import dataclass

from torchvision.transforms import ToTensor

@dataclass
class DatasetConfig:
    root_dir: str = "data"
    train_transforms: Iterable[Callable] = (
        ToTensor(),
    )
    test_transforms: Iterable[Callable] = (
        ToTensor(),
    )
    