from typing import Tuple


class ConverterBase:
    def __call__(self, *args, **kwargs) -> Tuple[list, dict]:
        return self.call(*args, **kwargs)

    def call(self, *args, **kwargs) -> Tuple[list, dict]:
        raise NotImplementedError

    def get_config(self) -> dict:
        return {}

    @classmethod
    def from_config(cls, config) -> "ConverterBase":
        return cls(**config)
