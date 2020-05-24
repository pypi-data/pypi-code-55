import functools
from typing import List, Any, TypeVar, Generic, Callable, Union, Type

from dataclasses import dataclass, field


class RegistryError(Exception):
    pass


P = TypeVar('P')
T = TypeVar('T')


@dataclass
class RegistryItem(Generic[P, T]):
    payload: P
    value: T


class PayloadFactory(Generic[P]):
    def __call__(self, *args, **kwargs) -> P:
        raise NotImplementedError()


class NonePayloadFactory(PayloadFactory[None]):

    def __call__(self, *args, **kwargs):
        return None


@dataclass
class ConstructorPayloadFactory(Generic[P], PayloadFactory[P]):
    cls: Type[P]

    def __call__(self, *args, **kwargs) -> P:
        return self.cls(*args, **kwargs)


class DecorateStrategy:
    """you can override this to only allow certain types of objects to be decorated"""

    def is_decoratable(self, registry: 'Registry', value: Any) -> bool:
        raise NotImplementedError()

    def check_decorate(self, registry: 'Registry', value: Any):
        raise NotImplementedError()


@dataclass
class DefaultDecorateStrategy(DecorateStrategy):
    allow_duplicates: bool = False

    def is_decoratable(self, registry: 'Registry', value: Any) -> bool:
        return callable(value)

    def check_decorate(self, registry: 'Registry', value: Any):
        if not self.allow_duplicates:
            duplicated = [x for x in registry.items if x.value == value]

            if len(duplicated):
                raise RegistryError('already registered')


@dataclass
class Registry(Generic[P, T]):
    payload_factory: PayloadFactory[P] = NonePayloadFactory()
    decorator_strategy: DecorateStrategy = DefaultDecorateStrategy()
    items: List[RegistryItem[P, T]] = field(default_factory=list)

    def decorate(self, payload: P, value: T) -> T:
        self.decorator_strategy.check_decorate(self, value)
        self.add(payload, value)
        return value

    def add(self, payload: P, value: T):
        self.items.append(RegistryItem(payload, value))

    def remove(self, value: T) -> P:
        """
        remove the last item in registry for `value`
        """
        *_, tail_idx = [i for i, x in enumerate(self.items) if x.value == value]

        tail = self.items.pop(tail_idx)

        return tail.payload

    def __call__(self, *args, **kwargs) -> Union[Callable[[T], T], T]:
        if len(args):
            decorated, *args_rest = args

            if self.decorator_strategy.is_decoratable(self, decorated):
                return self.decorate(
                    self.payload_factory(*args_rest, **kwargs),
                    decorated,
                )

        def wrapper(decorated_: T):
            return self.decorate(
                payload=self.payload_factory(*args, **kwargs),
                value=decorated_,
            )

        return wrapper
