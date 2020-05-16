"""
Simple How to Use By Hui
To import:
from mymodule import ViennaRNA

set folding temperature:
ViennaRNA.cvar.temperature=37
To get the minimum free energy folding:
fold_compound = ViennaRNA.fold_compound('ATCGATCG')
dotbracket,min_free_energy = fc.mfe()

to get subopt fold:
subopt = [(i.structure,i.energy) for i in fc.subopt(mferange)]

"""

from sys import version_info as _swig_python_version_info
if _swig_python_version_info < (2, 7, 0):
    raise RuntimeError('Python 2.7 or later required')

from . import _RNA

try:
    import builtins as __builtin__
except ImportError:
    import __builtin__

def _swig_setattr_nondynamic(self, class_type, name, value, static=1):
    if name == "thisown":
        return self.this.own(value)
    if name == "this":
        if type(value).__name__ == 'SwigPyObject':
            self.__dict__[name] = value
            return
    method = class_type.__swig_setmethods__.get(name, None)
    if method:
        return method(self, value)
    if not static:
        object.__setattr__(self, name, value)
    else:
        raise AttributeError("You cannot add attributes to %s" % self)


def _swig_setattr(self, class_type, name, value):
    return _swig_setattr_nondynamic(self, class_type, name, value, 0)


def _swig_getattr(self, class_type, name):
    if name == "thisown":
        return self.this.own()
    method = class_type.__swig_getmethods__.get(name, None)
    if method:
        return method(self)
    raise AttributeError("'%s' object has no attribute '%s'" % (class_type.__name__, name))


def _swig_repr(self):
    try:
        strthis = "proxy of " + self.this.__repr__()
    except __builtin__.Exception:
        strthis = ""
    return "<%s.%s; %s >" % (self.__class__.__module__, self.__class__.__name__, strthis,)


def _swig_setattr_nondynamic_instance_variable(set):
    def set_instance_attr(self, name, value):
        if name == "thisown":
            self.this.own(value)
        elif name == "this":
            set(self, name, value)
        elif hasattr(self, name) and isinstance(getattr(type(self), name), property):
            set(self, name, value)
        else:
            raise AttributeError("You cannot add instance attributes to %s" % self)
    return set_instance_attr


def _swig_setattr_nondynamic_class_variable(set):
    def set_class_attr(cls, name, value):
        if hasattr(cls, name) and not isinstance(getattr(cls, name), property):
            set(cls, name, value)
        else:
            raise AttributeError("You cannot add class attributes to %s" % cls)
    return set_class_attr


def _swig_add_metaclass(metaclass):
    """Class decorator for adding a metaclass to a SWIG wrapped class - a slimmed down version of six.add_metaclass"""
    def wrapper(cls):
        return metaclass(cls.__name__, cls.__bases__, cls.__dict__.copy())
    return wrapper


class _SwigNonDynamicMeta(type):
    """Meta class to enforce nondynamic attributes (no new attributes) for a class"""
    __setattr__ = _swig_setattr_nondynamic_class_variable(type.__setattr__)



def new_intP(nelements: 'size_t') -> "int *":
    return _RNA.new_intP(nelements)

def delete_intP(ary: 'int *') -> "void":
    return _RNA.delete_intP(ary)

def intP_getitem(ary: 'int *', index: 'size_t') -> "int":
    return _RNA.intP_getitem(ary, index)

def intP_setitem(ary: 'int *', index: 'size_t', value: 'int') -> "void":
    return _RNA.intP_setitem(ary, index, value)
class intArray(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, nelements: 'size_t'):
        _RNA.intArray_swiginit(self, _RNA.new_intArray(nelements))
    __swig_destroy__ = _RNA.delete_intArray

    def __getitem__(self, index: 'size_t') -> "int":
        return _RNA.intArray___getitem__(self, index)

    def __setitem__(self, index: 'size_t', value: 'int') -> "void":
        return _RNA.intArray___setitem__(self, index, value)

    def cast(self) -> "int *":
        return _RNA.intArray_cast(self)

    @staticmethod
    def frompointer(t: 'int *') -> "intArray *":
        return _RNA.intArray_frompointer(t)

# Register intArray in _RNA:
_RNA.intArray_swigregister(intArray)

def intArray_frompointer(t: 'int *') -> "intArray *":
    return _RNA.intArray_frompointer(t)


def new_floatP(nelements: 'size_t') -> "float *":
    return _RNA.new_floatP(nelements)

def delete_floatP(ary: 'float *') -> "void":
    return _RNA.delete_floatP(ary)

def floatP_getitem(ary: 'float *', index: 'size_t') -> "float":
    return _RNA.floatP_getitem(ary, index)

def floatP_setitem(ary: 'float *', index: 'size_t', value: 'float') -> "void":
    return _RNA.floatP_setitem(ary, index, value)
class floatArray(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, nelements: 'size_t'):
        _RNA.floatArray_swiginit(self, _RNA.new_floatArray(nelements))
    __swig_destroy__ = _RNA.delete_floatArray

    def __getitem__(self, index: 'size_t') -> "float":
        return _RNA.floatArray___getitem__(self, index)

    def __setitem__(self, index: 'size_t', value: 'float') -> "void":
        return _RNA.floatArray___setitem__(self, index, value)

    def cast(self) -> "float *":
        return _RNA.floatArray_cast(self)

    @staticmethod
    def frompointer(t: 'float *') -> "floatArray *":
        return _RNA.floatArray_frompointer(t)

# Register floatArray in _RNA:
_RNA.floatArray_swigregister(floatArray)

def floatArray_frompointer(t: 'float *') -> "floatArray *":
    return _RNA.floatArray_frompointer(t)


def new_doubleP(nelements: 'size_t') -> "double *":
    return _RNA.new_doubleP(nelements)

def delete_doubleP(ary: 'double *') -> "void":
    return _RNA.delete_doubleP(ary)

def doubleP_getitem(ary: 'double *', index: 'size_t') -> "double":
    return _RNA.doubleP_getitem(ary, index)

def doubleP_setitem(ary: 'double *', index: 'size_t', value: 'double') -> "void":
    return _RNA.doubleP_setitem(ary, index, value)
class doubleArray(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, nelements: 'size_t'):
        _RNA.doubleArray_swiginit(self, _RNA.new_doubleArray(nelements))
    __swig_destroy__ = _RNA.delete_doubleArray

    def __getitem__(self, index: 'size_t') -> "double":
        return _RNA.doubleArray___getitem__(self, index)

    def __setitem__(self, index: 'size_t', value: 'double') -> "void":
        return _RNA.doubleArray___setitem__(self, index, value)

    def cast(self) -> "double *":
        return _RNA.doubleArray_cast(self)

    @staticmethod
    def frompointer(t: 'double *') -> "doubleArray *":
        return _RNA.doubleArray_frompointer(t)

# Register doubleArray in _RNA:
_RNA.doubleArray_swigregister(doubleArray)

def doubleArray_frompointer(t: 'double *') -> "doubleArray *":
    return _RNA.doubleArray_frompointer(t)


def new_ushortP(nelements: 'size_t') -> "unsigned short *":
    return _RNA.new_ushortP(nelements)

def delete_ushortP(ary: 'unsigned short *') -> "void":
    return _RNA.delete_ushortP(ary)

def ushortP_getitem(ary: 'unsigned short *', index: 'size_t') -> "unsigned short":
    return _RNA.ushortP_getitem(ary, index)

def ushortP_setitem(ary: 'unsigned short *', index: 'size_t', value: 'unsigned short') -> "void":
    return _RNA.ushortP_setitem(ary, index, value)

def new_shortP(nelements: 'size_t') -> "short *":
    return _RNA.new_shortP(nelements)

def delete_shortP(ary: 'short *') -> "void":
    return _RNA.delete_shortP(ary)

def shortP_getitem(ary: 'short *', index: 'size_t') -> "short":
    return _RNA.shortP_getitem(ary, index)

def shortP_setitem(ary: 'short *', index: 'size_t', value: 'short') -> "void":
    return _RNA.shortP_setitem(ary, index, value)

def cdata(ptr: 'void *', nelements: 'size_t'=1) -> "SWIGCDATA":
    return _RNA.cdata(ptr, nelements)

def memmove(data: 'void *', indata: 'void const *') -> "void":
    return _RNA.memmove(data, indata)

__version__ = '2.4.13'

