#coding=utf8

########################################################################
###                                                                  ###
### Created by Martin Genet, 2012-2020                               ###
###                                                                  ###
### University of California at San Francisco (UCSF), USA            ###
### Swiss Federal Institute of Technology (ETH), Zurich, Switzerland ###
### École Polytechnique, Palaiseau, France                           ###
###                                                                  ###
###                                                                  ###
### And Cécile Patte, 2018-2020                                      ###
###                                                                  ###
### INRIA, Palaiseau, France                                         ###
###                                                                  ###
########################################################################

from builtins import range

import numpy
import vtk

import myPythonLibrary as mypy
import myVTKPythonLibrary as myvtk
from vtk.numpy_interface import dataset_adapter as dsa
from vtk.numpy_interface import algorithms as algs

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

    ugrid1 = vtk.vtkUnstructuredGrid()
    ugrid2 = vtk.vtkUnstructuredGrid()
    ugrid1.GetPointData().AddArray(array1)
    ugrid2.GetPointData().AddArray(array2)

    ugrid1 = dsa.WrapDataObject(ugrid1)
    ugrid2 = dsa.WrapDataObject(ugrid2)

    np_array1 = ugrid1.PointData[array1.GetName()]
    np_array2 = ugrid2.PointData[array2.GetName()]

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

    ugrid3 = vtk.vtkUnstructuredGrid()
    ugrid3.GetPointData().AddArray(array3)
    ugrid3 = dsa.WrapDataObject(ugrid3)
    np_array3 = ugrid3.PointData[array3.GetName()]

    np_array3[:] = np_array1[:] + np_array2[:]

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
    mypy.my_print(verbose-1, "n_components = "+str(n_components))

    n_tuples = array1.GetNumberOfTuples()
    assert (array2.GetNumberOfTuples() == n_tuples)
    mypy.my_print(verbose-1, "n_tuples = "+str(n_tuples))

    array_type = type(array1.GetTuple(0)[0])
    assert (array_type in [int, float])
    assert (type(array2.GetTuple(0)[0]) is array_type)
    mypy.my_print(verbose-1, "array_type = "+str(array_type))

    ugrid1 = vtk.vtkUnstructuredGrid()
    ugrid2 = vtk.vtkUnstructuredGrid()
    ugrid1.GetPointData().AddArray(array1)
    ugrid2.GetPointData().AddArray(array2)

    ugrid1 = dsa.WrapDataObject(ugrid1)
    ugrid2 = dsa.WrapDataObject(ugrid2)

    np_array1 = ugrid1.PointData[array1.GetName()]
    np_array2 = ugrid2.PointData[array2.GetName()]

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

    ugrid3 = vtk.vtkUnstructuredGrid()
    ugrid3.GetPointData().AddArray(array3)
    ugrid3 = dsa.WrapDataObject(ugrid3)
    np_array3 = ugrid3.PointData[array3.GetName()]

    np_array3[:] = np_array1[:] - np_array2[:]

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
    mypy.my_print(verbose-1, "n_components = "+str(n_components))

    n_tuples = array1.GetNumberOfTuples()
    assert (array2.GetNumberOfTuples() == n_tuples)
    mypy.my_print(verbose-1, "n_tuples = "+str(n_tuples))

    array_type = type(array1.GetTuple(0)[0])
    assert (array_type in [int, float])
    assert (type(array2.GetTuple(0)[0]) is array_type)
    mypy.my_print(verbose-1, "array_type = "+str(array_type))

    ugrid1 = vtk.vtkUnstructuredGrid()
    ugrid2 = vtk.vtkUnstructuredGrid()
    ugrid1.GetPointData().AddArray(array1)
    ugrid2.GetPointData().AddArray(array2)

    ugrid1 = dsa.WrapDataObject(ugrid1)
    ugrid2 = dsa.WrapDataObject(ugrid2)

    np_array1 = ugrid1.PointData[array1.GetName()]
    np_array2 = ugrid2.PointData[array2.GetName()]

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

    ugrid3 = vtk.vtkUnstructuredGrid()
    ugrid3.GetPointData().AddArray(array3)
    ugrid3 = dsa.WrapDataObject(ugrid3)
    np_array3 = ugrid3.PointData[array3.GetName()]

    np_array3[:] = np_array1[:] * np_array2[:]

    return array3
