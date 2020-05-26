# SPDX-FileCopyrightText: 2018 Christopher Kerr
#
# SPDX-License-Identifier: LGPL-3.0-or-later

__copyright__ = "Christopher Kerr"
__license__ = "LGPLv3+"

import functools

import numpy as np
from pkg_resources import resource_string
import pyopencl as cl
import pyopencl.array as cl_array


def with_some_queue(f):
    """Decorator which creates a queue if none is passed in the keywords.

    The wrapped function must be a method on an object with a `.context`
    attribute and must return an event and a value. If a queue is passed,
    the (event, value) tuple will be returned as-is (asynchronous). If no
    queue is passed, a new queue will be created and the wrapper waits for
    the event to complete before returning a value.

    """
    @functools.wraps(f)
    def wrapper(instance, *args,
                # queue=None,  # # Python 2 does not like this
                **kwargs):
        queue = kwargs.pop('queue', None)
        assert isinstance(instance.context, cl.Context)
        if queue is None:
            with cl.CommandQueue(instance.context) as queue:
                ev, value = f(instance, *args, queue=queue, **kwargs)
                ev.wait()
                return value
        else:
            assert instance.context == queue.context
            ev, value = f(instance, *args, queue=queue, **kwargs)
            return ev, value
    return wrapper


def check_array(array, shape, dtype=None, exact=True):
    """Check that the array has the correct shape.

    If exact is False, allow the leading dimension to be larger than the
    expected shape.
    """
    if dtype is not None:
        dtype = np.dtype(dtype)
        if array.dtype != dtype:
            raise TypeError('Array should have dtype %s, got %s' %
                            (dtype, array.dtype))

    if array.shape == shape:
        return
    elif ((not exact) and
          (array.shape[1:] == shape[1:]) and
          (array.shape[0] >= shape[0])):
        return
    else:
        raise ValueError('Array shape %r does not match expected shape %s' %
                         (array.shape, shape))


def optional_out_array(f=None, shape=None, dtype=None, **check_kwargs):
    """Decorator creating an output array if none is passed in the keywords.

    Entries in the shape tuple can either be integers, in which case they are
    used as-is, or strings, in which case they are looked up as attributes
    on the object of the wrapped method. Additional keyword arguments are
    passed to the `check_array()` function to check the shape of the passed
    array if one is passed.

    This includes the with_some_queue functionality as creating an array
    requires a queue.

    """
    shape = tuple(shape)
    dtype = np.dtype(dtype)
    if f is None:
        return functools.partial(optional_out_array,
                                 shape=shape, dtype=dtype, **check_kwargs)

    @with_some_queue
    @functools.wraps(f)
    def wrapper(instance, *args,
                # queue=None, out=None,  # Python 2 does not like this
                **kwargs):
        queue = kwargs.pop('queue')
        out = kwargs.pop('out', None)
        required_shape = []
        for item in shape:
            if isinstance(item, str):
                item = getattr(instance, item)
            required_shape.append(item)
        required_shape = tuple(required_shape)
        if out is None:
            out = cl_array.empty(queue, required_shape, dtype)
        check_array(out, required_shape, dtype=dtype, **check_kwargs)
        assert instance.context == out.context
        assert queue == out.queue
        ev, value = f(instance, *args, queue=queue, out=out, **kwargs)
        # The returned array should be the same as the `out` array
        assert value is out
        return ev, value
    return wrapper


class ClProgram(object):
    """Base class for OpenCL kernel programs."""

    def __init__(self, filename, options=(), context=None):
        """Build the CL program from the source file.

        Create a context using `cl.create_some_context()` if None is passed.
        """
        if context is None:
            context = cl.create_some_context()
        self.context = context
        # The path is internal to pkg_resources i.e. always '/' separators
        filepath = '/'.join(('cl-src', filename))
        program_src = resource_string(__name__, filepath)
        if not isinstance(program_src, str):  # Python 3
            program_src = str(program_src, 'ascii')
        self.program = cl.Program(context, program_src)
        self.program.build(options=options)


class LMAXMixin(object):
    """Super simple mixin which adds an LMAX1 attribute with value LMAX+1."""

    @property
    def LMAX1(self):
        return self.LMAX + 1


class PackedLMMixin(LMAXMixin):
    """Mixin class with methods for arrays with packed [L,M] dimensions.

    This version is for arrays only containing non-negative M values.

    If the LMAX attribute is set on the class, LMAX1 and NLM are available
    as properties.
    """

    @staticmethod
    def indexLM(L, M=0):
        """Index into a packed [L,M] array."""
        assert M >= 0
        assert L >= M
        return L * (L + 1) // 2 + M

    @property
    def NLM(self):
        return self.indexLM(self.LMAX1, 0)
