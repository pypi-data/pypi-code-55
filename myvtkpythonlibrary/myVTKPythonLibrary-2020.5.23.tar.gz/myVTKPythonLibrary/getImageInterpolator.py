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

def getImageInterpolator(
        image,
        mode="linear",
        out_value=None,
        verbose=0):

    mypy.my_print(verbose, "*** getImageInterpolator ***")

    interpolator = vtk.vtkImageInterpolator()
    assert (mode in ("nearest", "linear", "cubic"))
    if (mode == "nearest"):
        interpolator.SetInterpolationModeToNearest()
    elif (mode == "linear"):
        interpolator.SetInterpolationModeToLinear()
    elif (mode == "cubic"):
        interpolator.SetInterpolationModeToCubic()
    if (out_value is not None):
        interpolator.SetOutValue(out_value)
    interpolator.Initialize(image)
    interpolator.Update()

    return interpolator
