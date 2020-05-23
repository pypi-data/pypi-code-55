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

import myPythonLibrary as mypy
import myVTKPythonLibrary as myvtk

########################################################################

def readDynaDeformationGradients(
        mesh,
        hystory_files_basename,
        array_name,
        verbose=0):

    mypy.my_print(verbose, "*** readDynaDeformationGradients ***")

    n_cells = mesh.GetNumberOfCells()

    history_files_names = [hystory_files_basename + ".history#" + str(num) for num in range(11,20)]

    F_list = [[0. for k_component in range(9)] for k_cell in range(n_cells)]

    for k_component in range(9):
        history_file = open(history_files_names[k_component], "r")
        for line in history_file:
            if line.startswith("*") or line.startswith("$"): continue
            line = line.split()
            F_list[int(line[0])-1][k_component] = float(line[1])
        history_file.close()

    F_array = myvtk.createFloatArray(array_name, 9, n_cells)

    for k_cell in range(n_cells):
        F_array.SetTuple(k_cell, F_list[k_cell])

    mypy.my_print(verbose-1, "n_tuples = "+str(F_array.GetNumberOfTuples()))

    mesh.GetCellData().AddArray(F_array)
