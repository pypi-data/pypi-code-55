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

def addStrainsFromDeformationGradients(
        mesh,
        defo_grad_array_name="DeformationGradient",
        strain_array_name="Strain",
        mesh_w_local_basis=None,
        verbose=0):

    mypy.my_print(verbose, "*** addStrainsFromDeformationGradients ***")

    assert (mesh.GetCellData().HasArray(defo_grad_array_name))
    farray_f = mesh.GetCellData().GetArray(defo_grad_array_name)

    n_cells = mesh.GetNumberOfCells()
    if (mesh_w_local_basis is not None)\
    and (((mesh_w_local_basis.GetCellData().HasArray("eR"))\
      and (mesh_w_local_basis.GetCellData().HasArray("eC"))\
      and (mesh_w_local_basis.GetCellData().HasArray("eL")))\
    or ((mesh_w_local_basis.GetCellData().HasArray("eRR"))\
    and (mesh_w_local_basis.GetCellData().HasArray("eCC"))\
    and (mesh_w_local_basis.GetCellData().HasArray("eLL")))):
        farray_strain = myvtk.createFloatArray(
            name=strain_array_name+"_CAR",
            n_components=6,
            n_tuples=n_cells)
    else:
        farray_strain = myvtk.createFloatArray(
            name=strain_array_name,
            n_components=6,
            n_tuples=n_cells)
    mesh.GetCellData().AddArray(farray_strain)
    I = numpy.eye(3)
    E_vec = numpy.empty(6)
    #e_vec = numpy.empty(6)
    for k_cell in range(n_cells):
        F = numpy.reshape(farray_f.GetTuple(k_cell), (3,3), order="C")
        C = numpy.dot(numpy.transpose(F), F)
        E = (C - I)/2
        mypy.mat_sym33_to_vec_col6(E, E_vec)
        farray_strain.SetTuple(k_cell, E_vec)
        #if (add_almansi_strain):
            #Finv = numpy.linalg.inv(F)
            #c = numpy.dot(numpy.transpose(Finv), Finv)
            #e = (I - c)/2
            #mypy.mat_sym33_to_vec_col6(e, e_vec)
            #farray_almansi.SetTuple(k_cell, e_vec)

    if (mesh_w_local_basis is not None):
        if  (mesh_w_local_basis.GetCellData().HasArray("eR"))\
        and (mesh_w_local_basis.GetCellData().HasArray("eC"))\
        and (mesh_w_local_basis.GetCellData().HasArray("eL")):
            farray_strain_cyl = myvtk.rotateMatrixArray(
                old_array=mesh.GetCellData().GetArray(strain_array_name+"_CAR"),
                out_vecs=[mesh_w_local_basis.GetCellData().GetArray("eR"),
                          mesh_w_local_basis.GetCellData().GetArray("eC"),
                          mesh_w_local_basis.GetCellData().GetArray("eL")],
                verbose=0)
            farray_strain_cyl.SetName(strain_array_name+"_CYL")
            mesh.GetCellData().AddArray(farray_strain_cyl)

        if  (mesh_w_local_basis.GetCellData().HasArray("eRR"))\
        and (mesh_w_local_basis.GetCellData().HasArray("eCC"))\
        and (mesh_w_local_basis.GetCellData().HasArray("eLL")):
            farray_strain_pps = myvtk.rotateMatrixArray(
                old_array=mesh.GetCellData().GetArray(strain_array_name+"_CAR"),
                out_vecs=[mesh_w_local_basis.GetCellData().GetArray("eRR"),
                          mesh_w_local_basis.GetCellData().GetArray("eCC"),
                          mesh_w_local_basis.GetCellData().GetArray("eLL")],
                verbose=0)
            farray_strain_pps.SetName(strain_array_name+"_PPS")
            mesh.GetCellData().AddArray(farray_strain_pps)
