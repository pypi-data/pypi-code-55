import pytest
import numpy as np
import pandas.testing as pd_testing
from rpy2.robjects import pandas2ri
# sys.path.append("../../Source/ExpressionTools")
from ExpressionTools import EsetPrep
pandas2ri.activate()


@pytest.fixture(scope='module')
def setup_eset_data():
    data = EsetPrep.GeoPrep("GSE71998", "data")
    data.eset = data.load_geo()
    return data


class TestPyEsetAssignments:
    @classmethod
    def get_eset(cls):
        data = setup_eset_data()
        return data.eset

    @classmethod
    def shuffle_df(cls, df, n=1, axis=0):
        new_df = df.copy()
        for _ in range(n):
            new_df.apply(np.random.shuffle, axis=axis)
        return new_df
    @classmethod
    def shuffle_np(cls, array):
        np.random.shuffle(array)
        return array

    def test_assign_exprs(self, setup_eset_data):
        eset = setup_eset_data.eset
        start_data = eset.exprs
        expr_shuffle = self.shuffle_np(eset.exprs)
        eset.exprs = expr_shuffle
        assert not np.array_equal(start_data, eset.exprs)
        assert np.equal(expr_shuffle.all(), eset.exprs.all())

    def test_assign_pheno_data(self, setup_eset_data):
        eset = setup_eset_data.eset
        start_data = eset.pheno_data
        pheno_shuffle = eset.pheno_data.iloc[::-1].copy()
        eset.pheno_data = pheno_shuffle
        assert not start_data.equals(eset.pheno_data)
        pd_testing.assert_frame_equal(pheno_shuffle, eset.pheno_data)

    def test_assign_feature_data(self, setup_eset_data):
        eset = setup_eset_data.eset
        start_data = eset.feature_data
        feat_shuffle = eset.feature_data.iloc[::-1].copy()
        eset.feature_data = feat_shuffle
        assert not start_data.equals(eset.feature_data)
        pd_testing.assert_frame_equal(feat_shuffle, eset.feature_data)
