# This file was automatically generated by SWIG (http://www.swig.org).
# Version 4.0.1
#
# Do not make changes to this file unless you know what you are doing--modify
# the SWIG interface file instead.



import os,sys,platform

__this_dir__= os.path.dirname(os.path.abspath(__file__))

WIN32=platform.system()=="Windows" or platform.system()=="win32"
if WIN32:

# this is needed to find swig generated *.py file and DLLs
	def AddSysPath(value):
		os.environ['PATH'] = value + os.pathsep + os.environ['PATH']
		sys.path.insert(0,value)
		if hasattr(os,'add_dll_directory'): 
			os.add_dll_directory(value) # this is needed for python 38  

	AddSysPath(__this_dir__)
	AddSysPath(os.path.join(__this_dir__,"bin"))

else:

# this is needed to find swig generated *.py file
	sys.path.append(__this_dir__)




from sys import version_info as _swig_python_version_info
if _swig_python_version_info < (2, 7, 0):
    raise RuntimeError("Python 2.7 or later required")

# Import the low-level C/C++ module
if __package__ or "." in __name__:
    from . import _VisusDataflowPy
else:
    import _VisusDataflowPy

try:
    import builtins as __builtin__
except ImportError:
    import __builtin__

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


import weakref

class SwigPyIterator(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __swig_destroy__ = _VisusDataflowPy.delete_SwigPyIterator

    def value(self):
        return _VisusDataflowPy.SwigPyIterator_value(self)

    def incr(self, n=1):
        return _VisusDataflowPy.SwigPyIterator_incr(self, n)

    def decr(self, n=1):
        return _VisusDataflowPy.SwigPyIterator_decr(self, n)

    def distance(self, x):
        return _VisusDataflowPy.SwigPyIterator_distance(self, x)

    def equal(self, x):
        return _VisusDataflowPy.SwigPyIterator_equal(self, x)

    def copy(self):
        return _VisusDataflowPy.SwigPyIterator_copy(self)

    def next(self):
        return _VisusDataflowPy.SwigPyIterator_next(self)

    def __next__(self):
        return _VisusDataflowPy.SwigPyIterator___next__(self)

    def previous(self):
        return _VisusDataflowPy.SwigPyIterator_previous(self)

    def advance(self, n):
        return _VisusDataflowPy.SwigPyIterator_advance(self, n)

    def __eq__(self, x):
        return _VisusDataflowPy.SwigPyIterator___eq__(self, x)

    def __ne__(self, x):
        return _VisusDataflowPy.SwigPyIterator___ne__(self, x)

    def __iadd__(self, n):
        return _VisusDataflowPy.SwigPyIterator___iadd__(self, n)

    def __isub__(self, n):
        return _VisusDataflowPy.SwigPyIterator___isub__(self, n)

    def __add__(self, n):
        return _VisusDataflowPy.SwigPyIterator___add__(self, n)

    def __sub__(self, *args):
        return _VisusDataflowPy.SwigPyIterator___sub__(self, *args)
    def __iter__(self):
        return self

# Register SwigPyIterator in _VisusDataflowPy:
_VisusDataflowPy.SwigPyIterator_swigregister(SwigPyIterator)

SHARED_PTR_DISOWN = _VisusDataflowPy.SHARED_PTR_DISOWN
import VisusKernelPy
class VectorNode(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def iterator(self):
        return _VisusDataflowPy.VectorNode_iterator(self)
    def __iter__(self):
        return self.iterator()

    def __nonzero__(self):
        return _VisusDataflowPy.VectorNode___nonzero__(self)

    def __bool__(self):
        return _VisusDataflowPy.VectorNode___bool__(self)

    def __len__(self):
        return _VisusDataflowPy.VectorNode___len__(self)

    def __getslice__(self, i, j):
        return _VisusDataflowPy.VectorNode___getslice__(self, i, j)

    def __setslice__(self, *args):
        return _VisusDataflowPy.VectorNode___setslice__(self, *args)

    def __delslice__(self, i, j):
        return _VisusDataflowPy.VectorNode___delslice__(self, i, j)

    def __delitem__(self, *args):
        return _VisusDataflowPy.VectorNode___delitem__(self, *args)

    def __getitem__(self, *args):
        return _VisusDataflowPy.VectorNode___getitem__(self, *args)

    def __setitem__(self, *args):
        return _VisusDataflowPy.VectorNode___setitem__(self, *args)

    def pop(self):
        return _VisusDataflowPy.VectorNode_pop(self)

    def append(self, x):
        return _VisusDataflowPy.VectorNode_append(self, x)

    def empty(self):
        return _VisusDataflowPy.VectorNode_empty(self)

    def size(self):
        return _VisusDataflowPy.VectorNode_size(self)

    def swap(self, v):
        return _VisusDataflowPy.VectorNode_swap(self, v)

    def begin(self):
        return _VisusDataflowPy.VectorNode_begin(self)

    def end(self):
        return _VisusDataflowPy.VectorNode_end(self)

    def rbegin(self):
        return _VisusDataflowPy.VectorNode_rbegin(self)

    def rend(self):
        return _VisusDataflowPy.VectorNode_rend(self)

    def clear(self):
        return _VisusDataflowPy.VectorNode_clear(self)

    def get_allocator(self):
        return _VisusDataflowPy.VectorNode_get_allocator(self)

    def pop_back(self):
        return _VisusDataflowPy.VectorNode_pop_back(self)

    def erase(self, *args):
        return _VisusDataflowPy.VectorNode_erase(self, *args)

    def __init__(self, *args):
        _VisusDataflowPy.VectorNode_swiginit(self, _VisusDataflowPy.new_VectorNode(*args))

    def push_back(self, x):
        return _VisusDataflowPy.VectorNode_push_back(self, x)

    def front(self):
        return _VisusDataflowPy.VectorNode_front(self)

    def back(self):
        return _VisusDataflowPy.VectorNode_back(self)

    def assign(self, n, x):
        return _VisusDataflowPy.VectorNode_assign(self, n, x)

    def resize(self, *args):
        return _VisusDataflowPy.VectorNode_resize(self, *args)

    def insert(self, *args):
        return _VisusDataflowPy.VectorNode_insert(self, *args)

    def reserve(self, n):
        return _VisusDataflowPy.VectorNode_reserve(self, n)

    def capacity(self):
        return _VisusDataflowPy.VectorNode_capacity(self)
    __swig_destroy__ = _VisusDataflowPy.delete_VectorNode

# Register VectorNode in _VisusDataflowPy:
_VisusDataflowPy.VectorNode_swigregister(VectorNode)

class DataflowModule(VisusKernelPy.VisusModule):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr
    bAttached = property(_VisusDataflowPy.DataflowModule_bAttached_get, _VisusDataflowPy.DataflowModule_bAttached_set)

    @staticmethod
    def attach():
        return _VisusDataflowPy.DataflowModule_attach()

    @staticmethod
    def detach():
        return _VisusDataflowPy.DataflowModule_detach()

    def __init__(self):
        _VisusDataflowPy.DataflowModule_swiginit(self, _VisusDataflowPy.new_DataflowModule())
    __swig_destroy__ = _VisusDataflowPy.delete_DataflowModule

# Register DataflowModule in _VisusDataflowPy:
_VisusDataflowPy.DataflowModule_swigregister(DataflowModule)
cvar = _VisusDataflowPy.cvar

def DataflowModule_attach():
    return _VisusDataflowPy.DataflowModule_attach()

def DataflowModule_detach():
    return _VisusDataflowPy.DataflowModule_detach()

class ReturnReceipt(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self):
        _VisusDataflowPy.ReturnReceipt_swiginit(self, _VisusDataflowPy.new_ReturnReceipt())
    __swig_destroy__ = _VisusDataflowPy.delete_ReturnReceipt

    def isReady(self):
        return _VisusDataflowPy.ReturnReceipt_isReady(self)

    def waitReady(self, ready_semaphore):
        return _VisusDataflowPy.ReturnReceipt_waitReady(self, ready_semaphore)

    def needSignature(self, signer):
        return _VisusDataflowPy.ReturnReceipt_needSignature(self, signer)

    def addSignature(self, signer):
        return _VisusDataflowPy.ReturnReceipt_addSignature(self, signer)

    @staticmethod
    def createPassThroughtReceipt(node):
        return _VisusDataflowPy.ReturnReceipt_createPassThroughtReceipt(node)

# Register ReturnReceipt in _VisusDataflowPy:
_VisusDataflowPy.ReturnReceipt_swigregister(ReturnReceipt)

def ReturnReceipt_createPassThroughtReceipt(node):
    return _VisusDataflowPy.ReturnReceipt_createPassThroughtReceipt(node)

class DataflowValue(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self):
        _VisusDataflowPy.DataflowValue_swiginit(self, _VisusDataflowPy.new_DataflowValue())
    __swig_destroy__ = _VisusDataflowPy.delete_DataflowValue

# Register DataflowValue in _VisusDataflowPy:
_VisusDataflowPy.DataflowValue_swigregister(DataflowValue)

class DataflowMessage(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self):
        _VisusDataflowPy.DataflowMessage_swiginit(self, _VisusDataflowPy.new_DataflowMessage())
    __swig_destroy__ = _VisusDataflowPy.delete_DataflowMessage

    def getSender(self):
        return _VisusDataflowPy.DataflowMessage_getSender(self)

    def setSender(self, value):
        return _VisusDataflowPy.DataflowMessage_setSender(self, value)

    def getReturnReceipt(self):
        return _VisusDataflowPy.DataflowMessage_getReturnReceipt(self)

    def setReturnReceipt(self, value):
        return _VisusDataflowPy.DataflowMessage_setReturnReceipt(self, value)

    def getContent(self):
        return _VisusDataflowPy.DataflowMessage_getContent(self)

    def hasContent(self, key):
        return _VisusDataflowPy.DataflowMessage_hasContent(self, key)

    def readValue(self, key):
        return _VisusDataflowPy.DataflowMessage_readValue(self, key)

    def writeValue(self, key, value):
        return _VisusDataflowPy.DataflowMessage_writeValue(self, key, value)

    def writeInt(self, key, value):
        return _VisusDataflowPy.DataflowMessage_writeInt(self, key, value)

    def writeDouble(self, key, value):
        return _VisusDataflowPy.DataflowMessage_writeDouble(self, key, value)

    def writeString(self, key, value):
        return _VisusDataflowPy.DataflowMessage_writeString(self, key, value)

    def writeArray(self, key, value):
        return _VisusDataflowPy.DataflowMessage_writeArray(self, key, value)

# Register DataflowMessage in _VisusDataflowPy:
_VisusDataflowPy.DataflowMessage_swigregister(DataflowMessage)

class DataflowPortValue(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr
    value = property(_VisusDataflowPy.DataflowPortValue_value_get, _VisusDataflowPy.DataflowPortValue_value_set)
    write_id = property(_VisusDataflowPy.DataflowPortValue_write_id_get, _VisusDataflowPy.DataflowPortValue_write_id_set)
    write_timestamp = property(_VisusDataflowPy.DataflowPortValue_write_timestamp_get, _VisusDataflowPy.DataflowPortValue_write_timestamp_set)
    return_receipt = property(_VisusDataflowPy.DataflowPortValue_return_receipt_get, _VisusDataflowPy.DataflowPortValue_return_receipt_set)

    def __init__(self):
        _VisusDataflowPy.DataflowPortValue_swiginit(self, _VisusDataflowPy.new_DataflowPortValue())
    __swig_destroy__ = _VisusDataflowPy.delete_DataflowPortValue

# Register DataflowPortValue in _VisusDataflowPy:
_VisusDataflowPy.DataflowPortValue_swigregister(DataflowPortValue)

class DataflowPort(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr
    DoNotStoreValue = _VisusDataflowPy.DataflowPort_DoNotStoreValue
    StoreOnlyOnePersistentValue = _VisusDataflowPy.DataflowPort_StoreOnlyOnePersistentValue
    StoreOnlyOneVolatileValue = _VisusDataflowPy.DataflowPort_StoreOnlyOneVolatileValue
    StoreMultipleVolatileValues = _VisusDataflowPy.DataflowPort_StoreMultipleVolatileValues
    DefaultInputPortPolicy = _VisusDataflowPy.DataflowPort_DefaultInputPortPolicy
    DefaultOutputPortPolicy = _VisusDataflowPy.DataflowPort_DefaultOutputPortPolicy
    inputs = property(_VisusDataflowPy.DataflowPort_inputs_get, _VisusDataflowPy.DataflowPort_inputs_set)
    outputs = property(_VisusDataflowPy.DataflowPort_outputs_get, _VisusDataflowPy.DataflowPort_outputs_set)

    def __init__(self):
        _VisusDataflowPy.DataflowPort_swiginit(self, _VisusDataflowPy.new_DataflowPort())
    __swig_destroy__ = _VisusDataflowPy.delete_DataflowPort

    def getNode(self):
        return _VisusDataflowPy.DataflowPort_getNode(self)

    def setNode(self, node):
        return _VisusDataflowPy.DataflowPort_setNode(self, node)

    def getName(self):
        return _VisusDataflowPy.DataflowPort_getName(self)

    def setName(self, name):
        return _VisusDataflowPy.DataflowPort_setName(self, name)

    def getPolicy(self):
        return _VisusDataflowPy.DataflowPort_getPolicy(self)

    def setPolicy(self, value):
        return _VisusDataflowPy.DataflowPort_setPolicy(self, value)

    def isConnected(self):
        return _VisusDataflowPy.DataflowPort_isConnected(self)

    def isInputConnectedTo(self, other):
        return _VisusDataflowPy.DataflowPort_isInputConnectedTo(self, other)

    def isOutputConnectedTo(self, other):
        return _VisusDataflowPy.DataflowPort_isOutputConnectedTo(self, other)

    def hasNewValue(self):
        return _VisusDataflowPy.DataflowPort_hasNewValue(self)

    def writeValue(self, *args):
        return _VisusDataflowPy.DataflowPort_writeValue(self, *args)

    def writeInt(self, value):
        return _VisusDataflowPy.DataflowPort_writeInt(self, value)

    def writeDouble(self, value):
        return _VisusDataflowPy.DataflowPort_writeDouble(self, value)

    def writeString(self, value):
        return _VisusDataflowPy.DataflowPort_writeString(self, value)

    def writeArray(self, value):
        return _VisusDataflowPy.DataflowPort_writeArray(self, value)

    def readWriteTimestamp(self):
        return _VisusDataflowPy.DataflowPort_readWriteTimestamp(self)

    def readValue(self):
        return _VisusDataflowPy.DataflowPort_readValue(self)

    def previewValue(self):
        return _VisusDataflowPy.DataflowPort_previewValue(self)

    def disconnect(self):
        return _VisusDataflowPy.DataflowPort_disconnect(self)

# Register DataflowPort in _VisusDataflowPy:
_VisusDataflowPy.DataflowPort_swigregister(DataflowPort)

class NodeJob(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr
    aborted = property(_VisusDataflowPy.NodeJob_aborted_get, _VisusDataflowPy.NodeJob_aborted_set)
    done = property(_VisusDataflowPy.NodeJob_done_get, _VisusDataflowPy.NodeJob_done_set)

    def __init__(self):
        if self.__class__ == NodeJob:
            _self = None
        else:
            _self = self
        _VisusDataflowPy.NodeJob_swiginit(self, _VisusDataflowPy.new_NodeJob(_self, ))
    __swig_destroy__ = _VisusDataflowPy.delete_NodeJob

    def runJob(self):
        return _VisusDataflowPy.NodeJob_runJob(self)

    def abort(self):
        return _VisusDataflowPy.NodeJob_abort(self)
    def __disown__(self):
        self.this.disown()
        _VisusDataflowPy.disown_NodeJob(self)
        return weakref.proxy(self)

# Register NodeJob in _VisusDataflowPy:
_VisusDataflowPy.NodeJob_swigregister(NodeJob)

class Node(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr
    outputs = property(_VisusDataflowPy.Node_outputs_get, _VisusDataflowPy.Node_outputs_set)
    inputs = property(_VisusDataflowPy.Node_inputs_get, _VisusDataflowPy.Node_inputs_set)
    frameview_bounds = property(_VisusDataflowPy.Node_frameview_bounds_get, _VisusDataflowPy.Node_frameview_bounds_set)

    def __init__(self):
        if self.__class__ == Node:
            _self = None
        else:
            _self = self
        _VisusDataflowPy.Node_swiginit(self, _VisusDataflowPy.new_Node(_self, ))
    __swig_destroy__ = _VisusDataflowPy.delete_Node

    def getTypeName(self):
        return _VisusDataflowPy.Node_getTypeName(self)

    def getOsDependentTypeName(self):
        return _VisusDataflowPy.Node_getOsDependentTypeName(self)

    def getName(self):
        return _VisusDataflowPy.Node_getName(self)

    def setName(self, value):
        return _VisusDataflowPy.Node_setName(self, value)

    def getUUID(self):
        return _VisusDataflowPy.Node_getUUID(self)

    def setUUID(self, value):
        return _VisusDataflowPy.Node_setUUID(self, value)

    def getParent(self):
        return _VisusDataflowPy.Node_getParent(self)

    def isVisible(self):
        return _VisusDataflowPy.Node_isVisible(self)

    def setVisible(self, value):
        return _VisusDataflowPy.Node_setVisible(self, value)

    def getChilds(self):
        return _VisusDataflowPy.Node_getChilds(self)

    def getBounds(self):
        return _VisusDataflowPy.Node_getBounds(self)

    def getDataflow(self):
        return _VisusDataflowPy.Node_getDataflow(self)

    def enterInDataflow(self):
        return _VisusDataflowPy.Node_enterInDataflow(self)

    def exitFromDataflow(self):
        return _VisusDataflowPy.Node_exitFromDataflow(self)

    def addNodeJob(self, disown):
        return _VisusDataflowPy.Node_addNodeJob(self, disown)

    def abortProcessing(self):
        return _VisusDataflowPy.Node_abortProcessing(self)

    def joinProcessing(self):
        return _VisusDataflowPy.Node_joinProcessing(self)

    def addInputPort(self, *args):
        return _VisusDataflowPy.Node_addInputPort(self, *args)

    def addOutputPort(self, *args):
        return _VisusDataflowPy.Node_addOutputPort(self, *args)

    def getInputPort(self, iport):
        return _VisusDataflowPy.Node_getInputPort(self, iport)

    def getOutputPort(self, oport):
        return _VisusDataflowPy.Node_getOutputPort(self, oport)

    def removeInputPort(self, name):
        return _VisusDataflowPy.Node_removeInputPort(self, name)

    def removeOutputPort(self, name):
        return _VisusDataflowPy.Node_removeOutputPort(self, name)

    def hasInputPort(self, iport):
        return _VisusDataflowPy.Node_hasInputPort(self, iport)

    def hasOutputPort(self, oport):
        return _VisusDataflowPy.Node_hasOutputPort(self, oport)

    def getInputPortNames(self):
        return _VisusDataflowPy.Node_getInputPortNames(self)

    def getOutputPortNames(self):
        return _VisusDataflowPy.Node_getOutputPortNames(self)

    def isInputConnected(self, iport):
        return _VisusDataflowPy.Node_isInputConnected(self, iport)

    def isOutputConnected(self, oport):
        return _VisusDataflowPy.Node_isOutputConnected(self, oport)

    def isOrphan(self):
        return _VisusDataflowPy.Node_isOrphan(self)

    def needProcessInputs(self):
        return _VisusDataflowPy.Node_needProcessInputs(self)

    def readValue(self, iport):
        return _VisusDataflowPy.Node_readValue(self, iport)

    def readInt(self, key):
        return _VisusDataflowPy.Node_readInt(self, key)

    def readDouble(self, key):
        return _VisusDataflowPy.Node_readDouble(self, key)

    def readString(self, key):
        return _VisusDataflowPy.Node_readString(self, key)

    def readArray(self, key):
        return _VisusDataflowPy.Node_readArray(self, key)

    def previewInput(self, iport):
        return _VisusDataflowPy.Node_previewInput(self, iport)

    def publish(self, msg):
        return _VisusDataflowPy.Node_publish(self, msg)

    def messageHasBeenPublished(self, msg):
        return _VisusDataflowPy.Node_messageHasBeenPublished(self, msg)

    def getFirstInputPort(self):
        return _VisusDataflowPy.Node_getFirstInputPort(self)

    def getFirstOutputPort(self):
        return _VisusDataflowPy.Node_getFirstOutputPort(self)

    def getPathToRoot(self):
        return _VisusDataflowPy.Node_getPathToRoot(self)

    def getPathFromRoot(self):
        return _VisusDataflowPy.Node_getPathFromRoot(self)

    def getIndexInParent(self):
        return _VisusDataflowPy.Node_getIndexInParent(self)

    def goUpIncludingBrothers(self):
        return _VisusDataflowPy.Node_goUpIncludingBrothers(self)

    def breadthFirstSearch(self):
        return _VisusDataflowPy.Node_breadthFirstSearch(self)

    def reversedBreadthFirstSearch(self):
        return _VisusDataflowPy.Node_reversedBreadthFirstSearch(self)

    def findChildWithName(self, name):
        return _VisusDataflowPy.Node_findChildWithName(self, name)

    def guessUniqueChildName(self, prefix):
        return _VisusDataflowPy.Node_guessUniqueChildName(self, prefix)

    def createPassThroughtReceipt(self):
        return _VisusDataflowPy.Node_createPassThroughtReceipt(self)

    def execute(self, ar):
        return _VisusDataflowPy.Node_execute(self, ar)

    def write(self, ar):
        return _VisusDataflowPy.Node_write(self, ar)

    def read(self, ar):
        return _VisusDataflowPy.Node_read(self, ar)

    def processInput(self):
        return _VisusDataflowPy.Node_processInput(self)

    def __asPythonObject(self):
        return _VisusDataflowPy.Node___asPythonObject(self)

       # asPythonObject (whenever you have a director and need to access the python object)
    def asPythonObject(self):
     py_object=self.__asPythonObject()
     return py_object if py_object else self 

    def __disown__(self):
        self.this.disown()
        _VisusDataflowPy.disown_Node(self)
        return weakref.proxy(self)

# Register Node in _VisusDataflowPy:
_VisusDataflowPy.Node_swigregister(Node)

class NodeCreator(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self):
        if self.__class__ == NodeCreator:
            _self = None
        else:
            _self = self
        _VisusDataflowPy.NodeCreator_swiginit(self, _VisusDataflowPy.new_NodeCreator(_self, ))
    __swig_destroy__ = _VisusDataflowPy.delete_NodeCreator

    def createInstance(self):
        return _VisusDataflowPy.NodeCreator_createInstance(self)
    def __disown__(self):
        self.this.disown()
        _VisusDataflowPy.disown_NodeCreator(self)
        return weakref.proxy(self)

# Register NodeCreator in _VisusDataflowPy:
_VisusDataflowPy.NodeCreator_swigregister(NodeCreator)

class NodeFactory(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr

    @staticmethod
    def getSingleton():
        return _VisusDataflowPy.NodeFactory_getSingleton()

    @staticmethod
    def setSingleton(value):
        return _VisusDataflowPy.NodeFactory_setSingleton(value)

    @staticmethod
    def allocSingleton():
        return _VisusDataflowPy.NodeFactory_allocSingleton()

    @staticmethod
    def releaseSingleton():
        return _VisusDataflowPy.NodeFactory_releaseSingleton()
    __swig_destroy__ = _VisusDataflowPy.delete_NodeFactory

    def registerClass(self, portable_typename, os_typename, disown):
        return _VisusDataflowPy.NodeFactory_registerClass(self, portable_typename, os_typename, disown)

    def createInstance(self, portable_typename):
        return _VisusDataflowPy.NodeFactory_createInstance(self, portable_typename)

    def getTypeName(self, instance):
        return _VisusDataflowPy.NodeFactory_getTypeName(self, instance)

# Register NodeFactory in _VisusDataflowPy:
_VisusDataflowPy.NodeFactory_swigregister(NodeFactory)

def NodeFactory_getSingleton():
    return _VisusDataflowPy.NodeFactory_getSingleton()

def NodeFactory_setSingleton(value):
    return _VisusDataflowPy.NodeFactory_setSingleton(value)

def NodeFactory_allocSingleton():
    return _VisusDataflowPy.NodeFactory_allocSingleton()

def NodeFactory_releaseSingleton():
    return _VisusDataflowPy.NodeFactory_releaseSingleton()

class DataflowListener(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self):
        if self.__class__ == DataflowListener:
            _self = None
        else:
            _self = self
        _VisusDataflowPy.DataflowListener_swiginit(self, _VisusDataflowPy.new_DataflowListener(_self, ))
    __swig_destroy__ = _VisusDataflowPy.delete_DataflowListener

    def dataflowMessageHasBeenPublished(self, msg):
        return _VisusDataflowPy.DataflowListener_dataflowMessageHasBeenPublished(self, msg)

    def dataflowBeingDestroyed(self):
        return _VisusDataflowPy.DataflowListener_dataflowBeingDestroyed(self)

    def dataflowBeforeProcessInput(self, node):
        return _VisusDataflowPy.DataflowListener_dataflowBeforeProcessInput(self, node)

    def dataflowAfterProcessInput(self, node):
        return _VisusDataflowPy.DataflowListener_dataflowAfterProcessInput(self, node)

    def dataflowSetName(self, node, old_value, new_value):
        return _VisusDataflowPy.DataflowListener_dataflowSetName(self, node, old_value, new_value)

    def dataflowSetHidden(self, node, old_value, new_value):
        return _VisusDataflowPy.DataflowListener_dataflowSetHidden(self, node, old_value, new_value)

    def dataflowAddNode(self, node):
        return _VisusDataflowPy.DataflowListener_dataflowAddNode(self, node)

    def dataflowRemoveNode(self, node):
        return _VisusDataflowPy.DataflowListener_dataflowRemoveNode(self, node)

    def dataflowMoveNode(self, dst, src, index):
        return _VisusDataflowPy.DataflowListener_dataflowMoveNode(self, dst, src, index)

    def dataflowSetSelection(self, old_selection, new_selection):
        return _VisusDataflowPy.DataflowListener_dataflowSetSelection(self, old_selection, new_selection)

    def dataflowConnectNodes(self, _from, oport, iport, to):
        return _VisusDataflowPy.DataflowListener_dataflowConnectNodes(self, _from, oport, iport, to)

    def dataflowDisconnectNodes(self, _from, oport, iport, to):
        return _VisusDataflowPy.DataflowListener_dataflowDisconnectNodes(self, _from, oport, iport, to)
    def __disown__(self):
        self.this.disown()
        _VisusDataflowPy.disown_DataflowListener(self)
        return weakref.proxy(self)

# Register DataflowListener in _VisusDataflowPy:
_VisusDataflowPy.DataflowListener_swigregister(DataflowListener)

class Dataflow(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr
    listeners = property(_VisusDataflowPy.Dataflow_listeners_get, _VisusDataflowPy.Dataflow_listeners_set)

    def __init__(self):
        _VisusDataflowPy.Dataflow_swiginit(self, _VisusDataflowPy.new_Dataflow())
    __swig_destroy__ = _VisusDataflowPy.delete_Dataflow

    def addListener(self, value):
        return _VisusDataflowPy.Dataflow_addListener(self, value)

    def removeListener(self, value):
        return _VisusDataflowPy.Dataflow_removeListener(self, value)

    def guessNodeUIID(self, base):
        return _VisusDataflowPy.Dataflow_guessNodeUIID(self, base)

    def getRoot(self):
        return _VisusDataflowPy.Dataflow_getRoot(self)

    def getNodes(self):
        return _VisusDataflowPy.Dataflow_getNodes(self)

    def findNodeByUUID(self, uuid):
        return _VisusDataflowPy.Dataflow_findNodeByUUID(self, uuid)

    def processInput(self, node):
        return _VisusDataflowPy.Dataflow_processInput(self, node)

    def needProcessInput(self, node):
        return _VisusDataflowPy.Dataflow_needProcessInput(self, node)

    def publish(self, msg):
        return _VisusDataflowPy.Dataflow_publish(self, msg)

    def abortProcessing(self):
        return _VisusDataflowPy.Dataflow_abortProcessing(self)

    def joinProcessing(self):
        return _VisusDataflowPy.Dataflow_joinProcessing(self)

    def guessLastPublished(self, _from):
        return _VisusDataflowPy.Dataflow_guessLastPublished(self, _from)

    def dispatchPublishedMessages(self):
        return _VisusDataflowPy.Dataflow_dispatchPublishedMessages(self)

    def containsNode(self, node):
        return _VisusDataflowPy.Dataflow_containsNode(self, node)

    def getSelection(self):
        return _VisusDataflowPy.Dataflow_getSelection(self)

    def setSelection(self, value):
        return _VisusDataflowPy.Dataflow_setSelection(self, value)

    def dropSelection(self):
        return _VisusDataflowPy.Dataflow_dropSelection(self)

    def addNode(self, *args):
        return _VisusDataflowPy.Dataflow_addNode(self, *args)

    def canMoveNode(self, dst, src):
        return _VisusDataflowPy.Dataflow_canMoveNode(self, dst, src)

    def moveNode(self, dst, src, index=-1):
        return _VisusDataflowPy.Dataflow_moveNode(self, dst, src, index)

    def removeNode(self, node):
        return _VisusDataflowPy.Dataflow_removeNode(self, node)

    def connectNodes(self, *args):
        return _VisusDataflowPy.Dataflow_connectNodes(self, *args)

    def disconnectNodes(self, _from, oport, iport, to):
        return _VisusDataflowPy.Dataflow_disconnectNodes(self, _from, oport, iport, to)

    def write(self, ar):
        return _VisusDataflowPy.Dataflow_write(self, ar)

    def read(self, ar):
        return _VisusDataflowPy.Dataflow_read(self, ar)

# Register Dataflow in _VisusDataflowPy:
_VisusDataflowPy.Dataflow_swigregister(Dataflow)



class PyNodeCreator(NodeCreator):

    def __init__(self,creator):
        super().__init__()
        self.creator=creator

    def createInstance(self):
        return self.creator()

def VISUS_REGISTER_NODE_CLASS(TypeName, PyTypeName, creator):
    print("Registering python class",TypeName,PyTypeName)
    NodeFactory.getSingleton().registerClass(TypeName, PyTypeName , PyNodeCreator(creator))



