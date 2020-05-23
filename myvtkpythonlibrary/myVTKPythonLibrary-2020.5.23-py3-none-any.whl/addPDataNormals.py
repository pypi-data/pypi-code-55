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

def addPDataNormals(
        pdata,
        orient_outward=1,
        verbose=0):

    mypy.my_print(verbose, "*** addPDataNormals ***")

    pdata_normals = vtk.vtkPolyDataNormals()
    pdata_normals.ComputePointNormalsOff()
    pdata_normals.ComputeCellNormalsOn()
    if (vtk.vtkVersion.GetVTKMajorVersion() >= 6):
        pdata_normals.SetInputData(pdata)
    else:
        pdata_normals.SetInput(pdata)
    pdata_normals.Update()
    pdata.GetCellData().SetNormals(pdata_normals.GetOutput().GetCellData().GetNormals())

    if (orient_outward):
        cell_centers = myvtk.getCellCenters(
            mesh=pdata,
            verbose=verbose-1)
        cell_center = numpy.empty(3)

        mesh_center = numpy.array(pdata.GetCenter())

        normals = pdata.GetCellData().GetNormals()
        normal = numpy.empty(3)

        cnt_pos = 0
        cnt_neg = 0
        for k_cell in range(pdata.GetNumberOfCells()):
            cell_centers.GetPoint(k_cell, cell_center)
            outward  = cell_center-mesh_center
            outward /= numpy.linalg.norm(outward)
            normals.GetTuple(k_cell, normal)
            proj = numpy.dot(outward, normal)
            if (proj > 0): cnt_pos += 1
            else:          cnt_neg += 1
        #print cnt_pos
        #print cnt_neg

        if (cnt_neg > cnt_pos):
            pdata_normals.FlipNormalsOn()
            pdata_normals.Update()
            pdata.GetCellData().SetNormals(pdata_normals.GetOutput().GetCellData().GetNormals())
