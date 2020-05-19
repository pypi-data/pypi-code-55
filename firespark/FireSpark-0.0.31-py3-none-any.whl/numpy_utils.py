
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
"""FireSpark Numpy Dataloader Library """

import os
from pathlib import Path

import io
import cv2
import numpy as np
import pandas as pd
import pyarrow.parquet as pq

class NumpyLoaderBase(object):
    """ Base parquet data loader for vanila python numpy framework

            Args:
            path:    local file system path/paths to dataset. All the
                     Parquet files assume the same petastorm schema. 
            fname:   signale parquet filename.
            url:     file or s3 URL to parquet dataset
            dataset: string, name of the dataset
            columns: categories to load. Availale categories include:
                     (url, depth, width, height, format, imdata, label)
                     default: [imdata, label]
        """
    def __init__(self, **pars):
        self.pars = {
            'path' : "",
            'fname' : "",
            'url' : "",
            'dataset' : "",
            'columns' : ['imdata', 'label'],
            'mode' : ""
        }
        self.pars.update(pars)
        self.loader = None
        self.loader_size = 0
        self.loader_meta = None
        self._make_loader()

    def _make_loader(self):
        """ Instantiate numpy dataloader object	"""
        if self.pars['path'] or self.pars['fname']:
            parquets = []
            if self.pars['path']:            
                if not isinstance(self.pars['path'], list):
                    self.pars['path'] = [self.pars['path']]
                for _path in self.pars['path']:
                    parquets += list(
                        Path(os.path.abspath(_path)
                        ).glob('**/*.parquet')
                    )
            if self.pars['fname']:
                if not isinstance(self.pars['fname'], list):
                    self.pars['fname'] = [self.pars['fname']]
                for pf in self.pars['fname']:
                    if not os.path.isfile(pf): continue
                    f, e = os.path.splitext(pf)
                    if not e=='.parquet': continue
                    parquets.append(pf)
            if parquets:
                dfs = []
                for f in parquets:
                    dfs.append(
                        pq.read_table(source=f,
                            columns=self.pars['columns']
                        ).to_pandas())
                self.loader = pd.concat(dfs)
                self.loader_size = self.loader.shape[0]
                if not self.loader_meta:
                    self.loader_meta = pq.ParquetFile(parquets[0]).metadata        
        elif self.pars['url'].startswith("file://") or \
            self.pars['url'].startswith("s3://"):
            pass
        else:
            print("/Error/: incorrect URL or PATH string!")
    
    def get_dataset_name(self):
        """ Return dataset name	"""
        return self.pars['dataset']
    
    def __len__(self):
        """ get the length of the dataset loader """
        return self.loader_size
    
    def size(self):
        return self.__len__()
    
    def info(self):
        print('---------schema info-------')
        print(self.loader_meta)
        print('---------counts-------')
        print(self.loader.count())
    
    def __getitem__(self, id):
        example = self.loader.iloc[id]
        im_array = np.frombuffer(example.imdata, np.uint8)
        im = cv2.imdecode(im_array, cv2.IMREAD_COLOR)
        memfile = io.BytesIO(example.label)
        label = np.load(memfile)
        return (im, label)
    
    def partition(self, partition=[0.80, 0.10, 0.10], out_path=""):
        """Upload a file to an S3 bucket

        Args:
        partition: 3-element list of partition ratios
        out_path: directory to save exported datasets

        """
        if not out_path:
            raise Exception('Valid out_path has to be provided!')
        if not os.path.isdir(out_path):
            os.makedirs(out_path)
        if not sum(partition)==1.0:
            partition = [x/sum(partition) for x in partition]
        train, eval, test = np.split(
            self.loader.sample(frac=1),
            [int(partition[0]*len(self.loader)),
             int(sum(partition[:2])*len(self.loader))
            ]
        )
        dlen = []
        if len(train)>0:
            dlen.append(len(train))
            train.to_parquet(os.path.join(out_path, 'train.parquet'))
        if len(eval)>0:
            dlen.append(len(eval))
            eval.to_parquet(os.path.join(out_path, 'eval.parquet'))
        if len(test)>0:
            dlen.append(len(test))
            test.to_parquet(os.path.join(out_path, 'test.parquet'))
        print("///: The dataset was partitioned into train/eval/test")
        print("///: in ratios of {}".format(partition))
        print("///: train/eval/test size: {}".format(dlen))
            



