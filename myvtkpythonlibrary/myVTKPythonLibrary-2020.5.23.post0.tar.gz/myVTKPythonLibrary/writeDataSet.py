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

def writeDataSet(
        dataset,
        filename,
        verbose=0):

    mypy.my_print(verbose, "*** writeDataSet: "+filename+" ***")

    file_ext = filename[-3:]
    if (file_ext == "vti") or ((file_ext == "vtk") and dataset.IsA("vtkImageData")):
        myvtk.writeImage(
            image=dataset,
            filename=filename,
            verbose=verbose-1)
    elif (file_ext == "vtp") or ((file_ext == "vtk") and dataset.IsA("vtkPolyData")):
        myvtk.writePData(
            pdata=dataset,
            filename=filename,
            verbose=verbose-1)
    elif (file_ext == "stl"):
        myvtk.writeSTL(
            pdata=dataset,
            filename=filename,
            verbose=verbose-1)
    elif (file_ext == "vts") or ((file_ext == "vtk") and dataset.IsA("vtkStructuredGrid")):
        myvtk.writeSGrid(
            sgrid=dataset,
            filename=filename,
            verbose=verbose-1)
    elif (file_ext == "vtu") or ((file_ext == "vtk") and dataset.IsA("vtkUnstructuredGrid")):
        myvtk.writeUGrid(
            ugrid=dataset,
            filename=filename,
            verbose=verbose-1)
    else:
        assert 0, "Wrong extention ("+file_ext+"). Extention must be vtk, vti, vtp, stl, vts, vtu. Aborting."
