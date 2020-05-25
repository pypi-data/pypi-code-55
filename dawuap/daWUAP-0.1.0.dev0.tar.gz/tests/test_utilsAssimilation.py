from utils import utilsAssimilation
import json
import nose

class TestKalmanFilterUtils(object):

    @classmethod
    def setup_class(self):
        print
        "SETUP!"

        with open('test_data/4_parameter_ensemble.json') as json_pparams:
            self.dict = json.load(json_pparams)

        self.crop_size = len(self.dict[0]['deltas'])

    @classmethod
    def teardown_class(cls):
        print
        "TEAR DOWN!"

    def test_dict2pandas(self):
        df = utilsAssimilation.dict2pandas(self.dict)

    def test_dict2pandas_crop_list(self):
        crop_names = ["dryland barley", "dryland alfalfa", "irrigated alfalfa", "dryland peas",
                      "dryland spring wheat", "irrigated spring wheat", "dryland durum wheat", "dryland winter wheat"]
        df = utilsAssimilation.dict2pandas(self.dict, crop_names=crop_names)
        df['betas']['dryland peas_1']


