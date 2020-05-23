#!python3
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

def moveMeshWithWorldMatrix(
        mesh,
        M,
        in_place=True,
        verbose=0):

    mypy.my_print(verbose, "*** moveMeshWithWorldMatrix ***")

    if (in_place):
        mesh2 = mesh
    else:
        if mesh.IsA("vtkPolyData"):
            mesh2 = vtk.vtkPolyData()
        elif mesh.IsA("vtkUnstructuredGrid"):
            mesh2 = vtk.vtkUnstructuredGrid()
        else:
            assert (0), "Not implemented. Aborting."
        mesh2.DeepCopy(mesh)

    n_points = mesh2.GetNumberOfPoints()
    points = mesh2.GetPoints()
    P = numpy.empty(4)
    P[3] = 1.
    Q = numpy.empty(4)

    for k_point in range(n_points):
        P[0:3] = points.GetPoint(k_point)
        #print P

        Q = numpy.dot(M, P)
        #print Q

        points.SetPoint(k_point, Q[0:3])

    return mesh2
