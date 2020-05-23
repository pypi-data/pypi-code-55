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

def readAbaqusStressFromDAT(
        data_filename,
        verbose=0):

    mypy.my_print(verbose, "*** readAbaqusStressFromDAT: "+data_filename+" ***")

    s_array = myvtk.createFloatArray("", 6)

    data_file = open(data_filename, "r")
    context = ""
    k_cell = 0
    for line in data_file:
        if (context == "reading stresses"):
            #print line
            if ("MAXIMUM" in line):
                context = ""
                continue
            if ("OR" in line):
                splitted_line = line.split()
                assert (int(splitted_line[0]) == k_cell+1), "Wrong element number. Aborting."
                s_list = [float(splitted_line[k]) for k in range(3,9)]
                s_array.InsertNextTuple(s_list)
                k_cell += 1

        if (line == "    ELEMENT  PT FOOT-       S11         S22         S33         S12         S13         S23     \n"):
            context = "reading stresses"

    data_file.close()

    mypy.my_print(verbose-1, "n_tuples = "+str(s_array.GetNumberOfTuples()))

    return s_array
