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

import myPythonLibrary as mypy
import myVTKPythonLibrary as myvtk

########################################################################

def rotateMatrixArray(
        old_array,
        old_array_storage="vec",
        in_vecs=None,
        R=None,
        out_vecs=None,
        verbose=0):

    mypy.my_print(verbose, "*** rotateMatrixArray ***")
    mypy.my_print(min(verbose,1), "*** Warning: in rotateMatrixArray, the definition of the global rotation is probably the inverse of the definition in previous rotateTensors function. ***")

    n_components = old_array.GetNumberOfComponents()
    if   (old_array_storage == "vec"):
        assert (n_components == 6), "Wrong number of components (n_components="+str(n_components)+"). Aborting."
    elif (old_array_storage == "Cmat"):
        assert (n_components == 9), "Wrong number of components (n_components="+str(n_components)+"). Aborting."
    elif (old_array_storage == "Fmat"):
        assert (n_components == 9), "Wrong number of components (n_components="+str(n_components)+"). Aborting."
    else:
        assert (0), "Wrong storage (old_array_storage="+str(old_array_storage)+"). Aborting."
    n_tuples = old_array.GetNumberOfTuples()
    new_array = myvtk.createFloatArray(old_array.GetName(), n_components, n_tuples)
    new_vector = numpy.empty(n_components)

    if (old_array_storage == "vec"):
        old_vector = numpy.empty(6)
    elif (old_array_storage == "Cmat"):
        old_vector = numpy.empty(9)
    elif (old_array_storage == "Fmat"):
        old_vector = numpy.empty(9)
    old_matrix = numpy.empty((3,3))
    new_matrix = numpy.empty((3,3))
    for k_tuple in range(n_tuples):
        old_array.GetTuple(k_tuple, old_vector)
        if (old_array_storage == "vec"):
            mypy.vec_col6_to_mat_sym33(old_vector, old_matrix)
        elif (old_array_storage == "Cmat"):
            mypy.cvec9_to_mat33(old_vector, old_matrix)
        elif (old_array_storage == "Fmat"):
            mypy.fvec9_to_mat33(old_vector, old_matrix)

        if (in_vecs is None):
            in_R = numpy.eye(3)
        else:
            in_R = numpy.transpose(numpy.array([in_vecs[0].GetTuple(k_tuple),
                                                in_vecs[1].GetTuple(k_tuple),
                                                in_vecs[2].GetTuple(k_tuple)]))

        if (out_vecs is None):
            out_R = numpy.eye(3)
        else:
            out_R = numpy.transpose(numpy.array([out_vecs[0].GetTuple(k_tuple),
                                                 out_vecs[1].GetTuple(k_tuple),
                                                 out_vecs[2].GetTuple(k_tuple)]))

        if (R is None):
            R = numpy.eye(3)

        full_R = numpy.dot(numpy.dot(numpy.transpose(in_R), R), out_R)

        new_matrix[:] = numpy.dot(numpy.dot(numpy.transpose(full_R), old_matrix), full_R)

        if (old_array_storage == "vec"):
            mypy.mat_sym33_to_vec_col6(new_matrix, new_vector)
        elif (old_array_storage == "Cmat"):
            mypy.mat33_to_cvec9(new_matrix, new_vector)
        elif (old_array_storage == "Fmat"):
            mypy.mat33_to_fvec9(new_matrix, new_vector)

        new_array.SetTuple(k_tuple, new_vector)

    return new_array
