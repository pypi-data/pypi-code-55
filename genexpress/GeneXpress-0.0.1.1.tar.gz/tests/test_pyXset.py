import pytest
import pandas.testing as pd_testing
from ExpressionTools import pyXset, pyEset, EsetPrep


class TestXset:
    @pytest.fixture(scope='class')
    def create_xset(self):
        data = pyXset.Xset()
        data.load_exprs_file("data/GSE71998_inverse_log2_reads.csv")
        return data

    def test_update_gdata(self, create_xset):
        # searching for 16 and 30 here did not work correctly
        group = create_xset.search_numbers("516", "530", create_xset.exprs.columns, ['test'])
        create_xset.update_groups(group)
        pd_testing.assert_frame_equal(create_xset.get_groups(['test']).astype(bool), group.astype(bool))

    def test_subset_xset(self, create_xset):
        """
        edge cases:
        groups = []
        groups = list of 1 item
        groups = list of many items
        """
        group = create_xset.search_numbers("516", "530", create_xset.exprs.columns, ['test'])
        create_xset.update_groups(group)
        subbed = create_xset.subset(['test'])
        expected = pyXset.Xset(create_xset.exprs.loc[:, create_xset.get_groups(['test']).to_numpy()[0]],
                               create_xset.groups.loc[:, create_xset.get_groups(['test']).to_numpy()[0]])
        assert subbed == expected


class TestPyXset:

    @pytest.fixture(scope='class')
    def create_pyxset(self):
        data = EsetPrep.GeoPrep("GSE71998", "data")
        data.eset = data.load_geo()
        return data.eset

    def test_to_eset_to_xset(self, create_pyxset):
        xset = pyXset.PyXset(create_pyxset)
        eset = pyEset.PyEset(xset)
        assert eset == create_pyxset

    def test_update_gdata(self, create_pyxset):
        # searching for 16 and 30 here did not work correctly
        group = create_pyxset.search_numbers("516", "530", create_pyxset.exprs.columns, ['test'])
        create_pyxset.update_groups(group)
        pd_testing.assert_frame_equal(create_pyxset.get_groups(['test']).astype(bool), group.astype(bool))

    def test_subset_xset(self, create_pyxset):
        """
        edge cases:
        groups = []
        groups = list of 1 item
        groups = list of many items
        """
        group = create_pyxset.search_numbers("516", "530", create_pyxset.exprs.columns, ['test'])
        create_pyxset.update_groups(group)
        subbed = create_pyxset.subset(['test'])
        expected = pyXset.PyXset()
        assert subbed == expected



class TestPyXsetSubset:
    pass


class TestPyXsetFdata:
    pass


class TestEsetFromXset:
    pass