class SwigPyIterator(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __swig_destroy__ = _RNA.delete_SwigPyIterator

    def value(self) -> "PyObject *":
        return _RNA.SwigPyIterator_value(self)

    def incr(self, n: 'size_t'=1) -> "swig::SwigPyIterator *":
        return _RNA.SwigPyIterator_incr(self, n)

    def decr(self, n: 'size_t'=1) -> "swig::SwigPyIterator *":
        return _RNA.SwigPyIterator_decr(self, n)

    def distance(self, x: 'SwigPyIterator') -> "ptrdiff_t":
        return _RNA.SwigPyIterator_distance(self, x)

    def equal(self, x: 'SwigPyIterator') -> "bool":
        return _RNA.SwigPyIterator_equal(self, x)

    def copy(self) -> "swig::SwigPyIterator *":
        return _RNA.SwigPyIterator_copy(self)

    def next(self) -> "PyObject *":
        return _RNA.SwigPyIterator_next(self)

    def __next__(self) -> "PyObject *":
        return _RNA.SwigPyIterator___next__(self)

    def previous(self) -> "PyObject *":
        return _RNA.SwigPyIterator_previous(self)

    def advance(self, n: 'ptrdiff_t') -> "swig::SwigPyIterator *":
        return _RNA.SwigPyIterator_advance(self, n)

    def __eq__(self, x: 'SwigPyIterator') -> "bool":
        return _RNA.SwigPyIterator___eq__(self, x)

    def __ne__(self, x: 'SwigPyIterator') -> "bool":
        return _RNA.SwigPyIterator___ne__(self, x)

    def __iadd__(self, n: 'ptrdiff_t') -> "swig::SwigPyIterator &":
        return _RNA.SwigPyIterator___iadd__(self, n)

    def __isub__(self, n: 'ptrdiff_t') -> "swig::SwigPyIterator &":
        return _RNA.SwigPyIterator___isub__(self, n)

    def __add__(self, n: 'ptrdiff_t') -> "swig::SwigPyIterator *":
        return _RNA.SwigPyIterator___add__(self, n)

    def __sub__(self, *args) -> "ptrdiff_t":
        return _RNA.SwigPyIterator___sub__(self, *args)
    def __iter__(self):
        return self

# Register SwigPyIterator in _RNA:
_RNA.SwigPyIterator_swigregister(SwigPyIterator)

class DoublePair(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        _RNA.DoublePair_swiginit(self, _RNA.new_DoublePair(*args))
    first = property(_RNA.DoublePair_first_get, _RNA.DoublePair_first_set)
    second = property(_RNA.DoublePair_second_get, _RNA.DoublePair_second_set)
    def __len__(self):
        return 2
    def __repr__(self):
        return str((self.first, self.second))
    def __getitem__(self, index):
        if not (index % 2):
            return self.first
        else:
            return self.second
    def __setitem__(self, index, val):
        if not (index % 2):
            self.first = val
        else:
            self.second = val
    __swig_destroy__ = _RNA.delete_DoublePair

# Register DoublePair in _RNA:
_RNA.DoublePair_swigregister(DoublePair)

class IntVector(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def iterator(self) -> "swig::SwigPyIterator *":
        return _RNA.IntVector_iterator(self)
    def __iter__(self):
        return self.iterator()

    def __nonzero__(self) -> "bool":
        return _RNA.IntVector___nonzero__(self)

    def __bool__(self) -> "bool":
        return _RNA.IntVector___bool__(self)

    def __len__(self) -> "std::vector< int >::size_type":
        return _RNA.IntVector___len__(self)

    def __getslice__(self, i: 'std::vector< int >::difference_type', j: 'std::vector< int >::difference_type') -> "std::vector< int,std::allocator< int > > *":
        return _RNA.IntVector___getslice__(self, i, j)

    def __setslice__(self, *args) -> "void":
        return _RNA.IntVector___setslice__(self, *args)

    def __delslice__(self, i: 'std::vector< int >::difference_type', j: 'std::vector< int >::difference_type') -> "void":
        return _RNA.IntVector___delslice__(self, i, j)

    def __delitem__(self, *args) -> "void":
        return _RNA.IntVector___delitem__(self, *args)

    def __getitem__(self, *args) -> "std::vector< int >::value_type const &":
        return _RNA.IntVector___getitem__(self, *args)

    def __setitem__(self, *args) -> "void":
        return _RNA.IntVector___setitem__(self, *args)

    def pop(self) -> "std::vector< int >::value_type":
        return _RNA.IntVector_pop(self)

    def append(self, x: 'std::vector< int >::value_type const &') -> "void":
        return _RNA.IntVector_append(self, x)

    def empty(self) -> "bool":
        return _RNA.IntVector_empty(self)

    def size(self) -> "std::vector< int >::size_type":
        return _RNA.IntVector_size(self)

    def swap(self, v: 'IntVector') -> "void":
        return _RNA.IntVector_swap(self, v)

    def begin(self) -> "std::vector< int >::iterator":
        return _RNA.IntVector_begin(self)

    def end(self) -> "std::vector< int >::iterator":
        return _RNA.IntVector_end(self)

    def rbegin(self) -> "std::vector< int >::reverse_iterator":
        return _RNA.IntVector_rbegin(self)

    def rend(self) -> "std::vector< int >::reverse_iterator":
        return _RNA.IntVector_rend(self)

    def clear(self) -> "void":
        return _RNA.IntVector_clear(self)

    def get_allocator(self) -> "std::vector< int >::allocator_type":
        return _RNA.IntVector_get_allocator(self)

    def pop_back(self) -> "void":
        return _RNA.IntVector_pop_back(self)

    def erase(self, *args) -> "std::vector< int >::iterator":
        return _RNA.IntVector_erase(self, *args)

    def __init__(self, *args):
        _RNA.IntVector_swiginit(self, _RNA.new_IntVector(*args))

    def push_back(self, x: 'std::vector< int >::value_type const &') -> "void":
        return _RNA.IntVector_push_back(self, x)

    def front(self) -> "std::vector< int >::value_type const &":
        return _RNA.IntVector_front(self)

    def back(self) -> "std::vector< int >::value_type const &":
        return _RNA.IntVector_back(self)

    def assign(self, n: 'std::vector< int >::size_type', x: 'std::vector< int >::value_type const &') -> "void":
        return _RNA.IntVector_assign(self, n, x)

    def resize(self, *args) -> "void":
        return _RNA.IntVector_resize(self, *args)

    def insert(self, *args) -> "void":
        return _RNA.IntVector_insert(self, *args)

    def reserve(self, n: 'std::vector< int >::size_type') -> "void":
        return _RNA.IntVector_reserve(self, n)

    def capacity(self) -> "std::vector< int >::size_type":
        return _RNA.IntVector_capacity(self)
    __swig_destroy__ = _RNA.delete_IntVector

# Register IntVector in _RNA:
_RNA.IntVector_swigregister(IntVector)

class UIntVector(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def iterator(self) -> "swig::SwigPyIterator *":
        return _RNA.UIntVector_iterator(self)
    def __iter__(self):
        return self.iterator()

    def __nonzero__(self) -> "bool":
        return _RNA.UIntVector___nonzero__(self)

    def __bool__(self) -> "bool":
        return _RNA.UIntVector___bool__(self)

    def __len__(self) -> "std::vector< unsigned int >::size_type":
        return _RNA.UIntVector___len__(self)

    def __getslice__(self, i: 'std::vector< unsigned int >::difference_type', j: 'std::vector< unsigned int >::difference_type') -> "std::vector< unsigned int,std::allocator< unsigned int > > *":
        return _RNA.UIntVector___getslice__(self, i, j)

    def __setslice__(self, *args) -> "void":
        return _RNA.UIntVector___setslice__(self, *args)

    def __delslice__(self, i: 'std::vector< unsigned int >::difference_type', j: 'std::vector< unsigned int >::difference_type') -> "void":
        return _RNA.UIntVector___delslice__(self, i, j)

    def __delitem__(self, *args) -> "void":
        return _RNA.UIntVector___delitem__(self, *args)

    def __getitem__(self, *args) -> "std::vector< unsigned int >::value_type const &":
        return _RNA.UIntVector___getitem__(self, *args)

    def __setitem__(self, *args) -> "void":
        return _RNA.UIntVector___setitem__(self, *args)

    def pop(self) -> "std::vector< unsigned int >::value_type":
        return _RNA.UIntVector_pop(self)

    def append(self, x: 'std::vector< unsigned int >::value_type const &') -> "void":
        return _RNA.UIntVector_append(self, x)

    def empty(self) -> "bool":
        return _RNA.UIntVector_empty(self)

    def size(self) -> "std::vector< unsigned int >::size_type":
        return _RNA.UIntVector_size(self)

    def swap(self, v: 'UIntVector') -> "void":
        return _RNA.UIntVector_swap(self, v)

    def begin(self) -> "std::vector< unsigned int >::iterator":
        return _RNA.UIntVector_begin(self)

    def end(self) -> "std::vector< unsigned int >::iterator":
        return _RNA.UIntVector_end(self)

    def rbegin(self) -> "std::vector< unsigned int >::reverse_iterator":
        return _RNA.UIntVector_rbegin(self)

    def rend(self) -> "std::vector< unsigned int >::reverse_iterator":
        return _RNA.UIntVector_rend(self)

    def clear(self) -> "void":
        return _RNA.UIntVector_clear(self)

    def get_allocator(self) -> "std::vector< unsigned int >::allocator_type":
        return _RNA.UIntVector_get_allocator(self)

    def pop_back(self) -> "void":
        return _RNA.UIntVector_pop_back(self)

    def erase(self, *args) -> "std::vector< unsigned int >::iterator":
        return _RNA.UIntVector_erase(self, *args)

    def __init__(self, *args):
        _RNA.UIntVector_swiginit(self, _RNA.new_UIntVector(*args))

    def push_back(self, x: 'std::vector< unsigned int >::value_type const &') -> "void":
        return _RNA.UIntVector_push_back(self, x)

    def front(self) -> "std::vector< unsigned int >::value_type const &":
        return _RNA.UIntVector_front(self)

    def back(self) -> "std::vector< unsigned int >::value_type const &":
        return _RNA.UIntVector_back(self)

    def assign(self, n: 'std::vector< unsigned int >::size_type', x: 'std::vector< unsigned int >::value_type const &') -> "void":
        return _RNA.UIntVector_assign(self, n, x)

    def resize(self, *args) -> "void":
        return _RNA.UIntVector_resize(self, *args)

    def insert(self, *args) -> "void":
        return _RNA.UIntVector_insert(self, *args)

    def reserve(self, n: 'std::vector< unsigned int >::size_type') -> "void":
        return _RNA.UIntVector_reserve(self, n)

    def capacity(self) -> "std::vector< unsigned int >::size_type":
        return _RNA.UIntVector_capacity(self)
    __swig_destroy__ = _RNA.delete_UIntVector

# Register UIntVector in _RNA:
_RNA.UIntVector_swigregister(UIntVector)

class DoubleVector(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def iterator(self) -> "swig::SwigPyIterator *":
        return _RNA.DoubleVector_iterator(self)
    def __iter__(self):
        return self.iterator()

    def __nonzero__(self) -> "bool":
        return _RNA.DoubleVector___nonzero__(self)

    def __bool__(self) -> "bool":
        return _RNA.DoubleVector___bool__(self)

    def __len__(self) -> "std::vector< double >::size_type":
        return _RNA.DoubleVector___len__(self)

    def __getslice__(self, i: 'std::vector< double >::difference_type', j: 'std::vector< double >::difference_type') -> "std::vector< double,std::allocator< double > > *":
        return _RNA.DoubleVector___getslice__(self, i, j)

    def __setslice__(self, *args) -> "void":
        return _RNA.DoubleVector___setslice__(self, *args)

    def __delslice__(self, i: 'std::vector< double >::difference_type', j: 'std::vector< double >::difference_type') -> "void":
        return _RNA.DoubleVector___delslice__(self, i, j)

    def __delitem__(self, *args) -> "void":
        return _RNA.DoubleVector___delitem__(self, *args)

    def __getitem__(self, *args) -> "std::vector< double >::value_type const &":
        return _RNA.DoubleVector___getitem__(self, *args)

    def __setitem__(self, *args) -> "void":
        return _RNA.DoubleVector___setitem__(self, *args)

    def pop(self) -> "std::vector< double >::value_type":
        return _RNA.DoubleVector_pop(self)

    def append(self, x: 'std::vector< double >::value_type const &') -> "void":
        return _RNA.DoubleVector_append(self, x)

    def empty(self) -> "bool":
        return _RNA.DoubleVector_empty(self)

    def size(self) -> "std::vector< double >::size_type":
        return _RNA.DoubleVector_size(self)

    def swap(self, v: 'DoubleVector') -> "void":
        return _RNA.DoubleVector_swap(self, v)

    def begin(self) -> "std::vector< double >::iterator":
        return _RNA.DoubleVector_begin(self)

    def end(self) -> "std::vector< double >::iterator":
        return _RNA.DoubleVector_end(self)

    def rbegin(self) -> "std::vector< double >::reverse_iterator":
        return _RNA.DoubleVector_rbegin(self)

    def rend(self) -> "std::vector< double >::reverse_iterator":
        return _RNA.DoubleVector_rend(self)

    def clear(self) -> "void":
        return _RNA.DoubleVector_clear(self)

    def get_allocator(self) -> "std::vector< double >::allocator_type":
        return _RNA.DoubleVector_get_allocator(self)

    def pop_back(self) -> "void":
        return _RNA.DoubleVector_pop_back(self)

    def erase(self, *args) -> "std::vector< double >::iterator":
        return _RNA.DoubleVector_erase(self, *args)

    def __init__(self, *args):
        _RNA.DoubleVector_swiginit(self, _RNA.new_DoubleVector(*args))

    def push_back(self, x: 'std::vector< double >::value_type const &') -> "void":
        return _RNA.DoubleVector_push_back(self, x)

    def front(self) -> "std::vector< double >::value_type const &":
        return _RNA.DoubleVector_front(self)

    def back(self) -> "std::vector< double >::value_type const &":
        return _RNA.DoubleVector_back(self)

    def assign(self, n: 'std::vector< double >::size_type', x: 'std::vector< double >::value_type const &') -> "void":
        return _RNA.DoubleVector_assign(self, n, x)

    def resize(self, *args) -> "void":
        return _RNA.DoubleVector_resize(self, *args)

    def insert(self, *args) -> "void":
        return _RNA.DoubleVector_insert(self, *args)

    def reserve(self, n: 'std::vector< double >::size_type') -> "void":
        return _RNA.DoubleVector_reserve(self, n)

    def capacity(self) -> "std::vector< double >::size_type":
        return _RNA.DoubleVector_capacity(self)
    __swig_destroy__ = _RNA.delete_DoubleVector

# Register DoubleVector in _RNA:
_RNA.DoubleVector_swigregister(DoubleVector)

class StringVector(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def iterator(self) -> "swig::SwigPyIterator *":
        return _RNA.StringVector_iterator(self)
    def __iter__(self):
        return self.iterator()

    def __nonzero__(self) -> "bool":
        return _RNA.StringVector___nonzero__(self)

    def __bool__(self) -> "bool":
        return _RNA.StringVector___bool__(self)

    def __len__(self) -> "std::vector< std::string >::size_type":
        return _RNA.StringVector___len__(self)

    def __getslice__(self, i: 'std::vector< std::string >::difference_type', j: 'std::vector< std::string >::difference_type') -> "std::vector< std::string,std::allocator< std::string > > *":
        return _RNA.StringVector___getslice__(self, i, j)

    def __setslice__(self, *args) -> "void":
        return _RNA.StringVector___setslice__(self, *args)

    def __delslice__(self, i: 'std::vector< std::string >::difference_type', j: 'std::vector< std::string >::difference_type') -> "void":
        return _RNA.StringVector___delslice__(self, i, j)

    def __delitem__(self, *args) -> "void":
        return _RNA.StringVector___delitem__(self, *args)

    def __getitem__(self, *args) -> "std::vector< std::string >::value_type const &":
        return _RNA.StringVector___getitem__(self, *args)

    def __setitem__(self, *args) -> "void":
        return _RNA.StringVector___setitem__(self, *args)

    def pop(self) -> "std::vector< std::string >::value_type":
        return _RNA.StringVector_pop(self)

    def append(self, x: 'std::vector< std::string >::value_type const &') -> "void":
        return _RNA.StringVector_append(self, x)

    def empty(self) -> "bool":
        return _RNA.StringVector_empty(self)

    def size(self) -> "std::vector< std::string >::size_type":
        return _RNA.StringVector_size(self)

    def swap(self, v: 'StringVector') -> "void":
        return _RNA.StringVector_swap(self, v)

    def begin(self) -> "std::vector< std::string >::iterator":
        return _RNA.StringVector_begin(self)

    def end(self) -> "std::vector< std::string >::iterator":
        return _RNA.StringVector_end(self)

    def rbegin(self) -> "std::vector< std::string >::reverse_iterator":
        return _RNA.StringVector_rbegin(self)

    def rend(self) -> "std::vector< std::string >::reverse_iterator":
        return _RNA.StringVector_rend(self)

    def clear(self) -> "void":
        return _RNA.StringVector_clear(self)

    def get_allocator(self) -> "std::vector< std::string >::allocator_type":
        return _RNA.StringVector_get_allocator(self)

    def pop_back(self) -> "void":
        return _RNA.StringVector_pop_back(self)

    def erase(self, *args) -> "std::vector< std::string >::iterator":
        return _RNA.StringVector_erase(self, *args)

    def __init__(self, *args):
        _RNA.StringVector_swiginit(self, _RNA.new_StringVector(*args))

    def push_back(self, x: 'std::vector< std::string >::value_type const &') -> "void":
        return _RNA.StringVector_push_back(self, x)

    def front(self) -> "std::vector< std::string >::value_type const &":
        return _RNA.StringVector_front(self)

    def back(self) -> "std::vector< std::string >::value_type const &":
        return _RNA.StringVector_back(self)

    def assign(self, n: 'std::vector< std::string >::size_type', x: 'std::vector< std::string >::value_type const &') -> "void":
        return _RNA.StringVector_assign(self, n, x)

    def resize(self, *args) -> "void":
        return _RNA.StringVector_resize(self, *args)

    def insert(self, *args) -> "void":
        return _RNA.StringVector_insert(self, *args)

    def reserve(self, n: 'std::vector< std::string >::size_type') -> "void":
        return _RNA.StringVector_reserve(self, n)

    def capacity(self) -> "std::vector< std::string >::size_type":
        return _RNA.StringVector_capacity(self)
    __swig_destroy__ = _RNA.delete_StringVector

# Register StringVector in _RNA:
_RNA.StringVector_swigregister(StringVector)

class ConstCharVector(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def iterator(self) -> "swig::SwigPyIterator *":
        return _RNA.ConstCharVector_iterator(self)
    def __iter__(self):
        return self.iterator()

    def __nonzero__(self) -> "bool":
        return _RNA.ConstCharVector___nonzero__(self)

    def __bool__(self) -> "bool":
        return _RNA.ConstCharVector___bool__(self)

    def __len__(self) -> "std::vector< char const * >::size_type":
        return _RNA.ConstCharVector___len__(self)

    def __getslice__(self, i: 'std::vector< char const * >::difference_type', j: 'std::vector< char const * >::difference_type') -> "std::vector< char const *,std::allocator< char const * > > *":
        return _RNA.ConstCharVector___getslice__(self, i, j)

    def __setslice__(self, *args) -> "void":
        return _RNA.ConstCharVector___setslice__(self, *args)

    def __delslice__(self, i: 'std::vector< char const * >::difference_type', j: 'std::vector< char const * >::difference_type') -> "void":
        return _RNA.ConstCharVector___delslice__(self, i, j)

    def __delitem__(self, *args) -> "void":
        return _RNA.ConstCharVector___delitem__(self, *args)

    def __getitem__(self, *args) -> "std::vector< char const * >::value_type":
        return _RNA.ConstCharVector___getitem__(self, *args)

    def __setitem__(self, *args) -> "void":
        return _RNA.ConstCharVector___setitem__(self, *args)

    def pop(self) -> "std::vector< char const * >::value_type":
        return _RNA.ConstCharVector_pop(self)

    def append(self, x: 'std::vector< char const * >::value_type') -> "void":
        return _RNA.ConstCharVector_append(self, x)

    def empty(self) -> "bool":
        return _RNA.ConstCharVector_empty(self)

    def size(self) -> "std::vector< char const * >::size_type":
        return _RNA.ConstCharVector_size(self)

    def swap(self, v: 'ConstCharVector') -> "void":
        return _RNA.ConstCharVector_swap(self, v)

    def begin(self) -> "std::vector< char const * >::iterator":
        return _RNA.ConstCharVector_begin(self)

    def end(self) -> "std::vector< char const * >::iterator":
        return _RNA.ConstCharVector_end(self)

    def rbegin(self) -> "std::vector< char const * >::reverse_iterator":
        return _RNA.ConstCharVector_rbegin(self)

    def rend(self) -> "std::vector< char const * >::reverse_iterator":
        return _RNA.ConstCharVector_rend(self)

    def clear(self) -> "void":
        return _RNA.ConstCharVector_clear(self)

    def get_allocator(self) -> "std::vector< char const * >::allocator_type":
        return _RNA.ConstCharVector_get_allocator(self)

    def pop_back(self) -> "void":
        return _RNA.ConstCharVector_pop_back(self)

    def erase(self, *args) -> "std::vector< char const * >::iterator":
        return _RNA.ConstCharVector_erase(self, *args)

    def __init__(self, *args):
        _RNA.ConstCharVector_swiginit(self, _RNA.new_ConstCharVector(*args))

    def push_back(self, x: 'std::vector< char const * >::value_type') -> "void":
        return _RNA.ConstCharVector_push_back(self, x)

    def front(self) -> "std::vector< char const * >::value_type":
        return _RNA.ConstCharVector_front(self)

    def back(self) -> "std::vector< char const * >::value_type":
        return _RNA.ConstCharVector_back(self)

    def assign(self, n: 'std::vector< char const * >::size_type', x: 'std::vector< char const * >::value_type') -> "void":
        return _RNA.ConstCharVector_assign(self, n, x)

    def resize(self, *args) -> "void":
        return _RNA.ConstCharVector_resize(self, *args)

    def insert(self, *args) -> "void":
        return _RNA.ConstCharVector_insert(self, *args)

    def reserve(self, n: 'std::vector< char const * >::size_type') -> "void":
        return _RNA.ConstCharVector_reserve(self, n)

    def capacity(self) -> "std::vector< char const * >::size_type":
        return _RNA.ConstCharVector_capacity(self)
    __swig_destroy__ = _RNA.delete_ConstCharVector

# Register ConstCharVector in _RNA:
_RNA.ConstCharVector_swigregister(ConstCharVector)

class SOLUTIONVector(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def iterator(self) -> "swig::SwigPyIterator *":
        return _RNA.SOLUTIONVector_iterator(self)
    def __iter__(self):
        return self.iterator()

    def __nonzero__(self) -> "bool":
        return _RNA.SOLUTIONVector___nonzero__(self)

    def __bool__(self) -> "bool":
        return _RNA.SOLUTIONVector___bool__(self)

    def __len__(self) -> "std::vector< SOLUTION >::size_type":
        return _RNA.SOLUTIONVector___len__(self)

    def __getslice__(self, i: 'std::vector< SOLUTION >::difference_type', j: 'std::vector< SOLUTION >::difference_type') -> "std::vector< SOLUTION,std::allocator< SOLUTION > > *":
        return _RNA.SOLUTIONVector___getslice__(self, i, j)

    def __setslice__(self, *args) -> "void":
        return _RNA.SOLUTIONVector___setslice__(self, *args)

    def __delslice__(self, i: 'std::vector< SOLUTION >::difference_type', j: 'std::vector< SOLUTION >::difference_type') -> "void":
        return _RNA.SOLUTIONVector___delslice__(self, i, j)

    def __delitem__(self, *args) -> "void":
        return _RNA.SOLUTIONVector___delitem__(self, *args)

    def __getitem__(self, *args) -> "std::vector< SOLUTION >::value_type const &":
        return _RNA.SOLUTIONVector___getitem__(self, *args)

    def __setitem__(self, *args) -> "void":
        return _RNA.SOLUTIONVector___setitem__(self, *args)

    def pop(self) -> "std::vector< SOLUTION >::value_type":
        return _RNA.SOLUTIONVector_pop(self)

    def append(self, x: 'SOLUTION') -> "void":
        return _RNA.SOLUTIONVector_append(self, x)

    def empty(self) -> "bool":
        return _RNA.SOLUTIONVector_empty(self)

    def size(self) -> "std::vector< SOLUTION >::size_type":
        return _RNA.SOLUTIONVector_size(self)

    def swap(self, v: 'SOLUTIONVector') -> "void":
        return _RNA.SOLUTIONVector_swap(self, v)

    def begin(self) -> "std::vector< SOLUTION >::iterator":
        return _RNA.SOLUTIONVector_begin(self)

    def end(self) -> "std::vector< SOLUTION >::iterator":
        return _RNA.SOLUTIONVector_end(self)

    def rbegin(self) -> "std::vector< SOLUTION >::reverse_iterator":
        return _RNA.SOLUTIONVector_rbegin(self)

    def rend(self) -> "std::vector< SOLUTION >::reverse_iterator":
        return _RNA.SOLUTIONVector_rend(self)

    def clear(self) -> "void":
        return _RNA.SOLUTIONVector_clear(self)

    def get_allocator(self) -> "std::vector< SOLUTION >::allocator_type":
        return _RNA.SOLUTIONVector_get_allocator(self)

    def pop_back(self) -> "void":
        return _RNA.SOLUTIONVector_pop_back(self)

    def erase(self, *args) -> "std::vector< SOLUTION >::iterator":
        return _RNA.SOLUTIONVector_erase(self, *args)

    def __init__(self, *args):
        _RNA.SOLUTIONVector_swiginit(self, _RNA.new_SOLUTIONVector(*args))

    def push_back(self, x: 'SOLUTION') -> "void":
        return _RNA.SOLUTIONVector_push_back(self, x)

    def front(self) -> "std::vector< SOLUTION >::value_type const &":
        return _RNA.SOLUTIONVector_front(self)

    def back(self) -> "std::vector< SOLUTION >::value_type const &":
        return _RNA.SOLUTIONVector_back(self)

    def assign(self, n: 'std::vector< SOLUTION >::size_type', x: 'SOLUTION') -> "void":
        return _RNA.SOLUTIONVector_assign(self, n, x)

    def resize(self, *args) -> "void":
        return _RNA.SOLUTIONVector_resize(self, *args)

    def insert(self, *args) -> "void":
        return _RNA.SOLUTIONVector_insert(self, *args)

    def reserve(self, n: 'std::vector< SOLUTION >::size_type') -> "void":
        return _RNA.SOLUTIONVector_reserve(self, n)

    def capacity(self) -> "std::vector< SOLUTION >::size_type":
        return _RNA.SOLUTIONVector_capacity(self)
    __swig_destroy__ = _RNA.delete_SOLUTIONVector

# Register SOLUTIONVector in _RNA:
_RNA.SOLUTIONVector_swigregister(SOLUTIONVector)

class CoordinateVector(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def iterator(self) -> "swig::SwigPyIterator *":
        return _RNA.CoordinateVector_iterator(self)
    def __iter__(self):
        return self.iterator()

    def __nonzero__(self) -> "bool":
        return _RNA.CoordinateVector___nonzero__(self)

    def __bool__(self) -> "bool":
        return _RNA.CoordinateVector___bool__(self)

    def __len__(self) -> "std::vector< COORDINATE >::size_type":
        return _RNA.CoordinateVector___len__(self)

    def __getslice__(self, i: 'std::vector< COORDINATE >::difference_type', j: 'std::vector< COORDINATE >::difference_type') -> "std::vector< COORDINATE,std::allocator< COORDINATE > > *":
        return _RNA.CoordinateVector___getslice__(self, i, j)

    def __setslice__(self, *args) -> "void":
        return _RNA.CoordinateVector___setslice__(self, *args)

    def __delslice__(self, i: 'std::vector< COORDINATE >::difference_type', j: 'std::vector< COORDINATE >::difference_type') -> "void":
        return _RNA.CoordinateVector___delslice__(self, i, j)

    def __delitem__(self, *args) -> "void":
        return _RNA.CoordinateVector___delitem__(self, *args)

    def __getitem__(self, *args) -> "std::vector< COORDINATE >::value_type const &":
        return _RNA.CoordinateVector___getitem__(self, *args)

    def __setitem__(self, *args) -> "void":
        return _RNA.CoordinateVector___setitem__(self, *args)

    def pop(self) -> "std::vector< COORDINATE >::value_type":
        return _RNA.CoordinateVector_pop(self)

    def append(self, x: 'COORDINATE') -> "void":
        return _RNA.CoordinateVector_append(self, x)

    def empty(self) -> "bool":
        return _RNA.CoordinateVector_empty(self)

    def size(self) -> "std::vector< COORDINATE >::size_type":
        return _RNA.CoordinateVector_size(self)

    def swap(self, v: 'CoordinateVector') -> "void":
        return _RNA.CoordinateVector_swap(self, v)

    def begin(self) -> "std::vector< COORDINATE >::iterator":
        return _RNA.CoordinateVector_begin(self)

    def end(self) -> "std::vector< COORDINATE >::iterator":
        return _RNA.CoordinateVector_end(self)

    def rbegin(self) -> "std::vector< COORDINATE >::reverse_iterator":
        return _RNA.CoordinateVector_rbegin(self)

    def rend(self) -> "std::vector< COORDINATE >::reverse_iterator":
        return _RNA.CoordinateVector_rend(self)

    def clear(self) -> "void":
        return _RNA.CoordinateVector_clear(self)

    def get_allocator(self) -> "std::vector< COORDINATE >::allocator_type":
        return _RNA.CoordinateVector_get_allocator(self)

    def pop_back(self) -> "void":
        return _RNA.CoordinateVector_pop_back(self)

    def erase(self, *args) -> "std::vector< COORDINATE >::iterator":
        return _RNA.CoordinateVector_erase(self, *args)

    def __init__(self, *args):
        _RNA.CoordinateVector_swiginit(self, _RNA.new_CoordinateVector(*args))

    def push_back(self, x: 'COORDINATE') -> "void":
        return _RNA.CoordinateVector_push_back(self, x)

    def front(self) -> "std::vector< COORDINATE >::value_type const &":
        return _RNA.CoordinateVector_front(self)

    def back(self) -> "std::vector< COORDINATE >::value_type const &":
        return _RNA.CoordinateVector_back(self)

    def assign(self, n: 'std::vector< COORDINATE >::size_type', x: 'COORDINATE') -> "void":
        return _RNA.CoordinateVector_assign(self, n, x)

    def resize(self, *args) -> "void":
        return _RNA.CoordinateVector_resize(self, *args)

    def insert(self, *args) -> "void":
        return _RNA.CoordinateVector_insert(self, *args)

    def reserve(self, n: 'std::vector< COORDINATE >::size_type') -> "void":
        return _RNA.CoordinateVector_reserve(self, n)

    def capacity(self) -> "std::vector< COORDINATE >::size_type":
        return _RNA.CoordinateVector_capacity(self)
    __swig_destroy__ = _RNA.delete_CoordinateVector

# Register CoordinateVector in _RNA:
_RNA.CoordinateVector_swigregister(CoordinateVector)

class DoubleDoubleVector(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def iterator(self) -> "swig::SwigPyIterator *":
        return _RNA.DoubleDoubleVector_iterator(self)
    def __iter__(self):
        return self.iterator()

    def __nonzero__(self) -> "bool":
        return _RNA.DoubleDoubleVector___nonzero__(self)

    def __bool__(self) -> "bool":
        return _RNA.DoubleDoubleVector___bool__(self)

    def __len__(self) -> "std::vector< std::vector< double > >::size_type":
        return _RNA.DoubleDoubleVector___len__(self)

    def __getslice__(self, i: 'std::vector< std::vector< double > >::difference_type', j: 'std::vector< std::vector< double > >::difference_type') -> "std::vector< std::vector< double,std::allocator< double > >,std::allocator< std::vector< double,std::allocator< double > > > > *":
        return _RNA.DoubleDoubleVector___getslice__(self, i, j)

    def __setslice__(self, *args) -> "void":
        return _RNA.DoubleDoubleVector___setslice__(self, *args)

    def __delslice__(self, i: 'std::vector< std::vector< double > >::difference_type', j: 'std::vector< std::vector< double > >::difference_type') -> "void":
        return _RNA.DoubleDoubleVector___delslice__(self, i, j)

    def __delitem__(self, *args) -> "void":
        return _RNA.DoubleDoubleVector___delitem__(self, *args)

    def __getitem__(self, *args) -> "std::vector< std::vector< double > >::value_type const &":
        return _RNA.DoubleDoubleVector___getitem__(self, *args)

    def __setitem__(self, *args) -> "void":
        return _RNA.DoubleDoubleVector___setitem__(self, *args)

    def pop(self) -> "std::vector< std::vector< double > >::value_type":
        return _RNA.DoubleDoubleVector_pop(self)

    def append(self, x: 'DoubleVector') -> "void":
        return _RNA.DoubleDoubleVector_append(self, x)

    def empty(self) -> "bool":
        return _RNA.DoubleDoubleVector_empty(self)

    def size(self) -> "std::vector< std::vector< double > >::size_type":
        return _RNA.DoubleDoubleVector_size(self)

    def swap(self, v: 'DoubleDoubleVector') -> "void":
        return _RNA.DoubleDoubleVector_swap(self, v)

    def begin(self) -> "std::vector< std::vector< double > >::iterator":
        return _RNA.DoubleDoubleVector_begin(self)

    def end(self) -> "std::vector< std::vector< double > >::iterator":
        return _RNA.DoubleDoubleVector_end(self)

    def rbegin(self) -> "std::vector< std::vector< double > >::reverse_iterator":
        return _RNA.DoubleDoubleVector_rbegin(self)

    def rend(self) -> "std::vector< std::vector< double > >::reverse_iterator":
        return _RNA.DoubleDoubleVector_rend(self)

    def clear(self) -> "void":
        return _RNA.DoubleDoubleVector_clear(self)

    def get_allocator(self) -> "std::vector< std::vector< double > >::allocator_type":
        return _RNA.DoubleDoubleVector_get_allocator(self)

    def pop_back(self) -> "void":
        return _RNA.DoubleDoubleVector_pop_back(self)

    def erase(self, *args) -> "std::vector< std::vector< double > >::iterator":
        return _RNA.DoubleDoubleVector_erase(self, *args)

    def __init__(self, *args):
        _RNA.DoubleDoubleVector_swiginit(self, _RNA.new_DoubleDoubleVector(*args))

    def push_back(self, x: 'DoubleVector') -> "void":
        return _RNA.DoubleDoubleVector_push_back(self, x)

    def front(self) -> "std::vector< std::vector< double > >::value_type const &":
        return _RNA.DoubleDoubleVector_front(self)

    def back(self) -> "std::vector< std::vector< double > >::value_type const &":
        return _RNA.DoubleDoubleVector_back(self)

    def assign(self, n: 'std::vector< std::vector< double > >::size_type', x: 'DoubleVector') -> "void":
        return _RNA.DoubleDoubleVector_assign(self, n, x)

    def resize(self, *args) -> "void":
        return _RNA.DoubleDoubleVector_resize(self, *args)

    def insert(self, *args) -> "void":
        return _RNA.DoubleDoubleVector_insert(self, *args)

    def reserve(self, n: 'std::vector< std::vector< double > >::size_type') -> "void":
        return _RNA.DoubleDoubleVector_reserve(self, n)

    def capacity(self) -> "std::vector< std::vector< double > >::size_type":
        return _RNA.DoubleDoubleVector_capacity(self)
    __swig_destroy__ = _RNA.delete_DoubleDoubleVector

# Register DoubleDoubleVector in _RNA:
_RNA.DoubleDoubleVector_swigregister(DoubleDoubleVector)

class IntIntVector(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def iterator(self) -> "swig::SwigPyIterator *":
        return _RNA.IntIntVector_iterator(self)
    def __iter__(self):
        return self.iterator()

    def __nonzero__(self) -> "bool":
        return _RNA.IntIntVector___nonzero__(self)

    def __bool__(self) -> "bool":
        return _RNA.IntIntVector___bool__(self)

    def __len__(self) -> "std::vector< std::vector< int > >::size_type":
        return _RNA.IntIntVector___len__(self)

    def __getslice__(self, i: 'std::vector< std::vector< int > >::difference_type', j: 'std::vector< std::vector< int > >::difference_type') -> "std::vector< std::vector< int,std::allocator< int > >,std::allocator< std::vector< int,std::allocator< int > > > > *":
        return _RNA.IntIntVector___getslice__(self, i, j)

    def __setslice__(self, *args) -> "void":
        return _RNA.IntIntVector___setslice__(self, *args)

    def __delslice__(self, i: 'std::vector< std::vector< int > >::difference_type', j: 'std::vector< std::vector< int > >::difference_type') -> "void":
        return _RNA.IntIntVector___delslice__(self, i, j)

    def __delitem__(self, *args) -> "void":
        return _RNA.IntIntVector___delitem__(self, *args)

    def __getitem__(self, *args) -> "std::vector< std::vector< int > >::value_type const &":
        return _RNA.IntIntVector___getitem__(self, *args)

    def __setitem__(self, *args) -> "void":
        return _RNA.IntIntVector___setitem__(self, *args)

    def pop(self) -> "std::vector< std::vector< int > >::value_type":
        return _RNA.IntIntVector_pop(self)

    def append(self, x: 'IntVector') -> "void":
        return _RNA.IntIntVector_append(self, x)

    def empty(self) -> "bool":
        return _RNA.IntIntVector_empty(self)

    def size(self) -> "std::vector< std::vector< int > >::size_type":
        return _RNA.IntIntVector_size(self)

    def swap(self, v: 'IntIntVector') -> "void":
        return _RNA.IntIntVector_swap(self, v)

    def begin(self) -> "std::vector< std::vector< int > >::iterator":
        return _RNA.IntIntVector_begin(self)

    def end(self) -> "std::vector< std::vector< int > >::iterator":
        return _RNA.IntIntVector_end(self)

    def rbegin(self) -> "std::vector< std::vector< int > >::reverse_iterator":
        return _RNA.IntIntVector_rbegin(self)

    def rend(self) -> "std::vector< std::vector< int > >::reverse_iterator":
        return _RNA.IntIntVector_rend(self)

    def clear(self) -> "void":
        return _RNA.IntIntVector_clear(self)

    def get_allocator(self) -> "std::vector< std::vector< int > >::allocator_type":
        return _RNA.IntIntVector_get_allocator(self)

    def pop_back(self) -> "void":
        return _RNA.IntIntVector_pop_back(self)

    def erase(self, *args) -> "std::vector< std::vector< int > >::iterator":
        return _RNA.IntIntVector_erase(self, *args)

    def __init__(self, *args):
        _RNA.IntIntVector_swiginit(self, _RNA.new_IntIntVector(*args))

    def push_back(self, x: 'IntVector') -> "void":
        return _RNA.IntIntVector_push_back(self, x)

    def front(self) -> "std::vector< std::vector< int > >::value_type const &":
        return _RNA.IntIntVector_front(self)

    def back(self) -> "std::vector< std::vector< int > >::value_type const &":
        return _RNA.IntIntVector_back(self)

    def assign(self, n: 'std::vector< std::vector< int > >::size_type', x: 'IntVector') -> "void":
        return _RNA.IntIntVector_assign(self, n, x)

    def resize(self, *args) -> "void":
        return _RNA.IntIntVector_resize(self, *args)

    def insert(self, *args) -> "void":
        return _RNA.IntIntVector_insert(self, *args)

    def reserve(self, n: 'std::vector< std::vector< int > >::size_type') -> "void":
        return _RNA.IntIntVector_reserve(self, n)

    def capacity(self) -> "std::vector< std::vector< int > >::size_type":
        return _RNA.IntIntVector_capacity(self)
    __swig_destroy__ = _RNA.delete_IntIntVector

# Register IntIntVector in _RNA:
_RNA.IntIntVector_swigregister(IntIntVector)

class ElemProbVector(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def iterator(self) -> "swig::SwigPyIterator *":
        return _RNA.ElemProbVector_iterator(self)
    def __iter__(self):
        return self.iterator()

    def __nonzero__(self) -> "bool":
        return _RNA.ElemProbVector___nonzero__(self)

    def __bool__(self) -> "bool":
        return _RNA.ElemProbVector___bool__(self)

    def __len__(self) -> "std::vector< vrna_ep_t >::size_type":
        return _RNA.ElemProbVector___len__(self)

    def __getslice__(self, i: 'std::vector< vrna_ep_t >::difference_type', j: 'std::vector< vrna_ep_t >::difference_type') -> "std::vector< vrna_ep_t,std::allocator< vrna_ep_t > > *":
        return _RNA.ElemProbVector___getslice__(self, i, j)

    def __setslice__(self, *args) -> "void":
        return _RNA.ElemProbVector___setslice__(self, *args)

    def __delslice__(self, i: 'std::vector< vrna_ep_t >::difference_type', j: 'std::vector< vrna_ep_t >::difference_type') -> "void":
        return _RNA.ElemProbVector___delslice__(self, i, j)

    def __delitem__(self, *args) -> "void":
        return _RNA.ElemProbVector___delitem__(self, *args)

    def __getitem__(self, *args) -> "std::vector< vrna_ep_t >::value_type const &":
        return _RNA.ElemProbVector___getitem__(self, *args)

    def __setitem__(self, *args) -> "void":
        return _RNA.ElemProbVector___setitem__(self, *args)

    def pop(self) -> "std::vector< vrna_ep_t >::value_type":
        return _RNA.ElemProbVector_pop(self)

    def append(self, x: 'ep') -> "void":
        return _RNA.ElemProbVector_append(self, x)

    def empty(self) -> "bool":
        return _RNA.ElemProbVector_empty(self)

    def size(self) -> "std::vector< vrna_ep_t >::size_type":
        return _RNA.ElemProbVector_size(self)

    def swap(self, v: 'ElemProbVector') -> "void":
        return _RNA.ElemProbVector_swap(self, v)

    def begin(self) -> "std::vector< vrna_ep_t >::iterator":
        return _RNA.ElemProbVector_begin(self)

    def end(self) -> "std::vector< vrna_ep_t >::iterator":
        return _RNA.ElemProbVector_end(self)

    def rbegin(self) -> "std::vector< vrna_ep_t >::reverse_iterator":
        return _RNA.ElemProbVector_rbegin(self)

    def rend(self) -> "std::vector< vrna_ep_t >::reverse_iterator":
        return _RNA.ElemProbVector_rend(self)

    def clear(self) -> "void":
        return _RNA.ElemProbVector_clear(self)

    def get_allocator(self) -> "std::vector< vrna_ep_t >::allocator_type":
        return _RNA.ElemProbVector_get_allocator(self)

    def pop_back(self) -> "void":
        return _RNA.ElemProbVector_pop_back(self)

    def erase(self, *args) -> "std::vector< vrna_ep_t >::iterator":
        return _RNA.ElemProbVector_erase(self, *args)

    def __init__(self, *args):
        _RNA.ElemProbVector_swiginit(self, _RNA.new_ElemProbVector(*args))

    def push_back(self, x: 'ep') -> "void":
        return _RNA.ElemProbVector_push_back(self, x)

    def front(self) -> "std::vector< vrna_ep_t >::value_type const &":
        return _RNA.ElemProbVector_front(self)

    def back(self) -> "std::vector< vrna_ep_t >::value_type const &":
        return _RNA.ElemProbVector_back(self)

    def assign(self, n: 'std::vector< vrna_ep_t >::size_type', x: 'ep') -> "void":
        return _RNA.ElemProbVector_assign(self, n, x)

    def resize(self, *args) -> "void":
        return _RNA.ElemProbVector_resize(self, *args)

    def insert(self, *args) -> "void":
        return _RNA.ElemProbVector_insert(self, *args)

    def reserve(self, n: 'std::vector< vrna_ep_t >::size_type') -> "void":
        return _RNA.ElemProbVector_reserve(self, n)

    def capacity(self) -> "std::vector< vrna_ep_t >::size_type":
        return _RNA.ElemProbVector_capacity(self)
    __swig_destroy__ = _RNA.delete_ElemProbVector

# Register ElemProbVector in _RNA:
_RNA.ElemProbVector_swigregister(ElemProbVector)

class PathVector(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def iterator(self) -> "swig::SwigPyIterator *":
        return _RNA.PathVector_iterator(self)
    def __iter__(self):
        return self.iterator()

    def __nonzero__(self) -> "bool":
        return _RNA.PathVector___nonzero__(self)

    def __bool__(self) -> "bool":
        return _RNA.PathVector___bool__(self)

    def __len__(self) -> "std::vector< vrna_path_t >::size_type":
        return _RNA.PathVector___len__(self)

    def __getslice__(self, i: 'std::vector< vrna_path_t >::difference_type', j: 'std::vector< vrna_path_t >::difference_type') -> "std::vector< vrna_path_t,std::allocator< vrna_path_t > > *":
        return _RNA.PathVector___getslice__(self, i, j)

    def __setslice__(self, *args) -> "void":
        return _RNA.PathVector___setslice__(self, *args)

    def __delslice__(self, i: 'std::vector< vrna_path_t >::difference_type', j: 'std::vector< vrna_path_t >::difference_type') -> "void":
        return _RNA.PathVector___delslice__(self, i, j)

    def __delitem__(self, *args) -> "void":
        return _RNA.PathVector___delitem__(self, *args)

    def __getitem__(self, *args) -> "std::vector< vrna_path_t >::value_type const &":
        return _RNA.PathVector___getitem__(self, *args)

    def __setitem__(self, *args) -> "void":
        return _RNA.PathVector___setitem__(self, *args)

    def pop(self) -> "std::vector< vrna_path_t >::value_type":
        return _RNA.PathVector_pop(self)

    def append(self, x: 'path') -> "void":
        return _RNA.PathVector_append(self, x)

    def empty(self) -> "bool":
        return _RNA.PathVector_empty(self)

    def size(self) -> "std::vector< vrna_path_t >::size_type":
        return _RNA.PathVector_size(self)

    def swap(self, v: 'PathVector') -> "void":
        return _RNA.PathVector_swap(self, v)

    def begin(self) -> "std::vector< vrna_path_t >::iterator":
        return _RNA.PathVector_begin(self)

    def end(self) -> "std::vector< vrna_path_t >::iterator":
        return _RNA.PathVector_end(self)

    def rbegin(self) -> "std::vector< vrna_path_t >::reverse_iterator":
        return _RNA.PathVector_rbegin(self)

    def rend(self) -> "std::vector< vrna_path_t >::reverse_iterator":
        return _RNA.PathVector_rend(self)

    def clear(self) -> "void":
        return _RNA.PathVector_clear(self)

    def get_allocator(self) -> "std::vector< vrna_path_t >::allocator_type":
        return _RNA.PathVector_get_allocator(self)

    def pop_back(self) -> "void":
        return _RNA.PathVector_pop_back(self)

    def erase(self, *args) -> "std::vector< vrna_path_t >::iterator":
        return _RNA.PathVector_erase(self, *args)

    def __init__(self, *args):
        _RNA.PathVector_swiginit(self, _RNA.new_PathVector(*args))

    def push_back(self, x: 'path') -> "void":
        return _RNA.PathVector_push_back(self, x)

    def front(self) -> "std::vector< vrna_path_t >::value_type const &":
        return _RNA.PathVector_front(self)

    def back(self) -> "std::vector< vrna_path_t >::value_type const &":
        return _RNA.PathVector_back(self)

    def assign(self, n: 'std::vector< vrna_path_t >::size_type', x: 'path') -> "void":
        return _RNA.PathVector_assign(self, n, x)

    def resize(self, *args) -> "void":
        return _RNA.PathVector_resize(self, *args)

    def insert(self, *args) -> "void":
        return _RNA.PathVector_insert(self, *args)

    def reserve(self, n: 'std::vector< vrna_path_t >::size_type') -> "void":
        return _RNA.PathVector_reserve(self, n)

    def capacity(self) -> "std::vector< vrna_path_t >::size_type":
        return _RNA.PathVector_capacity(self)
    __swig_destroy__ = _RNA.delete_PathVector

# Register PathVector in _RNA:
_RNA.PathVector_swigregister(PathVector)

class MoveVector(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def iterator(self) -> "swig::SwigPyIterator *":
        return _RNA.MoveVector_iterator(self)
    def __iter__(self):
        return self.iterator()

    def __nonzero__(self) -> "bool":
        return _RNA.MoveVector___nonzero__(self)

    def __bool__(self) -> "bool":
        return _RNA.MoveVector___bool__(self)

    def __len__(self) -> "std::vector< vrna_move_t >::size_type":
        return _RNA.MoveVector___len__(self)

    def __getslice__(self, i: 'std::vector< vrna_move_t >::difference_type', j: 'std::vector< vrna_move_t >::difference_type') -> "std::vector< vrna_move_t,std::allocator< vrna_move_t > > *":
        return _RNA.MoveVector___getslice__(self, i, j)

    def __setslice__(self, *args) -> "void":
        return _RNA.MoveVector___setslice__(self, *args)

    def __delslice__(self, i: 'std::vector< vrna_move_t >::difference_type', j: 'std::vector< vrna_move_t >::difference_type') -> "void":
        return _RNA.MoveVector___delslice__(self, i, j)

    def __delitem__(self, *args) -> "void":
        return _RNA.MoveVector___delitem__(self, *args)

    def __getitem__(self, *args) -> "std::vector< vrna_move_t >::value_type const &":
        return _RNA.MoveVector___getitem__(self, *args)

    def __setitem__(self, *args) -> "void":
        return _RNA.MoveVector___setitem__(self, *args)

    def pop(self) -> "std::vector< vrna_move_t >::value_type":
        return _RNA.MoveVector_pop(self)

    def append(self, x: 'move') -> "void":
        return _RNA.MoveVector_append(self, x)

    def empty(self) -> "bool":
        return _RNA.MoveVector_empty(self)

    def size(self) -> "std::vector< vrna_move_t >::size_type":
        return _RNA.MoveVector_size(self)

    def swap(self, v: 'MoveVector') -> "void":
        return _RNA.MoveVector_swap(self, v)

    def begin(self) -> "std::vector< vrna_move_t >::iterator":
        return _RNA.MoveVector_begin(self)

    def end(self) -> "std::vector< vrna_move_t >::iterator":
        return _RNA.MoveVector_end(self)

    def rbegin(self) -> "std::vector< vrna_move_t >::reverse_iterator":
        return _RNA.MoveVector_rbegin(self)

    def rend(self) -> "std::vector< vrna_move_t >::reverse_iterator":
        return _RNA.MoveVector_rend(self)

    def clear(self) -> "void":
        return _RNA.MoveVector_clear(self)

    def get_allocator(self) -> "std::vector< vrna_move_t >::allocator_type":
        return _RNA.MoveVector_get_allocator(self)

    def pop_back(self) -> "void":
        return _RNA.MoveVector_pop_back(self)

    def erase(self, *args) -> "std::vector< vrna_move_t >::iterator":
        return _RNA.MoveVector_erase(self, *args)

    def __init__(self, *args):
        _RNA.MoveVector_swiginit(self, _RNA.new_MoveVector(*args))

    def push_back(self, x: 'move') -> "void":
        return _RNA.MoveVector_push_back(self, x)

    def front(self) -> "std::vector< vrna_move_t >::value_type const &":
        return _RNA.MoveVector_front(self)

    def back(self) -> "std::vector< vrna_move_t >::value_type const &":
        return _RNA.MoveVector_back(self)

    def assign(self, n: 'std::vector< vrna_move_t >::size_type', x: 'move') -> "void":
        return _RNA.MoveVector_assign(self, n, x)

    def resize(self, *args) -> "void":
        return _RNA.MoveVector_resize(self, *args)

    def insert(self, *args) -> "void":
        return _RNA.MoveVector_insert(self, *args)

    def reserve(self, n: 'std::vector< vrna_move_t >::size_type') -> "void":
        return _RNA.MoveVector_reserve(self, n)

    def capacity(self) -> "std::vector< vrna_move_t >::size_type":
        return _RNA.MoveVector_capacity(self)
    __swig_destroy__ = _RNA.delete_MoveVector

# Register MoveVector in _RNA:
_RNA.MoveVector_swigregister(MoveVector)

class param(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    hairpin = property(_RNA.param_hairpin_get, _RNA.param_hairpin_set)
    bulge = property(_RNA.param_bulge_get, _RNA.param_bulge_set)
    internal_loop = property(_RNA.param_internal_loop_get, _RNA.param_internal_loop_set)
    ninio = property(_RNA.param_ninio_get, _RNA.param_ninio_set)
    lxc = property(_RNA.param_lxc_get, _RNA.param_lxc_set)
    MLbase = property(_RNA.param_MLbase_get, _RNA.param_MLbase_set)
    MLintern = property(_RNA.param_MLintern_get, _RNA.param_MLintern_set)
    MLclosing = property(_RNA.param_MLclosing_get, _RNA.param_MLclosing_set)
    TerminalAU = property(_RNA.param_TerminalAU_get, _RNA.param_TerminalAU_set)
    DuplexInit = property(_RNA.param_DuplexInit_get, _RNA.param_DuplexInit_set)
    Tetraloop_E = property(_RNA.param_Tetraloop_E_get, _RNA.param_Tetraloop_E_set)
    Tetraloops = property(_RNA.param_Tetraloops_get, _RNA.param_Tetraloops_set)
    Triloop_E = property(_RNA.param_Triloop_E_get, _RNA.param_Triloop_E_set)
    Triloops = property(_RNA.param_Triloops_get, _RNA.param_Triloops_set)
    Hexaloop_E = property(_RNA.param_Hexaloop_E_get, _RNA.param_Hexaloop_E_set)
    Hexaloops = property(_RNA.param_Hexaloops_get, _RNA.param_Hexaloops_set)
    TripleC = property(_RNA.param_TripleC_get, _RNA.param_TripleC_set)
    MultipleCA = property(_RNA.param_MultipleCA_get, _RNA.param_MultipleCA_set)
    MultipleCB = property(_RNA.param_MultipleCB_get, _RNA.param_MultipleCB_set)
    temperature = property(_RNA.param_temperature_get, _RNA.param_temperature_set)
    model_details = property(_RNA.param_model_details_get, _RNA.param_model_details_set)
    param_file = property(_RNA.param_param_file_get, _RNA.param_param_file_set)

    def __init__(self, *args):
        _RNA.param_swiginit(self, _RNA.new_param(*args))

    def get_temperature(self) -> "double":
        return _RNA.param_get_temperature(self)
    __swig_destroy__ = _RNA.delete_param

# Register param in _RNA:
_RNA.param_swigregister(param)

class exp_param(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    exphairpin = property(_RNA.exp_param_exphairpin_get, _RNA.exp_param_exphairpin_set)
    expbulge = property(_RNA.exp_param_expbulge_get, _RNA.exp_param_expbulge_set)
    expinternal = property(_RNA.exp_param_expinternal_get, _RNA.exp_param_expinternal_set)
    lxc = property(_RNA.exp_param_lxc_get, _RNA.exp_param_lxc_set)
    expMLbase = property(_RNA.exp_param_expMLbase_get, _RNA.exp_param_expMLbase_set)
    expMLintern = property(_RNA.exp_param_expMLintern_get, _RNA.exp_param_expMLintern_set)
    expMLclosing = property(_RNA.exp_param_expMLclosing_get, _RNA.exp_param_expMLclosing_set)
    expTermAU = property(_RNA.exp_param_expTermAU_get, _RNA.exp_param_expTermAU_set)
    expDuplexInit = property(_RNA.exp_param_expDuplexInit_get, _RNA.exp_param_expDuplexInit_set)
    exptetra = property(_RNA.exp_param_exptetra_get, _RNA.exp_param_exptetra_set)
    exptri = property(_RNA.exp_param_exptri_get, _RNA.exp_param_exptri_set)
    exphex = property(_RNA.exp_param_exphex_get, _RNA.exp_param_exphex_set)
    Tetraloops = property(_RNA.exp_param_Tetraloops_get, _RNA.exp_param_Tetraloops_set)
    expTriloop = property(_RNA.exp_param_expTriloop_get, _RNA.exp_param_expTriloop_set)
    Triloops = property(_RNA.exp_param_Triloops_get, _RNA.exp_param_Triloops_set)
    Hexaloops = property(_RNA.exp_param_Hexaloops_get, _RNA.exp_param_Hexaloops_set)
    expTripleC = property(_RNA.exp_param_expTripleC_get, _RNA.exp_param_expTripleC_set)
    expMultipleCA = property(_RNA.exp_param_expMultipleCA_get, _RNA.exp_param_expMultipleCA_set)
    expMultipleCB = property(_RNA.exp_param_expMultipleCB_get, _RNA.exp_param_expMultipleCB_set)
    kT = property(_RNA.exp_param_kT_get, _RNA.exp_param_kT_set)
    pf_scale = property(_RNA.exp_param_pf_scale_get, _RNA.exp_param_pf_scale_set)
    temperature = property(_RNA.exp_param_temperature_get, _RNA.exp_param_temperature_set)
    alpha = property(_RNA.exp_param_alpha_get, _RNA.exp_param_alpha_set)
    model_details = property(_RNA.exp_param_model_details_get, _RNA.exp_param_model_details_set)
    param_file = property(_RNA.exp_param_param_file_get, _RNA.exp_param_param_file_set)

    def __init__(self, *args):
        _RNA.exp_param_swiginit(self, _RNA.new_exp_param(*args))

    def get_temperature(self) -> "double":
        return _RNA.exp_param_get_temperature(self)
    __swig_destroy__ = _RNA.delete_exp_param

# Register exp_param in _RNA:
_RNA.exp_param_swigregister(exp_param)

UNKNOWN = _RNA.UNKNOWN
QUIT = _RNA.QUIT
S = _RNA.S
S_H = _RNA.S_H
HP = _RNA.HP
HP_H = _RNA.HP_H
B = _RNA.B
B_H = _RNA.B_H
IL = _RNA.IL
IL_H = _RNA.IL_H
MMH = _RNA.MMH
MMH_H = _RNA.MMH_H
MMI = _RNA.MMI
MMI_H = _RNA.MMI_H
MMI1N = _RNA.MMI1N
MMI1N_H = _RNA.MMI1N_H
MMI23 = _RNA.MMI23
MMI23_H = _RNA.MMI23_H
MMM = _RNA.MMM
MMM_H = _RNA.MMM_H
MME = _RNA.MME
MME_H = _RNA.MME_H
D5 = _RNA.D5
D5_H = _RNA.D5_H
D3 = _RNA.D3
D3_H = _RNA.D3_H
INT11 = _RNA.INT11
INT11_H = _RNA.INT11_H
INT21 = _RNA.INT21
INT21_H = _RNA.INT21_H
INT22 = _RNA.INT22
INT22_H = _RNA.INT22_H
ML = _RNA.ML
TL = _RNA.TL
TRI = _RNA.TRI
HEX = _RNA.HEX
NIN = _RNA.NIN
MISC = _RNA.MISC

def last_parameter_file() -> "char const *":
    return _RNA.last_parameter_file()

def read_parameter_file(fname: 'char const []') -> "void":
    return _RNA.read_parameter_file(fname)

def write_parameter_file(fname: 'char const []') -> "void":
    return _RNA.write_parameter_file(fname)

def gettype(ident: 'char const *') -> "enum parset":
    return _RNA.gettype(ident)

def settype(s: 'enum parset') -> "char *":
    return _RNA.settype(s)
GASCONST = _RNA.GASCONST
K0 = _RNA.K0
INF = _RNA.INF
EMAX = _RNA.EMAX
FORBIDDEN = _RNA.FORBIDDEN
BONUS = _RNA.BONUS
NBPAIRS = _RNA.NBPAIRS
TURN = _RNA.TURN
MAXLOOP = _RNA.MAXLOOP
UNIT = _RNA.UNIT
MINPSCORE = _RNA.MINPSCORE
class md(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    temperature = property(_RNA.md_temperature_get, _RNA.md_temperature_set)
    betaScale = property(_RNA.md_betaScale_get, _RNA.md_betaScale_set)
    pf_smooth = property(_RNA.md_pf_smooth_get, _RNA.md_pf_smooth_set)
    dangles = property(_RNA.md_dangles_get, _RNA.md_dangles_set)
    special_hp = property(_RNA.md_special_hp_get, _RNA.md_special_hp_set)
    noLP = property(_RNA.md_noLP_get, _RNA.md_noLP_set)
    noGU = property(_RNA.md_noGU_get, _RNA.md_noGU_set)
    noGUclosure = property(_RNA.md_noGUclosure_get, _RNA.md_noGUclosure_set)
    logML = property(_RNA.md_logML_get, _RNA.md_logML_set)
    circ = property(_RNA.md_circ_get, _RNA.md_circ_set)
    gquad = property(_RNA.md_gquad_get, _RNA.md_gquad_set)
    uniq_ML = property(_RNA.md_uniq_ML_get, _RNA.md_uniq_ML_set)
    energy_set = property(_RNA.md_energy_set_get, _RNA.md_energy_set_set)
    backtrack = property(_RNA.md_backtrack_get, _RNA.md_backtrack_set)
    backtrack_type = property(_RNA.md_backtrack_type_get, _RNA.md_backtrack_type_set)
    compute_bpp = property(_RNA.md_compute_bpp_get, _RNA.md_compute_bpp_set)
    nonstandards = property(_RNA.md_nonstandards_get, _RNA.md_nonstandards_set)
    max_bp_span = property(_RNA.md_max_bp_span_get, _RNA.md_max_bp_span_set)
    min_loop_size = property(_RNA.md_min_loop_size_get, _RNA.md_min_loop_size_set)
    window_size = property(_RNA.md_window_size_get, _RNA.md_window_size_set)
    oldAliEn = property(_RNA.md_oldAliEn_get, _RNA.md_oldAliEn_set)
    ribo = property(_RNA.md_ribo_get, _RNA.md_ribo_set)
    cv_fact = property(_RNA.md_cv_fact_get, _RNA.md_cv_fact_set)
    nc_fact = property(_RNA.md_nc_fact_get, _RNA.md_nc_fact_set)
    sfact = property(_RNA.md_sfact_get, _RNA.md_sfact_set)
    rtype = property(_RNA.md_rtype_get, _RNA.md_rtype_set)
    alias = property(_RNA.md_alias_get, _RNA.md_alias_set)

    def __init__(self, *args):
        _RNA.md_swiginit(self, _RNA.new_md(*args))
    __swig_destroy__ = _RNA.delete_md

    def reset(self) -> "void":
        return _RNA.md_reset(self)

    def set_from_globals(self) -> "void":
        return _RNA.md_set_from_globals(self)

    def option_string(self) -> "char *":
        return _RNA.md_option_string(self)

# Register md in _RNA:
_RNA.md_swigregister(md)

NBASES = _RNA.NBASES
MAXALPHA = _RNA.MAXALPHA

def init_rand() -> "void":
    return _RNA.init_rand()

def urn() -> "double":
    return _RNA.urn()

def int_urn(_from: 'int', to: 'int') -> "int":
    return _RNA.int_urn(_from, to)

def hamming(s1: 'char const *', s2: 'char const *') -> "int":
    return _RNA.hamming(s1, s2)

def hamming_bound(s1: 'char const *', s2: 'char const *', n: 'int') -> "int":
    return _RNA.hamming_bound(s1, s2, n)

def encode_seq(sequence: 'char *') -> "short *":
    return _RNA.encode_seq(sequence)
FILENAME_MAX_LENGTH = _RNA.FILENAME_MAX_LENGTH
FILENAME_ID_LENGTH = _RNA.FILENAME_ID_LENGTH

def random_string(l: 'int', symbols: 'char const []') -> "char *":
    return _RNA.random_string(l, symbols)

def hamming_distance(s1: 'char const *', s2: 'char const *') -> "int":
    return _RNA.hamming_distance(s1, s2)

def hamming_distance_bound(s1: 'char const *', s2: 'char const *', n: 'int') -> "int":
    return _RNA.hamming_distance_bound(s1, s2, n)
class ep(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    i = property(_RNA.ep_i_get, _RNA.ep_i_set)
    j = property(_RNA.ep_j_get, _RNA.ep_j_set)
    p = property(_RNA.ep_p_get, _RNA.ep_p_set)
    type = property(_RNA.ep_type_get, _RNA.ep_type_set)

    def __init__(self, *args):
        _RNA.ep_swiginit(self, _RNA.new_ep(*args))

    def __str__(self) -> "char *":
        return _RNA.ep___str__(self)
    __swig_destroy__ = _RNA.delete_ep

# Register ep in _RNA:
_RNA.ep_swigregister(ep)
cvar = _RNA.cvar


def pack_structure(s: 'char const *') -> "char *":
    r"""pack_structure(char const * s) -> char *"""
    return _RNA.pack_structure(s)

def unpack_structure(packed: 'char const *') -> "char *":
    r"""unpack_structure(char const * packed) -> char *"""
    return _RNA.unpack_structure(packed)

def db_from_ptable(pt: 'IntVector') -> "char *":
    r"""db_from_ptable(IntVector pt) -> char *"""
    return _RNA.db_from_ptable(pt)

def db_flatten(*args) -> "void":
    return _RNA.db_flatten(*args)

def db_from_WUSS(wuss: 'std::string') -> "std::string":
    return _RNA.db_from_WUSS(wuss)

def ptable(str: 'std::string') -> "std::vector< int,std::allocator< int > >":
    r"""ptable(std::string str) -> IntVector"""
    return _RNA.ptable(str)

def ptable_from_string(*args, **kwargs) -> "std::vector< int,std::allocator< int > >":
    r"""ptable_from_string(std::string str, unsigned int options=) -> IntVector"""
    return _RNA.ptable_from_string(*args, **kwargs)

def ptable_pk(str: 'std::string') -> "std::vector< int,std::allocator< int > >":
    r"""ptable_pk(std::string str) -> IntVector"""
    return _RNA.ptable_pk(str)

def pt_pk_remove(pt: 'IntVector', options: 'unsigned int'=0) -> "std::vector< int,std::allocator< int > >":
    r"""pt_pk_remove(IntVector pt, unsigned int options=0) -> IntVector"""
    return _RNA.pt_pk_remove(pt, options)

def plist(structure: 'std::string', pr: 'float') -> "std::vector< vrna_ep_t,std::allocator< vrna_ep_t > >":
    r"""plist(std::string structure, float pr) -> ElemProbVector"""
    return _RNA.plist(structure, pr)

def db_from_plist(elem_probs: 'ElemProbVector', length: 'unsigned int') -> "std::string":
    r"""db_from_plist(ElemProbVector elem_probs, unsigned int length) -> std::string"""
    return _RNA.db_from_plist(elem_probs, length)

def db_pk_remove(*args, **kwargs) -> "std::string":
    r"""db_pk_remove(std::string structure, unsigned int options=) -> std::string"""
    return _RNA.db_pk_remove(*args, **kwargs)

def db_to_tree_string(structure: 'std::string', type: 'unsigned int') -> "std::string":
    r"""db_to_tree_string(std::string structure, unsigned int type) -> std::string"""
    return _RNA.db_to_tree_string(structure, type)

def tree_string_unweight(structure: 'std::string') -> "std::string":
    return _RNA.tree_string_unweight(structure)

def tree_string_to_db(structure: 'std::string') -> "std::string":
    return _RNA.tree_string_to_db(structure)

def make_loop_index(structure: 'char const *') -> "short *":
    return _RNA.make_loop_index(structure)

def loopidx_from_ptable(pt: 'IntVector') -> "std::vector< int,std::allocator< int > >":
    r"""loopidx_from_ptable(IntVector pt) -> IntVector"""
    return _RNA.loopidx_from_ptable(pt)

def bp_distance(str1: 'char const *', str2: 'char const *') -> "int":
    r"""bp_distance(char const * str1, char const * str2) -> int"""
    return _RNA.bp_distance(str1, str2)

def dist_mountain(str1: 'std::string', str2: 'std::string', p: 'unsigned int'=1) -> "double":
    return _RNA.dist_mountain(str1, str2, p)
PLIST_TYPE_BASEPAIR = _RNA.PLIST_TYPE_BASEPAIR
PLIST_TYPE_GQUAD = _RNA.PLIST_TYPE_GQUAD
PLIST_TYPE_H_MOTIF = _RNA.PLIST_TYPE_H_MOTIF
PLIST_TYPE_I_MOTIF = _RNA.PLIST_TYPE_I_MOTIF
PLIST_TYPE_UD_MOTIF = _RNA.PLIST_TYPE_UD_MOTIF
PLIST_TYPE_STACK = _RNA.PLIST_TYPE_STACK
STRUCTURE_TREE_HIT = _RNA.STRUCTURE_TREE_HIT
STRUCTURE_TREE_SHAPIRO_SHORT = _RNA.STRUCTURE_TREE_SHAPIRO_SHORT
STRUCTURE_TREE_SHAPIRO = _RNA.STRUCTURE_TREE_SHAPIRO
STRUCTURE_TREE_SHAPIRO_EXT = _RNA.STRUCTURE_TREE_SHAPIRO_EXT
STRUCTURE_TREE_SHAPIRO_WEIGHT = _RNA.STRUCTURE_TREE_SHAPIRO_WEIGHT
STRUCTURE_TREE_EXPANDED = _RNA.STRUCTURE_TREE_EXPANDED
BRACKETS_RND = _RNA.BRACKETS_RND
BRACKETS_ANG = _RNA.BRACKETS_ANG
BRACKETS_SQR = _RNA.BRACKETS_SQR
BRACKETS_CLY = _RNA.BRACKETS_CLY
BRACKETS_ALPHA = _RNA.BRACKETS_ALPHA
BRACKETS_DEFAULT = _RNA.BRACKETS_DEFAULT
BRACKETS_ANY = _RNA.BRACKETS_ANY

def db_pack(struc: 'char const *') -> "char *":
    return _RNA.db_pack(struc)

def db_unpack(packed: 'char const *') -> "char *":
    return _RNA.db_unpack(packed)

def db_to_element_string(structure: 'char const *') -> "char *":
    return _RNA.db_to_element_string(structure)

def consensus(alignment: 'StringVector', md_p: 'md'=None) -> "std::string":
    r"""consensus(StringVector alignment, md md_p=None) -> std::string"""
    return _RNA.consensus(alignment, md_p)

def consens_mis(alignment: 'StringVector', md_p: 'md'=None) -> "std::string":
    r"""consens_mis(StringVector alignment, md md_p=None) -> std::string"""
    return _RNA.consens_mis(alignment, md_p)

def aln_mpi(alignment: 'StringVector') -> "int":
    r"""aln_mpi(StringVector alignment) -> int"""
    return _RNA.aln_mpi(alignment)

def aln_pscore(alignment: 'StringVector', md: 'md'=None) -> "std::vector< std::vector< int,std::allocator< int > >,std::allocator< std::vector< int,std::allocator< int > > > >":
    r"""aln_pscore(StringVector alignment, md md=None) -> IntIntVector"""
    return _RNA.aln_pscore(alignment, md)

def aln_conservation_struct(alignment: 'StringVector', structure: 'std::string', md: 'md'=None) -> "std::vector< double,std::allocator< double > >":
    r"""aln_conservation_struct(StringVector alignment, std::string structure, md md=None) -> DoubleVector"""
    return _RNA.aln_conservation_struct(alignment, structure, md)

def aln_conservation_col(*args, **kwargs) -> "std::vector< double,std::allocator< double > >":
    r"""aln_conservation_col(StringVector alignment, md md=None, unsigned int options=) -> DoubleVector"""
    return _RNA.aln_conservation_col(*args, **kwargs)
ALN_DEFAULT = _RNA.ALN_DEFAULT
ALN_RNA = _RNA.ALN_RNA
ALN_DNA = _RNA.ALN_DNA
ALN_UPPERCASE = _RNA.ALN_UPPERCASE
ALN_LOWERCASE = _RNA.ALN_LOWERCASE
MEASURE_SHANNON_ENTROPY = _RNA.MEASURE_SHANNON_ENTROPY

def move_standard(seq: 'char *', struc: 'char *', type: 'enum MOVE_TYPE', verbosity_level: 'int', shifts: 'int', noLP: 'int') -> "int *":
    r"""move_standard(char * seq, char * struc, enum MOVE_TYPE type, int verbosity_level, int shifts, int noLP) -> char *"""
    return _RNA.move_standard(seq, struc, type, verbosity_level, shifts, noLP)
class struct_en(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    energy = property(_RNA.struct_en_energy_get, _RNA.struct_en_energy_set)
    structure = property(_RNA.struct_en_structure_get, _RNA.struct_en_structure_set)

    def __init__(self):
        _RNA.struct_en_swiginit(self, _RNA.new_struct_en())
    __swig_destroy__ = _RNA.delete_struct_en

# Register struct_en in _RNA:
_RNA.struct_en_swigregister(struct_en)

GRADIENT = _RNA.GRADIENT
FIRST = _RNA.FIRST
ADAPTIVE = _RNA.ADAPTIVE

def filename_sanitize(*args) -> "std::string":
    return _RNA.filename_sanitize(*args)

def get_xy_coordinates(structure: 'char const *') -> "COORDINATE *":
    r"""get_xy_coordinates(char const * structure) -> COORDINATE"""
    return _RNA.get_xy_coordinates(structure)

def simple_circplot_coordinates(arg1: 'std::string') -> "std::vector< COORDINATE,std::allocator< COORDINATE > >":
    r"""simple_circplot_coordinates(std::string arg1) -> CoordinateVector"""
    return _RNA.simple_circplot_coordinates(arg1)

def naview_xy_coordinates(arg1: 'std::string') -> "std::vector< COORDINATE,std::allocator< COORDINATE > >":
    r"""naview_xy_coordinates(std::string arg1) -> CoordinateVector"""
    return _RNA.naview_xy_coordinates(arg1)
class COORDINATE(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def get(self, i: 'int') -> "COORDINATE *":
        return _RNA.COORDINATE_get(self, i)
    X = property(_RNA.COORDINATE_X_get, _RNA.COORDINATE_X_set)
    Y = property(_RNA.COORDINATE_Y_get, _RNA.COORDINATE_Y_set)

    def __init__(self):
        _RNA.COORDINATE_swiginit(self, _RNA.new_COORDINATE())
    __swig_destroy__ = _RNA.delete_COORDINATE

# Register COORDINATE in _RNA:
_RNA.COORDINATE_swigregister(COORDINATE)


def simple_xy_coordinates(*args) -> "int":
    return _RNA.simple_xy_coordinates(*args)

def my_PS_rna_plot_snoop_a(sequence: 'std::string', structure: 'std::string', filename: 'std::string', relative_access: 'IntVector', seqs: 'StringVector') -> "int":
    r"""my_PS_rna_plot_snoop_a(std::string sequence, std::string structure, std::string filename, IntVector relative_access, StringVector seqs) -> int"""
    return _RNA.my_PS_rna_plot_snoop_a(sequence, structure, filename, relative_access, seqs)

def file_PS_rnaplot(*args) -> "int":
    return _RNA.file_PS_rnaplot(*args)

def file_PS_rnaplot_a(*args) -> "int":
    return _RNA.file_PS_rnaplot_a(*args)

def gmlRNA(string: 'char *', structure: 'char *', ssfile: 'char *', option: 'char') -> "int":
    return _RNA.gmlRNA(string, structure, ssfile, option)

def ssv_rna_plot(string: 'char *', structure: 'char *', ssfile: 'char *') -> "int":
    return _RNA.ssv_rna_plot(string, structure, ssfile)

def svg_rna_plot(string: 'char *', structure: 'char *', ssfile: 'char *') -> "int":
    return _RNA.svg_rna_plot(string, structure, ssfile)

def xrna_plot(string: 'char *', structure: 'char *', ssfile: 'char *') -> "int":
    return _RNA.xrna_plot(string, structure, ssfile)

def PS_rna_plot(string: 'char *', structure: 'char *', file: 'char *') -> "int":
    return _RNA.PS_rna_plot(string, structure, file)

def PS_rna_plot_a(string: 'char *', structure: 'char *', file: 'char *', pre: 'char *', post: 'char *') -> "int":
    return _RNA.PS_rna_plot_a(string, structure, file, pre, post)

def PS_rna_plot_a_gquad(string: 'char *', structure: 'char *', ssfile: 'char *', pre: 'char *', post: 'char *') -> "int":
    return _RNA.PS_rna_plot_a_gquad(string, structure, ssfile, pre, post)

def file_PS_aln(filename: 'std::string', alignment: 'StringVector', identifiers: 'StringVector', structure: 'std::string', start: 'unsigned int'=0, end: 'unsigned int'=0, offset: 'int'=0, columns: 'unsigned int'=60) -> "int":
    r"""file_PS_aln(std::string filename, StringVector alignment, StringVector identifiers, std::string structure, unsigned int start=0, unsigned int end=0, int offset=0, unsigned int columns=60) -> int"""
    return _RNA.file_PS_aln(filename, alignment, identifiers, structure, start, end, offset, columns)

def PS_color_dot_plot(string: 'char *', pi: 'cpair *', filename: 'char *') -> "int":
    return _RNA.PS_color_dot_plot(string, pi, filename)

def PS_color_dot_plot_turn(seq: 'char *', pi: 'cpair *', filename: 'char *', winSize: 'int') -> "int":
    return _RNA.PS_color_dot_plot_turn(seq, pi, filename, winSize)

def PS_dot_plot_turn(seq: 'char *', pl: 'plist *', filename: 'char *', winSize: 'int') -> "int":
    return _RNA.PS_dot_plot_turn(seq, pl, filename, winSize)

def PS_dot_plot_list(seq: 'char *', filename: 'char *', pl: 'plist *', mf: 'plist *', comment: 'char *') -> "int":
    return _RNA.PS_dot_plot_list(seq, filename, pl, mf, comment)

def PS_dot_plot(string: 'char *', file: 'char *') -> "int":
    return _RNA.PS_dot_plot(string, file)
DECOMP_PAIR_HP = _RNA.DECOMP_PAIR_HP
DECOMP_PAIR_IL = _RNA.DECOMP_PAIR_IL
DECOMP_PAIR_ML = _RNA.DECOMP_PAIR_ML
DECOMP_ML_ML_ML = _RNA.DECOMP_ML_ML_ML
DECOMP_ML_STEM = _RNA.DECOMP_ML_STEM
DECOMP_ML_ML = _RNA.DECOMP_ML_ML
DECOMP_ML_UP = _RNA.DECOMP_ML_UP
DECOMP_ML_ML_STEM = _RNA.DECOMP_ML_ML_STEM
DECOMP_ML_COAXIAL = _RNA.DECOMP_ML_COAXIAL
DECOMP_EXT_EXT = _RNA.DECOMP_EXT_EXT
DECOMP_EXT_UP = _RNA.DECOMP_EXT_UP
DECOMP_EXT_STEM = _RNA.DECOMP_EXT_STEM
DECOMP_EXT_EXT_EXT = _RNA.DECOMP_EXT_EXT_EXT
DECOMP_EXT_STEM_EXT = _RNA.DECOMP_EXT_STEM_EXT
DECOMP_EXT_STEM_OUTSIDE = _RNA.DECOMP_EXT_STEM_OUTSIDE
DECOMP_EXT_EXT_STEM = _RNA.DECOMP_EXT_EXT_STEM
DECOMP_EXT_EXT_STEM1 = _RNA.DECOMP_EXT_EXT_STEM1
CONSTRAINT_DB = _RNA.CONSTRAINT_DB
CONSTRAINT_DB_ENFORCE_BP = _RNA.CONSTRAINT_DB_ENFORCE_BP
CONSTRAINT_DB_PIPE = _RNA.CONSTRAINT_DB_PIPE
CONSTRAINT_DB_DOT = _RNA.CONSTRAINT_DB_DOT
CONSTRAINT_DB_X = _RNA.CONSTRAINT_DB_X
CONSTRAINT_DB_ANG_BRACK = _RNA.CONSTRAINT_DB_ANG_BRACK
CONSTRAINT_DB_RND_BRACK = _RNA.CONSTRAINT_DB_RND_BRACK
CONSTRAINT_DB_INTRAMOL = _RNA.CONSTRAINT_DB_INTRAMOL
CONSTRAINT_DB_INTERMOL = _RNA.CONSTRAINT_DB_INTERMOL
CONSTRAINT_DB_GQUAD = _RNA.CONSTRAINT_DB_GQUAD
CONSTRAINT_DB_DEFAULT = _RNA.CONSTRAINT_DB_DEFAULT
CONSTRAINT_CONTEXT_EXT_LOOP = _RNA.CONSTRAINT_CONTEXT_EXT_LOOP
CONSTRAINT_CONTEXT_HP_LOOP = _RNA.CONSTRAINT_CONTEXT_HP_LOOP
CONSTRAINT_CONTEXT_INT_LOOP = _RNA.CONSTRAINT_CONTEXT_INT_LOOP
CONSTRAINT_CONTEXT_INT_LOOP_ENC = _RNA.CONSTRAINT_CONTEXT_INT_LOOP_ENC
CONSTRAINT_CONTEXT_MB_LOOP = _RNA.CONSTRAINT_CONTEXT_MB_LOOP
CONSTRAINT_CONTEXT_MB_LOOP_ENC = _RNA.CONSTRAINT_CONTEXT_MB_LOOP_ENC
CONSTRAINT_CONTEXT_ENFORCE = _RNA.CONSTRAINT_CONTEXT_ENFORCE
CONSTRAINT_CONTEXT_NO_REMOVE = _RNA.CONSTRAINT_CONTEXT_NO_REMOVE
CONSTRAINT_CONTEXT_ALL_LOOPS = _RNA.CONSTRAINT_CONTEXT_ALL_LOOPS
CONSTRAINT_CONTEXT_NONE = _RNA.CONSTRAINT_CONTEXT_NONE
CONSTRAINT_CONTEXT_CLOSING_LOOPS = _RNA.CONSTRAINT_CONTEXT_CLOSING_LOOPS
CONSTRAINT_CONTEXT_ENCLOSED_LOOPS = _RNA.CONSTRAINT_CONTEXT_ENCLOSED_LOOPS

def eval_structure_simple(*args) -> "float":
    return _RNA.eval_structure_simple(*args)

def eval_circ_structure(*args) -> "float":
    return _RNA.eval_circ_structure(*args)

def eval_gquad_structure(*args) -> "float":
    return _RNA.eval_gquad_structure(*args)

def eval_circ_gquad_structure(*args) -> "float":
    return _RNA.eval_circ_gquad_structure(*args)

def eval_structure_pt_simple(*args) -> "float":
    return _RNA.eval_structure_pt_simple(*args)

def energy_of_structure(string: 'char const *', structure: 'char const *', verbosity_level: 'int') -> "float":
    return _RNA.energy_of_structure(string, structure, verbosity_level)

def energy_of_circ_structure(string: 'char const *', structure: 'char const *', verbosity_level: 'int') -> "float":
    return _RNA.energy_of_circ_structure(string, structure, verbosity_level)

def energy_of_gquad_structure(string: 'char const *', structure: 'char const *', verbosity_level: 'int') -> "float":
    return _RNA.energy_of_gquad_structure(string, structure, verbosity_level)

def energy_of_structure_pt(string: 'char const *', ptable: 'short *', s: 'short *', s1: 'short *', verbosity_level: 'int') -> "int":
    return _RNA.energy_of_structure_pt(string, ptable, s, s1, verbosity_level)

def energy_of_move(string: 'char const *', structure: 'char const *', m1: 'int', m2: 'int') -> "float":
    return _RNA.energy_of_move(string, structure, m1, m2)

def energy_of_move_pt(pt: 'short *', s: 'short *', s1: 'short *', m1: 'int', m2: 'int') -> "int":
    return _RNA.energy_of_move_pt(pt, s, s1, m1, m2)

def loop_energy(ptable: 'short *', s: 'short *', s1: 'short *', i: 'int') -> "int":
    return _RNA.loop_energy(ptable, s, s1, i)

def energy_of_struct(string: 'char const *', structure: 'char const *') -> "float":
    return _RNA.energy_of_struct(string, structure)

def energy_of_struct_pt(string: 'char const *', ptable: 'short *', s: 'short *', s1: 'short *') -> "int":
    return _RNA.energy_of_struct_pt(string, ptable, s, s1)

def energy_of_circ_struct(string: 'char const *', structure: 'char const *') -> "float":
    return _RNA.energy_of_circ_struct(string, structure)

def E_Stem(type: 'int', si1: 'int', sj1: 'int', extLoop: 'int', P: 'param') -> "int":
    return _RNA.E_Stem(type, si1, sj1, extLoop, P)

def E_ExtLoop(type: 'int', si1: 'int', sj1: 'int', P: 'param') -> "int":
    return _RNA.E_ExtLoop(type, si1, sj1, P)

def exp_E_ExtLoop(type: 'int', si1: 'int', sj1: 'int', P: 'exp_param') -> "FLT_OR_DBL":
    return _RNA.exp_E_ExtLoop(type, si1, sj1, P)

def exp_E_Stem(type: 'int', si1: 'int', sj1: 'int', extLoop: 'int', P: 'exp_param') -> "FLT_OR_DBL":
    return _RNA.exp_E_Stem(type, si1, sj1, extLoop, P)

def E_Hairpin(size: 'int', type: 'int', si1: 'int', sj1: 'int', string: 'char const *', P: 'param') -> "int":
    return _RNA.E_Hairpin(size, type, si1, sj1, string, P)

def exp_E_Hairpin(u: 'int', type: 'int', si1: 'short', sj1: 'short', string: 'char const *', P: 'exp_param') -> "FLT_OR_DBL":
    return _RNA.exp_E_Hairpin(u, type, si1, sj1, string, P)

def E_IntLoop(n1: 'int', n2: 'int', type: 'int', type_2: 'int', si1: 'int', sj1: 'int', sp1: 'int', sq1: 'int', P: 'param') -> "int":
    return _RNA.E_IntLoop(n1, n2, type, type_2, si1, sj1, sp1, sq1, P)

def exp_E_IntLoop(u1: 'int', u2: 'int', type: 'int', type2: 'int', si1: 'short', sj1: 'short', sp1: 'short', sq1: 'short', P: 'exp_param') -> "FLT_OR_DBL":
    return _RNA.exp_E_IntLoop(u1, u2, type, type2, si1, sj1, sp1, sq1, P)

def E_IntLoop_Co(type: 'int', type_2: 'int', i: 'int', j: 'int', p: 'int', q: 'int', cutpoint: 'int', si1: 'short', sj1: 'short', sp1: 'short', sq1: 'short', dangles: 'int', P: 'param') -> "int":
    return _RNA.E_IntLoop_Co(type, type_2, i, j, p, q, cutpoint, si1, sj1, sp1, sq1, dangles, P)

def ubf_eval_int_loop(i: 'int', j: 'int', p: 'int', q: 'int', i1: 'int', j1: 'int', p1: 'int', q1: 'int', si: 'short', sj: 'short', sp: 'short', sq: 'short', type: 'unsigned char', type_2: 'unsigned char', rtype: 'int *', ij: 'int', cp: 'int', P: 'param', sc: 'vrna_sc_t *') -> "int":
    return _RNA.ubf_eval_int_loop(i, j, p, q, i1, j1, p1, q1, si, sj, sp, sq, type, type_2, rtype, ij, cp, P, sc)

def ubf_eval_int_loop2(i: 'int', j: 'int', p: 'int', q: 'int', i1: 'int', j1: 'int', p1: 'int', q1: 'int', si: 'short', sj: 'short', sp: 'short', sq: 'short', type: 'unsigned char', type_2: 'unsigned char', rtype: 'int *', ij: 'int', sn: 'unsigned int *', ss: 'unsigned int *', P: 'param', sc: 'vrna_sc_t *') -> "int":
    return _RNA.ubf_eval_int_loop2(i, j, p, q, i1, j1, p1, q1, si, sj, sp, sq, type, type_2, rtype, ij, sn, ss, P, sc)

def ubf_eval_ext_int_loop(i: 'int', j: 'int', p: 'int', q: 'int', i1: 'int', j1: 'int', p1: 'int', q1: 'int', si: 'short', sj: 'short', sp: 'short', sq: 'short', type: 'unsigned char', type_2: 'unsigned char', length: 'int', P: 'param', sc: 'vrna_sc_t *') -> "int":
    return _RNA.ubf_eval_ext_int_loop(i, j, p, q, i1, j1, p1, q1, si, sj, sp, sq, type, type_2, length, P, sc)

def E_ml_rightmost_stem(i: 'int', j: 'int', fc: 'fold_compound') -> "int":
    return _RNA.E_ml_rightmost_stem(i, j, fc)

def E_MLstem(type: 'int', si1: 'int', sj1: 'int', P: 'param') -> "int":
    return _RNA.E_MLstem(type, si1, sj1, P)

def exp_E_MLstem(type: 'int', si1: 'int', sj1: 'int', P: 'exp_param') -> "FLT_OR_DBL":
    return _RNA.exp_E_MLstem(type, si1, sj1, P)

def maximum_matching(sequence: 'std::string') -> "int":
    return _RNA.maximum_matching(sequence)

def fold(*args) -> "float *":
    return _RNA.fold(*args)

def circfold(*args) -> "float *":
    return _RNA.circfold(*args)

def free_arrays() -> "void":
    return _RNA.free_arrays()

def update_fold_params() -> "void":
    return _RNA.update_fold_params()

def cofold(*args) -> "float *":
    return _RNA.cofold(*args)

def free_co_arrays() -> "void":
    return _RNA.free_co_arrays()

def update_cofold_params() -> "void":
    return _RNA.update_cofold_params()

def initialize_cofold(length: 'int') -> "void":
    return _RNA.initialize_cofold(length)

def alifold(*args) -> "float *":
    return _RNA.alifold(*args)

def circalifold(strings: 'char const **', structure: 'char *') -> "float":
    return _RNA.circalifold(strings, structure)

def free_alifold_arrays() -> "void":
    return _RNA.free_alifold_arrays()

def Lfoldz(sequence: 'std::string', window_size: 'int', min_z: 'double', nullfile: 'FILE *'=None) -> "float":
    return _RNA.Lfoldz(sequence, window_size, min_z, nullfile)

def Lfold(sequence: 'std::string', window_size: 'int', nullfile: 'FILE *'=None) -> "float":
    return _RNA.Lfold(sequence, window_size, nullfile)

def aliLfold(alignment: 'StringVector', window_size: 'int', nullfile: 'FILE *'=None) -> "float":
    return _RNA.aliLfold(alignment, window_size, nullfile)

def pf_fold(*args) -> "float *":
    return _RNA.pf_fold(*args)

def pf_circ_fold(*args) -> "float *":
    return _RNA.pf_circ_fold(*args)

def pf_float_precision() -> "int":
    return _RNA.pf_float_precision()

def pbacktrack(sequence: 'char *') -> "char *":
    return _RNA.pbacktrack(sequence)

def pbacktrack5(sequence: 'char *', length: 'int') -> "char *":
    return _RNA.pbacktrack5(sequence, length)

def pbacktrack_circ(sequence: 'char *') -> "char *":
    return _RNA.pbacktrack_circ(sequence)

def free_pf_arrays() -> "void":
    return _RNA.free_pf_arrays()

def update_pf_params(length: 'int') -> "void":
    return _RNA.update_pf_params(length)

def mean_bp_distance(length: 'int') -> "double":
    return _RNA.mean_bp_distance(length)

def init_pf_fold(length: 'int') -> "void":
    return _RNA.init_pf_fold(length)

def centroid(length: 'int', dist: 'double *') -> "char *":
    return _RNA.centroid(length, dist)

def co_pf_fold(*args) -> "float *, float *, float *, float *":
    return _RNA.co_pf_fold(*args)

def get_concentrations(FcAB: 'double', FcAA: 'double', FcBB: 'double', FEA: 'double', FEB: 'double', A0: 'double', BO: 'double') -> "double *, double *, double *, double *, double *":
    return _RNA.get_concentrations(FcAB, FcAA, FcBB, FEA, FEB, A0, BO)

def free_co_pf_arrays() -> "void":
    return _RNA.free_co_pf_arrays()

def update_co_pf_params(length: 'int') -> "void":
    return _RNA.update_co_pf_params(length)

def get_pr(i: 'int', j: 'int') -> "double":
    return _RNA.get_pr(i, j)

def MEA(p: 'plist *', structure: 'char *', gamma: 'double') -> "float":
    return _RNA.MEA(p, structure, gamma)

def MEA_seq(p: 'plist *', sequence: 'char const *', structure: 'char *', gamma: 'double', pf: 'exp_param') -> "float":
    return _RNA.MEA_seq(p, sequence, structure, gamma, pf)
class pbacktrack_mem(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self):
        _RNA.pbacktrack_mem_swiginit(self, _RNA.new_pbacktrack_mem())
    __swig_destroy__ = _RNA.delete_pbacktrack_mem

# Register pbacktrack_mem in _RNA:
_RNA.pbacktrack_mem_swigregister(pbacktrack_mem)

PBACKTRACK_DEFAULT = _RNA.PBACKTRACK_DEFAULT
PBACKTRACK_NON_REDUNDANT = _RNA.PBACKTRACK_NON_REDUNDANT

def pfl_fold(sequence: 'std::string', w: 'int', L: 'int', cutoff: 'double') -> "std::vector< vrna_ep_t,std::allocator< vrna_ep_t > >":
    r"""pfl_fold(std::string sequence, int w, int L, double cutoff) -> ElemProbVector"""
    return _RNA.pfl_fold(sequence, w, L, cutoff)

def pfl_fold_up(sequence: 'std::string', ulength: 'int', window_size: 'int', max_bp_span: 'int') -> "std::vector< std::vector< double,std::allocator< double > >,std::allocator< std::vector< double,std::allocator< double > > > >":
    r"""pfl_fold_up(std::string sequence, int ulength, int window_size, int max_bp_span) -> DoubleDoubleVector"""
    return _RNA.pfl_fold_up(sequence, ulength, window_size, max_bp_span)
EXT_LOOP = _RNA.EXT_LOOP
HP_LOOP = _RNA.HP_LOOP
INT_LOOP = _RNA.INT_LOOP
MB_LOOP = _RNA.MB_LOOP
ANY_LOOP = _RNA.ANY_LOOP
PROBS_WINDOW_BPP = _RNA.PROBS_WINDOW_BPP
PROBS_WINDOW_UP = _RNA.PROBS_WINDOW_UP
PROBS_WINDOW_STACKP = _RNA.PROBS_WINDOW_STACKP
PROBS_WINDOW_UP_SPLIT = _RNA.PROBS_WINDOW_UP_SPLIT
PROBS_WINDOW_PF = _RNA.PROBS_WINDOW_PF
class SOLUTION(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    energy = property(_RNA.SOLUTION_energy_get, _RNA.SOLUTION_energy_set)
    structure = property(_RNA.SOLUTION_structure_get, _RNA.SOLUTION_structure_set)

    def get(self, i: 'int') -> "SOLUTION *":
        return _RNA.SOLUTION_get(self, i)

    def size(self) -> "int":
        return _RNA.SOLUTION_size(self)
    __swig_destroy__ = _RNA.delete_SOLUTION

    def __init__(self):
        _RNA.SOLUTION_swiginit(self, _RNA.new_SOLUTION())

# Register SOLUTION in _RNA:
_RNA.SOLUTION_swigregister(SOLUTION)

class subopt_solution(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    energy = property(_RNA.subopt_solution_energy_get, _RNA.subopt_solution_energy_set)
    structure = property(_RNA.subopt_solution_structure_get, _RNA.subopt_solution_structure_set)
    __swig_destroy__ = _RNA.delete_subopt_solution

    def __init__(self):
        _RNA.subopt_solution_swiginit(self, _RNA.new_subopt_solution())

# Register subopt_solution in _RNA:
_RNA.subopt_solution_swigregister(subopt_solution)

class SuboptVector(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def iterator(self) -> "swig::SwigPyIterator *":
        return _RNA.SuboptVector_iterator(self)
    def __iter__(self):
        return self.iterator()

    def __nonzero__(self) -> "bool":
        return _RNA.SuboptVector___nonzero__(self)

    def __bool__(self) -> "bool":
        return _RNA.SuboptVector___bool__(self)

    def __len__(self) -> "std::vector< subopt_solution >::size_type":
        return _RNA.SuboptVector___len__(self)

    def __getslice__(self, i: 'std::vector< subopt_solution >::difference_type', j: 'std::vector< subopt_solution >::difference_type') -> "std::vector< subopt_solution,std::allocator< subopt_solution > > *":
        return _RNA.SuboptVector___getslice__(self, i, j)

    def __setslice__(self, *args) -> "void":
        return _RNA.SuboptVector___setslice__(self, *args)

    def __delslice__(self, i: 'std::vector< subopt_solution >::difference_type', j: 'std::vector< subopt_solution >::difference_type') -> "void":
        return _RNA.SuboptVector___delslice__(self, i, j)

    def __delitem__(self, *args) -> "void":
        return _RNA.SuboptVector___delitem__(self, *args)

    def __getitem__(self, *args) -> "std::vector< subopt_solution >::value_type const &":
        return _RNA.SuboptVector___getitem__(self, *args)

    def __setitem__(self, *args) -> "void":
        return _RNA.SuboptVector___setitem__(self, *args)

    def pop(self) -> "std::vector< subopt_solution >::value_type":
        return _RNA.SuboptVector_pop(self)

    def append(self, x: 'subopt_solution') -> "void":
        return _RNA.SuboptVector_append(self, x)

    def empty(self) -> "bool":
        return _RNA.SuboptVector_empty(self)

    def size(self) -> "std::vector< subopt_solution >::size_type":
        return _RNA.SuboptVector_size(self)

    def swap(self, v: 'SuboptVector') -> "void":
        return _RNA.SuboptVector_swap(self, v)

    def begin(self) -> "std::vector< subopt_solution >::iterator":
        return _RNA.SuboptVector_begin(self)

    def end(self) -> "std::vector< subopt_solution >::iterator":
        return _RNA.SuboptVector_end(self)

    def rbegin(self) -> "std::vector< subopt_solution >::reverse_iterator":
        return _RNA.SuboptVector_rbegin(self)

    def rend(self) -> "std::vector< subopt_solution >::reverse_iterator":
        return _RNA.SuboptVector_rend(self)

    def clear(self) -> "void":
        return _RNA.SuboptVector_clear(self)

    def get_allocator(self) -> "std::vector< subopt_solution >::allocator_type":
        return _RNA.SuboptVector_get_allocator(self)

    def pop_back(self) -> "void":
        return _RNA.SuboptVector_pop_back(self)

    def erase(self, *args) -> "std::vector< subopt_solution >::iterator":
        return _RNA.SuboptVector_erase(self, *args)

    def __init__(self, *args):
        _RNA.SuboptVector_swiginit(self, _RNA.new_SuboptVector(*args))

    def push_back(self, x: 'subopt_solution') -> "void":
        return _RNA.SuboptVector_push_back(self, x)

    def front(self) -> "std::vector< subopt_solution >::value_type const &":
        return _RNA.SuboptVector_front(self)

    def back(self) -> "std::vector< subopt_solution >::value_type const &":
        return _RNA.SuboptVector_back(self)

    def assign(self, n: 'std::vector< subopt_solution >::size_type', x: 'subopt_solution') -> "void":
        return _RNA.SuboptVector_assign(self, n, x)

    def resize(self, *args) -> "void":
        return _RNA.SuboptVector_resize(self, *args)

    def insert(self, *args) -> "void":
        return _RNA.SuboptVector_insert(self, *args)

    def reserve(self, n: 'std::vector< subopt_solution >::size_type') -> "void":
        return _RNA.SuboptVector_reserve(self, n)

    def capacity(self) -> "std::vector< subopt_solution >::size_type":
        return _RNA.SuboptVector_capacity(self)
    __swig_destroy__ = _RNA.delete_SuboptVector

# Register SuboptVector in _RNA:
_RNA.SuboptVector_swigregister(SuboptVector)


def subopt(*args) -> "std::vector< subopt_solution,std::allocator< subopt_solution > >":
    return _RNA.subopt(*args)
MAXDOS = _RNA.MAXDOS

def zukersubopt(string: 'char const *') -> "SOLUTION *":
    return _RNA.zukersubopt(string)

def inverse_fold(start: 'char *', target: 'char const *') -> "float *":
    r"""inverse_fold(char * start, char const * target) -> char *"""
    return _RNA.inverse_fold(start, target)

def inverse_pf_fold(start: 'char *', target: 'char const *') -> "float *":
    r"""inverse_pf_fold(char * start, char const * target) -> char *"""
    return _RNA.inverse_pf_fold(start, target)

def b2HIT(structure: 'char *') -> "char *":
    return _RNA.b2HIT(structure)

def b2C(structure: 'char *') -> "char *":
    return _RNA.b2C(structure)

def b2Shapiro(structure: 'char *') -> "char *":
    return _RNA.b2Shapiro(structure)

def add_root(arg1: 'char *') -> "char *":
    return _RNA.add_root(arg1)

def expand_Shapiro(coarse: 'char *') -> "char *":
    return _RNA.expand_Shapiro(coarse)

def expand_Full(structure: 'char *') -> "char *":
    return _RNA.expand_Full(structure)

def unexpand_Full(ffull: 'char *') -> "char *":
    return _RNA.unexpand_Full(ffull)

def unweight(wcoarse: 'char *') -> "char *":
    return _RNA.unweight(wcoarse)

def unexpand_aligned_F(align: 'char *[2]') -> "void":
    return _RNA.unexpand_aligned_F(align)

def parse_structure(structure: 'char *') -> "void":
    return _RNA.parse_structure(structure)

def make_tree(struc: 'char *') -> "Tree *":
    return _RNA.make_tree(struc)

def tree_edit_distance(T1: 'Tree *', T2: 'Tree *') -> "float":
    return _RNA.tree_edit_distance(T1, T2)

def print_tree(t: 'Tree *') -> "void":
    return _RNA.print_tree(t)

def free_tree(t: 'Tree *') -> "void":
    return _RNA.free_tree(t)

def Make_swString(string: 'char *') -> "swString *":
    return _RNA.Make_swString(string)

def string_edit_distance(T1: 'swString *', T2: 'swString *') -> "float":
    return _RNA.string_edit_distance(T1, T2)

def profile_edit_distance(T1: 'float const *', T2: 'float const *') -> "float":
    return _RNA.profile_edit_distance(T1, T2)

def Make_bp_profile_bppm(bppm: 'FLT_OR_DBL *', length: 'int') -> "float *":
    return _RNA.Make_bp_profile_bppm(bppm, length)

def print_bppm(T: 'float const *') -> "void":
    return _RNA.print_bppm(T)

def free_profile(T: 'float *') -> "void":
    return _RNA.free_profile(T)

def Make_bp_profile(length: 'int') -> "float *":
    return _RNA.Make_bp_profile(length)

def deref_any(ptr: 'void **', index: 'int') -> "void *":
    return _RNA.deref_any(ptr, index)

def get_aligned_line(arg1: 'int') -> "char *":
    return _RNA.get_aligned_line(arg1)

def file_SHAPE_read(file_name: 'char const *', length: 'int', default_value: 'double') -> "std::string *, int *":
    return _RNA.file_SHAPE_read(file_name, length, default_value)

def extract_record_rest_structure(lines: 'char const **', length: 'unsigned int', option: 'unsigned int') -> "char *":
    return _RNA.extract_record_rest_structure(lines, length, option)

def read_record(header: 'char **', sequence: 'char **', rest: 'char ***', options: 'unsigned int') -> "unsigned int":
    return _RNA.read_record(header, sequence, rest, options)

def get_multi_input_line(string: 'char **', options: 'unsigned int') -> "unsigned int":
    return _RNA.get_multi_input_line(string, options)

def file_msa_detect_format(*args, **kwargs) -> "unsigned int":
    r"""file_msa_detect_format(std::string filename, unsigned int options=) -> unsigned int"""
    return _RNA.file_msa_detect_format(*args, **kwargs)

def file_msa_write(*args, **kwargs) -> "int":
    r"""file_msa_write(std::string filename, StringVector names, StringVector alignment, std::string id="", std::string structure="", std::string source="", unsigned int options=VRNA_FILE_FORMAT_MSA_STOCKHOLM|VRNA_FILE_FORMAT_MSA_APPEND) -> int"""
    return _RNA.file_msa_write(*args, **kwargs)

def file_msa_read(*args, **kwargs) -> "std::vector< std::string > *, std::vector< std::string > *, std::string *, std::string *":
    r"""file_msa_read(std::string filename, unsigned int options=) -> int"""
    return _RNA.file_msa_read(*args, **kwargs)

def file_msa_read_record(*args, **kwargs) -> "std::vector< std::string > *, std::vector< std::string > *, std::string *, std::string *":
    r"""file_msa_read_record(FILE * filehandle, unsigned int options=) -> int"""
    return _RNA.file_msa_read_record(*args, **kwargs)
FILE_FORMAT_MSA_CLUSTAL = _RNA.FILE_FORMAT_MSA_CLUSTAL
FILE_FORMAT_MSA_DEFAULT = _RNA.FILE_FORMAT_MSA_DEFAULT
FILE_FORMAT_MSA_FASTA = _RNA.FILE_FORMAT_MSA_FASTA
FILE_FORMAT_MSA_MAF = _RNA.FILE_FORMAT_MSA_MAF
FILE_FORMAT_MSA_NOCHECK = _RNA.FILE_FORMAT_MSA_NOCHECK
FILE_FORMAT_MSA_STOCKHOLM = _RNA.FILE_FORMAT_MSA_STOCKHOLM
FILE_FORMAT_MSA_MIS = _RNA.FILE_FORMAT_MSA_MIS
FILE_FORMAT_MSA_UNKNOWN = _RNA.FILE_FORMAT_MSA_UNKNOWN
FILE_FORMAT_MSA_QUIET = _RNA.FILE_FORMAT_MSA_QUIET
FILE_FORMAT_MSA_SILENT = _RNA.FILE_FORMAT_MSA_SILENT
FILE_FORMAT_MSA_APPEND = _RNA.FILE_FORMAT_MSA_APPEND
SEQUENCE_RNA = _RNA.SEQUENCE_RNA
SEQUENCE_DNA = _RNA.SEQUENCE_DNA
UNSTRUCTURED_DOMAIN_EXT_LOOP = _RNA.UNSTRUCTURED_DOMAIN_EXT_LOOP
UNSTRUCTURED_DOMAIN_HP_LOOP = _RNA.UNSTRUCTURED_DOMAIN_HP_LOOP
UNSTRUCTURED_DOMAIN_INT_LOOP = _RNA.UNSTRUCTURED_DOMAIN_INT_LOOP
UNSTRUCTURED_DOMAIN_MB_LOOP = _RNA.UNSTRUCTURED_DOMAIN_MB_LOOP
UNSTRUCTURED_DOMAIN_ALL_LOOPS = _RNA.UNSTRUCTURED_DOMAIN_ALL_LOOPS
UNSTRUCTURED_DOMAIN_MOTIF = _RNA.UNSTRUCTURED_DOMAIN_MOTIF
class cmd(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self):
        _RNA.cmd_swiginit(self, _RNA.new_cmd())
    __swig_destroy__ = _RNA.delete_cmd

# Register cmd in _RNA:
_RNA.cmd_swigregister(cmd)


def file_commands_read(*args, **kwargs) -> "vrna_command_s *":
    r"""file_commands_read(std::string filename, unsigned int options=) -> cmd"""
    return _RNA.file_commands_read(*args, **kwargs)
CMD_PARSE_DEFAULTS = _RNA.CMD_PARSE_DEFAULTS
CMD_PARSE_HC = _RNA.CMD_PARSE_HC
CMD_PARSE_SC = _RNA.CMD_PARSE_SC
CMD_PARSE_SD = _RNA.CMD_PARSE_SD
CMD_PARSE_UD = _RNA.CMD_PARSE_UD

def enumerate_necklaces(entity_counts: 'UIntVector') -> "std::vector< std::vector< int,std::allocator< int > >,std::allocator< std::vector< int,std::allocator< int > > > >":
    return _RNA.enumerate_necklaces(entity_counts)

def rotational_symmetry(*args) -> "std::vector< unsigned int,std::allocator< unsigned int > >":
    return _RNA.rotational_symmetry(*args)
class duplexT(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    i = property(_RNA.duplexT_i_get, _RNA.duplexT_i_set)
    j = property(_RNA.duplexT_j_get, _RNA.duplexT_j_set)
    structure = property(_RNA.duplexT_structure_get, _RNA.duplexT_structure_set)
    energy = property(_RNA.duplexT_energy_get, _RNA.duplexT_energy_set)
    __swig_destroy__ = _RNA.delete_duplexT

# Register duplexT in _RNA:
_RNA.duplexT_swigregister(duplexT)

class duplex_list_t(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    i = property(_RNA.duplex_list_t_i_get, _RNA.duplex_list_t_i_set)
    j = property(_RNA.duplex_list_t_j_get, _RNA.duplex_list_t_j_set)
    energy = property(_RNA.duplex_list_t_energy_get, _RNA.duplex_list_t_energy_set)
    structure = property(_RNA.duplex_list_t_structure_get, _RNA.duplex_list_t_structure_set)
    __swig_destroy__ = _RNA.delete_duplex_list_t

    def __init__(self):
        _RNA.duplex_list_t_swiginit(self, _RNA.new_duplex_list_t())

# Register duplex_list_t in _RNA:
_RNA.duplex_list_t_swigregister(duplex_list_t)

class DuplexVector(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def iterator(self) -> "swig::SwigPyIterator *":
        return _RNA.DuplexVector_iterator(self)
    def __iter__(self):
        return self.iterator()

    def __nonzero__(self) -> "bool":
        return _RNA.DuplexVector___nonzero__(self)

    def __bool__(self) -> "bool":
        return _RNA.DuplexVector___bool__(self)

    def __len__(self) -> "std::vector< duplex_list_t >::size_type":
        return _RNA.DuplexVector___len__(self)

    def __getslice__(self, i: 'std::vector< duplex_list_t >::difference_type', j: 'std::vector< duplex_list_t >::difference_type') -> "std::vector< duplex_list_t,std::allocator< duplex_list_t > > *":
        return _RNA.DuplexVector___getslice__(self, i, j)

    def __setslice__(self, *args) -> "void":
        return _RNA.DuplexVector___setslice__(self, *args)

    def __delslice__(self, i: 'std::vector< duplex_list_t >::difference_type', j: 'std::vector< duplex_list_t >::difference_type') -> "void":
        return _RNA.DuplexVector___delslice__(self, i, j)

    def __delitem__(self, *args) -> "void":
        return _RNA.DuplexVector___delitem__(self, *args)

    def __getitem__(self, *args) -> "std::vector< duplex_list_t >::value_type const &":
        return _RNA.DuplexVector___getitem__(self, *args)

    def __setitem__(self, *args) -> "void":
        return _RNA.DuplexVector___setitem__(self, *args)

    def pop(self) -> "std::vector< duplex_list_t >::value_type":
        return _RNA.DuplexVector_pop(self)

    def append(self, x: 'duplex_list_t') -> "void":
        return _RNA.DuplexVector_append(self, x)

    def empty(self) -> "bool":
        return _RNA.DuplexVector_empty(self)

    def size(self) -> "std::vector< duplex_list_t >::size_type":
        return _RNA.DuplexVector_size(self)

    def swap(self, v: 'DuplexVector') -> "void":
        return _RNA.DuplexVector_swap(self, v)

    def begin(self) -> "std::vector< duplex_list_t >::iterator":
        return _RNA.DuplexVector_begin(self)

    def end(self) -> "std::vector< duplex_list_t >::iterator":
        return _RNA.DuplexVector_end(self)

    def rbegin(self) -> "std::vector< duplex_list_t >::reverse_iterator":
        return _RNA.DuplexVector_rbegin(self)

    def rend(self) -> "std::vector< duplex_list_t >::reverse_iterator":
        return _RNA.DuplexVector_rend(self)

    def clear(self) -> "void":
        return _RNA.DuplexVector_clear(self)

    def get_allocator(self) -> "std::vector< duplex_list_t >::allocator_type":
        return _RNA.DuplexVector_get_allocator(self)

    def pop_back(self) -> "void":
        return _RNA.DuplexVector_pop_back(self)

    def erase(self, *args) -> "std::vector< duplex_list_t >::iterator":
        return _RNA.DuplexVector_erase(self, *args)

    def __init__(self, *args):
        _RNA.DuplexVector_swiginit(self, _RNA.new_DuplexVector(*args))

    def push_back(self, x: 'duplex_list_t') -> "void":
        return _RNA.DuplexVector_push_back(self, x)

    def front(self) -> "std::vector< duplex_list_t >::value_type const &":
        return _RNA.DuplexVector_front(self)

    def back(self) -> "std::vector< duplex_list_t >::value_type const &":
        return _RNA.DuplexVector_back(self)

    def assign(self, n: 'std::vector< duplex_list_t >::size_type', x: 'duplex_list_t') -> "void":
        return _RNA.DuplexVector_assign(self, n, x)

    def resize(self, *args) -> "void":
        return _RNA.DuplexVector_resize(self, *args)

    def insert(self, *args) -> "void":
        return _RNA.DuplexVector_insert(self, *args)

    def reserve(self, n: 'std::vector< duplex_list_t >::size_type') -> "void":
        return _RNA.DuplexVector_reserve(self, n)

    def capacity(self) -> "std::vector< duplex_list_t >::size_type":
        return _RNA.DuplexVector_capacity(self)
    __swig_destroy__ = _RNA.delete_DuplexVector

# Register DuplexVector in _RNA:
_RNA.DuplexVector_swigregister(DuplexVector)


def duplexfold(s1: 'std::string', s2: 'std::string') -> "duplexT":
    r"""duplexfold(std::string s1, std::string s2) -> duplexT"""
    return _RNA.duplexfold(s1, s2)

def duplex_subopt(s1: 'std::string', s2: 'std::string', delta: 'int', w: 'int') -> "std::vector< duplex_list_t,std::allocator< duplex_list_t > >":
    r"""duplex_subopt(std::string s1, std::string s2, int delta, int w) -> DuplexVector"""
    return _RNA.duplex_subopt(s1, s2, delta, w)

def aliduplexfold(alignment1: 'StringVector', alignment2: 'StringVector') -> "duplexT":
    r"""aliduplexfold(StringVector alignment1, StringVector alignment2) -> duplexT"""
    return _RNA.aliduplexfold(alignment1, alignment2)

def aliduplex_subopt(alignment1: 'StringVector', alignment2: 'StringVector', delta: 'int', w: 'int') -> "std::vector< duplex_list_t,std::allocator< duplex_list_t > >":
    r"""aliduplex_subopt(StringVector alignment1, StringVector alignment2, int delta, int w) -> DuplexVector"""
    return _RNA.aliduplex_subopt(alignment1, alignment2, delta, w)
class move(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    pos_5 = property(_RNA.move_pos_5_get, _RNA.move_pos_5_set)
    pos_3 = property(_RNA.move_pos_3_get, _RNA.move_pos_3_set)

    def __init__(self, *args):
        _RNA.move_swiginit(self, _RNA.new_move(*args))
    __swig_destroy__ = _RNA.delete_move

# Register move in _RNA:
_RNA.move_swigregister(move)

MOVESET_INSERTION = _RNA.MOVESET_INSERTION
MOVESET_DELETION = _RNA.MOVESET_DELETION
MOVESET_SHIFT = _RNA.MOVESET_SHIFT
MOVESET_NO_LP = _RNA.MOVESET_NO_LP
MOVESET_DEFAULT = _RNA.MOVESET_DEFAULT
PATH_STEEPEST_DESCENT = _RNA.PATH_STEEPEST_DESCENT
PATH_RANDOM = _RNA.PATH_RANDOM
PATH_NO_TRANSITION_OUTPUT = _RNA.PATH_NO_TRANSITION_OUTPUT
PATH_DEFAULT = _RNA.PATH_DEFAULT
class path(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    type = property(_RNA.path_type_get, _RNA.path_type_set)
    en = property(_RNA.path_en_get, _RNA.path_en_set)
    s = property(_RNA.path_s_get, _RNA.path_s_set)
    move = property(_RNA.path_move_get, _RNA.path_move_set)
    __swig_destroy__ = _RNA.delete_path

    def __init__(self):
        _RNA.path_swiginit(self, _RNA.new_path())

# Register path in _RNA:
_RNA.path_swigregister(path)

class path_options(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self):
        _RNA.path_options_swiginit(self, _RNA.new_path_options())
    __swig_destroy__ = _RNA.delete_path_options

# Register path_options in _RNA:
_RNA.path_options_swigregister(path_options)


def path_options_findpath(*args) -> "vrna_path_options_s *":
    return _RNA.path_options_findpath(*args)

def get_path(seq: 'std::string', s1: 'std::string', s2: 'std::string', maxkeep: 'int') -> "std::vector< vrna_path_t,std::allocator< vrna_path_t > >":
    r"""get_path(std::string seq, std::string s1, std::string s2, int maxkeep) -> PathVector"""
    return _RNA.get_path(seq, s1, s2, maxkeep)
PATH_TYPE_DOT_BRACKET = _RNA.PATH_TYPE_DOT_BRACKET
PATH_TYPE_MOVES = _RNA.PATH_TYPE_MOVES

def find_saddle(seq: 'char const *', s1: 'char const *', s2: 'char const *', width: 'int') -> "int":
    return _RNA.find_saddle(seq, s1, s2, width)

def free_path(path: 'path') -> "void":
    return _RNA.free_path(path)
class basepair(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    i = property(_RNA.basepair_i_get, _RNA.basepair_i_set)
    j = property(_RNA.basepair_j_get, _RNA.basepair_j_set)

    def __init__(self):
        _RNA.basepair_swiginit(self, _RNA.new_basepair())
    __swig_destroy__ = _RNA.delete_basepair

# Register basepair in _RNA:
_RNA.basepair_swigregister(basepair)


def fc_add_pycallback(vc: 'fold_compound', PyFunc: 'PyObject *') -> "void":
    return _RNA.fc_add_pycallback(vc, PyFunc)

def fc_add_pydata(vc: 'fold_compound', data: 'PyObject *', PyFuncOrNone: 'PyObject *') -> "void":
    return _RNA.fc_add_pydata(vc, data, PyFuncOrNone)

def sc_add_f_pycallback(vc: 'fold_compound', PyFunc: 'PyObject *') -> "void":
    return _RNA.sc_add_f_pycallback(vc, PyFunc)

def sc_add_bt_pycallback(vc: 'fold_compound', PyFunc: 'PyObject *') -> "void":
    return _RNA.sc_add_bt_pycallback(vc, PyFunc)

def sc_add_exp_f_pycallback(vc: 'fold_compound', PyFunc: 'PyObject *') -> "void":
    return _RNA.sc_add_exp_f_pycallback(vc, PyFunc)

def sc_add_pydata(vc: 'fold_compound', data: 'PyObject *', PyFuncOrNone: 'PyObject *') -> "void":
    return _RNA.sc_add_pydata(vc, data, PyFuncOrNone)

def ud_set_pydata(vc: 'fold_compound', data: 'PyObject *', PyFuncOrNone: 'PyObject *') -> "void":
    return _RNA.ud_set_pydata(vc, data, PyFuncOrNone)

def ud_set_prod_cb(vc: 'fold_compound', prod_cb: 'PyObject *', eval_cb: 'PyObject *') -> "void":
    return _RNA.ud_set_prod_cb(vc, prod_cb, eval_cb)

def ud_set_exp_prod_cb(vc: 'fold_compound', prod_cb: 'PyObject *', eval_cb: 'PyObject *') -> "void":
    return _RNA.ud_set_exp_prod_cb(vc, prod_cb, eval_cb)

def ud_set_prob_cb(vc: 'fold_compound', setter: 'PyObject *', getter: 'PyObject *') -> "void":
    return _RNA.ud_set_prob_cb(vc, setter, getter)

def Lfold_cb(string: 'char *', window_size: 'int', PyFunc: 'PyObject *', data: 'PyObject *') -> "float":
    r"""Lfold_cb(char * string, int window_size, PyObject * PyFunc, PyObject * data) -> float"""
    return _RNA.Lfold_cb(string, window_size, PyFunc, data)

def Lfoldz_cb(string: 'char *', window_size: 'int', min_z: 'double', PyFunc: 'PyObject *', data: 'PyObject *') -> "float":
    r"""Lfoldz_cb(char * string, int window_size, double min_z, PyObject * PyFunc, PyObject * data) -> float"""
    return _RNA.Lfoldz_cb(string, window_size, min_z, PyFunc, data)

def aliLfold_cb(alignment: 'StringVector', window_size: 'int', PyFunc: 'PyObject *', data: 'PyObject *') -> "float":
    r"""aliLfold_cb(StringVector alignment, int window_size, PyObject * PyFunc, PyObject * data) -> float"""
    return _RNA.aliLfold_cb(alignment, window_size, PyFunc, data)

def pfl_fold_cb(*args, **kwargs) -> "int":
    r"""pfl_fold_cb(std::string sequence, int window_size, int max_bp_span, PyObject * PyFunc, PyObject * data=Py_None) -> int"""
    return _RNA.pfl_fold_cb(*args, **kwargs)

def pfl_fold_up_cb(*args, **kwargs) -> "int":
    r"""pfl_fold_up_cb(std::string sequence, int ulength, int window_size, int max_bp_span, PyObject * PyFunc, PyObject * data=Py_None) -> int"""
    return _RNA.pfl_fold_up_cb(*args, **kwargs)
FC_TYPE_SINGLE = _RNA.FC_TYPE_SINGLE
FC_TYPE_COMPARATIVE = _RNA.FC_TYPE_COMPARATIVE
class fold_compound(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def exp_params_rescale(self, *args) -> "void":
        return _RNA.fold_compound_exp_params_rescale(self, *args)

    def plist_from_probs(self, cutoff: 'double') -> "std::vector< vrna_ep_t,std::allocator< vrna_ep_t > >":
        r"""plist_from_probs(fold_compound self, double cutoff) -> ElemProbVector"""
        return _RNA.fold_compound_plist_from_probs(self, cutoff)

    def constraints_add(self, *args, **kwargs) -> "void":
        r"""constraints_add(fold_compound self, char const * constraint, unsigned int options=)"""
        return _RNA.fold_compound_constraints_add(self, *args, **kwargs)

    def hc_init(self) -> "void":
        return _RNA.fold_compound_hc_init(self)

    def hc_add_up(self, *args, **kwargs) -> "void":
        r"""hc_add_up(fold_compound self, int i, unsigned int option=VRNA_CONSTRAINT_CONTEXT_ALL_LOOPS)"""
        return _RNA.fold_compound_hc_add_up(self, *args, **kwargs)

    def hc_add_bp_nonspecific(self, *args, **kwargs) -> "void":
        r"""hc_add_bp_nonspecific(fold_compound self, int i, int d, unsigned int option=VRNA_CONSTRAINT_CONTEXT_ALL_LOOPS)"""
        return _RNA.fold_compound_hc_add_bp_nonspecific(self, *args, **kwargs)

    def hc_add_bp(self, *args, **kwargs) -> "void":
        r"""hc_add_bp(fold_compound self, int i, int j, unsigned int option=VRNA_CONSTRAINT_CONTEXT_ALL_LOOPS)"""
        return _RNA.fold_compound_hc_add_bp(self, *args, **kwargs)

    def hc_add_from_db(self, *args, **kwargs) -> "int":
        r"""hc_add_from_db(fold_compound self, char const * constraint, unsigned int options=) -> int"""
        return _RNA.fold_compound_hc_add_from_db(self, *args, **kwargs)

    def sc_remove(self) -> "void":
        return _RNA.fold_compound_sc_remove(self)

    def sc_init(self) -> "void":
        return _RNA.fold_compound_sc_init(self)

    def sc_add_up(self, *args) -> "void":
        return _RNA.fold_compound_sc_add_up(self, *args)

    def sc_add_bp(self, *args) -> "void":
        return _RNA.fold_compound_sc_add_bp(self, *args)

    def sc_set_bp(self, *args, **kwargs) -> "void":
        r"""sc_set_bp(fold_compound self, DoubleDoubleVector constraints, unsigned int options=)"""
        return _RNA.fold_compound_sc_set_bp(self, *args, **kwargs)

    def sc_set_up(self, *args, **kwargs) -> "void":
        r"""sc_set_up(fold_compound self, DoubleVector constraints, unsigned int options=)"""
        return _RNA.fold_compound_sc_set_up(self, *args, **kwargs)

    def sc_set_stack(self, *args, **kwargs) -> "void":
        r"""sc_set_stack(fold_compound self, DoubleVector constraints, unsigned int options=)"""
        return _RNA.fold_compound_sc_set_stack(self, *args, **kwargs)

    def sc_add_stack(self, *args, **kwargs) -> "void":
        r"""sc_add_stack(fold_compound self, int i, double energy, unsigned int options=)"""
        return _RNA.fold_compound_sc_add_stack(self, *args, **kwargs)

    def sc_add_SHAPE_deigan(self, *args, **kwargs) -> "int":
        r"""sc_add_SHAPE_deigan(fold_compound self, DoubleVector reactivities, double m, double b, unsigned int options=) -> int"""
        return _RNA.fold_compound_sc_add_SHAPE_deigan(self, *args, **kwargs)

    def sc_add_SHAPE_deigan_ali(self, *args, **kwargs) -> "int":
        r"""sc_add_SHAPE_deigan_ali(fold_compound self, StringVector shape_files, IntVector shape_file_association, double m, double b, unsigned int options=) -> int"""
        return _RNA.fold_compound_sc_add_SHAPE_deigan_ali(self, *args, **kwargs)

    def sc_add_SHAPE_zarringhalam(self, *args, **kwargs) -> "int":
        r"""sc_add_SHAPE_zarringhalam(fold_compound self, DoubleVector reactivities, double b, double default_value, char const * shape_conversion, unsigned int options=) -> int"""
        return _RNA.fold_compound_sc_add_SHAPE_zarringhalam(self, *args, **kwargs)

    def sc_add_hi_motif(self, *args, **kwargs) -> "int":
        r"""sc_add_hi_motif(fold_compound self, char const * seq, char const * structure, FLT_OR_DBL energy, unsigned int options=) -> int"""
        return _RNA.fold_compound_sc_add_hi_motif(self, *args, **kwargs)

    def eval_structure(self, structure: 'char const *') -> "float":
        return _RNA.fold_compound_eval_structure(self, structure)

    def eval_structure_pt(self, pt: 'IntVector') -> "int":
        return _RNA.fold_compound_eval_structure_pt(self, pt)

    def eval_structure_verbose(self, structure: 'char *', nullfile: 'FILE *'=None) -> "float":
        return _RNA.fold_compound_eval_structure_verbose(self, structure, nullfile)

    def eval_structure_pt_verbose(self, pt: 'IntVector', nullfile: 'FILE *'=None) -> "int":
        return _RNA.fold_compound_eval_structure_pt_verbose(self, pt, nullfile)

    def eval_covar_structure(self, structure: 'char *') -> "float":
        return _RNA.fold_compound_eval_covar_structure(self, structure)

    def eval_loop_pt(self, i: 'int', pt: 'IntVector') -> "int":
        return _RNA.fold_compound_eval_loop_pt(self, i, pt)

    def eval_move(self, structure: 'char const *', m1: 'int', m2: 'int') -> "float":
        return _RNA.fold_compound_eval_move(self, structure, m1, m2)

    def eval_move_pt(self, pt: 'IntVector', m1: 'int', m2: 'int') -> "int":
        return _RNA.fold_compound_eval_move_pt(self, pt, m1, m2)

    def E_ext_loop(self, i: 'int', j: 'int') -> "int":
        r"""E_ext_loop(fold_compound self, int i, int j) -> int"""
        return _RNA.fold_compound_E_ext_loop(self, i, j)

    def eval_hp_loop(self, i: 'int', j: 'int') -> "int":
        r"""eval_hp_loop(fold_compound self, int i, int j) -> int"""
        return _RNA.fold_compound_eval_hp_loop(self, i, j)

    def eval_int_loop(self, i: 'int', j: 'int', k: 'int', l: 'int') -> "int":
        r"""eval_int_loop(fold_compound self, int i, int j, int k, int l) -> int"""
        return _RNA.fold_compound_eval_int_loop(self, i, j, k, l)

    def maxmimum_matching(self) -> "int":
        return _RNA.fold_compound_maxmimum_matching(self)

    def mfe(self) -> "char *":
        r"""mfe(fold_compound self) -> char *"""
        return _RNA.fold_compound_mfe(self)

    def mfe_dimer(self) -> "char *":
        r"""mfe_dimer(fold_compound self) -> char *"""
        return _RNA.fold_compound_mfe_dimer(self)

    def backtrack(self, *args) -> "char *":
        r"""
        backtrack(fold_compound self, unsigned int length) -> char
        backtrack(fold_compound self) -> char *
        """
        return _RNA.fold_compound_backtrack(self, *args)

    def mfe_window(self, nullfile: 'FILE *'=None) -> "float":
        r"""mfe_window(fold_compound self, FILE * nullfile=None) -> float"""
        return _RNA.fold_compound_mfe_window(self, nullfile)

    def mfe_window_zscore(self, min_z: 'double', nullfile: 'FILE *'=None) -> "float":
        return _RNA.fold_compound_mfe_window_zscore(self, min_z, nullfile)

    def pf(self) -> "char *":
        return _RNA.fold_compound_pf(self)

    def mean_bp_distance(self) -> "double":
        return _RNA.fold_compound_mean_bp_distance(self)

    def ensemble_defect(self, structure: 'std::string') -> "double":
        return _RNA.fold_compound_ensemble_defect(self, structure)

    def positional_entropy(self) -> "std::vector< double,std::allocator< double > >":
        return _RNA.fold_compound_positional_entropy(self)

    def pf_dimer(self) -> "char *":
        return _RNA.fold_compound_pf_dimer(self)

    def bpp(self) -> "std::vector< std::vector< double,std::allocator< double > >,std::allocator< std::vector< double,std::allocator< double > > > >":
        return _RNA.fold_compound_bpp(self)

    def subopt(self, delta: 'int', sorted: 'int'=1, nullfile: 'FILE *'=None) -> "std::vector< subopt_solution,std::allocator< subopt_solution > >":
        r"""subopt(fold_compound self, int delta, int sorted=1, FILE * nullfile=None) -> SuboptVector"""
        return _RNA.fold_compound_subopt(self, delta, sorted, nullfile)

    def subopt_zuker(self) -> "std::vector< subopt_solution,std::allocator< subopt_solution > >":
        return _RNA.fold_compound_subopt_zuker(self)

    def sequence_add(self, *args) -> "int":
        return _RNA.fold_compound_sequence_add(self, *args)

    def sequence_remove(self, i: 'unsigned int') -> "int":
        return _RNA.fold_compound_sequence_remove(self, i)

    def sequence_remove_all(self) -> "void":
        return _RNA.fold_compound_sequence_remove_all(self)

    def sequence_prepare(self) -> "void":
        return _RNA.fold_compound_sequence_prepare(self)

    def ud_add_motif(self, *args, **kwargs) -> "void":
        r"""ud_add_motif(fold_compound self, std::string motif, double motif_en, std::string name="", unsigned int options=)"""
        return _RNA.fold_compound_ud_add_motif(self, *args, **kwargs)

    def ud_remove(self) -> "void":
        return _RNA.fold_compound_ud_remove(self)

    def commands_apply(self, *args, **kwargs) -> "int":
        r"""commands_apply(fold_compound self, cmd commands, unsigned int options=) -> int"""
        return _RNA.fold_compound_commands_apply(self, *args, **kwargs)

    def file_commands_apply(self, *args, **kwargs) -> "int":
        r"""file_commands_apply(fold_compound self, std::string filename, unsigned int options=) -> int"""
        return _RNA.fold_compound_file_commands_apply(self, *args, **kwargs)

    def rotational_symmetry_db(self, structure: 'std::string') -> "std::vector< unsigned int,std::allocator< unsigned int > >":
        return _RNA.fold_compound_rotational_symmetry_db(self, structure)

    def neighbors(self, *args, **kwargs) -> "std::vector< vrna_move_t,std::allocator< vrna_move_t > >":
        r"""neighbors(fold_compound self, IntVector pt, unsigned int options=(4|8)) -> MoveVector"""
        return _RNA.fold_compound_neighbors(self, *args, **kwargs)

    def path(self, *args, **kwargs) -> "std::vector< vrna_move_t,std::allocator< vrna_move_t > >":
        r"""path(fold_compound self, IntVector pt, unsigned int steps, unsigned int options=) -> MoveVector"""
        return _RNA.fold_compound_path(self, *args, **kwargs)

    def path_gradient(self, *args, **kwargs) -> "std::vector< vrna_move_t,std::allocator< vrna_move_t > >":
        r"""path_gradient(fold_compound self, IntVector pt, unsigned int options=) -> MoveVector"""
        return _RNA.fold_compound_path_gradient(self, *args, **kwargs)

    def path_random(self, *args, **kwargs) -> "std::vector< vrna_move_t,std::allocator< vrna_move_t > >":
        r"""path_random(fold_compound self, IntVector pt, unsigned int steps, unsigned int options=) -> MoveVector"""
        return _RNA.fold_compound_path_random(self, *args, **kwargs)

    def path_findpath_saddle(self, *args, **kwargs) -> "PyObject *":
        r"""path_findpath_saddle(fold_compound self, std::string s1, std::string s2, int width=1, int maxE=INT_MAX) -> PyObject *"""
        return _RNA.fold_compound_path_findpath_saddle(self, *args, **kwargs)

    def path_findpath(self, *args, **kwargs) -> "std::vector< vrna_path_t,std::allocator< vrna_path_t > >":
        r"""path_findpath(fold_compound self, std::string s1, std::string s2, int width=1, int maxE=INT_MAX-1) -> PathVector"""
        return _RNA.fold_compound_path_findpath(self, *args, **kwargs)

    def path_direct(self, *args, **kwargs) -> "std::vector< vrna_path_t,std::allocator< vrna_path_t > >":
        r"""path_direct(fold_compound self, std::string s1, std::string s2, int maxE=INT_MAX-1, path_options options=None) -> PathVector"""
        return _RNA.fold_compound_path_direct(self, *args, **kwargs)

    def add_auxdata(self, *args, **kwargs) -> "PyObject *":
        r"""add_auxdata(fold_compound self, PyObject * data, PyObject * PyFuncOrNone=Py_None) -> PyObject *"""
        return _RNA.fold_compound_add_auxdata(self, *args, **kwargs)

    def add_callback(self, PyFunc: 'PyObject *') -> "PyObject *":
        r"""add_callback(fold_compound self, PyObject * PyFunc) -> PyObject *"""
        return _RNA.fold_compound_add_callback(self, PyFunc)

    def sc_add_data(self, *args, **kwargs) -> "PyObject *":
        r"""sc_add_data(fold_compound self, PyObject * data, PyObject * PyFuncOrNone=Py_None) -> PyObject *"""
        return _RNA.fold_compound_sc_add_data(self, *args, **kwargs)

    def sc_add_f(self, PyFunc: 'PyObject *') -> "PyObject *":
        r"""sc_add_f(fold_compound self, PyObject * PyFunc) -> PyObject *"""
        return _RNA.fold_compound_sc_add_f(self, PyFunc)

    def sc_add_bt(self, PyFunc: 'PyObject *') -> "PyObject *":
        r"""sc_add_bt(fold_compound self, PyObject * PyFunc) -> PyObject *"""
        return _RNA.fold_compound_sc_add_bt(self, PyFunc)

    def sc_add_exp_f(self, PyFunc: 'PyObject *') -> "PyObject *":
        r"""sc_add_exp_f(fold_compound self, PyObject * PyFunc) -> PyObject *"""
        return _RNA.fold_compound_sc_add_exp_f(self, PyFunc)

    def ud_set_data(self, *args, **kwargs) -> "PyObject *":
        r"""ud_set_data(fold_compound self, PyObject * data, PyObject * PyFuncOrNone=Py_None) -> PyObject *"""
        return _RNA.fold_compound_ud_set_data(self, *args, **kwargs)

    def ud_set_prod_rule_cb(self, prod_cb: 'PyObject *', eval_cb: 'PyObject *') -> "PyObject *":
        r"""ud_set_prod_rule_cb(fold_compound self, PyObject * prod_cb, PyObject * eval_cb) -> PyObject *"""
        return _RNA.fold_compound_ud_set_prod_rule_cb(self, prod_cb, eval_cb)

    def ud_set_exp_prod_rule_cb(self, prod_cb: 'PyObject *', eval_cb: 'PyObject *') -> "PyObject *":
        r"""ud_set_exp_prod_rule_cb(fold_compound self, PyObject * prod_cb, PyObject * eval_cb) -> PyObject *"""
        return _RNA.fold_compound_ud_set_exp_prod_rule_cb(self, prod_cb, eval_cb)

    def ud_set_prob_cb(self, setter: 'PyObject *', getter: 'PyObject *') -> "PyObject *":
        r"""ud_set_prob_cb(fold_compound self, PyObject * setter, PyObject * getter) -> PyObject *"""
        return _RNA.fold_compound_ud_set_prob_cb(self, setter, getter)

    def subopt_cb(self, *args, **kwargs) -> "PyObject *":
        r"""subopt_cb(fold_compound self, int delta, PyObject * PyFunc, PyObject * data=Py_None) -> PyObject *"""
        return _RNA.fold_compound_subopt_cb(self, *args, **kwargs)

    def pbacktrack(self, *args) -> "unsigned int":
        r"""
        pbacktrack(fold_compound self) -> char
        pbacktrack(fold_compound self, unsigned int num_samples, unsigned int options=) -> StringVector
        pbacktrack(fold_compound self, unsigned int num_samples, pbacktrack_mem nr_memory, unsigned int options=) -> StringVector
        pbacktrack(self, num_samples, PyFunc, data=Py_None, options=0) -> unsigned int

        Parameters
        ----------
        num_samples: unsigned int
        PyFunc: PyObject *
        data: PyObject *
        options: unsigned int

        pbacktrack(self, num_samples, PyFunc, data, nr_memory, options=0) -> unsigned int

        Parameters
        ----------
        num_samples: unsigned int
        PyFunc: PyObject *
        data: PyObject *
        nr_memory: vrna_pbacktrack_mem_t *
        options: unsigned int

        """
        return _RNA.fold_compound_pbacktrack(self, *args)

    def pbacktrack5(self, *args) -> "unsigned int":
        r"""
        pbacktrack5(fold_compound self, unsigned int length) -> char
        pbacktrack5(fold_compound self, unsigned int num_samples, unsigned int length, unsigned int options=) -> StringVector
        pbacktrack5(fold_compound self, unsigned int num_samples, unsigned int length, pbacktrack_mem nr_memory, unsigned int options=) -> StringVector
        pbacktrack5(fold_compound self, unsigned int num_samples, unsigned int length, PyObject * PyFunc, PyObject * data=Py_None, unsigned int options=0) -> unsigned int
        pbacktrack5(fold_compound self, unsigned int num_samples, unsigned int length, PyObject * PyFunc, PyObject * data, pbacktrack_mem nr_memory, unsigned int options=0) -> unsigned int
        """
        return _RNA.fold_compound_pbacktrack5(self, *args)

    def mfe_window_cb(self, *args, **kwargs) -> "float":
        r"""mfe_window_cb(fold_compound self, PyObject * PyFunc, PyObject * data=Py_None) -> float"""
        return _RNA.fold_compound_mfe_window_cb(self, *args, **kwargs)

    def mfe_window_score_cb(self, *args, **kwargs) -> "float":
        r"""mfe_window_score_cb(fold_compound self, double min_z, PyObject * PyFunc, PyObject * data=Py_None) -> float"""
        return _RNA.fold_compound_mfe_window_score_cb(self, *args, **kwargs)

    def probs_window(self, *args, **kwargs) -> "int":
        r"""probs_window(fold_compound self, int ulength, unsigned int options, PyObject * PyFunc, PyObject * data=Py_None) -> int"""
        return _RNA.fold_compound_probs_window(self, *args, **kwargs)

    def __init__(self, *args):
        _RNA.fold_compound_swiginit(self, _RNA.new_fold_compound(*args))
    __swig_destroy__ = _RNA.delete_fold_compound

    def type(self) -> "vrna_fc_type_e":
        return _RNA.fold_compound_type(self)

    def length(self) -> "unsigned int":
        return _RNA.fold_compound_length(self)

    def centroid(self) -> "char *":
        r"""centroid(fold_compound self) -> char *"""
        return _RNA.fold_compound_centroid(self)

# Register fold_compound in _RNA:
_RNA.fold_compound_swigregister(fold_compound)

STATUS_MFE_PRE = _RNA.STATUS_MFE_PRE
STATUS_MFE_POST = _RNA.STATUS_MFE_POST
STATUS_PF_PRE = _RNA.STATUS_PF_PRE
STATUS_PF_POST = _RNA.STATUS_PF_POST
OPTION_DEFAULT = _RNA.OPTION_DEFAULT
OPTION_MFE = _RNA.OPTION_MFE
OPTION_PF = _RNA.OPTION_PF
OPTION_HYBRID = _RNA.OPTION_HYBRID
OPTION_EVAL_ONLY = _RNA.OPTION_EVAL_ONLY
OPTION_WINDOW = _RNA.OPTION_WINDOW

base_pair = cvar.base_pair
pr = cvar.pr
iindx = cvar.iindx
