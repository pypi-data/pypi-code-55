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

def getPointsInCell(
        points,
        cell,
        verbose=0):

    mypy.my_print(verbose, "*** getPointsInCell ***")

    ugrid_cell = vtk.vtkUnstructuredGrid()
    ugrid_cell.SetPoints(cell.GetPoints())
    cell = vtk.vtkHexahedron()
    for k_point in range(8): cell.GetPointIds().SetId(k_point, k_point)
    cell_array_cell = vtk.vtkCellArray()
    cell_array_cell.InsertNextCell(cell)
    ugrid_cell.SetCells(vtk.VTK_HEXAHEDRON, cell_array_cell)

    geometry_filter = vtk.vtkGeometryFilter()
    if (vtk.vtkVersion.GetVTKMajorVersion() >= 6):
        geometry_filter.SetInputData(ugrid_cell)
    else:
        geometry_filter.SetInput(ugrid_cell)
    geometry_filter.Update()
    cell_boundary = geometry_filter.GetOutput()

    pdata_points = vtk.vtkPolyData()
    pdata_points.SetPoints(points)

    enclosed_points_filter = vtk.vtkSelectEnclosedPoints()
    enclosed_points_filter.SetSurfaceData(cell_boundary)
    if (vtk.vtkVersion.GetVTKMajorVersion() >= 6):
        enclosed_points_filter.SetInputData(pdata_points)
    else:
        enclosed_points_filter.SetInput(pdata_points)
    enclosed_points_filter.Update()

    points_in_cell = [k_point for k_point in range(points.GetNumberOfPoints()) if enclosed_points_filter.GetOutput().GetPointData().GetArray("SelectedPoints").GetTuple1(k_point)]
    return points_in_cell
