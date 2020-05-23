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

def getImageDimensions(
        image,
        verbose=0):

    mypy.my_print(verbose, "*** getImageDimensions ***")

    [DX, DY, DZ] = image.GetDimensions()
    mypy.my_print(verbose-1, "dimensions = "+str([DX, DY, DZ]))

    if   (DX >  1) and (DY >  1) and (DZ >  1):
        dimensions = [DX, DY, DZ]
    elif (DX >  1) and (DY >  1) and (DZ == 1):
        dimensions = [DX, DY]
    elif (DX >  1) and (DY == 1) and (DZ == 1):
        dimensions = [DX]
    else:
        assert (0), "Wrong image dimensions ("+str([DX, DY, DZ])+")"
    mypy.my_print(verbose-1, "dimensions = "+str(dimensions))

    return dimensions
