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

def readDataSet(
        filename,
        verbose=0):

    mypy.my_print(verbose, "*** readDataSet: "+filename+" ***")

    assert (os.path.isfile(filename)), "Wrong filename (\""+filename+"\"). Aborting."

    file_ext = filename[-3:]
    if (file_ext == "vtk"):
        for line in open(filename):
            if (line.split()[0] == "DATASET"):
                dataset_type = line.split()[-1]
                break
        assert ("dataset_type" in locals()), "Wrong file format. Aborting."

        if (dataset_type == "STRUCTURED_POINTS"):
            return myvtk.readSPoints(
                filename=filename,
                verbose=verbose-1)
        elif (dataset_type == "STRUCTURED_GRID"):
            return myvtk.readSGrid(
                filename=filename,
                verbose=verbose-1)
        elif (dataset_type == "UNSTRUCTURED_GRID"):
            return myvtk.readUGrid(
                filename=filename,
                verbose=verbose-1)
        elif (dataset_type == "POLYDATA"):
            return myvtk.readPData(
                filename=filename,
                verbose=verbose-1)
        elif (dataset_type == "RECTILINEAR_GRID") or (dataset_type == "FIELD"):
            assert 0, "Not implemented. Aborting."
        else:
            assert 0, "Wrong dataset type ("+dataset_type+"). Aborting."
    elif (file_ext == "vti"):
        return myvtk.readImage(
            filename=filename,
            verbose=verbose-1)
    elif (file_ext == "vtp") or (file_ext == "stl"):
        return myvtk.readPData(
            filename=filename,
            verbose=verbose-1)
    elif (file_ext == "vts"):
        return myvtk.readSGrid(
            filename=filename,
            verbose=verbose-1)
    elif (file_ext == "vtu"):
        return myvtk.readUGrid(
            filename=filename,
            verbose=verbose-1)
    else:
        assert 0, "Wrong extention ("+file_ext+"). Extention must be vtk, vti, vtp, stl, vts, vtu. Aborting."
