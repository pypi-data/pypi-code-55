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
    parser.add_argument("vtk_filename", type=str)
    args = parser.parse_args()

    assert (args.vtk_filename.endswith(".vtk"))
    mesh = myvtk.readUGrid(
        filename=args.vtk_filename)
    myvtk.writeUGrid(
        ugrid=mesh,
        filename=args.vtk_filename.replace(".vtk", ".vtu"))
