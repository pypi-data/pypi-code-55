# (c) 2012-2018 The company fomerly known as Dativa, all rights reserved
# -----------------------------------------
#  This code is licensed under MIT license (see license.txt for details)

import unittest
import os
import pyarrow as pa

import pandas as pd
import numpy as np
import boto3
from pandas.testing import assert_frame_equal

from newtools import PandasDoggo, FileDoggo, S3Location


class TestDoggos(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_data', 'pandas_doggo_tests')

    def test_read_csv_local(self):
        """read a local csv"""

        expected_df = pd.DataFrame({'e-mail': {0: 'n@gmail.com', 1: 'p@gmail.com', 2: 'h@gmail.com', 3: 's@gmail.com',
                                               4: 'l@gmail.com', 5: 'v@gmail.com', 6: None},
                                    'number': {0: 0, 1: 1, 2: 0, 3: 0, 4: 1, 5: 0, 6: 0}})
        pth = os.path.join(self.base_path, 'csv', 'generic', 'email_test.csv')
        session = boto3.Session()
        fh = PandasDoggo(boto_session=session)
        df = fh.load(pth)
        assert_frame_equal(df, expected_df)

    def test_read_csv_local_gzip(self):
        pth = os.path.join(self.base_path, 'csv', 'gzip', 'test.csv.gz')

        fh = PandasDoggo()
        df = fh.load_csv(pth, compression='gzip')

    def test_read_csv_local_gzip_infer(self):
        pth = os.path.join(self.base_path, 'csv', 'gzip', 'test.csv.gz')

        fh = PandasDoggo()
        df = fh.load(pth)

    def test_write_csv_local(self):
        df = pd.DataFrame({'e-mail': {0: 'n@gmail.com', 1: 'p@gmail.com', 2: 'h@gmail.com', 3: 's@gmail.com',
                                      4: 'l@gmail.com', 5: 'v@gmail.com', 6: None},
                           'number': {0: 0, 1: 1, 2: 0, 3: 0, 4: 1, 5: 0, 6: 0}})
        pth = os.path.join(self.base_path, 'csv', 'generic', 'email_test_copy.csv')
        expected_pth = os.path.join(self.base_path, 'csv', 'generic', 'email_test.csv')
        fh = PandasDoggo()
        fh.save(df, pth, index=None)
        with open(pth) as p, open(expected_pth) as p2:
            self.assertEqual(p.read().strip(), p2.read().strip())

        os.remove(pth)

    def test_read_pq_local(self):
        fh = PandasDoggo()
        pth = os.path.join(self.base_path, 'parquet', 'data.parquet')
        df = fh.load(pth)

    def test_write_pq_local(self):
        fh = PandasDoggo()
        df = pd.read_csv(os.path.join(self.base_path, 'parquet', 'emails.csv'))
        fh.save_parquet(df, os.path.join(self.base_path, 'parquet', 'emails.parquet'))
        os.remove(os.path.join(self.base_path, 'parquet', 'emails.parquet'))

    def test_read_pq_local_with_args(self):
        fh = PandasDoggo()
        pth = os.path.join(self.base_path, 'parquet', 'data.parquet')
        df = fh.load_parquet(pth, columns=['country', 'birthdate', 'salary', 'title'])
        self.assertEqual(sorted(list(df.columns)), sorted(['country', 'birthdate', 'salary', 'title']))

    def test_pq_schema_int64(self):
        new_file_path = os.path.join(self.base_path,
                                     'parquet',
                                     'new_data.parquet')
        test_df = pd.DataFrame(
            {"col1": [1, 2, 3, 4, 5], "col2": ["a", "s", "6", "7", "t"]})
        fields = [
            pa.field("col1", pa.int64()),
            pa.field("col2", pa.string())
        ]
        my_schema = pa.schema(fields)
        fh = PandasDoggo()

        fh.save_parquet(test_df, new_file_path, schema=my_schema)

        assert_frame_equal(test_df, fh.load_parquet(new_file_path))
        os.remove(new_file_path)

    def test_pq_schema_int32(self):
        # Tests the down casting of int64 to int32 without explicit conversion
        new_file_path = os.path.join(self.base_path,
                                     'parquet',
                                     'new_data.parquet')
        test_df = pd.DataFrame(
            {"col1": [1, 2, 3, 4, 128], "col2": ["a", "s", "6", "7", "t"]})
        fields = [
            pa.field("col1", pa.int32()),
            pa.field("col2", pa.string())
        ]
        test_df = test_df.astype({"col1": 'Int32'})
        my_schema = pa.schema(fields)
        fh = PandasDoggo()

        fh.save_parquet(test_df, new_file_path, schema=my_schema)

        assert_frame_equal(test_df, fh.load_parquet(new_file_path))
        os.remove(new_file_path)

    def test_pq_schema_int32_nulls(self):

        new_file_path = os.path.join(self.base_path,
                                     'parquet',
                                     'new_data_nulls.parquet')
        test_df = pd.DataFrame(
            {"col1": pd.Series([1, 2, 3, 4, 128, pd.NA, None], dtype='Int32'), "col2": ["a", "s", "6", "7", "t", 'pd.NA', 'None']})
        fields = [
            pa.field("col1", pa.int32()),
            pa.field("col2", pa.string())
        ]

        my_schema = pa.schema(fields)
        fh = PandasDoggo()

        fh.save_parquet(test_df, new_file_path, schema=my_schema)

        assert_frame_equal(test_df, fh.load_parquet(new_file_path))
        os.remove(new_file_path)

    def test_pq_schema_int64_nulls(self):
        new_file_path = os.path.join(self.base_path,
                                     'parquet',
                                     'new_data_nulls.parquet')
        test_df = pd.DataFrame(
            {"col1": pd.Series([1, 2, 3, 4, 128, pd.NA, None], dtype='Int64'),
             "col2": ["a", "s", "6", "7", "t", 'pd.NA', 'None']})
        fields = [
            pa.field("col1", pa.int64()),
            pa.field("col2", pa.string())
        ]

        my_schema = pa.schema(fields)
        fh = PandasDoggo()

        fh.save_parquet(test_df, new_file_path, schema=my_schema)

        assert_frame_equal(test_df, fh.load_parquet(new_file_path))
        os.remove(new_file_path)

    def test_pq_schema_datetime(self):
        new_file_path = os.path.join(self.base_path,
                                     'parquet',
                                     'new_data.parquet')
        rng = pd.date_range('2015-02-24', periods=5, freq='23H')
        test_df = pd.DataFrame({'Date': rng, 'Val': np.random.randn(len(rng))})

        test_df['Date'] = pd.to_datetime(test_df['Date'], unit='D')
        fields = [
            pa.field("Date", pa.timestamp('ms')),
            pa.field("Val", pa.float64())
        ]
        my_schema = pa.schema(fields)
        fh = PandasDoggo()

        fh.save_parquet(test_df, new_file_path, schema=my_schema)

        assert_frame_equal(test_df, fh.load_parquet(new_file_path))
        os.remove(new_file_path)

    def test_read_csv_s3(self):
        """read a csv from s3"""
        expected_df = pd.DataFrame({'e-mail': {0: 'n@gmail.com', 1: 'p@gmail.com', 2: 'h@gmail.com', 3: 's@gmail.com',
                                               4: 'l@gmail.com', 5: 'v@gmail.com', 6: None},
                                    'number': {0: 0, 1: 1, 2: 0, 3: 0, 4: 1, 5: 0, 6: 0}})
        pth = S3Location('gd.dativa.test').join('generic', 'email_test.csv')
        session = boto3.Session()
        fh = PandasDoggo(boto_session=session)
        df = fh.load(pth)
        assert_frame_equal(df, expected_df)

    def test_write_csv_s3(self):
        df = pd.DataFrame({'e-mail': {0: 'n@gmail.com', 1: 'p@gmail.com', 2: 'h@gmail.com', 3: 's@gmail.com',
                                      4: 'l@gmail.com', 5: 'v@gmail.com', 6: None},
                           'number': {0: 0, 1: 1, 2: 0, 3: 0, 4: 1, 5: 0, 6: 0}})
        pth = S3Location('gd.dativa.test').join('generic', 'email_test_copy.csv')
        expected_pth = S3Location('gd.dativa.test').join('generic', 'email_test.csv')
        fh = PandasDoggo()
        fh.save(df, pth, index=None)
        with FileDoggo(pth) as p, FileDoggo(expected_pth) as p2:
            self.assertEqual(p.read().strip(), p2.read().strip())

        s3 = boto3.resource('s3')
        obj = s3.Object(pth.bucket, pth.key)
        obj.delete()

    def test_read_pq_s3(self):
        fh = PandasDoggo()

        df_s3 = fh.load_parquet('s3://07092018pqtest/data.parquet')

        pth_local = os.path.join(self.base_path, 'parquet', 'data.parquet')
        df_l = fh.load_parquet(pth_local)

        assert_frame_equal(df_s3, df_l)

    def test_write_pq_s3(self):
        fh = PandasDoggo()
        pth_local = os.path.join(self.base_path, 'parquet', 'data.parquet')
        df_l = fh.load_parquet(pth_local)
        s3 = boto3.resource('s3')
        obj = s3.Object('07092018pqtest', 'write.parquet')
        obj.delete()  # just in case
        fh.save(df_l, 's3://07092018pqtest/write.parquet')

        obj.load()  # checks that it was written
        obj.delete()

    def test_cant_guess_format(self):
        fh = PandasDoggo()
        with self.assertRaises(ValueError):
            fh.load('some_text_file')

    def test_invalid_format_detected(self):
        fh = PandasDoggo()
        with self.assertRaises(ValueError):
            fh.load('some_text_file.dat')
        with self.assertRaises(ValueError):
            fh.save(pd.DataFrame(), 'some_text_file.dat')

    def test_invalid_format_passed(self):
        fh = PandasDoggo()
        with self.assertRaises(ValueError):
            fh.load('some_text_file.dat', file_format='bees?')

    def test_whos_a_good_boi_den(self):
        with self.assertRaises(ValueError):
            with FileDoggo('some_path_to_a_file', mode='justusewb', is_s3=True) as f:
                f.write('should have read the docs')
