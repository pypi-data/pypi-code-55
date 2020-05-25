import plotting
import nose


class TestEnsembleResults(object):
    @classmethod
    def setup_class(cls):
        print("setting up class " + cls.__name__)
        info_fn = r'../tests/test_data/4_kf_info.json'
        #info_fn = r'test_data/30005_kf_info.json'
        #info_fn = r'/home/maneta/workspace/dawuaphydroengine/tests/test_data/4_kf_info.json'
        cls.ens_info = plotting.EnsembleResults(info_fn)

    @classmethod
    def teardown_class(cls):
        print("tearing down class " + cls.__name__)

    def setup(self):
        pass

    def teardown(self):
        pass

    def test_load_ensemble(self):

        df_ens = self.ens_info.load_ensemble()
        nose.tools.assert_tuple_equal((500, 610), df_ens.shape)

    def test_plot_parameter_ensemble(self):
        self.ens_info.plot_parameter_ensemble(innovation=False, param_lst=None, crop_lst=None)

    def test_plot_parameter_innovation(self):
        self.ens_info.plot_parameter_ensemble(innovation=True, param_lst=None, crop_lst=None)

    def test_plot_simulation_ensemble(self):
        self.ens_info.plot_simulation_ensemble('test_data/4_simul_ensemble.h5', state_list=['used_land'])


