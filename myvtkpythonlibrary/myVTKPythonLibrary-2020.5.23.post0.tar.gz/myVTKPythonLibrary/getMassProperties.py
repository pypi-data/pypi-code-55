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

def getMassProperties(
        pdata,
        verbose=0):

    mypy.my_print(verbose, "*** getMassProperties ***")

    mass_properties = vtk.vtkMassProperties()
    if (vtk.vtkVersion.GetVTKMajorVersion() >= 6):
        mass_properties.SetInputData(pdata)
    else:
        mass_properties.SetInput(pdata)

    return mass_properties
