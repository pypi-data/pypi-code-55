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

def addImageHessian(
        image,
        image_dimensionality=None,
        verbose=0):

    mypy.my_print(verbose, "*** addImageHessian ***")

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
    image_w_gradient = image_gradient.GetOutput()

    image_append_components = vtk.vtkImageAppendComponents()
    for k_dim in range(image_dimensionality):
        image_extract_components = vtk.vtkImageExtractComponents()
        if (vtk.vtkVersion.GetVTKMajorVersion() >= 6):
            image_extract_components.SetInputData(image_w_gradient)
        else:
            image_extract_components.SetInput(image_w_gradient)
        image_extract_components.SetComponents(k_dim)
        image_extract_components.Update()
        image_w_gradient_component = image_extract_components.GetOutput()

        image_gradient = vtk.vtkImageGradient()
        if (vtk.vtkVersion.GetVTKMajorVersion() >= 6):
            image_gradient.SetInputData(image_w_gradient_component)
        else:
            image_gradient.SetInput(image_w_gradient_component)
        image_gradient.SetDimensionality(image_dimensionality)
        image_gradient.Update()
        image_w_hessian_component = image_gradient.GetOutput()
        if (vtk.vtkVersion.GetVTKMajorVersion() >= 6):
            image_append_components.AddInputData(image_w_hessian_component)
        else:
            image_append_components.AddInput(image_w_hessian_component)

    image_append_components.Update()
    image_w_hessian = image_append_components.GetOutput()

    name = image.GetPointData().GetScalars().GetName()
    image.GetPointData().AddArray(image_w_gradient.GetPointData().GetArray(name+"Gradient"))
    image.GetPointData().AddArray(image_w_hessian.GetPointData().GetArray(name+"GradientGradient"))
    image.GetPointData().SetActiveScalars(name+"GradientGradient")

########################################################################

if (__name__ == "__main__"):
    parser = argparse.ArgumentParser()
    parser.add_argument("image_filename", type=str)
    parser.add_argument("--verbose", "-v", type=int, default=1)
    args = parser.parse_args()

    image = myvtk.readImage(
        filename=args.image_filename,
        verbose=args.verbose)

    myvtk.addImageHessian(
        image=image,
        verbose=args.verbose)

    myvtk.writeImage(
        image=image,
        filename=args.image_filename.replace(".vti", "-hessian.vti"),
        verbose=args.verbose)
