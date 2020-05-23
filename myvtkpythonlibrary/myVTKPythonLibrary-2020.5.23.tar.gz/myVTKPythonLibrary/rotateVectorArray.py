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

def rotateVectorArray(
        old_array,
        in_vecs=None,
        R=None,
        out_vecs=None,
        verbose=0):

    mypy.my_print(verbose, "*** rotateVectorArray ***")

    n_components = old_array.GetNumberOfComponents()
    assert (n_components == 3), "Wrong number of components (n_components="+str(n_components)+", should be 3). Aborting."
    n_tuples = old_array.GetNumberOfTuples()
    new_array = myvtk.createFloatArray(old_array.GetName(), 3, n_tuples)
    new_vector = numpy.empty(3)
    old_vector = numpy.empty(3)

    for k_tuple in range(n_tuples):
        old_array.GetTuple(k_tuple, old_vector)

        if (in_vecs is None):
            in_R = numpy.eye(3)
        else:
            in_R = numpy.transpose(numpy.array([in_vecs[0].GetTuple(k_tuple),
                                                in_vecs[1].GetTuple(k_tuple),
                                                in_vecs[2].GetTuple(k_tuple)]))

        if (R is None):
            R = numpy.eye(3)

        if (out_vecs is None):
            out_R = numpy.eye(3)
        else:
            out_R = numpy.transpose(numpy.array([out_vecs[0].GetTuple(k_tuple),
                                                 out_vecs[1].GetTuple(k_tuple),
                                                 out_vecs[2].GetTuple(k_tuple)]))

        full_R = numpy.dot(numpy.dot(numpy.transpose(in_R), R), out_R)

        new_vector[:] = numpy.dot(numpy.transpose(full_R), old_vector)
        new_array.SetTuple(k_tuple, new_vector)

    return new_array
