# type: ignore
import functools
import sys

from msgpack import *

dump_ = dump
dumps_ = dumps
pack_ = pack
packb_ = packb
Packer_ = Packer

load_ = load
loads_ = loads
unpack_ = unpack
unpackb_ = unpackb
Unpacker_ = Unpacker


class ArrayInterface:
    def __init__(self, array_interface):
        array_interface["shape"] = tuple(array_interface["shape"])
        self.__array_interface__ = array_interface


def pack_ndarray(ndarray):
    interface = ndarray.__array_interface__
    if "strides" in interface:
        if interface["strides"] is not None:
            raise PackException(
                "Strided array attempted to pack, please pack as C-Contiguous"
            )
        del interface["strides"]
    if "descr" in interface and len(interface["descr"]) == 1:
        del interface["descr"]
    interface["data"] = ndarray.tobytes()
    ser = packb_(interface)
    return ExtType(110, ser)


def ext_hook(code, data):
    if code == 110:
        interface = ArrayInterface(unpackb_(data))
        if "numpy" in sys.modules:
            import numpy as np

            return np.array(interface)
        return interface

    return ExtType(code, data)


def with_default(**default_kwargs):
    def decorator(f):
        @functools.wraps(f)
        def inner(*args, **kwargs):
            default_kwargs.update(kwargs)
            return f(*args, **default_kwargs)

        inner.__doc__ = f.__doc__
        return inner

    return decorator


dump = with_default(default=pack_ndarray)(dump_)
dumps = with_default(default=pack_ndarray)(dumps_)
pack = with_default(default=pack_ndarray)(pack_)
packb = with_default(default=pack_ndarray)(packb_)
Packer = with_default(default=pack_ndarray)(Packer_)

load = with_default(ext_hook=ext_hook)(load_)
loads = with_default(ext_hook=ext_hook)(loads_)
unpack = with_default(ext_hook=ext_hook)(unpack_)
unpackb = with_default(ext_hook=ext_hook)(unpackb_)
Unpacker = with_default(ext_hook=ext_hook)(Unpacker_)
