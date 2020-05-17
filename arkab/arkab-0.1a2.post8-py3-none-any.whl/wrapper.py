"""
Tensor and data operations

Functions:

1. Provide datasets

2. Change list data to
"""

import tensorflow as tf
import torch as th

BACKENDS = ['tf', 'tensorflow', 'torch', 'th', 'pytorch']
TFBACKEND = ['tf', 'tensorflow']
TORCHBACKEND = ['torch', 'th', 'pytorch']
REALBACKENDS = ['tf', 'th']


class TensorWrapper:
    def __init__(self, backend: str = None, *gpu):
        assert backend in BACKENDS, f"NOT SUPPORT BACKEND!" \
                                    f"Please give a correct backend in {BACKENDS}"
        if backend in TFBACKEND:
            self.wrapper = TensorflowWrapper(gpu)
            # use tensorflow gpu
        else:
            self._backend = 1  # 1 for torch
            self.wrapper = TorchWrapper(gpu)


class TorchWrapper:  # torch wrapper
    # TODO: Multi GPU support
    def __init__(self, *gpu):
        self.gpu_enable = len(gpu) > 0


# Tensorflow operations
class TensorflowWrapper:
    # TODO: Multi GPU support
    def __init__(self, *gpu):
        self.gpu_enable = len(gpu) > 0
