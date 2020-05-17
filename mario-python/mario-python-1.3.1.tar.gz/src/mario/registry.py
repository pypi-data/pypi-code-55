from typing import Iterable, List, Type
from mario.funcs import DoFn
from mario.attrdict import AttrDict


class UndefinedStepError(KeyError):
    """Error class for when there is an attempt to access a Step that doesnt exist"""


class Registry:
    def __init__(self):
        self.__funcs__ = AttrDict()

    def __len__(self) -> int:
        return len(self.__funcs__)

    def __next__(self) -> Iterable:
        return next(self._wrapped_iter)

    def __iter__(self):
        self._wrapped_iter = iter(self.__funcs__)
        return self

    def __getattr__(self, item):
        try:
            return self.__funcs__[item]
        except KeyError:
            raise UndefinedStepError(f"The Step you are trying to access does not exist: {item}")

    def __getitem__(self, key: str):
        try:
            return self.__funcs__[key]
        except KeyError:
            raise UndefinedStepError(f"The Step you are trying to access does not exist: {key}")

    def register(self, funcs: List[Type[DoFn]]):
        for func in funcs:
            if not issubclass(func, DoFn):
                raise TypeError(
                    (
                        f'Unregisterable Type: {func}. Registerable types'
                        'must be concrete subclasses of DoFn'
                    )
                )
            if func.__name__ in self.__funcs__:
                raise ValueError(f'cannot overwite values in Registry objects')
            self.__funcs__[func.__name__] = func
