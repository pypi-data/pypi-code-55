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
"""FireSpark LMDB dataset utility library

Methods for pcking information from level5 dynamic object
lmdb dataset to MAS protobuf.

"""

import os
import lmdb
import tqdm
import ntpath
import tempfile
import shutil

from ..core.proto_utils import ProtoDataset
from ..protos.mas import annotation_pb2 as annotation_proto
from ..protos.mas import image_data_pb2 as image_proto
from ..protos.mas import labels_pb2 as label_proto
from ..protos.src.perception.annotation.proto import annotation_pb2 as l5annotation_proto


class LmdbDataset(ProtoDataset):
    """ Level5 Lmdb dataset class """
    def __init__(self, **job):
        super().__init__(**job)
        self.l2l = {0:0, 1:0, 2:0, 3:1, 1001:4001, 1002:4002, 1003:4006, 1004:4004,
                    1005:4003, 1006:4005, 1007:4000, 1008:4007, 1009:4100, 1010:4000,
                    2001:3001, 2002:3200, 3001:3101, 3002:3201, 3003:3100, 4001:1001,
                    5001:2000, 6001:5100, 6002:5220, 6003:6001, 6004:6001, 7001:11000,
                    7002:11000, 7003:11300, 12001:5200, 12002:5000, 13002:11400,
                    13003:5001, 13007:4200}
    
    def _record_provider(self):
        """ provide raw record files from the source dataset directory """
        if not os.path.isdir(self._datasrc): return
        records = set()
        for r, _, f in os.walk(self._datasrc):
            if "data.mdb" in f:
                records.add(r)
        self._n_records = len(records)
        for r in records:
            yield r
    
    def get_data_from_files(self, record):
        """ Method for extracting level5 annotated protobuf from a local record.
        
            Returns: a list of protobuf messages
        """
        if self._bucket_name:
            workspace_ = tempfile.mkdtemp()
            lmdb_file = os.path.join(workspace_, ntpath.basename(record))
            self.aws.download_file(self._bucket_name, record, lmdb_file)
            record = workspace_        

        env = lmdb.open(record, max_readers=1, 
                    readonly=True, lock=False,
                    readahead=False, meminit=False)

        if self._bucket_name:
            shutil.rmtree(workspace_)
        
        pbs = []
        with env.begin(write=False) as txn:
            length = txn.stat()['entries']
            # print("/////// {} contains {} records".format(record, length))
            lmdb_cursor = txn.cursor()
            for _, serialized_string in lmdb_cursor:
                l5proto = l5annotation_proto.AnnotatedImageProto()
                l5proto.ParseFromString(serialized_string)
                pbs.append(l5proto)

        return pbs
    
    def _example_record(self, f):
        """ Method for providing one dataset example record
            Modified for lmdb dataset

            Returns: lmdb file string or None
        """
        if "data.mdb" in f:
            return f
        else:
            return None

    def _add_to_proto(self, record):
        """ Method for processing level5 joint example to protobuf message

            Args:
            record: a level5 annotated protobuf object

            Returns:
            new MAS protobuf message for dataset example
        """
        pd = image_proto.ImageDataProto()
        pd.host.host_id = record.car_id
        pd.host.host_type = 1
        pd.device.camera_id = record.camera_id
        pd.image_data.host_state.timestamp_ns = record.timestamp_ns
        pd.image_data.host_state.longitude = record.longitude
        pd.image_data.host_state.latitude = record.latitude
        pd.image_data.host_state.motion_state = 0
        pd.image_data.image.width = 1920
        pd.image_data.image.height = 1080
        pd.image_data.image.depth = 3
        pd.image_data.image.format = 1
        pd.image_data.image.data = record.compressed_image.data

        for obj in record.objects:
            obj_proto = annotation_proto.ObjectProto()       
            obj_proto.cbox.x = (obj.box.max.x + obj.box.min.x)/2.0/1920
            obj_proto.cbox.y = (obj.box.max.y + obj.box.min.y)/2.0/1080
            obj_proto.cbox.w = (obj.box.max.x - obj.box.min.x)/1920
            obj_proto.cbox.h = (obj.box.max.y - obj.box.min.y)/1080
            obj_proto.oclass = self.l2l[obj.label]
            obj_proto.attributes.extend(obj.attributes)
            pd.image_data.annotation.objects.append(obj_proto)
        return pd
    
    def pack_protos(self):
        """ Process mas data examples into proto format in batches
            For child classes implemented for different raw datasets,
            this method shall be overridden.
        """
        num_proc = 0
        self._workspace = tempfile.mkdtemp()
        pbar = tqdm.tqdm(total=1000)
        for rec in self._record_list:
            record = self._example_record(rec)
            if not record: continue
            for emp_data in self.get_data_from_files(record):
                if not emp_data.compressed_image.compression_format == 1:
                    continue
                proto_data = self._add_to_proto(emp_data)
                if not proto_data: continue
                self._pb.proto_batch.append(proto_data)
                num_proc += 1
                self._num_to_batch += 1
            pbar.update(int(1.0/self._n_records*1000))

            if self._num_to_batch >= self._batch_size:
                self._gen_proto_record()

        if self._num_to_batch > 0:
            self._gen_proto_record()
        shutil.rmtree(self._workspace)
        print("///: Totally {} examples from {} lmdb files saved to {}".format(
            num_proc, self._n_records, self._datadst)
        )


class TLLmdbDataset(LmdbDataset):
    """ Level5 Lmdb dataset class for traffic light """
    def __init__(self, **job):
        super().__init__(**job)
        self.l2l = {6001:5100, 6002:5101, 6003:5102, 6004:5103}
        self.tl_attributes = {301: 'red', 302: 'yellow', 303: 'green',
                 304: 'multiple', 305: 'unknown', 401: 'circle',
                 402: 'left arrow', 403: 'right arrow',
                 404: 'straight arrow', 405: 'mulitple',
                 406: 'unknown', 407: 'other'}

    def _add_to_proto(self, record):
        """ Method for processing level5 joint example to protobuf message

            Args:
            record: a level5 annotated protobuf object

            Returns:
            new MAS protobuf message for dataset example
        """
        pd = image_proto.ImageDataProto()
        pd.host.host_id = record.car_id
        pd.host.host_type = 1
        pd.device.camera_id = record.camera_id
        pd.image_data.host_state.timestamp_ns = record.timestamp_ns
        pd.image_data.host_state.longitude = record.longitude
        pd.image_data.host_state.latitude = record.latitude
        pd.image_data.host_state.motion_state = 0
        pd.image_data.image.width = 1920
        pd.image_data.image.height = 1080
        pd.image_data.image.depth = 3
        pd.image_data.image.format = 1
        pd.image_data.image.data = record.compressed_image.data

        for obj in record.objects:
            if not obj.label in self.l2l.keys(): continue
            obj_proto = annotation_proto.ObjectProto()       
            obj_proto.cbox.x = (obj.box.max.x + obj.box.min.x)/2.0/1920
            obj_proto.cbox.y = (obj.box.max.y + obj.box.min.y)/2.0/1080
            obj_proto.cbox.w = (obj.box.max.x - obj.box.min.x)/1920
            obj_proto.cbox.h = (obj.box.max.y - obj.box.min.y)/1080
            obj_proto.oclass = self.l2l[obj.label]
            attributes_ = []
            for oa in obj.attributes:
                if oa in self.tl_attributes.keys():
                    attributes_.append(oa)
            obj_proto.attributes[:] = attributes_
            pd.image_data.annotation.objects.append(obj_proto)
        return pd