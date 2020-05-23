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

import vtk

import myPythonLibrary as mypy
import myVTKPythonLibrary as myvtk

########################################################################

def readAbaqusMeshFromINP(
        mesh_filename,
        elem_types="all",
        verbose=0):

    mypy.my_print(verbose, "*** readAbaqusMeshFromINP: "+mesh_filename+" ***")

    points = vtk.vtkPoints()
    cell_array = vtk.vtkCellArray()

    mesh_file = open(mesh_filename, "r")

    context = ""
    for line in mesh_file:
        if line.startswith("**"): continue

        line = line.strip("\n ,")
        #mypy.my_print(verbose-1, "line =", line)

        if (context != ""):
            if line.startswith("*"):
                context = ""
            else:
                if (context == "reading nodes"):
                    splitted_line = line.split(",")
                    points.InsertNextPoint([float(coord) for coord in splitted_line[1:4]])
                elif (context == "reading elems"):
                    splitted_line = line.split(",")
                    assert (len(splitted_line) == 1+cell_n_points), "Wrong number of elements in line. Aborting."
                    for k_point in range(cell_n_points): cell.GetPointIds().SetId(k_point, int(splitted_line[1+k_point])-1)
                    cell_array.InsertNextCell(cell)

        if line.startswith("*NODE"):
            context = "reading nodes"
        elif line.startswith("*ELEMENT"):
            if (("TYPE=CPS3" in line) or ("type=CPS3" in line) or ("TYPE=CPE3" in line) or ("type=CPE3" in line)) and (("tri" in elem_types) or (elem_types == "all")):
                context = "reading elems"
                cell_vtk_type = vtk.VTK_TRIANGLE
                cell_n_points = 3
                cell = vtk.vtkTriangle()
            elif (("TYPE=F3D4" in line) or ("type=F3D4" in line)) and (("quad" in elem_types) or (elem_types == "all")):
                context = "reading elems"
                cell_vtk_type = vtk.VTK_QUAD
                cell_n_points = 4
                cell = vtk.vtkQuad()
            elif (("TYPE=C3D4" in line) or ("type=C3D4" in line)) and (("tet" in elem_types) or (elem_types == "all")):
                context = "reading elems"
                cell_vtk_type = vtk.VTK_TETRA
                cell_n_points = 4
                cell = vtk.vtkTetra()
            elif (("TYPE=C3D8" in line) or ("type=C3D8" in line)) and (("hex" in elem_types) or (elem_types == "all")):
                context = "reading elems"
                cell_vtk_type = vtk.VTK_HEXAHEDRON
                cell_n_points = 8
                cell = vtk.vtkHexahedron()
            else:
                mypy.my_print(verbose, "Warning: elements not read: "+line+".")

    mesh_file.close()

    ugrid = vtk.vtkUnstructuredGrid()
    ugrid.SetPoints(points)
    ugrid.SetCells(cell_vtk_type, cell_array)

    mypy.my_print(verbose-1, "n_cells = "+str(ugrid.GetNumberOfCells()))

    return ugrid
