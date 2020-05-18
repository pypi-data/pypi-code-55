import unittest
import w7x
import os
import shutil

folder = '~/tmp/VMEC/test/'

magnetic_config = w7x.flt.MagneticConfig.default()
pressure_profile = w7x.vmec.PowerSeries()
current_profile = w7x.vmec.PowerSeries()
magneticAxis = w7x.vmec.SurfaceCoefficients.default_axis()
boundary = w7x.vmec.SurfaceCoefficients.default_boundary()
coil_currents = [w7x.config.Defaults.MagneticConfig.high_iota_b_rw]

# TODO(@amerlo): can not find Peaking class
# class VmecPeakingProfileTest(unittest.TestCase):
#     def setUp(self):
#         self.peaking = w7x.vmec.Peaking()
#
#     def test_default(self):
#         self.assertEqual(self.peaking.ProfileType, 'cubic_spline')
#         self.assertEqual(self.peaking.coefficients, [1e-6, 2])
#
#     #  TODO(@amerlo): This will have to be solved in a more elegant way
#     def test_create(self):
#         peaking = w7x.vmec.create_profile(ProfileType='peaking',
#                                           coefficients=[1.0, 2])
#         self.assertEqual(peaking.ProfileType, 'cubic_spline')
#         self.assertEqual(len(peaking.coefficients), 128)
#
#     def test_peaking(self):
#         values = self.peaking([0.0, 0.5, 1.0])
#         self.assertEqual(values[0], 1e-6)
#         self.assertEqual(values[1], 0.75e-6)
#         self.assertTrue(values[2] < 1e-20)
#
#     def test_set_norm(self):
#         self.peaking.norm = 10
#         self.assertEqual(self.peaking.coefficients, [10, 2])


class VmecPowerSeriesProfileTest(unittest.TestCase):
    def setUp(self):
        self.power_series = w7x.vmec.PowerSeries()

    def test_default(self):
        self.assertEqual(self.power_series.ProfileType, 'power_series')
        self.assertEqual(self.power_series.coefficients, [1e-6, -1e-6])

    def test_create(self):
        power_series = w7x.vmec.create_profile(ProfileType='power_series',
                                               coefficients=[5e-7, -5e-7])
        self.assertEqual(power_series.ProfileType, 'power_series')
        self.assertEqual(power_series.coefficients, [5e-7, -5e-7])

    def test_set_value(self):
        self.power_series.set_value(1.0, 5e-7)
        self.assertEqual(self.power_series(0.0), 1e-6)
        self.assertEqual(self.power_series(1.0), 5e-7)


class VmecRunTest(unittest.TestCase):
    def setUp(self):
        self.run = w7x.vmec.Run(magnetic_config=magnetic_config,
                                pressure_profile=pressure_profile,
                                current_profile=current_profile,
                                folder=folder,
                                backend='hpc')
        self.run.magneticAxis = magneticAxis
        self.run.boundary = boundary

    def tearDown(self):
        folder = os.path.expanduser(self.run._folder + self.run.vmec_id)
        shutil.rmtree(os.path.expanduser(folder), ignore_errors=True)

    def test_not_null_vmec_id(self):
        self.assertTrue(self.run.vmec_id != None)

    def test_not_implemented_backend(self):
        run = w7x.vmec.Run(magnetic_config=magnetic_config,
                           pressure_profile=pressure_profile,
                           current_profile=current_profile,
                           folder=folder,
                           backend='abc')
        self.assertRaises(ValueError, run.gen)

    def test_gen_hpc_folder(self):
        self.run.gen()
        folder = os.path.expanduser(self.run._folder + self.run.vmec_id)
        self.assertTrue(os.path.isdir(folder))

    def test_input_file(self):
        self.run.gen()
        path = os.path.expanduser(self.run._folder + self.run.vmec_id +
                                  "/input." + self.run.vmec_id)
        self.assertTrue(os.path.isfile(path))

    def test_slurm_file(self):
        self.run.gen()
        path = os.path.expanduser(self.run._folder + self.run.vmec_id +
                                  "/slurm_vmec")
        self.assertTrue(os.path.isfile(path))


#  TODO(@dboe): Check the validity of this test. It is here only for reference.
@unittest.skip("Test has to be checked")
class TestBeta(unittest.TestCase):
    def test_adjust_beta(self):

        i_tors = []
        runs = []

        for currents_rw in coil_currents:
            magnetic_config = w7x.flt.MagneticConfig.from_currents(
                *currents_rw, unit='rw')
            initial_run = w7x.vmec.Run(
                'w7x_v_0.1.0.dev8_id_1000_1000_1000_1000_+0000_-0250_pres_00_it_7'
            )
            initial_run = initial_run.converge()

            for i_tor in [
                    0. + i * 5000 for i in range(10, 100) if i * 5000 < 51000
            ]:
                run = w7x.vmec.adjust_beta(
                    magnetic_config.coil_currents(unit='rw'),
                    0.0,
                    b_axis=2.5,
                    rel_pressure_profile=[1, -1],
                    rel_current_profile=[0, 1, -1],
                    totalToroidalCurrent=float(i_tor),
                    beta_precision=0.001,
                    beta_scan_runs=[initial_run])
            runs.append(run)
            i_tors.append(i_tor)

        for run, i_tor in zip(runs, i_tors):
            self.assertEqual(i_tor, 5000)


if __name__ == '__main__':
    unittest.main()
