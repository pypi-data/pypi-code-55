import struct
from typing import TypeVar, Tuple, Any, Callable, Dict, List
from .strict_type import *

from .architecture import Architecture

T = TypeVar("T")


def raise_(ex):
    raise ex


X86_ARCHITECTURE: Architecture = Architecture()


def generate_pack_with_architecture(
        arc: Architecture = X86_ARCHITECTURE,
) -> Callable[[Any], bytes]:
    pack_dict: Dict[type, Callable[[Any], bytes]] = {
        int: (lambda obj: _pack(Int(obj))),
        bool: (lambda obj: struct.pack("=?", obj)),
        float: (lambda obj: _pack(Float(obj))),
        Char: (lambda obj: obj.__pack__()),
        UnsignedChar: (lambda obj: obj.__pack__()),
        SignedChar: (lambda obj: obj.__pack__()),
        Short: (lambda obj: obj.__pack__()),
        UnsignedShort: (lambda obj: obj.__pack__()),
        Int: (lambda obj: obj.__pack__()),
        UnsignedInt: (lambda obj: obj.__pack__()),
        Long: (lambda obj: obj.__pack__()),
        UnsignedLong: (lambda obj: obj.__pack__()),
        LongLong: (lambda obj: obj.__pack__()),
        UnsignedLongLong: (lambda obj: obj.__pack__()),
        Float: (lambda obj: obj.__pack__()),
        Double: (lambda obj: obj.__pack__()),
        bytes: (
            lambda obj: struct.pack("i{}s".format(len(obj)), len(obj), obj)
        ),
        str: (
            lambda obj: struct.pack("i{}s".format(len(obj)), len(obj), obj.encode(arc.encoding))

        ),
        list: (lambda obj: b"".join([_pack(x) for x in vars(obj)])),
        set: (lambda obj: raise_(NotImplementedError)),
        dict: (lambda obj: raise_(NotImplementedError)),
        tuple: (lambda obj: _pack(*obj)),
    }

    def _pack(*objs: Any) -> bytes:
        return b"".join(
            [
                pack_dict.get(
                    type(obj),
                    lambda o: b"".join([_pack(o.__getattribute__(x)) for x in vars(o)]),
                )(obj)
                for obj in objs
            ]
        )

    return _pack


def generate_unpack_with_architecture(
        arc: Architecture = X86_ARCHITECTURE,
) -> Callable[[bytes, Any], Tuple[Any, ...]]:
    unpack_dict: Dict[type, Callable[[T, bytes], T]] = {
        int: (lambda obj, data: _unpack_helper(data, Int(obj))),
        bool: (
            lambda _, data: (
                struct.unpack("=?", data[: 1])[0],
                data[1:],
            )
        ),
        float: (lambda obj, data: _unpack_helper(data, Float(obj))),
        Char: (lambda obj, data: obj.__unpack__(data)),
        UnsignedChar: (lambda obj, data: obj.__unpack__(data)),
        SignedChar: (lambda obj, data: obj.__unpack__(data)),
        Short: (lambda obj, data: obj.__unpack__(data)),
        UnsignedShort: (lambda obj, data: obj.__unpack__(data)),
        Int: (lambda obj, data: obj.__unpack__(data)),
        UnsignedInt: (lambda obj, data: obj.__unpack__(data)),
        Long: (lambda obj, data: obj.__unpack__(data)),
        UnsignedLong: (lambda obj, data: obj.__unpack__(data)),
        LongLong: (lambda obj, data: obj.__unpack__(data)),
        UnsignedLongLong: (lambda obj, data: obj.__unpack__(data)),
        Float: (lambda obj, data: obj.__unpack__(data)),
        Double: (lambda obj, data: obj.__unpack__(data)),
        bytes: (lambda _, data: unpack_bytes(data)),
        str: (lambda _, data: unpack_string(data)),
        list: (lambda obj, _: raise_(NotImplementedError)),
        set: (lambda obj, _: raise_(NotImplementedError)),
        dict: (lambda obj, _: raise_(NotImplementedError)),
        tuple: (lambda obj, data: unpack_tuple(data, obj)),
    }

    def unpack_string(data: bytes) -> (str, bytes):
        result, data = unpack_bytes(data)
        return result.decode(arc.encoding), data

    def unpack_bytes(data: bytes) -> (bytes, bytes):
        length = struct.unpack(
            "i", data[: 4]
        )[0]
        data = data[4:]
        return (
            struct.unpack("{}s".format(length), data[:length])[0],
            data[length:],
        )

    def unpack_tuple(data: bytes, t: Tuple[Any]) -> (Tuple[Any], bytes):
        unpacked_objs: List[Any] = []
        for obj in t:
            (result, data) = _unpack_helper(data, obj)
            unpacked_objs.append(result)
        return tuple(unpacked_objs), data

    def _unpack_helper(data: bytes, obj: T) -> (T, bytes):
        if type(obj) in unpack_dict:
            return unpack_dict[type(obj)](obj, data)
        else:
            for v in vars(obj):
                (result, data) = _unpack_helper(data, obj.__getattribute__(v))
                obj.__dict__[v] = result
        return obj, data

    def _unpack(data: bytes, *objs: Any) -> Tuple[Any]:
        if len(objs) == 0:
            raise TypeError("unpack() takes a variable number of objects")
        if len(objs) == 1:
            return _unpack_helper(data, objs[0])[0]
        else:
            unpacked_objs: List[Any] = []
            for obj in objs:
                (result, data) = _unpack_helper(data, obj)
                unpacked_objs.append(result)
            return tuple(unpacked_objs)

    return _unpack


pack: Callable[[Any], bytes] = generate_pack_with_architecture()
unpack: Callable[[bytes, Any], Tuple[Any, ...]] = generate_unpack_with_architecture()
