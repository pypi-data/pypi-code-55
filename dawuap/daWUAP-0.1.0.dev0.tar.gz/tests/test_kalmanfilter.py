import nose
from mock import patch
import econengine as econ
import json
import numpy as np
from utils import utilsAssimilation
from assimilation import kalmanfilter

class TestKalmanFilter(object):

    @classmethod
    def setup_class(self):
        print
        "SETUP!"

        self.ens_size = 500

        with open('test_data/Farms.json') as json_farms:
            farms = json.load(json_farms)
        with open('test_data/observations.json') as json_params:
            self.obs_data = json.load(json_params)
        self.lst_prior_params = utilsAssimilation.read_pandas('test_data/4_parameter_ensemble.csv', results=True)

        self.farm1 = farms['farms'][0]

        self.a = econ.econfuncs.Farm(**self.farm1)

        self.f = kalmanfilter.KalmanFilter(self.a, fn_info_file='test_data/4_kf_info.json')


    @classmethod
    def teardown_class(cls):
        print("TEAR DOWN!")

    def setup_function(self):
        pass
        #print("Creating second Kalman Filter")
        #self.f2 = kalmanfilter.KalmanFilter(self.a, self.ens_size, 'test_data/4_parameter_ensemble.json')

    def teardown_function(self):
        pass
        #print("Destroying second Kalman Filter")
        #self.f2 = None

    def test_initialization_none(self):
        f = kalmanfilter.KalmanFilter(self.a)
        nose.tools.assert_is_not_none(f.posterior_params_k)
        nose.tools.assert_is_instance(f.farm, econ.Farm)

    def test_initialization_readjson(self):
        f = kalmanfilter.KalmanFilter(self.a, fn_info_file='test_data/4_kf_info.json')
        nose.tools.assert_is_not_none(f.posterior_params_k)
        nose.tools.assert_is_instance(f.farm, econ.Farm)

    def test_parse_names(self):
        testnames = ["par1_morestuff", "par2_morestuff"]
        names = ["mean_par1_morestuff", "std_par1_morestuff", "mean_par2_morestuff",
                 "std_par2_morestuff"]
        lst = self.f._parse_obs_params(names)
        nose.tools.assert_list_equal(sorted(list(lst)), sorted(testnames))

    def test_jitter_obs_normal(self):
        np.random.seed(5)
        ens_jitter = self.f._jitter_obs(self.obs_data)
        ens_names = self.f._parse_obs_params(self.obs_data.keys())
        # Find mean and stddev of the ensemble
        for key in ens_names:
            key_arr = np.asarray([ens_jitter[i][key] for i in range(self.ens_size)])
            key_mean = key_arr.mean(axis=0)
            key_std = key_arr.std(axis=0)
            np.testing.assert_array_almost_equal(key_mean, self.obs_data["mean_" + key], 0,
                                                 "Key " + key + " observations failed.")
            np.testing.assert_array_almost_equal(key_std, self.obs_data["std_" + key], 0,
                                                 "Key " + key + " params failed.")

    def test_jitter_obs_normal_hyperparam_const(self):
        np.random.seed(5)
        ens_jitter = self.f._jitter_obs(self.obs_data, hyper_par_var=2)
        ens_names = self.f._parse_obs_params(self.obs_data.keys())
        # Find mean and stddev of the ensemble
        for key in ens_names:
            key_arr = np.asarray([ens_jitter[i][key] for i in range(self.ens_size)])
            key_mean = key_arr.mean(axis=0)
            key_std = key_arr.std(axis=0)
            np.testing.assert_array_almost_equal(key_mean, self.obs_data["mean_" + key], 0,
                                                 "Key " + key + " observations failed.")
            np.testing.assert_array_almost_equal(key_std, np.asarray(self.obs_data["std_" + key])*2, 0,
                                                 "Key " + key + " params failed.")

    @nose.tools.raises(ValueError)
    def test_jitter_obs_valueerror(self):
        nose.tools.assert_raises(ValueError, self.f._jitter_obs({}))

    @nose.tools.raises(ValueError)
    def test_jitter_obs_valueerror2(self):
        nose.tools.assert_raises(ValueError, self.f._jitter_obs({'Hello': 6.}))

    def test_jitter_obs_uniform(self):
        from collections import OrderedDict
        np.random.seed(5)
        obs_params = OrderedDict({'min_par1': -1.0, 'min_par2': 0.0, 'max_par1': 1.0, 'max_par2': 1.0})
        ens_jitter = self.f._jitter_obs(obs_params, param_names=['min', 'max'], dist_func=np.random.uniform)
        ens_names = self.f._parse_obs_params(obs_params.keys())

        # Find mean
        j = iter([0.5, 0.0])
        for key in ens_names:
            key_arr = np.asarray([ens_jitter[i][key] for i in range(self.ens_size)])
            key_mean = key_arr.mean(axis=0)
            np.testing.assert_array_almost_equal(key_mean, j.next(), 1, "Key " + key + " observations failed.")

    def test_update_farm_params(self):
        import copy
        new_params = self.farm1
        for key in self.farm1['parameters']:
            new_params['parameters'][key] = np.zeros_like(new_params['parameters'][key])
        df_newpars = utilsAssimilation.dict2pandas([new_params['parameters']], crop_names=new_params['crop_list'])
        kf2 = copy.copy(self.f)
        kf2._update_farm_params(df_newpars)
        np.testing.assert_array_equal(np.asarray(kf2.farm.deltas), np.zeros_like(kf2.farm.deltas))

    def test_initialize_ensemble(self):
        self.f._initialize_ensemble()

    def test_jitter_farm_params(self):
        test = self.f._generate_prior_params()
        return test

    def test_generate_prior_params(self):
        self.f._generate_prior_params()
        self.f.prior_params_k1

    def test_assimilation(self):
        self.f.assimilate(self.obs_data)
        self.f.posterior_params_k1

    def test_json_to_array(self):
        np.testing.assert_array_equal(self.f.posterior_params_k.shape, (len(self.lst_prior_params),7))

    def test_save_kalman_filter_new(self):
        import os
        try:
            os.remove('test_data/output_data/4_kf_info.json')
        except:
            pass
        try:
            os.remove('test_data/output_data/4_parameter_ensembles.csv')
        except:
            pass
        self.f.assimilate(self.obs_data)
        self.f.save_kalman_filter('test_data/output_data/')
        nose.tools.assert_true(os.path.isfile('test_data/output_data/4_kf_info.json'))
        nose.tools.assert_true(os.path.isfile('test_data/output_data/4_innovation.csv'))
        nose.tools.assert_true(os.path.isfile('test_data/output_data/4_parameter_ensemble.csv'))

    def test_save_kalman_filter_append(self):
        import os
        try:
            os.remove('test_data/output_data/4_kf_info.json')
        except:
            pass
        try:
            os.remove('test_data/output_data/4_parameter_ensemble.csv')
        except:
            pass
        try:
            os.remove('test_data/output_data/4_innovation.csv')
        except:
            pass
        self.f.assimilate(self.obs_data)
        self.f.save_kalman_filter('test_data/output_data/')
        self.f.assimilate(self.obs_data)
        self.f.save_kalman_filter('test_data/output_data/')
        params_results = utilsAssimilation.read_pandas('test_data/output_data/4_parameter_ensemble.csv', results=True)
        nose.tools.assert_equal(params_results.shape, (self.f.ens_size, 14))

    @patch('builtins.input', return_value='N')
    def test_save_kalman_filter_overwrite_no(self, raw_inp):
        import os
        try:
            os.remove('test_data/output_data/4_kf_info.json')
        except:
            pass
        try:
            os.remove('test_data/output_data/4_parameter_ensembles.csv')
        except:
            pass
        self.f.assimilate(self.obs_data)
        self.f.save_kalman_filter('test_data/output_data/')
        f2 = kalmanfilter.KalmanFilter(self.a)
        f2.save_kalman_filter('test_data/output_data/')
        nose.tools.assert_true(os.path.isfile('test_data/output_data/4_kf_info.json'))
        nose.tools.assert_true(os.path.isfile('test_data/output_data/4_innovation.csv'))
        nose.tools.assert_true(os.path.isfile('test_data/output_data/4_parameter_ensemble.csv'))

    @patch('builtins.input', return_value='J')
    def test_save_kalman_filter_overwrite_yes(self, raw_inp):
        import os
        try:
            os.remove('test_data/output_data/4_kf_info.json')
        except:
            pass
        try:
            os.remove('test_data/output_data/4_parameter_ensemble.csv')
        except:
            pass
        try:
            os.remove('test_data/output_data/4_innovation.csv')
        except:
            pass
        self.f.assimilate(self.obs_data)
        self.f.save_kalman_filter('test_data/output_data/')
        f2 = kalmanfilter.KalmanFilter(self.a)
        f2.assimilate(self.obs_data)
        f2.save_kalman_filter('test_data/output_data/')
        nose.tools.assert_true(os.path.isfile('test_data/output_data/4_kf_info.json'))
        nose.tools.assert_true(os.path.isfile('test_data/output_data/4_innovation.csv'))
        nose.tools.assert_true(os.path.isfile('test_data/output_data/4_parameter_ensemble.csv'))

    # # @with_setup(setup_function, teardown_function)
    # def test_assimilate_loop(self):
    #     f2 = kalmanfilter.KalmanFilter(self.a, fn_info_file='test_data')
    #     for i in range(10):
    #         f2.assimilate(self.obs_data)
    #         f2.save_kalman_filter('test_data', timestep_label=str(i))
    #         f2 = kalmanfilter.KalmanFilter(self.a, fn_info_file='test_data')

    def test_assimilate_loop_noParams(self):

        # observs = {
        # "eta": [0.29],
        # "ybar": [2.3697761357788],
        # "obs_land": [5710.08610],
        # "obs_water": [911.39894],
        # "ybar_w": [0.08388704],
        # "prices": [168.7818],
        # "costs": [[392.02, 65.67]]}

        with open('test_data/Farms.json') as json_farms:
            farms = json.load(json_farms)
        with open('test_data/observations.json') as json_params:
            obs_data = json.load(json_params)

        farm1 = farms['farms'][0]

        a = econ.econfuncs.Farm(**farm1)


        observs = {
            "eta": [0.35, 0.29, 0.29, 1.33, 0.38, 0.38, 0.35, 0.35],
            "ybar": [35, 2.2, 5.4, 1.7, 30, 110, 36, 36],
            "obs_land": [0.1220, 0.0250, 0.0078, 0.0328, 0.1636, 0.0051, 0.0189, 0.6247],
            "obs_water": [25.0, 25.0, 52.25, 25.0, 25.0, 45.0, 25.0, 25.0],
            "ybar_w": [0.06, 0.21, 0.21, 0.26, 0.06, 0.06, 0.06, 0.06],
            "prices": [5.82, 125, 125, 111.72, 4.80, 4.80, 6.88, 4.59],
            "costs": [[111.56, 0.0],
                           [193.95, 0.0],
                           [390.02, 65.67],
                           [187.38, 0.0],
                           [120.8, 0.0],
                           [365.33, 48.2],
                           [135.13, 0.0],
                           [135.13, 0.0]],

        }

        res = a.calibrate(**observs)
        print("True values ",  res.x)

        import pandas as pd

        pars = res.x[:-1].reshape(-1, 8).T
        dic_res = {'first_stage_lambda': res.x[-1],
                    'deltas': pars[:, 0],
                    'betas': pars[:, 1:3],
                    'mus': pars[:, 3],
                    'lambdas_land': pars[:, 4:]
                    }

        f2 = kalmanfilter.KalmanFilter(a, self.ens_size, cv=3.0, xi=0.35)

        for i in range(20):
            print("assimilation cycle ", i)
            f2.assimilate(obs_data)
            f2.save_kalman_filter('test_data/output_data/', timestep_label=str(i))
            f2 = kalmanfilter.KalmanFilter(a, fn_info_file='test_data/output_data/4_kf_info.json')

    # def test_montana(self):
    #     import os
    #     ens_size = 500
    #     path_ens = 'test_data'
    #
    #     # Read farm objects
    #     with open('/home/maneta/Documents/sandbox/MT_hydroecon_simulation/EconomicComponentData/Farms_2008.json') as json_farms:
    #     #with open('test_data/Blaine_2008.json') as json_farms:
    #         farms = json.load(json_farms)
    #
    #     # open first year observations
    #     with open('/home/maneta/Documents/sandbox/MT_hydroecon_simulation/EconomicComponentData/observed_user_json/county_information_2008.json') as json_obs2008:
    #     #with open('test_data/observed_Blaine2008.json') as json_obs2008:
    #         obs_data2008 = json.load(json_obs2008)
    #
    #     for farm in farms['farms']:
    #         print("Processing farm ", farm['name'])
    #         farm['irrigation_mask'] = [int(m) for m in farm['irrigation_mask']]
    #
    #         # load the farm object
    #         f = econ.econfuncs.Farm (**farm)
    #
    #         # load observations for farm
    #         obs = [ob for ob in obs_data2008 if ob['id'] == farm['id']]
    #
    #         # res = f.calibrate(**obs[0])
    #         # print(res.x)
    #
    #         # initialize kalman filter with random parameters values using a cv=3 (sd 3 time the param mean)
    #         kf = kalmanfilter.KalmanFilter(f, ens_size=ens_size, cv=3.1, xi=0.5)
    #
    #         # spin up the calibration for 20 years using first year observations
    #         for i in range(20):
    #             print("Spin up assimilation cycle ", i)
    #             kf.assimilate(obs[0], obs_var_scale_factor=0.2)
    #             print("assimilation done")
    #             kf.save_kalman_filter(path_ens, timestep_label=str(i))
    #             kf = kalmanfilter.KalmanFilter(f, fn_info_file=os.path.join(path_ens, str(farm['id']) + '_kf_info.json'))

    def test_simulate(self):

        with open('test_data/Farms.json') as json_farms:
            farms = json.load(json_farms)

        with open('test_data/Scenario.json') as json_scenario:
            scenario = json.load(json_scenario)

        farm1 = farms['farms'][0]

        f = econ.econfuncs.Farm(**farm1)

        kf = kalmanfilter.KalmanFilter(f, fn_info_file='test_data/4_kf_info.json')

        import time
        start = time.time()
        kf.simulate(scenario[0], fn_write_ensemble_states='test_data/4_simul_ensemble.h5')
        end = time.time()
        print("--- %s seconds ---" % (end - start))
