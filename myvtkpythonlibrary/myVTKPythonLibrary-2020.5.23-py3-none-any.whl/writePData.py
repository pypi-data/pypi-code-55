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

def writePData(
        pdata,
        filename,
        verbose=0):

    mypy.my_print(verbose, "*** writePData: "+filename+" ***")

    if (filename.endswith("vtk")):
        pdata_writer = vtk.vtkPolyDataWriter()
    elif (filename.endswith("vtp")):
        pdata_writer = vtk.vtkXMLPolyDataWriter()
    else:
        assert 0, "File must be .vtk or .vtp. Aborting."

    pdata_writer.SetFileName(filename)
    if (vtk.vtkVersion.GetVTKMajorVersion() >= 6):
        pdata_writer.SetInputData(pdata)
    else:
        pdata_writer.SetInput(pdata)
    pdata_writer.Update()
    pdata_writer.Write()
