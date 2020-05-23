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

import numpy

import myPythonLibrary as mypy
import myVTKPythonLibrary as myvtk

########################################################################

def addArrays(
    array1,
    array2,
    array3=None,
    verbose=0):

    mypy.my_print(verbose, "*** addArrays ***")

    n_components = array1.GetNumberOfComponents()
    assert (array2.GetNumberOfComponents() == n_components)
    mypy.my_print(verbose-1, "n_components = "+str(n_components))

    n_tuples = array1.GetNumberOfTuples()
    assert (array2.GetNumberOfTuples() == n_tuples)
    mypy.my_print(verbose-1, "n_tuples = "+str(n_tuples))

    array_type = type(array1.GetTuple(0)[0])
    assert (array_type in [int, float])
    assert (type(array2.GetTuple(0)[0]) is array_type)
    mypy.my_print(verbose-1, "array_type = "+str(array_type))

    if (array3 is None):
        array3 = myvtk.createArray(
            name="",
            n_components=n_components,
            n_tuples=n_tuples,
            array_type=array_type)
    else:
        assert (array3.GetNumberOfComponents() == n_components)
        assert (array3.GetNumberOfTuples() == n_tuples)
        assert (type(array3.GetTuple(0)[0]) is array_type)

    for k_tuple in range(n_tuples):
        mypy.my_print(verbose-2, "k_tuple = "+str(k_tuple))

        array3.SetTuple(
            k_tuple,
            numpy.array(array1.GetTuple(k_tuple)) + numpy.array(array2.GetTuple(k_tuple)))

    return array3

########################################################################

def subArrays(
    array1,
    array2,
    array3=None,
    verbose=0):

    mypy.my_print(verbose, "*** subArrays ***")

    n_components = array1.GetNumberOfComponents()
    assert (array2.GetNumberOfComponents() == n_components)

    n_tuples = array1.GetNumberOfTuples()
    assert (array2.GetNumberOfTuples() == n_tuples)

    array_type = type(array1.GetTuple(0)[0])
    assert (array_type in [int, float])
    assert (type(array2.GetTuple(0)[0]) is array_type)

    if (array3 is None):
        array3 = myvtk.createArray(
            name="",
            n_components=n_components,
            n_tuples=n_tuples,
            array_type=array_type)
    else:
        assert (array3.GetNumberOfComponents() == n_components)
        assert (array3.GetNumberOfTuples() == n_tuples)
        assert (type(array3.GetTuple(0)[0]) is array_type)

    for k_tuple in range(n_tuples):
        array3.SetTuple(
            k_tuple,
            numpy.array(array1.GetTuple(k_tuple)) - numpy.array(array2.GetTuple(k_tuple)))

    return array3

########################################################################

def mulArrays(
    array1,
    array2,
    array3=None,
    verbose=0):

    mypy.my_print(verbose, "*** mulArrays ***")

    n_components = array1.GetNumberOfComponents()
    assert (array2.GetNumberOfComponents() == n_components)

    n_tuples = array1.GetNumberOfTuples()
    assert (array2.GetNumberOfTuples() == n_tuples)

    array_type = type(array1.GetTuple(0)[0])
    assert (array_type in [int, float])
    assert (type(array2.GetTuple(0)[0]) is array_type)

    if (array3 is None):
        array3 = myvtk.createArray(
            name="",
            n_components=n_components,
            n_tuples=n_tuples,
            array_type=array_type)
    else:
        assert (array3.GetNumberOfComponents() == n_components)
        assert (array3.GetNumberOfTuples() == n_tuples)
        assert (type(array3.GetTuple(0)[0]) is array_type)

    for k_tuple in range(n_tuples):
        array3.SetTuple(
            k_tuple,
            numpy.array(array1.GetTuple(k_tuple)) * numpy.array(array2.GetTuple(k_tuple)))

    return array3
