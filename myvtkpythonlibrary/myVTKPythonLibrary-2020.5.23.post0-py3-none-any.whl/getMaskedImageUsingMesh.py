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

def getMaskedImageUsingMesh(
        image,
        mesh,
        filter_with_field=None,
        verbose=0):

    mypy.my_print(verbose, "*** getMaskedImageUsingMesh ***")

    n_points = image.GetNumberOfPoints()
    farray_scalars_image = image.GetPointData().GetArray("scalars") # note that the field is defined at the points, not the cells

    (cell_locator,
     closest_point,
     generic_cell,
     k_cell,
     subId,
     dist) = myvtk.getCellLocator(
        mesh=mesh,
        verbose=verbose-1)

    if (filter_with_field != None):
        field = mesh.GetCellData().GetArray(filter_with_field[0])
        field_values = filter_with_field[1]

    points = vtk.vtkPoints()

    farray_scalars = myvtk.createFloatArray(
        name="scalars",
        n_components=1)

    point = numpy.empty(3)
    for k_point in range(n_points):
        image.GetPoint(k_point, point)

        k_cell = cell_locator.FindCell(point)
        if (k_cell == -1): continue
        if (filter_with_field != None) and (field.GetTuple1(k_cell) not in field_values): continue

        points.InsertNextPoint(point)
        farray_scalars.InsertNextTuple(farray_scalars_image.GetTuple(k_point))

    ugrid = vtk.vtkUnstructuredGrid()
    ugrid.SetPoints(points)
    ugrid.GetPointData().AddArray(farray_scalars)
    myvtk.addVertices(
        ugrid)

    return ugrid
