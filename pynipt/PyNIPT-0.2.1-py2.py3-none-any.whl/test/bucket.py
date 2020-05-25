import os
import unittest
from ..lib.bucket import Bucket


def clean_up(path):
    import shutil
    try:
        for p in os.listdir(path):
            if p in ['Processing', 'Results', 'Mask', 'Temp']:
                shutil.rmtree(os.path.join(path, p))
    except PermissionError:
        return 1
    return 0


class TestBucket(unittest.TestCase):

    def setUp(self) -> None:
        """set path"""
        sample_bids = os.path.abspath(os.path.dirname(__file__)).split(os.sep)[:-2]
        sample_bids.extend(['examples'])
        self.path = os.sep.join(sample_bids)

    def tearDown(self):
        """clean all derived folder"""
        clean_up(self.path)      # remove all other dataclass

    def test_01_CheckPathExists(self):
        self.assertTrue(os.path.exists(self.path))  # check if path exists

    def test_02_CheckNumData(self):
        with Bucket(self.path) as dset:
            self.assertEqual(len(dset(0)), 32)     # check if number of data is 32 in dataset_path
            self.assertFalse(dset(0).is_multi_session())
            self.assertFalse(len(dset(1)))         # check if working_path is empty
            self.assertFalse(len(dset(2)))         # check if results_path is empty
            self.assertFalse(len(dset(3)))         # check if mask_path is empty

    def test_03_FileNameFilter(self):
        with Bucket(self.path) as dset:
            self.assertIn('contain', dset._fname_keys)
            self.assertEqual(len(dset(0, contain='sub-01')), 8)
            self.assertEqual(len(dset(0, contain='fieldmap')), 4)

            self.assertIn('ignore', dset._fname_keys)
            self.assertEqual(len(dset(0, ignore='sub-02')), 24)

            self.assertIn('ext', dset._fname_keys)
            self.assertEqual(len(dset(0, ext='nii.gz')), 32)
            self.assertEqual(len(dset(0, ext='nii')), 0)
            self.assertEqual(len(dset(0, ext=['nii.gz', '1D'])), 32)

            self.assertIn('regex', dset._fname_keys)
            self.assertEqual(len(dset(0, regex=r'sub-\d{2}_task-rs.*')), 24)
            self.assertEqual(len(dset(0, regex=r'sub-\d{2}_T2w')), 4)

    def test_04_(self):
        with Bucket(self.path) as dset:
            self.assertIn('subjects', dset.param_keys[0])
            self.assertEqual(len(dset(0, subjects='sub-01', contain='T2w')), 1)
            self.assertIn('datatypes', dset.param_keys[0])
            self.assertEqual(len(dset(0, datatypes='anat', contain='T2w')), 4)


if __name__ == '__main__':
    unittest.main()
