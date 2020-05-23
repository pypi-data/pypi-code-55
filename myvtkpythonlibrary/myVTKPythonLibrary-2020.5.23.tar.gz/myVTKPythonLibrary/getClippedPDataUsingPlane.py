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

def getClippedPDataUsingPlane(
        pdata_mesh,
        plane_O,
        plane_N,
        generate_clipped_output=False, # 2017/12/01: this seems to mess up everything with the returned pointers…
        verbose=0):

    mypy.my_print(verbose, "*** getClippedPDataUsingPlane ***")

    plane = vtk.vtkPlane()
    plane.SetOrigin(plane_O)
    plane.SetNormal(plane_N)

    #mypy.my_print(verbose-1, "pdata_mesh.GetBounds() = "+str(pdata_mesh.GetBounds()))
    #mypy.my_print(verbose-1, "plane_O = "+str(plane_O))
    #mypy.my_print(verbose-1, "plane_N = "+str(plane_N))

    clip = vtk.vtkClipPolyData()
    clip.SetClipFunction(plane)
    if (generate_clipped_output):
        clip.GenerateClippedOutputOn()
    if (vtk.vtkVersion.GetVTKMajorVersion() >= 6):
        clip.SetInputData(pdata_mesh)
    else:
        clip.SetInput(pdata_mesh)
    clip.Update()
    if (generate_clipped_output):
        clipped0 = clip.GetOutput(0)
        clipped1 = clip.GetOutput(1)
    else:
        clipped = clip.GetOutput()

    #mypy.my_print(verbose-1, "clipped0.GetNumberOfPoints() = "+str(clipped0.GetNumberOfPoints()))
    #mypy.my_print(verbose-1, "clipped1.GetNumberOfPoints() = "+str(clipped1.GetNumberOfPoints()))
    #mypy.my_print(verbose-1, "clipped0.GetNumberOfCells() = "+str(clipped0.GetNumberOfCells()))
    #mypy.my_print(verbose-1, "clipped1.GetNumberOfCells() = "+str(clipped1.GetNumberOfCells()))

    #if (myvtk.getPDataSurfaceArea(clipped0) >= myvtk.getPDataSurfaceArea(clipped1)):
        #return clipped0, clipped1
    #else:
        #return clipped1, clipped0

    if (generate_clipped_output):
        return clipped0, clipped1
    else:
        return clipped
