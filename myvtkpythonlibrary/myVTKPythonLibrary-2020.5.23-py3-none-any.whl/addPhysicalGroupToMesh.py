#!python3
#coding=utf8

########################################################################
###                                                                  ###
### Created by Martin Genet, 2012-2020                               ###
###     (Inspired by Lik Chuan Lee)                                  ###
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
import myVTKPythonLibrary as myVTK

########################################################################

def addPhysicalGroupToMesh(
        mesh,
        msh_filename,
        verbose=0):

    mypy.my_print(verbose, "*** addPhysicalGroupToMesh ***")

    n_cells = mesh.GetNumberOfCells()

    iarray_part_id = myVTK.createIntArray(
        name="part_id",
        n_tuples=n_cells,
        n_components=1)
    mesh.GetCellData().AddArray(iarray_part_id)

    msh = open(msh_filename)
    context = ""
    for line in msh:
        if line.startswith("$Elements"):
            context = "reading element number"
            continue
        elif line.startswith("$EndElements"):
            context = ""
            continue

        if (context == "reading elements"):
            splitted_line = line.split()
            iarray_part_id.SetTuple(int(splitted_line[0])-1, [int(splitted_line[3])-1])
        elif (context == "reading element number"):
            n_elements = int(line)
            assert (n_elements == n_cells)
            context = "reading elements"

########################################################################

if (__name__ == "__main__"):
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', type=str)
    args = parser.parse_args()

    mesh = myVTK.readDataSet(
        filename=args.filename)

    mesh_basename = args.filename.rsplit(".",1)[0]
    mesh_ext = args.filename.rsplit(".",1)[1]
    msh_filename = mesh_basename+".msh"

    myVTK.addPhysicalGroupToMesh(
        mesh=mesh,
        msh_filename=msh_filename)

    myVTK.writeDataSet(
        dataset=mesh,
        filename=mesh_basename+"-withPartID."+mesh_ext)
