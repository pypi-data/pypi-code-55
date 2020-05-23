#coding=utf8

########################################################################
###                                                                  ###
### Created by Martin Genet, 2012-2020                               ###
###                                                                  ###
### University of California at San Francisco (UCSF), USA            ###
### Swiss Federal Institute of Technology (ETH), Zurich, Switzerland ###
### École Polytechnique, Palaiseau, France                           ###
###                                                                  ###
###                                                                  ###
### And Cécile Patte, 2019                                           ###
###                                                                  ###
### INRIA, Palaiseau, France                                         ###
###                                                                  ###
########################################################################

from builtins import range

import glob
import numpy
import vtk

import myPythonLibrary    as mypy
import myVTKPythonLibrary as myvtk

################################################################################

def computeMaskFromMesh(
        image,
        mesh,
        warp_mesh=1,
        mesh_displacement_field_name="U",
        binary_mask=1,
        in_value=1.0,
        out_value=0.0,
        verbose=0):

    mypy.my_print(verbose, "*** computeMaskFromMesh ***")

    if (binary_mask):
        thres = vtk.vtkImageThreshold()
        thres.SetInputData(image)
        thres.ThresholdByUpper(0.)
        thres.SetInValue(in_value)
        thres.ReplaceInOn()
        thres.Update()
        image = thres.GetOutput()

    geom = vtk.vtkGeometryFilter()
    if (warp_mesh):
        assert (mesh.GetPointData().HasArray(mesh_displacement_field_name)),\
            "No array '" + mesh_displacement_field_name + "' in mesh. Aborting."
        mesh.GetPointData().SetActiveVectors(mesh_displacement_field_name)
        warp = vtk.vtkWarpVector()
        warp.SetInputData(mesh)
        warp.Update()
        geom.SetInputData(warp.GetOutput())
    else:
        geom.SetInputData(mesh)
    geom.Update()

    pol2stenc = vtk.vtkPolyDataToImageStencil()
    pol2stenc.SetInputData(geom.GetOutput())
    pol2stenc.SetOutputOrigin(image.GetOrigin())
    pol2stenc.SetOutputSpacing(image.GetSpacing())
    pol2stenc.SetOutputWholeExtent(image.GetExtent())
    # pol2stenc.CopyInformationFromPipeline(image.GetInformation())
    pol2stenc.Update()

    imgstenc = vtk.vtkImageStencil()
    imgstenc.SetInputData(image)
    imgstenc.SetStencilData(pol2stenc.GetOutput())
    imgstenc.ReverseStencilOff()
    imgstenc.SetBackgroundValue(out_value)
    imgstenc.Update()

    return imgstenc.GetOutput()
