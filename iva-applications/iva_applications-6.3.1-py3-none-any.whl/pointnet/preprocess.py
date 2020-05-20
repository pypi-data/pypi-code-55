"""Pointnet preprocessing."""
import numpy as np


def object_to_tensor(obj: np.ndarray) -> np.ndarray:
    """Convert obj data to tensor."""
    tensor = np.resize(obj, (2048, 3))
    assert tensor.shape == (2048, 3)
    return tensor
