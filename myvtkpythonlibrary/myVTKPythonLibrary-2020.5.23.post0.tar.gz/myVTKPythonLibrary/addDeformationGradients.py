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

def addDeformationGradients(
        mesh,
        disp_array_name="Displacement",
        defo_grad_array_name="DeformationGradient",
        verbose=0):

    mypy.my_print(verbose, "*** addDeformationGradients ***")

    mypy.my_print(min(verbose,1), "*** Warning: at some point the ordering of vector gradient components has changed, and uses C ordering instead of F. ***")
    if   (vtk.vtkVersion.GetVTKMajorVersion() >= 8):
        ordering = "C"
    elif (vtk.vtkVersion.GetVTKMajorVersion() == 7) and ((vtk.vtkVersion.GetVTKMinorVersion() > 0) or (vtk.vtkVersion.GetVTKBuildVersion() > 0)):
        ordering = "C"
    else:
        ordering = "F"

    n_cells = mesh.GetNumberOfCells()

    assert (mesh.GetPointData().HasArray(disp_array_name))
    mesh.GetPointData().SetActiveVectors(disp_array_name)
    cell_derivatives = vtk.vtkCellDerivatives()
    cell_derivatives.SetVectorModeToPassVectors()
    cell_derivatives.SetTensorModeToComputeGradient()
    if (vtk.vtkVersion.GetVTKMajorVersion() >= 6):
        cell_derivatives.SetInputData(mesh)
    else:
        cell_derivatives.SetInput(mesh)
    cell_derivatives.Update()
    farray_gu = cell_derivatives.GetOutput().GetCellData().GetArray("VectorGradient")

    farray_defo_grad = myvtk.createFloatArray(
        name=defo_grad_array_name,
        n_components=9,
        n_tuples=n_cells)
    mesh.GetCellData().AddArray(farray_defo_grad)
    I = numpy.eye(3)
    for k_cell in range(n_cells):
        GU = numpy.reshape(farray_gu.GetTuple(k_cell), (3,3), order=ordering)
        F = I + GU
        farray_defo_grad.SetTuple(k_cell, numpy.reshape(F, 9, order="C"))
