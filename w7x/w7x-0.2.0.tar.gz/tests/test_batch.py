import unittest
import w7x
import os
import shutil
import numpy as np
import pandas as pd

folder = '~/tmp/VMEC/test/'
vmec_features = ["phiedge", "coilCurrents"]
size = 10

magnetic_config = w7x.flt.MagneticConfig.default()
pressure_profile = w7x.vmec.PowerSeries()
current_profile = w7x.vmec.PowerSeries()
magneticAxis = w7x.vmec.SurfaceCoefficients.default_axis()
boundary = w7x.vmec.SurfaceCoefficients.default_boundary()

coil_currents_standard = w7x.Defaults.MagneticConfig.standard_rw
coil_currents_low = [0.6, 0.6, 0.6, 0.6, 0.6, -1.0, -1.0, 0.0, 0.0]
coil_currents_high = [1.4, 1.4, 1.4, 1.4, 1.4, 1.0, 1.0, 0.0, 0.0]


class VmecBatchTest(unittest.TestCase):
    def setUp(self):
        self.batch = w7x.batch.Vmec(folder=folder)
        self.batch.size = size

    def tearDown(self):
        folder = os.path.expanduser(self.batch.folder + self.batch.batch_id)
        shutil.rmtree(os.path.expanduser(folder), ignore_errors=True)

    def test_not_null_batch_id(self):
        self.assertTrue(self.batch.batch_id != None)

    def test_batch_default_size(self):
        self.assertEqual(self.batch.size, size)

    def test_gen_batch_folder(self):
        self.batch.gen()
        batch_folder = os.path.expanduser(folder + self.batch.batch_id)
        self.assertTrue(os.path.isdir(batch_folder))

    def test_gen_runs_folder(self):
        self.batch.gen()
        runs_ids = self.batch.runs
        for run_id in runs_ids:
            run_folder = os.path.expanduser(folder + self.batch.batch_id +
                                            "/" + run_id)
            self.assertTrue(os.path.isdir(run_folder))

    def test_default_magnetic_config(self):
        self.assertEqual(self.batch.magnetic_config.coil_currents(),
                         coil_currents_standard)

    def test_sample_and_set_single_magnetic_config(self):
        self.batch.magnetic_config = (w7x.batch.Distribution(
            np.random.uniform, coil_currents_low, coil_currents_high), 'rw')
        self.assertFalse(self.batch.magnetic_config.coil_currents() ==
                         coil_currents_standard)

    def test_default_pressure_profile(self):
        self.assertEqual(self.batch.pressure_profile.coefficients,
                         w7x.vmec.PowerSeries().coefficients)
        self.assertEqual(self.batch.pressure_profile.ProfileType,
                         w7x.vmec.PowerSeries().ProfileType)

    def test_sample_and_set_single_pressure_profile(self):
        self.batch.pressure_profile = (w7x.batch.Distribution(
            np.random.uniform, [0, 0], [1e-6, -1e-6]), 'power_series')
        self.assertFalse((self.batch.pressure_profile.coefficients ==
                          w7x.vmec.PowerSeries().coefficients).any())

    def test_default_phiedge(self):
        self.assertEqual(self.batch.phiedge,
                         w7x.config.Defaults.VMEC.maxToroidalMagneticFlux)

    def test_sample_and_default_phiedge(self):
        samples = [self.batch.phiedge for i in range(10)]
        for s in samples:
            self.assertEqual(s,
                             w7x.config.Defaults.VMEC.maxToroidalMagneticFlux)

    def test_sample_and_set_single_phiedge(self):
        self.batch.phiedge = w7x.batch.Distribution(np.random.uniform, -3.0,
                                                    -1.0)
        self.assertFalse(self.batch.phiedge ==
                         w7x.config.Defaults.VMEC.maxToroidalMagneticFlux)

    def test_sample_and_set_multiple_phiedge(self):
        self.batch.phiedge = w7x.batch.Distribution(np.random.uniform, -3.0,
                                                    -1.0)
        samples = [self.batch.phiedge for i in range(10)]
        check = [w7x.config.Defaults.VMEC.maxToroidalMagneticFlux
                 ] * len(samples)
        self.assertFalse(
            samples == w7x.config.Defaults.VMEC.maxToroidalMagneticFlux)

    def test_sample_and_set_multiple_relative_phiedge(self):
        self.batch.phiedge = w7x.batch.Distribution(np.random.uniform, -3.0,
                                                    -1.0)
        sample1 = self.batch.phiedge
        sample2 = self.batch.phiedge
        self.assertFalse(sample1 == sample2)

    def test_empty_features_list(self):
        self.batch.gen()
        self.assertRaises(ValueError, self.batch.to_dataframe)

    def test_dataframe_columns(self):
        self.batch.gen()
        self.batch.features = vmec_features
        df = self.batch.to_dataframe()
        self.assertEqual(set(df.columns), set(vmec_features))

    def test_dataframe_len(self):
        self.batch.gen()
        self.batch.features = vmec_features
        df = self.batch.to_dataframe()
        self.assertEqual(len(df), self.batch.size)


if __name__ == '__main__':
    unittest.main()
