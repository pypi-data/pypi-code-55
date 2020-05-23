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

def readImage(
        filename,
        verbose=0):

    mypy.my_print(verbose, "*** readImage: "+filename+" ***")

    assert (os.path.isfile(filename)), "Wrong filename (\""+filename+"\"). Aborting."

    if   (filename.endswith("vtk")):
        image_reader = vtk.vtkImageReader()
    elif (filename.endswith("vti")):
        image_reader = vtk.vtkXMLImageDataReader()
    else:
        assert 0, "File must be .vtk or .vti. Aborting."

    image_reader.SetFileName(filename)
    image_reader.Update()
    image = image_reader.GetOutput()

    mypy.my_print(verbose-1, "n_points = "+str(image.GetNumberOfPoints()))

    return image
