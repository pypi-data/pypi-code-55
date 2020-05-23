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

def addVertices(
        ugrid,
        verbose=0):

    mypy.my_print(verbose, "*** addVertices ***")

    cell = vtk.vtkVertex()
    cell_array = vtk.vtkCellArray()

    n_points = ugrid.GetPoints().GetNumberOfPoints()
    for k_point in range(n_points):
        cell.GetPointIds().SetId(0, k_point)
        cell_array.InsertNextCell(cell)

    ugrid.SetCells(vtk.VTK_VERTEX, cell_array)

    n_arrays = ugrid.GetPointData().GetNumberOfArrays()
    for k_array in range(n_arrays):
        ugrid.GetCellData().AddArray(ugrid.GetPointData().GetArray(k_array))
