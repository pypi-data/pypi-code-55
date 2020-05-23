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

def getCellCenters(
        mesh,
        verbose=0):

    mypy.my_print(verbose, "*** getCellCenters ***")

    filter_cell_centers = vtk.vtkCellCenters()
    if (vtk.vtkVersion.GetVTKMajorVersion() >= 6):
        filter_cell_centers.SetInputData(mesh)
    else:
        filter_cell_centers.SetInput(mesh)
    filter_cell_centers.Update()
    cell_centers = filter_cell_centers.GetOutput()

    return cell_centers
