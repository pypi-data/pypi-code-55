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
""" FireSpark
Methods for pcking information from raw dataset 
to proto template. 

Instructions:
In order to process protobuf record for a new dataset, 
a dataset object class has to be defined, which 
implementing method to:

1). A record provider method "_example_record()" that take
    one raw dataset record from the original dataset and 
    produce a (image, annotation) tuple. Users defining new
    class have the flexibility to have other data types for
    the record list given that such record can be correctly
    used in "_example_template()" method. 
2). Override the "_example_template()" method if necessary. 
    The output of this method is a template dictionary 
    containing all defined protobuf fields. For user's 
    dataset, filling the dataset inforamtion as much as
    possible in this method. After that, the template dict
    is converted to protobuf message based on target protobuf
    message definition. 
3). If necessary, make change to the protobuf record's naming
    method in "_proto_file()". 

Those are all you need before protobuf database archiving task. 

"""

import os
import cv2
from ..core.proto_utils import ProtoDataset
from ..protos.mas import annotation_pb2 as annotation_proto
from ..protos.mas import image_data_pb2 as image_proto
from ..protos.mas import labels_pb2 as label_proto 


class DowntownDataset(ProtoDataset):
    """ Downtown dataset class """
    def __init__(self, **donwtwon_job):
        super().__init__(**donwtwon_job)
        self.catetory_map = {
                0: label_proto.PCP_L_PEDESTRIAN,
                1: label_proto.PCP_L_BICYCLE,
                2: label_proto.PCP_L_CAR,
                3: label_proto.PCP_L_BUS,
                4: label_proto.PCP_L_TRUCK
            }
    
    def _example_record(self, f):
        """ Method for providing one downtown dataset example record
            For child classes implemented for different raw datasets,
            this method shall be overridden.

            Returns: a tuple of (image file, annotation file)
        """
        if '.txt' in f:
            return (f[:-3]+"jpg", f)
        else:
            return None

    def _add_to_proto(self, record):
        """ Method for processing downtown dataset example to protobuf message
            For child classes implemented for different raw datasets,
            this method shall be overridden.

            Args:
            record: a tuple of (url, image_array, annotation_string)

            Returns:
            new protobuf message for dataset example
        """
        imh, imw, imc = record[1].shape
        obstacles = []
        for line in record[2]:
            a = line.rstrip().split(" ")
            obstacles.append({"class": self.catetory_map[int(a[0])],
                "bbx": (float(a[1]), float(a[2]), float(a[3]), float(a[4]))})
        if not obstacles: return None

        pd = image_proto.ImageDataProto()
        if 'Main' in record[0]:
            pd.device.camera_id = 'AtsBr_ZL_Rr60_v2_FRONT'
            pd.device.calib.optical_center.x = 645.590088
            pd.device.calib.optical_center.y = 404.268311
            pd.device.calib.pose.offset_x = -699.9972
            pd.device.calib.pose.offset_y = -92.075
            pd.device.calib.pose.offset_z = 695.325
            pd.device.calib.pose.rectified_yaw = -180
            pd.device.calib.pose.relative_yaw = 0.938434893
            pd.device.calib.pose.relative_pitch = 72.16128929
            pd.device.calib.pose.relative_roll = 1.779883214
        elif 'LEFT' in record[0]:
            pd.device.camera_id = 'AtsBr_ZL_Rr60_v2_LEFT'
            pd.device.calib.optical_center.x = 646.712524
            pd.device.calib.optical_center.y = 403.630188
            pd.device.calib.pose.offset_x = 920.75
            pd.device.calib.pose.offset_y = -1039.625
            pd.device.calib.pose.offset_z = 920.75
            pd.device.calib.pose.rectified_yaw = -90
            pd.device.calib.pose.relative_yaw = 0.274599064
            pd.device.calib.pose.relative_pitch = 44.01960357
            pd.device.calib.pose.relative_roll = 1.0391655
        elif 'REAR' in record[0]:
            pd.device.camera_id = 'AtsBr_ZL_Rr60_v2_REAR'
            pd.device.calib.optical_center.x = 646.2454
            pd.device.calib.optical_center.y = 404.3708
            pd.device.calib.pose.offset_x = 3736.9386
            pd.device.calib.pose.offset_y = -41.0967
            pd.device.calib.pose.offset_z = 839.1389
            pd.device.calib.pose.rectified_yaw = 0
            pd.device.calib.pose.relative_yaw = -2.397
            pd.device.calib.pose.relative_pitch = 60.1193
            pd.device.calib.pose.relative_roll = 1.2359
        elif 'RIGHT' in record[0]:
            pd.device.camera_id = 'AtsBr_ZL_Rr60_v2_RIGHT'
            pd.device.calib.optical_center.x = 642.071594
            pd.device.calib.optical_center.y = 404.993286
            pd.device.calib.pose.offset_x = 920.75
            pd.device.calib.pose.offset_y = 1039.625
            pd.device.calib.pose.offset_z = 920.75
            pd.device.calib.pose.rectified_yaw = 90
            pd.device.calib.pose.relative_yaw = -1.258962111
            pd.device.calib.pose.relative_pitch = 44.22432222
            pd.device.calib.pose.relative_roll = -2.9152963
        else:
            pd.device.camera_id = 'UNKNOWN'

        pd.device.calib.lens_type = 1
        pd.device.calib.pixelsize = 0.003
        pd.device.calib.focal_length.x = 1.0
        pd.device.calib.focal_length.y = 1.0
        pd.device.calib.radial_distortion_I2W.extend(
            [0, 0.949960, -0.001374, -0.063414, -0.014087, 0.017911])
        pd.device.calib.radial_distortion_W2I.extend(
            [0, 1.044910, 0.074981, -0.148220, 0.303387, -0.132219])
        pd.device.calib.pose.ref_origin = "front axle center at group"
        pd.device.calib.pose.ref_axis_x = "to rear axle"
        pd.device.calib.pose.ref_axis_y = "to vehicle body right"
        pd.device.calib.pose.ref_axis_z = "to up"
        pd.device.calib.pose.rectified_pitch = 0
        pd.device.calib.pose.rectified_roll = 0
        pd.image_data.image.width = imw
        pd.image_data.image.height = imh
        pd.image_data.image.depth = imc
        pd.image_data.image.format = 1
        pd.image_data.image.url = record[0]
        for obj in obstacles:
            obj_proto = annotation_proto.ObjectProto()
            obj_proto.oclass = obj['class']
            obj_proto.cbox.x = obj['bbx'][0]
            obj_proto.cbox.y = obj['bbx'][1]
            obj_proto.cbox.w = obj['bbx'][2]
            obj_proto.cbox.h = obj['bbx'][3]
            pd.image_data.annotation.objects.append(obj_proto)
        return pd
    
    def _proto_file(self):
        """ get the filename of a proto batch """
        return "{}_{}_batch_{}.proto".format(
                            self._dataset_name,
                            self._pb.proto_batch[0].device.camera_id,
                            self._batch_id)
    
    
