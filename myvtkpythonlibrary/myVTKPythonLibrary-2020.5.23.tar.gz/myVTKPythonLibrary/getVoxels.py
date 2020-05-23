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

def getVoxels(
        ugrid,
        verbose=0):

    mypy.my_print(verbose, "*** getVoxels ***")

    n_points = ugrid.GetPoints().GetNumberOfPoints()
    seed_point = n_points//2

    point_locator = myvtk.getPointLocator(ugrid)

    n_closest_points = 100
    closest_points = vtk.vtkIdList()
    point_locator.FindClosestNPoints(
        n_closest_points,
        ugrid.GetPoint(seed_point),
        closest_points)

    P0 = numpy.empty(3)
    P1 = numpy.empty(3)
    P2 = numpy.empty(3)
    P3 = numpy.empty(3)

    ugrid.GetPoint(closest_points.GetId(0), P0)
    #print "P0 = "+str(P0)

    ugrid.GetPoint(closest_points.GetId(1), P1)
    #print "P1 = "+str(P1)

    X = P1-P0
    dX = numpy.linalg.norm(X)
    X /= dX
    #print "X = "+str(X)
    #print "dX = "+str(dX)

    for k_point in range(2, n_closest_points):
        #print "k_point = "+str(k_point)
        ugrid.GetPoint(closest_points.GetId(k_point), P2)

        Y = P2-P0
        dY = numpy.linalg.norm(Y)
        Y /= dY
        #print "P2 = "+str(P2)
        #print "Y = "+str(Y)
        #print "dY = "+str(dY)
        #print "numpy.dot(Y, X) = "+str(numpy.dot(Y, X))
        if (abs(numpy.dot(Y, X)) < 0.001):
            Y = P2-P0
            dY = numpy.linalg.norm(Y)
            Y /= dY
            break
    #print "Y = "+str(Y)
    #print "dY = "+str(dY)

    Z = numpy.cross(X, Y)
    dZ_list = []

    for k_point in range(2, n_closest_points):
        #print "k_point = "+str(k_point)
        ugrid.GetPoint(closest_points.GetId(k_point), P3)

        ZZ = P3-P0
        dZ = numpy.linalg.norm(ZZ)
        ZZ /= dZ
        #print "P3 = "+str(P3)
        #print "ZZ = "+str(ZZ)
        #print "dZ = "+str(dZ)
        #print "numpy.dot(ZZ, Z) = "+str(numpy.dot(ZZ, Z))
        if (abs(numpy.dot(ZZ, Z)) > 0.999):
            dZ_list.append(dZ)
    dZ = min(dZ_list)
    #print "Z = "+str(Z)
    #print "dZ = "+str(dZ)

    #print "numpy.dot(Y, X) = "+str(numpy.dot(Y, X))
    #print "numpy.dot(Z, X) = "+str(numpy.dot(Z, X))
    #print "numpy.dot(Z, Y) = "+str(numpy.dot(Z, Y))

    points = vtk.vtkPoints()

    point_locator = vtk.vtkPointLocator()
    point_locator.InitPointInsertion(points, ugrid.GetBounds())
    radius = min(dX, dY, dZ)/2

    cell = vtk.vtkHexahedron()
    cell_array = vtk.vtkCellArray()

    P = numpy.empty(3)
    PPP = numpy.empty(3)
    for k_point in range(n_points):
        ugrid.GetPoint(k_point, P)

        point_ids = []
        for pm_Z in [-1,+1]:
            for pm_Y in [-1,+1]:
                if (pm_Y == -1):   pm_X_list = [-1,+1]
                elif (pm_Y == +1): pm_X_list = [+1,-1]
                for pm_X in pm_X_list:
                    PP = P + pm_Z * dZ/2 * Z + pm_Y * dY/2 * Y + pm_X * dX/2 * X

                    if (points.GetNumberOfPoints() == 0):
                        point_id = point_locator.InsertNextPoint(PP)
                    else:
                        point_id = point_locator.FindClosestInsertedPoint(PP)
                        points.GetPoint(point_id, PPP)
                        dist = numpy.linalg.norm(PPP-PP)
                        if (dist > radius):
                            point_id = point_locator.InsertNextPoint(PP)

                    #point_id = point_locator.IsInsertedPoint(PP)
                    #if (point_id == -1):
                        #point_id = point_locator.InsertNextPoint(PP)

                    point_ids.append(point_id)

        for i in range(8):
            cell.GetPointIds().SetId(i, point_ids[i])

        cell_array.InsertNextCell(cell)

    new_ugrid = vtk.vtkUnstructuredGrid()
    new_ugrid.SetPoints(points)
    new_ugrid.SetCells(vtk.VTK_HEXAHEDRON, cell_array)

    n_arrays = ugrid.GetPointData().GetNumberOfArrays()
    for k_array in range(n_arrays):
        new_ugrid.GetCellData().AddArray(ugrid.GetPointData().GetArray(k_array))

    return new_ugrid
