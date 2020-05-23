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

def writeImage(
        image,
        filename,
        verbose=0):

    mypy.my_print(verbose, "*** writeImage: "+filename+" ***")

    if (filename.endswith("vtk")):
        image_writer = vtk.vtkImageWriter()
    elif (filename.endswith("vti")):
        image_writer = vtk.vtkXMLImageDataWriter()
    else:
        assert 0, "File must be .vtk or .vti. Aborting."

    mypy.my_print(verbose, "n_points = "+str(image.GetNumberOfPoints()))

    image_writer.SetFileName(filename)
    if (vtk.vtkVersion.GetVTKMajorVersion() >= 6):
        image_writer.SetInputData(image)
    else:
        image_writer.SetInput(image)
    image_writer.Update()
    image_writer.Write()
