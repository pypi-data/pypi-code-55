from typing import Iterable, List, Type, Dict
from mario.funcs import DoFn
from mario.attrdict import AttrDict
import inspect


class UndefinedStepError(KeyError):
    """Error class for when there is an attempt to access a Step that doesnt exist"""


class Registry:
    def __init__(self):
        self._funcs = AttrDict()

    def __len__(self) -> int:
        return len(self._funcs)

    def __next__(self) -> Iterable:
        return next(self._wrapped_iter)

    def __iter__(self):
        self._wrapped_iter = iter(self._funcs.items())
        return self._wrapped_iter

    def __getattr__(self, item):
        try:
            return self._funcs[item]
        except KeyError:
            raise UndefinedStepError(f"The Step you are trying to access does not exist: {item}")

    def __getitem__(self, key: str):
        try:
            return self._funcs[key]
        except KeyError:
            raise UndefinedStepError(f"The Step you are trying to access does not exist: {key}")

    @staticmethod
    def fn_signature(fn: Type[DoFn]) -> Dict:
        args = inspect.signature(fn)

        out = dict(
            fn=fn.__name__,
            args=[],
            return_type=str(args.return_annotation)
        )

        for k, v in args.parameters.items():
            if k != 'self':
                out["args"].append({k: str(v.annotation)})
        return out

    def func_signatures(self) -> List[Dict]:
        signatures = []
        for name, func in self:
            signatures.append(self.fn_signature(func))
        return signatures

    def register(self, funcs: List[Type[DoFn]]):
        for func in funcs:
            if not issubclass(func, DoFn):
                raise TypeError(
                    (
                        f'Unregisterable Type: {func}. Registerable types'
                        'must be concrete subclasses of DoFn'
                    )
                )
            if func.__name__ in self._funcs:
                raise ValueError(f'cannot overwite values in Registry objects')
            self._funcs[func.__name__] = func
