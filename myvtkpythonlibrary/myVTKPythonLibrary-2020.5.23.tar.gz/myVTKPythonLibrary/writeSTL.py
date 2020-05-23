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

def writeSTL(
        pdata,
        filename,
        verbose=0):

    mypy.my_print(verbose, "*** writeSTL: "+filename+" ***")

    stl_writer = vtk.vtkSTLWriter()
    stl_writer.SetFileName(filename)
    if (vtk.vtkVersion.GetVTKMajorVersion() >= 6):
        stl_writer.SetInputData(pdata)
    else:
        stl_writer.SetInput(pdata)
    stl_writer.Update()
    stl_writer.Write()
