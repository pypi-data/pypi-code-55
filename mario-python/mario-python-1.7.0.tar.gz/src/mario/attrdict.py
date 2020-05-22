from typing import Any


class AttrDict(dict):
    def __init__(self, **kwargs):
        super().__init__()
        for k, v in kwargs.items():
            self.__setitem__(k, v)

    def __getattr__(self, k: str):
        return self[k]

    def __setitem__(self, k: str, v: Any):
        if isinstance(v, dict):
            v = AttrDict(**v)
        super().__setitem__(k, v)

    def __setattr__(self, k: str, v: Any):
        self[k] = v
