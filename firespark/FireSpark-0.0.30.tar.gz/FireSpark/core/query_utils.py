
# FireSpark -- the Data Work
# Copyright 2020 The FireSpark Author. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""FireSpark Dataset Query Library """

import io
import numpy as np
import pandas as pd
from pandas.io import sql
import sqlite3
from .numpy_utils import NumpyLoaderBase

class QueryDataset(NumpyLoaderBase):
    """ Base parquet dataset query class

        Args:
        path:    local file system path to dataset. All the
                    Parquet files assume the same petastorm schema. 
        url:     file or s3 URL to parquet dataset
        dataset: string, name of the dataset
        columns: categories to load. Availale categories include:
                    (url, depth, width, height, format, imdata, label)
                    default: [cam, url, label]
        label_partition: a dict object that prescribe rule that 
                         partition label column to individual label
                         field. For example, the detection label 
                         can be partiioned as:
                         {"bbx": [0,1,2,3], "category": [4]}
        """
    def __init__(self, **pars):
        if not 'columns' in pars:
            pars['columns'] = ['cam', 'url', 'label']
        super().__init__(**pars)
        self.label_partition = {"bbx": [0,1,2,3], "category": [4]}
        if 'label_partition' in self.pars:
            self.label_partition = self.pars['label_partition']
        sqlite3.register_adapter(np.ndarray, self.adapt_array)
        sqlite3.register_converter("arraytodb", self.to_array)
        self.connect = sqlite3.connect(":memory:", detect_types=sqlite3.PARSE_DECLTYPES)

    @staticmethod
    def adapt_array(arr):
        """ converts np.array to TEXT when inserting """
        out = io.BytesIO()
        np.save(out, arr)
        out.seek(0)
        return sqlite3.Binary(out.read())

    @staticmethod
    def to_array(data):
        """ converts TEXT to np.array when selecting """
        memfile = io.BytesIO(data)
        memfile.seek(0)
        return np.squeeze(np.load(memfile))
    
    def query(self, sqlstr=""):
        if not sqlstr:
            raise Exception('Please provide valid query string!')
        df = self.loader.copy()
        df['label'] = df['label'].apply(lambda x: self.to_array(x))
        for k, v in self.label_partition.items():
            df[k] = df.apply(lambda row: row.label[:,v], axis=1)
        df.drop('label', axis=1, inplace=True)
        df.to_sql(
            self.pars['dataset'],
            self.connect, 
            if_exists='replace',
            dtype={'bbx':"arraytodb",'category':"arraytodb"}
        )        
        return pd.read_sql(sqlstr, self.connect)        
        

        





        



