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

def getThresholdedUGrid(
        ugrid,
        field_support,
        field_name,
        threshold_value,
        threshold_by_upper_or_lower,
        verbose=0):

    mypy.my_print(verbose, "*** getThresholdedUGrid ***")

    threshold = vtk.vtkThreshold()
    if (vtk.vtkVersion.GetVTKMajorVersion() >= 6):
        threshold.SetInputData(ugrid)
    else:
        threshold.SetInput(ugrid)
    if (field_support == "points"):
        association = vtk.vtkDataObject.FIELD_ASSOCIATION_POINTS
    elif (field_support == "cells"):
        association = vtk.vtkDataObject.FIELD_ASSOCIATION_CELLS
    threshold.SetInputArrayToProcess(0, 0, 0, association, field_name)
    if (threshold_by_upper_or_lower == "upper"):
        threshold.ThresholdByUpper(threshold_value)
    elif (threshold_by_upper_or_lower == "lower"):
        threshold.ThresholdByLower(threshold_value)
    threshold.Update()
    thresholded_ugrid = threshold.GetOutput()

    return thresholded_ugrid
