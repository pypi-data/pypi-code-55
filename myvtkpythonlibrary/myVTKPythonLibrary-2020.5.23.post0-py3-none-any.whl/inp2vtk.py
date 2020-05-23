#!python3
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

import argparse

import myPythonLibrary as mypy
import myVTKPythonLibrary as myvtk

########################################################################

if (__name__ == "__main__"):
    parser = argparse.ArgumentParser()
    parser.add_argument("inp_filename", type=str)
    args = parser.parse_args()

    mesh = myvtk.readAbaqusMeshFromINP(
        mesh_filename=args.inp_filename,
        elem_types="all",
        verbose=1)

    myvtk.writeUGrid(
        ugrid=mesh,
        filename=args.inp_filename.replace(".inp", ".vtk"),
        verbose=1)
