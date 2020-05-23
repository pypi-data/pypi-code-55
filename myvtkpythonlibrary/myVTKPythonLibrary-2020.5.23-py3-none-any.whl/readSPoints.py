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

def readSPoints(
        filename,
        verbose=0):

    mypy.my_print(verbose, "*** readSPoints: "+filename+" ***")

    assert (os.path.isfile(filename)), "Wrong filename (\""+filename+"\"). Aborting."

    spoints_reader = vtk.vtkStructuredPointsReader()

    spoints_reader.SetFileName(filename)
    spoints_reader.Update()
    spoints = spoints_reader.GetOutput()

    mypy.my_print(verbose-1, "n_points = "+str(spoints.GetNumberOfPoints()))
    mypy.my_print(verbose-1, "n_cells = "+str(spoints.GetNumberOfCells()))

    return spoints
