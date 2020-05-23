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

import numpy
import vtk

import myPythonLibrary as mypy
import myVTKPythonLibrary as myvtk

########################################################################

def addMappingToPointData(
        mesh_from,
        type_of_support,
        mesh_to,
        farray_names,
        radius=1.,
        threshold_min=None,
        threshold_max=None,
        verbose=0):

    mypy.my_print(verbose, "*** addMappingToPointData ***")

    if (type_of_support == "point"):
        dataset = mesh_from.GetPointData()
        point_locator = myvtk.getPointLocator(
            mesh_from)
    elif (type_of_support == "cell"):
        dataset = mesh_from.GetPointData()
        pdata_cell_centers_fr = myvtk.getCellCenters(
            mesh=mesh_from,
            verbose=verbose-1)
        point_locator = myvtk.getPointLocator(
            pdata_cell_centers_fr)

    n_points = mesh_to.GetNumberOfPoints()

    farrays_avg = {}
    farrays_std = {}
    farrays_rat = {}
    for farray_name in farray_names:
        assert (dataset.HasArray(farray_name)),\
            "mesh has no array named "+farray_name+". Aborting."

        farray_type = dataset.GetArray(farray_name).GetDataTypeAsString()
        farray_n_components = dataset.GetArray(farray_name).GetNumberOfComponents()
        farrays_avg[farray_name] = myvtk.createArray(
            farray_name+"_avg",
            farray_n_components,
            n_points,
            farray_type)
        farrays_std[farray_name] = myvtk.createArray(
            farray_name+"_std",
            farray_n_components,
            n_points,
            farray_type)
        farrays_rat[farray_name] = myvtk.createArray(
            farray_name+"_rat",
            farray_n_components,
            n_points,
            farray_type)

    points_within_radius = vtk.vtkIdList()

    for k_point in range(n_points):
        #point_locator.FindClosestNPoints(
            #3,
            #mesh_to.GetPoints().GetPoint(k_point),
            #points_within_radius)
        point_locator.FindPointsWithinRadius(
            radius,
            mesh_to.GetPoints().GetPoint(k_point),
            points_within_radius)

        for farray_name in farray_names:
            farray_n_components = dataset.GetArray(farray_name).GetNumberOfComponents()
            if (points_within_radius.GetNumberOfIds() > 0):
                values = [numpy.array(dataset.GetArray(farray_name).GetTuple(points_within_radius.GetId(k_id))) for k_id in range(points_within_radius.GetNumberOfIds())]
                #print "values = "+str(values)
                if (threshold_min != None):
                    values = [value for value in values if (numpy.linalg.norm(value) > threshold_min)]
                if (threshold_max != None):
                    values = [value for value in values if (numpy.linalg.norm(value) < threshold_max)]
                #print "values = "+str(values)
                if (len(values) > 0):
                    avg = numpy.mean(values, 0)
                    std = numpy.std(values, 0)
                    if (avg != 0).all():
                        rat = std/avg
                    else:
                        rat = [0]*farray_n_components
                else:
                    avg = [0]*farray_n_components
                    std = [0]*farray_n_components
                    rat = [0]*farray_n_components
            else:
                avg = [0]*farray_n_components
                std = [0]*farray_n_components
                rat = [0]*farray_n_components
            farrays_avg[farray_name].SetTuple(k_point, avg)
            farrays_std[farray_name].SetTuple(k_point, std)
            farrays_rat[farray_name].SetTuple(k_point, rat)

    for farray_name in farray_names:
        mesh_to.GetPointData().AddArray(farrays_avg[farray_name])
        mesh_to.GetPointData().AddArray(farrays_std[farray_name])
        mesh_to.GetPointData().AddArray(farrays_rat[farray_name])
