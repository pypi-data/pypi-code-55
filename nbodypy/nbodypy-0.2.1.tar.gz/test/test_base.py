#!/usr/bin/env python

import unittest
import numpy
import nbodypy


class TestSimple(unittest.TestCase):
    """
    Simple unit test for the nbodyby module
    """
    def setUp(self):
        """
        Initialization
        """
    def test_construtor(self):
        """
        Basic constructor
        """
        system = nbodypy.Nbody()
        self.assertEqual(system.get_N(),2)
        self.assertEqual(system.get_dim(),4)
    def test_initN(self):
        """
        Test the constructor defining the number of bodies
        """
        system = nbodypy.Nbody(8)
        self.assertEqual(system.get_N(),8)
    def test_initDim(self):
        """
        Test the constructor defining the dimension
        """
        system = nbodypy.Nbody(dim=6)
        self.assertEqual(system.get_dim(),6)
    def test_initZ(self):
        """
        Test the constructor defining the initial condition
        """
        zinit = numpy.array([1.382857, 0.0, 0.0, 0.584873, 0.0, 0.157030, 1.1871935, 0.0, -1.382857, 0.0, 0.0, -0.584873, 0.0, -0.157030, -1.1871935, 0.0])
        system = nbodypy.Nbody(init=zinit)
        self.assertIsNone(numpy.testing.assert_array_equal(system.z,zinit))
    def test_getR(self):
        """
        Test the method to get the position
        """
        zinit = numpy.array([1.382857, 0.0, 0.0, 0.584873, 0.0, 0.157030, 1.1871935, 0.0, -1.382857, 0.0, 0.0, -0.584873, 0.0, -0.157030, -1.1871935, 0.0])
        system = nbodypy.Nbody(init=zinit)
        self.assertIsNone(numpy.testing.assert_array_equal(system.get_r(0),zinit[0:2]))
    def test_getV(self):
        """
        Test the Method to get the velocity
        """
        zinit = numpy.array([1.382857, 0.0, 0.0, 0.584873, 0.0, 0.157030, 1.1871935, 0.0, -1.382857, 0.0, 0.0, -0.584873, 0.0, -0.157030, -1.1871935, 0.0])
        system = nbodypy.Nbody(init=zinit)
        self.assertIsNone(numpy.testing.assert_array_equal(system.get_v(0),zinit[2:4]))


if __name__ =='__main__':
    unittest.main()
