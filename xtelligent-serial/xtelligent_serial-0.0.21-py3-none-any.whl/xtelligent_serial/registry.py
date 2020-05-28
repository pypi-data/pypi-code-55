from collections.abc import Sequence, Iterable, Mapping
from dataclasses import is_dataclass, fields
from functools import singledispatch
from inspect import ismethod, isfunction
from typing import Any, Type

from .signatures import JSONSerializable, Serializer, Deserializer

# pylint: disable=redefined-builtin

def iscallable(v):
    return ismethod(v) or isfunction(v)

def props(target):
    return {k: v for k, v in [(k, getattr(target, k)) for k in dir(target) if not k.startswith('_')] if not iscallable(v)}

@singledispatch
def to_serializable(target) -> JSONSerializable:
    return None if target is None else to_serializable(props(target))

@to_serializable.register
def _(target: Mapping) -> JSONSerializable:
    return {k: to_serializable(v) for k, v in target.items()}

@to_serializable.register
def _(target: Sequence) -> JSONSerializable:
    return [to_serializable(item) for item in list(target)]

@to_serializable.register
def _(target: Iterable) -> JSONSerializable:
    return [to_serializable(item) for item in target]

@to_serializable.register
def _(target: int) -> JSONSerializable:
    return target

@to_serializable.register
def _(target: float) -> JSONSerializable:
    return target

@to_serializable.register
def _(target: bool) -> JSONSerializable:
    return target

@to_serializable.register
def _(target: str) -> JSONSerializable:
    return target

TYPEKEY = '?__type__?'

def fjd_for_dataclass(type, raw_data):
    type_fields = {f.name:f for f in fields(type)}
    kwargs = {k: from_serializable(type_fields[k].type, v) for k, v in raw_data.items() if k in type_fields}
    return type(**kwargs)

@singledispatch
def fjd(raw_data: JSONSerializable) -> Any:
    if raw_data is None:
        return None
    t = raw_data.get(TYPEKEY) or type(object)
    if is_dataclass(t):
        return fjd_for_dataclass(t, raw_data)
    raise ValueError(f'No deserialization method for {raw_data}')

def from_serializable(type: Type, raw_data: JSONSerializable) -> Any:
    func = fjd.dispatch(type)
    if not func:
        raise ValueError(f'No deserialization handler for type {type}')
    return func(raw_data) if not isinstance(raw_data, Mapping) else func({**raw_data, TYPEKEY: type})

@fjd.register
def _(i: int):
    return i
@fjd.register
def _(f: float):
    return f
@fjd.register
def _(s: str):
    return s
@fjd.register
def _(b: bool):
    return b


def register_serializer(type: Type, func: Serializer):
    assert isfunction(func)
    @to_serializable.register
    def _(target: type) -> JSONSerializable:
        return func(target)

def register_deserializer(type: Type, func: Deserializer):
    assert isfunction(func)
    @fjd.register
    def _ds(raw_data) -> type:
        return func(raw_data)
