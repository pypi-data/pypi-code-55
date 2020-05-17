import sys

__all__ = ['is_torch_available']


def is_torch_available() -> bool:
    try:
        import torch
        return torch.__version__.startswith('1')
    except ImportError:
        print("PyTorch is not available!")
        return False
