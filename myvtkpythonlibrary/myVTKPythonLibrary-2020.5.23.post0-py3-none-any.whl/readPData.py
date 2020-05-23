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

def readPData(
        filename,
        verbose=0):

    mypy.my_print(verbose, "*** readPData: "+filename+" ***")

    assert (os.path.isfile(filename)), "Wrong filename (\""+filename+"\"). Aborting."

    if   (filename.endswith("vtk")):
        pdata_reader = vtk.vtkPolyDataReader()
    elif (filename.endswith("vtp")):
        pdata_reader = vtk.vtkXMLPolyDataReader()
    elif (filename.endswith("stl")):
        pdata_reader = vtk.vtkSTLReader()
    else:
        assert 0, "File must be .vtk, .vtp or .stl. Aborting."

    pdata_reader.SetFileName(filename)
    pdata_reader.Update()
    pdata = pdata_reader.GetOutput()

    mypy.my_print(verbose-1, "n_points = "+str(pdata.GetNumberOfPoints()))
    mypy.my_print(verbose-1, "n_cells = "+str(pdata.GetNumberOfCells()))

    return pdata
