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

def writeSGrid(
        sgrid,
        filename,
        verbose=0):

    mypy.my_print(verbose, "*** writeSGrid: "+filename+" ***")

    if (filename.endswith("vtk")):
        sgrid_writer = vtk.vtkStructuredGridWriter()
    elif (filename.endswith("vts")):
        sgrid_writer = vtk.vtkXMLStructuredGridWriter()
    else:
        assert 0, "File must be .vtk or .vts. Aborting."

    sgrid_writer.SetFileName(filename)
    if (vtk.vtkVersion.GetVTKMajorVersion() >= 6):
        sgrid_writer.SetInputData(sgrid)
    else:
        sgrid_writer.SetInput(sgrid)
    sgrid_writer.Update()
    sgrid_writer.Write()
