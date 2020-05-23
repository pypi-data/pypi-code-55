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

def getPDataSurfaceArea(
        pdata,
        verbose=0):

    mypy.my_print(verbose, "*** getPDataSurfaceArea ***")

    mass_properties = myvtk.getMassProperties(
        pdata=pdata,
        verbose=verbose-1)

    return mass_properties.GetSurfaceArea()
