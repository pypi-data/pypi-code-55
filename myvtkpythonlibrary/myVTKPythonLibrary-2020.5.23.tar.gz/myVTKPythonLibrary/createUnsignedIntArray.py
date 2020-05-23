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

import vtk

import myPythonLibrary as mypy
import myVTKPythonLibrary as myvtk

########################################################################

def createUnsignedIntArray(
        name,
        n_components=1,
        n_tuples=0,
        init_to_zero=0,
        verbose=0):

    array = vtk.vtkUnsignedIntArray()
    array.SetName(name)
    array.SetNumberOfComponents(n_components)
    array.SetNumberOfTuples(n_tuples)

    if (init_to_zero):
        for k_component in range(n_components):
            array.FillComponent(k_component, 0.)

    return array