class DirtyLenseDataset(ProtoDataset):
    """ Dirty-lense dataset class """
    def __init__(self, **dl_job):
        super().__init__(**dl_job)

    def _example_record(self, f):
        """ Method for provide one downtown dataset example record
            For child classes implemented for different raw dataset, 
            this method shall be overrided. 

            Return: image and annotation file tuple
        """
        if '..json' in f:
            imf = f.replace("/Annotations/", "/Images/")
            return (imf[:-5]+"jpg", f)
        else:
            return None

    def _add_to_proto(self, record):
        """ Method for process downtown dataset example to protobuf
            For child classes implemented for different raw dataset, 
            this method shall be overrided. 

            Args:
            record: a tuple of (url, image_array, annotation_string)

            Returns:
            new protobuf message for dataset example
        """
        imh, imw, imc = record[1].shape
        pd = image_proto.ImageDataProto()
        pd.image_data.image.width = imw
        pd.image_data.image.height = imh
        pd.image_data.image.depth = imc
        pd.image_data.image.format = 1
        pd.image_data.image.url = record[0]
        for c in record[2]['cells']:			
            dl_proto = annotation_proto.DirtyLensCell()
            dl_proto.location.min.x = float(c['left'])
            dl_proto.location.min.y = float(c['top'])
            dl_proto.location.max.x = float(c['right'])
            dl_proto.location.max.y = float(c['bottom'])
            dl_proto.occlusion_type = c['occlusion_type']
            dl_proto.occlusion_percentage = c['occlusion_percentage']
            dl_proto.occlusion_density = c['occlusion_density']
            pd.image_data.annotation.dl_cell.append(dl_proto)
        return pd
    
    def _proto_file(self):
        return "{}_batch_{}.proto".format(
                            self._dataset_name,
                            self._batch_id)


