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

import myPythonLibrary as mypy
import myVTKPythonLibrary as myvtk

########################################################################

def addMappingFromPointsToCells(
        ugrid_points,
        ugrid_cells,
        verbose=0):

    mypy.my_print(verbose, "*** addMappingFromPointsToCells ***")

    n_points = ugrid_points.GetNumberOfPoints()
    n_cells = ugrid_cells.GetNumberOfCells()
    #print "n_points = "+str(n_points)
    #print "n_cells = "+str(n_cells)

    (cell_locator,
     closest_point,
     generic_cell,
     k_cell,
     subId,
     dist) = getCellLocator(
         mesh=ugrid_cells,
         verbose=verbose-1)

    iarray_k_cell = createIntArray(
        name="k_cell",
        n_components=1,
        n_tuples=n_points,
        verbose=verbose-1)
    ugrid_points.GetPointData().AddArray(iarray_k_cell)
    ugrid_points.GetCellData().AddArray(iarray_k_cell)

    point = numpy.empty(3)
    for k_point in range(n_points):
        ugrid_points.GetPoint(
            k_point,
            point)

        cell_locator.FindClosestPoint(
            point,
            closest_point,
            generic_cell,
            k_cell,
            subId,
            dist)
        #k_cell = cell_locator.FindCell(point)
        #print "k_point = "+str(k_point)
        #print "k_cell = "+str(k_cell)

        iarray_k_cell.SetTuple1(
            k_point,
            k_cell)
