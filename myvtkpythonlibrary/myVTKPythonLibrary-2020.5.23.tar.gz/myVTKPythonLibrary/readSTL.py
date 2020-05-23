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

def readSTL(
        filename,
        verbose=0):

    mypy.my_print(verbose, "*** readSTL: "+filename+" ***")
    mypy.my_print(1, "*** DEPRECATED: USE READPDATA INSTEAD! ***")

    assert (os.path.isfile(filename)), "Wrong filename (\""+filename+"\"). Aborting."

    stl_reader = vtk.vtkSTLReader()
    stl_reader.SetFileName(filename)
    stl_reader.Update()
    pdata = stl_reader.GetOutput()

    mypy.my_print(verbose-1, "n_points = "+str(pdata.GetNumberOfPoints()))
    mypy.my_print(verbose-1, "n_cells = "+str(pdata.GetNumberOfCells()))

    mypy.my_print(verbose-1, "n_verts = "+str(pdata.GetNumberOfVerts()))
    mypy.my_print(verbose-1, "n_lines = "+str(pdata.GetNumberOfLines()))
    mypy.my_print(verbose-1, "n_polys = "+str(pdata.GetNumberOfPolys()))
    mypy.my_print(verbose-1, "n_strips = "+str(pdata.GetNumberOfStrips()))

    return pdata
