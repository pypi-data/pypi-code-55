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

def getCellLocator(
        mesh,
        verbose=0):

    mypy.my_print(verbose, "*** getCellLocator ***")

    cell_locator = vtk.vtkCellLocator()
    cell_locator.SetDataSet(mesh)
    cell_locator.Update()

    closest_point = [0.]*3
    generic_cell = vtk.vtkGenericCell()
    k_cell = vtk.mutable(0)
    subId = vtk.mutable(0)
    dist = vtk.mutable(0.)

    return (cell_locator,
            closest_point,
            generic_cell,
            k_cell,
            subId,
            dist)