class BDD100k_Seg(ProtoDataset):
    """ BDD100k Segmentation dataset 
        The detailed BDD label definitin is available at:
        https://github.com/ucbdrive/bdd100k/blob/master/bdd100k/label.py    
    """

    """ [2020.05.17]: only a selected subset of labels are used in this 
        dataset processing task """
    l2l = {3:11200, 7:11300, 20:11400, 23:5001,
           25:5100, 26:5200, 28:11100, 29:11101,
           30:11001, 31:1000, 32:3100, 33:3001,
           34:4004, 35:4001, 36:4002, 37:3200,
           38:4100, 39:4006, 40:4003}

    def __init__(self, **job):
        super().__init__(**job)

    def _example_record(self, f):
        """ Method for provide one dataset example record

            Args:
            f: one file from file list

            Return: image and annotation file tuple
        """
        if '.png' in f:
            example_id = os.path.basename(f).split("_")[0]
            imf = f.replace("/labels/", "/images/")
            return (os.path.join(os.path.dirname(imf), example_id+'.jpg'), f)
        else:
            return None

    @staticmethod
    def get_data_from_keys(client, bucket, record):
        """ Method for obtaining image and annotation data from a record from s3 bucket.

            Args:
                bucket: bucket name
                record: tuple of image and annotation keys (str)

            Returns: a tuple of (image_url, annotation_mask_url)
        """
        image_key, annot_key = record
        image_file = os.path.join("s3://", bucket, image_key)
        annot_file = os.path.join("s3://", bucket, annot_key)
        return (image_file, annot_file)
    
    @staticmethod
    def get_data_from_files(record):
        """ Method for obtaining image and annotation data from a local record.

            Args:
            record: tuple of image and annotation files (str)

            Returns: a tuple of (image_url, annotation_mask_url)
        """
        image_file, annot_file = record
        return (image_file, annot_file)

    def _add_to_proto(self, record):
        """ Method for process downtown dataset example to protobuf
            For child classes implemented for different raw dataset, 
            this method shall be overrided. 

            Args:
            record: a tuple of (image_url, mask_url)

            Returns:
            new protobuf message for dataset example
        """
        pd = image_proto.ImageDataProto()
        pd.image_data.image.width = 1280
        pd.image_data.image.height = 720
        pd.image_data.image.depth = 3
        pd.image_data.image.format = 1
        pd.image_data.image.url_only = 1
        pd.image_data.image.url = record[0]

        seg_proto = annotation_proto.SegmentationLabel()
        seg_proto.class_label_map.update(self.l2l)
        seg_proto.mask.width = 1280
        seg_proto.mask.height = 720
        seg_proto.mask.depth = 3
        seg_proto.mask.format = 2
        seg_proto.mask.url_only = 1
        seg_proto.mask.url = record[1]
        pd.image_data.annotation.semseg_labels.CopyFrom(seg_proto)

        return pd


class Carvana_Seg(ProtoDataset):
    """ Carvana Segmentation dataset """
    l2l = {0:1, 1:4001}

    def __init__(self, **job):
        super().__init__(**job)

    def _example_record(self, f):
        """ Method for provide one dataset example record

            Args:
            f: one file from file list

            Return: image and annotation file tuple
        """
        if '.jpg' in f:
            example_id = f.split(".")[0]
            anf = example_id.replace("/train/", "/train_masks/")
            return (f, anf+'_mask.gif')
        else:
            return None

    @staticmethod
    def get_data_from_keys(client, bucket, record):
        """ Method for obtaining image and annotation data from a record from s3 bucket.

            Args:
                bucket: bucket name
                record: tuple of image and annotation keys (str)

            Returns: a tuple of (image_url, annotation_mask_url)
        """
        image_key, annot_key = record
        image_file = os.path.join("s3://", bucket, image_key)
        annot_file = os.path.join("s3://", bucket, annot_key)
        return (image_file, annot_file)
    
    @staticmethod
    def get_data_from_files(record):
        """ Method for obtaining image and annotation data from a local record.

            Args:
            record: tuple of image and annotation files (str)

            Returns: a tuple of (image_url, annotation_mask_url)
        """
        image_file, annot_file = record
        return (image_file, annot_file)

    def _add_to_proto(self, record):
        """ Method for process downtown dataset example to protobuf
            For child classes implemented for different raw dataset, 
            this method shall be overrided. 

            Args:
            record: a tuple of (image_url, mask_url)

            Returns:
            new protobuf message for dataset example
        """
        pd = image_proto.ImageDataProto()
        pd.image_data.image.width = 1918
        pd.image_data.image.height = 1280
        pd.image_data.image.depth = 3
        pd.image_data.image.format = 1
        pd.image_data.image.url_only = 1
        pd.image_data.image.url = record[0]

        seg_proto = annotation_proto.SegmentationLabel()
        seg_proto.class_label_map.update(self.l2l)
        seg_proto.mask.width = 1918
        seg_proto.mask.height = 1280
        seg_proto.mask.depth = 1
        seg_proto.mask.format = 3
        seg_proto.mask.url_only = 1
        seg_proto.mask.url = record[1]
        pd.image_data.annotation.semseg_labels.CopyFrom(seg_proto)

        return pd