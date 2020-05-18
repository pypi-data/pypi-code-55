from tempfile import NamedTemporaryFile
import tfields
import numpy as np
import unittest
import sympy  # NOQA: F401
import os
import sys
from .test_core import TensorMaps_Check
THIS_DIR = os.path.dirname(
    os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(THIS_DIR)))


class Mesh3D_Check(TensorMaps_Check):
    def test_cut_split(self):
        x, y, z = sympy.symbols('x y z')
        self._inst.cut(x + 1./100*y > 0, at_intersection='split')

    def test_triangle(self):
        tri = self._inst.triangles()
        mesh = tri.mesh()
        tri_2 = mesh.triangles()  # mesh will not nec. be equal to self._inst
        # that is ok because self._inst could have stale indices etc..
        self.assertTrue(tri.equal(tri_2))

    def test_save_obj(self):
        out_file = NamedTemporaryFile(suffix='.obj')
        self._inst.save(out_file.name)
        _ = out_file.seek(0)  # this is only necessary in the test
        load_inst = type(self._inst).load(out_file.name)
        print(self._inst, load_inst)
        self.demand_equal(load_inst)


class Square_Test(Mesh3D_Check, unittest.TestCase):
    def setUp(self):
        self._inst = tfields.Mesh3D.plane((0, 1, 2j), (0, 1, 2j), (0, 0, 1j))


class Sphere_Test(Mesh3D_Check, unittest.TestCase):
    def setUp(self):
        basis_points = 4
        self._inst = tfields.Mesh3D.grid(
                (1, 1, 1),
                (-np.pi, np.pi, basis_points),
                (-np.pi / 2, np.pi / 2, basis_points),
                coord_sys='spherical')
        self._inst.transform('cartesian')
        self._inst[:, 1] += 2
        clean = self._inst.cleaned()
        # self.demand_equal(clean)
        self._inst = clean


class IO_Stl_test(unittest.TestCase):  # no Mesh3D_Check for speed
    def setUp(self):
        self._inst = tfields.Mesh3D.load(os.path.join(THIS_DIR,
                                                      '../data/baffle.stl'))


if __name__ == '__main__':
    unittest.main()
