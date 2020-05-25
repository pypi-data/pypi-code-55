from utils import exim_funcs
import nose
from nose.tools import raises


class TestEximFuncs(object):

    @classmethod
    def setup_class(self):
        print("SETUP!")

        self.fn_csv_obs_file = "test_data/county_information.csv"

    @classmethod
    def teardown_class(self):
        print("TEAR DOWN!")

    def setup(self):
        pass

    def teardown(self):
        pass

    def test_import_obs_from_csv(self):
        """Check import observations from csv"""
        temp =exim_funcs.import_obs_from_csv(self.fn_csv_obs_file, 'test_data/county_information.json')
        nose.tools.assert_is_instance(temp,
            list)
        nose.tools.assert_greater(len(temp), 0)

    def test_import_obs_from_csv_year(self):
        """Check import observations from csv"""
        nose.tools.assert_true(all(x['year'] == 2008 for x in
                                   exim_funcs.import_obs_from_csv(self.fn_csv_obs_file,
                                                                  fn_out_json='test_data/county_information_2008.json',
                                                                  year=2008))
                               )
    def test_import_obs_from_csv_year_specific_crop(self):
        """Check import observations from csv"""
        nose.tools.assert_true(x['crop_list'] == ['Durum Wheat', 'Peas'] for x in
                                   exim_funcs.import_obs_from_csv(self.fn_csv_obs_file,
                                                                  fn_out_json='test_data/county_information_2008.json',
                                                                  year=2008, crops=['Peas', 'Durum Wheat'])
                               )
