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

import os
import vtk

import myPythonLibrary as mypy
import myVTKPythonLibrary as myvtk

########################################################################

def readMatLabImage(
        filename,
        field_name,
        field_type,
        spacing=[1.,1.,1.],
        verbose=0):

    mypy.my_print(verbose, "*** readMatLabImage ***")

    assert (os.path.isfile(filename)), "Wrong filename (\""+filename+"\"). Aborting."

    import scipy
    data = scipy.io.loadmat(filename)[field_name]

    n_pixels_x = len(data)
    n_pixels_y = len(data[0])
    n_pixels_z = len(data[0][0])

    n_pixels = n_pixels_x * n_pixels_y * n_pixels_z

    #points = vtk.vtkPoints()
    #points.SetNumberOfPoints(n_pixels)

    #cell_array = vtk.vtkCellArray()
    #cell = vtk.vtkVertex()

    if (field_type == "int"):
        array_data = myvtk.createIntArray(
            name=field_name,
            n_components=1,
            n_tuples=n_pixels)
    elif (field_type == "double"):
        array_data = myvtk.createFloatArray(
            name=field_name,
            n_components=1,
            n_tuples=n_pixels)

    k_pixel = 0
    for k_z in range(n_pixels_z):
        for k_y in range(n_pixels_y):
            for k_x in range(n_pixels_x):
                #points.InsertPoint(k_pixel, [(k_x+0.5)/n_pixels_x,\
                                               #(k_y+0.5)/n_pixels_y,\
                                               #(k_z+0.5)/n_pixels_z])

                #cell.GetPointIds().SetId(0, k_pixel)
                #cell_array.InsertNextCell(cell)

                #array_data.SetTuple1(k_pixel, data[n_pixels_y-1-k_y][n_pixels_x-1-k_x][k_z])
                #array_data.SetTuple1(k_pixel, data[n_pixels_y-1-k_y][k_x][k_z])
                #array_data.SetTuple1(k_pixel, data[k_y][n_pixels_x-1-k_x][k_z])
                array_data.SetTuple1(k_pixel, data[k_y][k_x][k_z])
                #array_data.SetTuple1(k_pixel, data[n_pixels_x-1-k_x][n_pixels_y-1-k_y][k_z])
                #array_data.SetTuple1(k_pixel, data[n_pixels_x-1-k_x][k_y][k_z])
                #array_data.SetTuple1(k_pixel, data[k_x][n_pixels_y-1-k_y][k_z])
                #array_data.SetTuple1(k_pixel, data[k_x][k_y][k_z])

                k_pixel += 1

    #ugrid = vtk.vtkUnstructuredGrid()
    #ugrid.SetPoints(points)
    #ugrid.SetCells(vtk.VTK_VERTEX, cell_array)
    #ugrid.GetCellData().AddArray(array_data)
    #writeXMLUGrid(ugrid, case+".vtu")

    image = vtk.vtkImageData()
    image.SetExtent(0, n_pixels_x-1, 0, n_pixels_y-1, 0, n_pixels_z-1)
    image.SetSpacing(spacing)
    image.GetPointData().AddArray(array_data)

    return image
