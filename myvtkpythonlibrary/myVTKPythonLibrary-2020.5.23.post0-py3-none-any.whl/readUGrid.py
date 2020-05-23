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

def readUGrid(
        filename,
        verbose=0):

    mypy.my_print(verbose, "*** readUGrid: "+filename+" ***")

    assert (os.path.isfile(filename)), "Wrong filename (\""+filename+"\"). Aborting."

    if   (filename.endswith("vtk")):
        ugrid_reader = vtk.vtkUnstructuredGridReader()
    elif (filename.endswith("vtu")):
        ugrid_reader = vtk.vtkXMLUnstructuredGridReader()
    else:
        assert 0, "File must be .vtk or .vtu. Aborting."

    ugrid_reader.SetFileName(filename)
    ugrid_reader.Update()
    ugrid = ugrid_reader.GetOutput()

    mypy.my_print(verbose-1, "n_points = "+str(ugrid.GetNumberOfPoints()))
    mypy.my_print(verbose-1, "n_cells = "+str(ugrid.GetNumberOfCells()))

    return ugrid
