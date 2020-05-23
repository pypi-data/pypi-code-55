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

def pdata2ugrid(
        pdata,
        verbose=0):

    mypy.my_print(verbose, "*** pdata2ugrid ***")

    filter_append = vtk.vtkAppendFilter()
    if (vtk.vtkVersion.GetVTKMajorVersion() >= 6):
        filter_append.SetInputData(pdata)
    else:
        filter_append.SetInput(pdata)
    filter_append.Update()
    ugrid = filter_append.GetOutput()

    return ugrid

########################################################################

if (__name__ == "__main__"):
    parser = argparse.ArgumentParser()
    parser.add_argument("pdata_filename", type=str)
    args = parser.parse_args()

    assert (args.ugrid_filename.endswith(".vtp"))
    pdata = myvtk.readPData(
        filename=args.pdata_filename)
    ugrid = myvtk.pdata2ugrid(
        pdata=pdata)
    myvtk.writeUGrid(
        ugrid=ugrid,
        filename=args.pdata_filename.replace(".vtp", ".vtu"))
