from typing import Union, Callable, Any
from collections.abc import Sequence, Iterable, Mapping

JSONSerializable = Union[int, float, bool, str, Sequence, Iterable, Mapping]
Serializer = Callable[[Any], JSONSerializable]
Deserializer = Callable[[JSONSerializable], Any]
