import unittest
from ddt import ddt, file_data
from unittest.mock import Mock, patch

import numpy as np
from scipy import sparse

from azureml.automl.core.shared.exceptions import AutoMLException, MemorylimitException, TransformException
from azureml.automl.runtime.featurization._featurized_data_combiners import FeaturizedDataCombiners


@ddt
class TestFeaturizedDataCombiner(unittest.TestCase):
    @file_data("test_featurized_data_combiner.json")
    def test_get(self, is_sparse, is_inference_time, is_low_memory, expected):
        combiner = FeaturizedDataCombiners.get(is_sparse, is_inference_time, is_low_memory)
        assert combiner is not None, "Combiner should not be None"
        actual = combiner.__name__
        msg = "Sparse: {}, Inference: {}, LowMemory: {}, Expected: {}, Actual: {}"
        assert combiner.__name__ == expected, msg.format(is_sparse, is_inference_time, is_low_memory, expected, actual)

    @patch('azureml.automl.runtime.featurization._featurized_data_combiners.np.zeros')
    def test_disk_based_sparse_combiner_exceptions(self, mock_np_zeros):
        array = np.repeat([1, 2, 3, 4, 5], 1000)
        sparse_matrix = sparse.csr_matrix(array)

        mock_np_zeros.side_effect = Exception("Something went wrong")
        with self.assertRaisesRegex(TransformException, "Exception while trying to combine transformed data"):
            FeaturizedDataCombiners.disk_based_sparse_combiner([sparse_matrix, sparse_matrix])

        mock_np_zeros.side_effect = MemoryError("Something went wrong")
        with self.assertRaisesRegex(
                MemorylimitException,
                "MemoryError caused by insufficient memory while trying to combine transformed data."):
            FeaturizedDataCombiners.disk_based_sparse_combiner([sparse_matrix, sparse_matrix])

        mock_np_zeros.side_effect = AutoMLException("Something went wrong")
        with self.assertRaisesRegex(AutoMLException, "Something went wrong"):
            FeaturizedDataCombiners.disk_based_sparse_combiner([sparse_matrix, sparse_matrix])

    @patch('azureml.automl.runtime.featurization._featurized_data_combiners.DefaultPickler.dump')
    def test_disk_based_sparse_combiner_exceptions_pickler(self, mock_pickler_dump):
        array = np.repeat([1, 2, 3, 4, 5], 1000)
        sparse_matrix = sparse.csr_matrix(array)

        mock_pickler_dump.side_effect = MemorylimitException("Exception while trying to combine transformed data")
        with self.assertRaisesRegex(MemorylimitException, "Exception while trying to combine transformed data"):
            FeaturizedDataCombiners.disk_based_sparse_combiner([sparse_matrix, sparse_matrix])


if __name__ == '__main__':
    unittest.main()
