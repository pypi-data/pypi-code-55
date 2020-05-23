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

def getClippedPDataUsingField(
        pdata_mesh,
        array_name,
        threshold_value,
        verbose=0):

    mypy.my_print(verbose, "*** getClippedPDataUsingField ***")

    pdata_mesh.GetPointData().SetActiveScalars(array_name)
    clip_poly_data = vtk.vtkClipPolyData()
    if (vtk.vtkVersion.GetVTKMajorVersion() >= 6):
        clip_poly_data.SetInputData(pdata_mesh)
    else:
        clip_poly_data.SetInput(pdata_mesh)
    clip_poly_data.SetValue(threshold_value)
    clip_poly_data.GenerateClippedOutputOn()
    clip_poly_data.Update()

    return clip_poly_data.GetOutput(0), clip_poly_data.GetOutput(1)
