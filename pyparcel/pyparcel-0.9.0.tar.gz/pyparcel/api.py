from typing import Tuple, Callable, Dict, List
from functools import wraps
import codecs
from .strict_type import *

T = TypeVar("T")
global_encoding: str = "utf-8"


def _lambda_raise_(ex):
    raise ex


def check_encoding(func):
    @wraps(func)
    def func_wrapper(*args, **kwargs):
        for key, value in kwargs.items():
            if key == "encoding":
                try:
                    codecs.lookup(value)
                except LookupError:
                    raise Exception(f"{value} is not a proper encoding.")
                return func(*args, **kwargs)
        return func(*args, **kwargs)

    return func_wrapper


pack_dict: Dict[type, Callable[[Any], bytes]] = {
    int: (lambda obj: pack(Int(obj))),
    bool: (lambda obj: struct.pack("=?", obj)),
    float: (lambda obj: pack(Float(obj))),
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
    bytes: (lambda obj: struct.pack("i{}s".format(len(obj)), len(obj), obj)),
    str: (lambda obj: pack(obj.encode(global_encoding))),
    list: (lambda obj: _pack_list(obj)),
    set: (lambda obj: _lambda_raise_(NotImplementedError)),
    dict: (lambda obj: _lambda_raise_(NotImplementedError)),
    tuple: (lambda obj: pack(*obj)),
}

unpack_dict: Dict[type, Callable[[T, bytes], T]] = {
    int: (lambda obj, data: _unpack_helper(data, Int(obj))),
    bool: (lambda _, data: (struct.unpack("=?", data[:1])[0], data[1:],)),
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
    bytes: (lambda _, data: _unpack_bytes(data)),
    str: (lambda _, data: _unpack_string(data)),
    list: (lambda obj, data: _unpack_list(data, obj)),
    set: (lambda obj, _: _lambda_raise_(NotImplementedError)),
    dict: (lambda obj, _: _lambda_raise_(NotImplementedError)),
    tuple: (lambda obj, data: _unpack_tuple(data, obj)),
}


def _pack_list(li: List[T]) -> bytes:
    """
    Packs *li* of size *n* in the following format:
    ``[n][li_1][li_2]...[li_n]``

    :param li: List to be packed
    :return: Packed byte string of *list*
    """
    if len(li) == 0:
        return pack(len(li))
    conformed_list = _conform_list(li)
    return b"".join([pack(i) for i in [len(conformed_list)] + conformed_list])


def _conform_list(li: List[Any]) -> List[T]:
    """
    Ensures that every element in *li* can conform to one type
    :param li: list to conform
    :return: conformed list
    """
    conform_type = li[0].__class__
    for i in li:
        if isinstance(i, StrictType):
            conform_type = i.__class__
            break
    base_type = (
        conform_type.__base__ if conform_type.__base__ != object else None
    )  # do not let base_type be 'object'
    if not all(type(i) == conform_type or type(i) == base_type for i in li):
        raise Exception(f"{li} can not be conformed to the {conform_type}")
    return [i if isinstance(i, conform_type) else conform_type(i) for i in li]


def _unpack_string(data: bytes) -> (str, bytes):
    result, data = _unpack_bytes(data)
    return result.decode(global_encoding), data


def _unpack_bytes(data: bytes) -> (bytes, bytes):
    length = struct.unpack("i", data[:4])[0]
    data = data[4:]
    return (
        struct.unpack("{}s".format(length), data[:length])[0],
        data[length:],
    )


def _unpack_tuple(data: bytes, t: Tuple[Any]) -> (Tuple[Any], bytes):
    unpacked_objs: List[Any] = []
    for obj in t:
        (result, data) = _unpack_helper(data, obj)
        unpacked_objs.append(result)
    return tuple(unpacked_objs), data


def _unpack_list(data: bytes, t: List[T]) -> (List[T], bytes):
    length = struct.unpack("i", data[:4])[0]
    data = data[4:]
    obj_shell = t[0]
    t.pop()
    for i in range(0, length):
        (result, data) = _unpack_helper(data, obj_shell)
        t.append(result)
    return t, data


def _unpack_helper(data: bytes, obj: T) -> (T, bytes):
    if type(obj) in unpack_dict:
        return unpack_dict[type(obj)](obj, data)
    else:
        for v in vars(obj):
            (result, data) = _unpack_helper(data, obj.__getattribute__(v))
            obj.__dict__[v] = result
    return obj, data


@check_encoding
def pack(*objs: Any, encoding: str = "utf-8") -> bytes:
    """
    Converts *objs* into a byte string format in order.

    :param encoding: encoding for strings to be encoded in
    :param objs: Objects to be converted to byte string
    :return: Byte string of *objs*
    """
    global global_encoding
    global_encoding = encoding
    return b"".join(
        [
            pack_dict.get(
                type(obj),
                lambda o: b"".join([pack(o.__getattribute__(v)) for v in vars(o)]),
            )(obj)
            for obj in objs
        ]
    )


@check_encoding
def unpack(data: bytes, *objs: Any, encoding: str = "utf-8") -> Tuple[Any]:
    """
    Converts *data* into python objects, in the order and format of *objs*

    :param encoding: encoding that strings are encoded in
    :param data: data to be converted
    :param objs: order and objects that data conforms to
    :return: One object if *objs* contains one element, or tuple of objects if *objs* contains more than 1 element
    """
    global global_encoding
    global_encoding = encoding
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
