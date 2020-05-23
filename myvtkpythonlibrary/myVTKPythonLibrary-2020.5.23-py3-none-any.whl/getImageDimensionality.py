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

def getImageDimensionality(
        image,
        verbose=0):

    mypy.my_print(verbose, "*** getImageDimensionality ***")

    dimensions = myvtk.getImageDimensions(
        image=image,
        verbose=verbose-1)
    mypy.my_print(verbose-1, "dimensions = "+str(dimensions))

    dimensionality = len(dimensions)
    mypy.my_print(verbose-1, "dimensionality = "+str(dimensionality))

    return dimensionality
