#coding=utf8

########################################################################
###                                                                  ###
### Created by Martin Genet, 2012-2020                               ###
###                                                                  ###
### University of California at San Francisco (UCSF), USA            ###
### Swiss Federal Institute of Technology (ETH), Zurich, Switzerland ###
### École Polytechnique, Palaiseau, France                           ###
###                                                                  ###
########################################################################

from builtins import range

import myPythonLibrary as mypy
import myVTKPythonLibrary as myvtk

########################################################################

def createArray(
        name,
        n_components=1,
        n_tuples=0,
        array_type="float",
        init_to_zero=0,
        verbose=0):

    assert (type(array_type) in (type, str)), "array_type must be a type or a str. Aborting."

    if (type(array_type) is type):
        assert (array_type in (float, int)), "Wrong array type. Aborting."

        if (array_type == float):
            return myvtk.createFloatArray(
                       name=name,
                       n_components=n_components,
                       n_tuples=n_tuples,
                       init_to_zero=init_to_zero,
                       verbose=verbose-1)
        elif (array_type == int):
            return myvtk.createIntArray(
                       name=name,
                       n_components=n_components,
                       n_tuples=n_tuples,
                       init_to_zero=init_to_zero,
                       verbose=verbose-1)
    elif (type(array_type) is str):
        assert (array_type in ("double", "float", "long", "unsigned long", "int", "unsigned int", "short", "unsigned short", "char", "unsigned char", "int64", "uint64", "int32", "uint32", "int16", "uint16", "int8", "uint8")), "Wrong array type. Aborting."

        if (array_type == "float"):
            return myvtk.createFloatArray(
                       name=name,
                       n_components=n_components,
                       n_tuples=n_tuples,
                       init_to_zero=init_to_zero,
                       verbose=verbose-1)
        elif (array_type == "double"):
            return myvtk.createDoubleArray(
                       name=name,
                       n_components=n_components,
                       n_tuples=n_tuples,
                       init_to_zero=init_to_zero,
                       verbose=verbose-1)
        elif (array_type in ("long", "int64")):
            return myvtk.createLongArray(
                       name=name,
                       n_components=n_components,
                       n_tuples=n_tuples,
                       init_to_zero=init_to_zero,
                       verbose=verbose-1)
        elif (array_type in ("unsigned long", "uint64")):
            return myvtk.createUnsignedLongArray(
                       name=name,
                       n_components=n_components,
                       n_tuples=n_tuples,
                       init_to_zero=init_to_zero,
                       verbose=verbose-1)
        elif (array_type in ("int", "int32")):
            return myvtk.createIntArray(
                       name=name,
                       n_components=n_components,
                       n_tuples=n_tuples,
                       init_to_zero=init_to_zero,
                       verbose=verbose-1)
        elif (array_type in ("unsigned int", "uint32")):
            return myvtk.createUnsignedIntArray(
                       name=name,
                       n_components=n_components,
                       n_tuples=n_tuples,
                       init_to_zero=init_to_zero,
                       verbose=verbose-1)
        elif (array_type in ("short", "int16")):
            return myvtk.createShortArray(
                       name=name,
                       n_components=n_components,
                       n_tuples=n_tuples,
                       init_to_zero=init_to_zero,
                       verbose=verbose-1)
        elif (array_type in ("unsigned short", "uint16")):
            return myvtk.createUnsignedShortArray(
                       name=name,
                       n_components=n_components,
                       n_tuples=n_tuples,
                       init_to_zero=init_to_zero,
                       verbose=verbose-1)
        elif (array_type in ("char", "int8")):
            return myvtk.createCharArray(
                       name=name,
                       n_components=n_components,
                       n_tuples=n_tuples,
                       init_to_zero=init_to_zero,
                       verbose=verbose-1)
        elif (array_type in ("unsigned char", "uint8")):
            return myvtk.createUnsignedCharArray(
                       name=name,
                       n_components=n_components,
                       n_tuples=n_tuples,
                       init_to_zero=init_to_zero,
                       verbose=verbose-1)
