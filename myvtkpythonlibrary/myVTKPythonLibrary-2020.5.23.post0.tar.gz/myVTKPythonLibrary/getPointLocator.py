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

def getPointLocator(
        mesh,
        verbose=0):

    mypy.my_print(verbose, "*** getPointLocator ***")

    point_locator = vtk.vtkPointLocator()
    point_locator.SetDataSet(mesh)
    point_locator.Update()

    return point_locator
