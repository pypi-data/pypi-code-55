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

import vtk

import myPythonLibrary    as mypy
import myVTKPythonLibrary as myvtk

########################################################################

def computeUInt16MaskFromMesh(
        image,
        mesh,
        out_value,
        binary_mask=0,
        warp_mesh=0,
        verbose=0):

    mypy.my_print(verbose, "*** computeUInt16MaskFromMesh ***")

    assert (out_value <= 65535)
    cast = vtk.vtkImageCast()
    cast.SetInputData(image)
    cast.SetOutputScalarTypeToUnsignedShort()
    cast.Update()
    image_for_mask = cast.GetOutput()

    mask = myvtk.computeMaskFromMesh(
        image=image_for_mask,
        mesh=mesh,
        warp_mesh=warp_mesh,
        binary_mask=binary_mask,
        out_value=out_value)
    assert (mask.GetPointData().GetScalars().GetDataType() == 5)

    return mask
