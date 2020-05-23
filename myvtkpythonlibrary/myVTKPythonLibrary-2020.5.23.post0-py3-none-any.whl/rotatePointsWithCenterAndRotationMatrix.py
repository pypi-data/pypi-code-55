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

import numpy
import vtk

import myPythonLibrary as mypy
import myVTKPythonLibrary as myvtk

########################################################################

def rotatePointsWithCenterAndRotationMatrix(
        points,
        C,
        R,
        verbose=0):

    mypy.my_print(verbose, "*** rotatePointsWithCenterAndRotationMatrix ***")

    n_points = points.GetNumberOfPoints()

    point = numpy.empty(3)
    for k_point in range(n_points):
        points.GetPoint(k_point, point)
        #print point

        point = C + numpy.dot(R, point - C)
        #print new_point

        points.SetPoint(k_point, point)
