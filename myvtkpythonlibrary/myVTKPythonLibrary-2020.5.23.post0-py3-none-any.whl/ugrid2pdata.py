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

import argparse
import vtk

import myPythonLibrary as mypy
import myVTKPythonLibrary as myvtk

########################################################################

def ugrid2pdata(
        ugrid,
        only_trianlges=False,
        verbose=0):

    mypy.my_print(verbose, "*** ugrid2pdata ***")

    filter_geometry = vtk.vtkGeometryFilter()
    if (vtk.vtkVersion.GetVTKMajorVersion() >= 6):
        filter_geometry.SetInputData(ugrid)
    else:
        filter_geometry.SetInput(ugrid)
    filter_geometry.Update()
    pdata = filter_geometry.GetOutput()

    if (only_trianlges):
        filter_triangle = vtk.vtkTriangleFilter()
        if (vtk.vtkVersion.GetVTKMajorVersion() >= 6):
            filter_triangle.SetInputData(pdata)
        else:
            filter_triangle.SetInput(pdata)
        filter_triangle.Update()
        pdata = filter_triangle.GetOutput()

    return pdata

########################################################################

if (__name__ == "__main__"):
    parser = argparse.ArgumentParser()
    parser.add_argument("ugrid_filename", type=str)
    args = parser.parse_args()

    assert (args.ugrid_filename.endswith(".vtu"))
    ugrid = myvtk.readUGrid(
        filename=args.ugrid_filename)
    pdata = myvtk.ugrid2pdata(
        ugrid=ugrid)
    myvtk.writePData(
        pdata=pdata,
        filename=args.ugrid_filename.replace(".vtu", ".vtp"))
