import unittest
import w7x
import numpy as np


class MagneticConfig_Test(unittest.TestCase):
    def setUp(self):
        self.inst = w7x.flt.MagneticConfig.default()

    def test_current_units(self):
        units = ['rw', 'Aw', 'A', 'r']
        for unit in units:
            m_tmp = w7x.flt.MagneticConfig.from_currents(
                *self.inst.coil_currents(unit=unit),
                unit=unit, scale=None)
            for check_unit in units:
                self.assertTrue(
                    np.isclose(m_tmp.coil_currents(check_unit),
                               self.inst.coil_currents(check_unit)).all()
                )


class MagneticConfig_FromCurrents_Test(MagneticConfig_Test):
    def setUp(self):
        self.inst = w7x.flt.MagneticConfig.from_currents(
            1, 1, 1, 1, 1,
            -0.23, -0.23,
            0.001, 0.001,
            0.0002, 0.0002, 0.0002, 0.0002, 0.0002,
            unit='rw')


if __name__ == '__main__':
    # m = MagneticConfig_FromCurrents_Test()
    # m.setUp()
    # m.test_current_units()
    unittest.main()
