#!python3
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

import argparse
import vtk

import myPythonLibrary as mypy
import myVTKPythonLibrary as myvtk

########################################################################

def addImageGradient(
        image,
        image_dimensionality=None,
        verbose=0):

    mypy.my_print(verbose, "*** addImageGradient ***")

    if (image_dimensionality is None):
        image_dimensionality = myvtk.getImageDimensionality(
            image=image,
            verbose=verbose-1)

    image_gradient = vtk.vtkImageGradient()
    if (vtk.vtkVersion.GetVTKMajorVersion() >= 6):
        image_gradient.SetInputData(image)
    else:
        image_gradient.SetInput(image)
    image_gradient.SetDimensionality(image_dimensionality)
    image_gradient.Update()
    image_w_grad = image_gradient.GetOutput()

    name = image.GetPointData().GetScalars().GetName()
    image.GetPointData().AddArray(image_w_gradient.GetPointData().GetArray(name+"Gradient"))
    image.GetPointData().SetActiveScalars(name+"Gradient")

########################################################################

if (__name__ == "__main__"):
    parser = argparse.ArgumentParser()
    parser.add_argument("image_filename", type=str)
    parser.add_argument("--verbose", "-v", type=int, default=1)
    args = parser.parse_args()

    image = myvtk.readImage(
        filename=args.image_filename,
        verbose=args.verbose)

    myvtk.addImageGradient(
        image=image,
        verbose=args.verbose)

    myvtk.writeImage(
        image=image,
        filename=args.image_filename.replace(".vti", "-gradient.vti"),
        verbose=args.verbose)
