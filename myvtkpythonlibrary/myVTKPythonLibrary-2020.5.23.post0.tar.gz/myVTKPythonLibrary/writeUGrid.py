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

def writeUGrid(
        ugrid,
        filename,
        verbose=0):

    mypy.my_print(verbose, "*** writeUGrid: "+filename+" ***")

    if (filename.endswith("vtk")):
        ugrid_writer = vtk.vtkUnstructuredGridWriter()
    elif (filename.endswith("vtu")):
        ugrid_writer = vtk.vtkXMLUnstructuredGridWriter()
    else:
        assert 0, "File must be .vtk or .vtu. Aborting."

    ugrid_writer.SetFileName(filename)
    if (vtk.vtkVersion.GetVTKMajorVersion() >= 6):
        ugrid_writer.SetInputData(ugrid)
    else:
        ugrid_writer.SetInput(ugrid)
    ugrid_writer.Update()
    ugrid_writer.Write()
