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

def readSGrid(
        filename,
        verbose=0):

    mypy.my_print(verbose, "*** readSGrid: "+filename+" ***")

    assert (os.path.isfile(filename)), "Wrong filename (\""+filename+"\"). Aborting."

    if   (filename.endswith("vtk")):
        sgrid_reader = vtk.vtkStructuredGridReader()
    elif (filename.endswith("vts")):
        sgrid_reader = vtk.vtkXMLStructuredGridReader()
    else:
        assert 0, "File must be .vtk or .vts. Aborting."

    sgrid_reader.SetFileName(filename)
    sgrid_reader.Update()
    sgrid = sgrid_reader.GetOutput()

    mypy.my_print(verbose-1, "n_points = "+str(sgrid.GetNumberOfPoints()))
    mypy.my_print(verbose-1, "n_cells = "+str(sgrid.GetNumberOfCells()))

    return sgrid
