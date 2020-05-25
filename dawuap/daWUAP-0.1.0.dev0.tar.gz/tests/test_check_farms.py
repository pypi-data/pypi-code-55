import nose
import json
from utils import check_farms as cf
from nose.tools import raises


class TestCheckJson(object):

    @classmethod
    def setup_class(self):
        print("SETUP!")

        with open('test_data/Farms_test.json') as json_farms:
            self.farms = json.load(json_farms)['farms']

    @classmethod
    def teardown_class(self):
        print("TEAR DOWN!")

    def setup(self):
        self.farms2 = self.farms

    def teardown(self):
        self.farms2 = None

    @raises(Exception)
    def test_key_names(self):
        """Check key names are correct"""
        new_farm = self.farms2[3]
        new_farm['constraint'] = new_farm.pop('constraints')
        self.farms2[3] = new_farm
        cf.check_farms(self.farms2)

    @raises(Exception)
    def test_number_of_keys(self):
        """Check the total number of keys"""
        self.farms2[2].pop('constraints')
        cf.check_farms(self.farms2)

    @raises(Exception)
    def test_crop_list_n(self):
        """Check number of crops"""
        self.farms2[1]['crop_list'].remove("Maize")
        cf.check_farms(self.farms2)

    @raises(Exception)
    def test_crop_list_instance(self):
        """Check crop_list is list of strings"""
        self.farms2[1]['crop_list'][0] = 8
        cf.check_farms(self.farms2)

    @raises(Exception)
    def test_input_list_n(self):
        """Check number of inputs"""
        self.farms2[8]['input_list'].remove("water")
        cf.check_farms(self.farms2)

    @raises(Exception)
    def test_input_list_instance(self):
        """Check input_list is list of strings"""
        self.farms2[8]['input_list'][0] = 8
        cf.check_farms(self.farms2)

    @raises(Exception)
    def test_irrigation_eff_n(self):
        """Check number of irrigation_eff inputs"""
        self.farms2[10]['irrigation_eff'].remove(0)
        cf.check_farms(self.farms2)

    @raises(Exception)
    def test_irrigation_eff_instance(self):
        """Check irrigation_eff is list of floats"""
        self.farms2[10]['irrigation_eff'][0] = "notafloat"
        cf.check_farms(self.farms2)

    @raises(Exception)
    def test_irrigation_mask_n(self):
        """Check number of irrigation_mask inputs"""
        self.farms2[0]['irrigation_mask'].remove(0)
        cf.check_farms(self.farms2)

    @raises(Exception)
    def test_irrigation_mask_instance(self):
        """Check irrigation_mask is list of ints"""
        self.farms2[0]['irrigation_mask'][0] = "notaint"
        cf.check_farms(self.farms2)

    @raises(Exception)
    def test_crop_id_n(self):
        """Check number of crop_id inputs"""
        self.farms2[0]['crop_id'].remove(63)
        cf.check_farms(self.farms2)

    @raises(Exception)
    def test_crop_id_instance(self):
        """Check crop_id is list of booleans"""
        self.farms2[0]['crop_id'][0] = "notaint"
        cf.check_farms(self.farms2)

    @raises(Exception)
    def test_simulated_states_instance(self):
        """Check simulated_states is a dictionary"""
        self.farms2[0]['simulated_states'] = ["this", "is", "not", "a", "dictionary"]
        cf.check_farms(self.farms2)

    @raises(Exception)
    def test_name_instance(self):
        """Check name is a string"""
        self.farms2[0]['name'] = []
        cf.check_farms(self.farms2)

    @raises(Exception)
    def test_parameters_instance(self):
        """Check parameters is a dictionary"""
        self.farms2[0]['parameters'] = ["this", "is", "not", "a", "dictionary"]
        cf.check_farms(self.farms2)

    @raises(Exception)
    def test_parameter_names(self):
        """Check parameter names are correct"""
        new_farm = self.farms2[3]['parameters']
        new_farm['delas'] = new_farm.pop('deltas')
        self.farms2[3]['parameters'] = new_farm
        cf.check_farms(self.farms2)

    @raises(Exception)
    def test_number_of_parameters(self):
        """Check the total number of parameters"""
        self.farms2[2]['parameters'].pop('deltas')
        cf.check_farms(self.farms2)

    @raises(Exception)
    def test_deltas_n(self):
        """Check number of deltas inputs"""
        self.farms2[0]['parameters']['deltas'].pop(0)
        cf.check_farms(self.farms2)

    @raises(Exception)
    def test_deltas_instance(self):
        """Check deltas is list of floats"""
        self.farms2[0]['parameters']['deltas'][0] = "notafloat"
        cf.check_farms(self.farms2)

    @raises(Exception)
    def test_mus_n(self):
        """Check number of mus inputs"""
        self.farms2[0]['parameters']['mus'].pop(0)
        cf.check_farms(self.farms2)

    @raises(Exception)
    def test_mus_instance(self):
        """Check mus is list of floats"""
        self.farms2[0]['parameters']['mus'][0] = "notafloat"
        cf.check_farms(self.farms2)

    @raises(Exception)
    def test_lambdas_land_n(self):
        """Check number of flattened lambdas_land inputs"""
        self.farms2[1]['parameters']['lambdas_land'][0].pop(0)
        cf.check_farms(self.farms2)

    @raises(Exception)
    def test_lambdas_land_instance(self):
        """Check flattened lambdas_land is list of floats or ints"""
        self.farms2[1]['parameters']['lambdas_land'][0][0] = "notafloat"
        cf.check_farms(self.farms2)

    @raises(Exception)
    def test_first_stage_lambda_n(self):
        """Check number of first_stage_lambda inputs"""
        self.farms2[1]['parameters']['first_stage_lambda'].append(0.123)
        cf.check_farms(self.farms2)

    @raises(Exception)
    def test_first_stage_lambda_instance(self):
        """Check first_stage_lambda is list of a float"""
        self.farms2[1]['parameters']['first_stage_lambda'][0] = "notafloat"
        cf.check_farms(self.farms2)

    @raises(Exception)
    def test_betas_n(self):
        """Check number of flattened betas inputs"""
        self.farms2[1]['parameters']['betas'][0].pop(0)
        cf.check_farms(self.farms2)

    @raises(Exception)
    def test_betas_instance(self):
        """Check flattened betas is list of floats or ints"""
        self.farms2[1]['parameters']['betas'][0][0] = "notafloat"
        cf.check_farms(self.farms2)

    @raises(Exception)
    def test_sigmas_n(self):
        """Check number of sigmas inputs"""
        self.farms2[1]['parameters']['sigmas'].append(0.123)
        cf.check_farms(self.farms2)

    @raises(Exception)
    def test_sigmas_instance(self):
        """Check sigmas is list of a float"""
        self.farms2[1]['parameters']['sigmas'][0] = "notafloat"
        cf.check_farms(self.farms2)

    @raises(Exception)
    def test_id_instance(self):
        """Check id is a string"""
        self.farms2[0]['id'] = []
        cf.check_farms(self.farms2)

    @raises(Exception)
    def test_source_id_instance(self):
        """Check source_id is a string"""
        self.farms2[0]['source_id'] = []
        cf.check_farms(self.farms2)

    @raises(Exception)
    def test_normalization_refs_instance(self):
        """Check parameters is a dictionary"""
        self.farms2[0]['normalization_refs'] = ["this", "is", "not", "a", "dictionary"]
        cf.check_farms(self.farms2)

    @raises(Exception)
    def test_normalization_refs_names(self):
        """Check normalization_refs names are correct"""
        new_farm = self.farms2[3]['normalization_refs']
        new_farm['ref_et'] = new_farm.pop('reference_et')
        self.farms2[3]['normalization_refs'] = new_farm
        cf.check_farms(self.farms2)

    @raises(Exception)
    def test_number_of_normalization_refs(self):
        """Check the total number of normalization_refs"""
        self.farms2[2]['normalization_refs'].pop('reference_et')
        cf.check_farms(self.farms2)

    @raises(Exception)
    def test_reference_yields_n(self):
        """Check number of reference_yields inputs"""
        self.farms2[0]['normalization_refs']['reference_yields'].pop(0)
        cf.check_farms(self.farms2)

    @raises(Exception)
    def test_reference_yields_instance(self):
        """Check reference_yields is list of floats"""
        self.farms2[0]['normalization_refs']['reference_yields'][0] = "notafloat"
        cf.check_farms(self.farms2)

    @raises(Exception)
    def test_reference_et_n(self):
        """Check number of reference_et inputs"""
        self.farms2[0]['normalization_refs']['reference_et'].pop(0)
        cf.check_farms(self.farms2)

    @raises(Exception)
    def test_reference_et_instance(self):
        """Check reference_et is list of floats"""
        self.farms2[0]['normalization_refs']['reference_et'][0] = "notafloat"
        cf.check_farms(self.farms2)

    @raises(Exception)
    def test_reference_land_n(self):
        """Check number of reference_land inputs"""
        self.farms2[0]['normalization_refs']['reference_land'].pop(0)
        cf.check_farms(self.farms2)

    @raises(Exception)
    def test_reference_land_instance(self):
        """Check reference_land is list of floats"""
        self.farms2[0]['normalization_refs']['reference_land'][0] = "notafloat"
        cf.check_farms(self.farms2)

    @raises(Exception)
    def test_reference_prices_n(self):
        """Check number of reference_prices inputs"""
        self.farms2[0]['normalization_refs']['reference_prices'].pop(0)
        cf.check_farms(self.farms2)

    @raises(Exception)
    def test_reference_prices_instance(self):
        """Check reference_prices is list of floats"""
        self.farms2[0]['normalization_refs']['reference_prices'][0] = "notafloat"
        cf.check_farms(self.farms2)

    @raises(Exception)
    def test_constraints_instance(self):
        """Check constraints is a dictionary"""
        self.farms2[0]['constraints'] = ["this", "is", "not", "a", "dictionary"]
        cf.check_farms(self.farms2)

    @raises(Exception)
    def test_constraints_names(self):
        """Check constraints names are correct"""
        new_farm = self.farms2[3]['constraints']
        new_farm['watr'] = new_farm.pop('water')
        self.farms2[3]['constraints'] = new_farm
        cf.check_farms(self.farms2)

    @raises(Exception)
    def test_number_of_constraints(self):
        """Check the total number of constraints"""
        self.farms2[2]['constraints'].pop('water')
        cf.check_farms(self.farms2)

    @raises(Exception)
    def test_water_instance(self):
        """Check water is list of floats or ints"""
        self.farms2[0]['constraints']['water'][0] = "notafloat"
        cf.check_farms(self.farms2)

    @raises(Exception)
    def test_water_n(self):
        """Check number of water inputs"""
        self.farms2[0]['constraints']['water'].append(0.123)
        cf.check_farms(self.farms2)

    @raises(Exception)
    def test_land_instance(self):
        """Check land is list of floats or ints"""
        self.farms2[0]['constraints']['land'][0] = "notafloat"
        cf.check_farms(self.farms2)

    @raises(Exception)
    def test_land_n(self):
        """Check number of land inputs"""
        self.farms2[0]['constraints']['land'].append(0.123)
        cf.check_farms(self.farms2)
