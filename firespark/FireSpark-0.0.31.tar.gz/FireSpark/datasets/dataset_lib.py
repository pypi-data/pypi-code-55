
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
"""FireSpark custom dataset utility library """

import cv2
import numpy as np
from ..core.data_utils import SparkDataset


class L5ImageDataset(SparkDataset):
    """ Level5 image dataset class """
    def __init__(self, **job):
        super().__init__(**job)
    
    def _row_generator(self, pd):
        """ generate information from an image proto

            Args:
            pd: image proto message

            Return:
            dictionary of image data and annotation
        """		
        if self.prepare_label_fn:
            label = self.prepare_label_fn(pd.image_data.annotation)
        else:
            label = self.prepare_label(pd.image_data.annotation)
        im = cv2.imdecode(np.fromstring(pd.image_data.image.data, dtype=np.uint8), -1)

        if label.size == 0 or im is None:
            return None

        return {
            'width': pd.image_data.image.width,
            'height': pd.image_data.image.height,
            'depth': pd.image_data.image.depth,
            'format': pd.image_data.image.format,
            'imdata': im,
            'label': label
        }


class L5TLImageDataset(SparkDataset):
    """ Level5 traffic light image dataset class """
    def __init__(self, **job):
        super().__init__(**job)
        self.l2l = {5100:5100, 5101:5100, 5102:5100, 5103:5100}
    
    def prepare_label(self, annotation):
        label = []
        bbxs = []
        attributes = []
        for obj in annotation.objects:
            if not obj.oclass in self.l2l.keys(): continue
            label.append([self.l2l[obj.oclass]])
            bbxs.append((obj.cbox.x, obj.cbox.y, obj.cbox.w, obj.cbox.h))
            if obj.attributes:
                attri = []
                for a in obj.attributes:
                    attri.append(a)
                if len(attri)==1: attri.append(0)
                if len(attri)>2: attri=attri[:2]
                attributes.append(attri)
            else:
                attributes.append([0, 0])
        return np.array(label), np.array(bbxs), np.array(attributes)

    def _row_generator(self, pd):
        """ generate information from an image proto

            Args:
            pd: image proto message

            Return:
            dictionary of image data and annotation
        """		
        label, bbxs, attribs = self.prepare_label(pd.image_data.annotation)
        im = cv2.imdecode(np.fromstring(pd.image_data.image.data, dtype=np.uint8), -1)
        if label.size == 0 or im is None:
            return None

        return {
            'width': pd.image_data.image.width,
            'height': pd.image_data.image.height,
            'depth': pd.image_data.image.depth,
            'format': pd.image_data.image.format,
            'imdata': im,
            'label': label,
            'attributes': attribs,
            'bbxs': bbxs
        }


class SemsegDataset(SparkDataset):
    """ Level5 image dataset class """
    def __init__(self, **job):
        super().__init__(**job)
    
    def _decode_imdata(self, url):
        bucket, image_key = self.aws.url_to_bnk(url, False)
        im_obj = self.aws.client.get_object(Bucket=bucket, Key=image_key)
        im_data = im_obj["Body"].read()
        im_array = np.fromstring(im_data, np.uint8)
        im = cv2.imdecode(im_array, cv2.IMREAD_COLOR)
        return im
    
    def _row_generator(self, pd):
        """ generate information from an image proto

            Args:
            pd: image proto message

            Return:
            dictionary of image data and annotation
        """
        if self.aws.S3_BUCKET_BASE in pd.image_data.image.url:
            im = self._decode_imdata(pd.image_data.image.url)
        else:
            im = cv2.imread(pd.image_data.image.url)

        if self.aws.S3_BUCKET_BASE in pd.image_data.annotation.semseg_labels.mask.url:
            label = self._decode_imdata(pd.image_data.annotation.semseg_labels.mask.url)
        else:
            label = cv2.imread(pd.image_data.annotation.semseg_labels.mask.url)
        
        if label is None or im is None:
            return None

        return {
            'width': pd.image_data.image.width,
            'height': pd.image_data.image.height,
            'depth': pd.image_data.image.depth,
            'format': pd.image_data.image.format,
            'label_format': pd.image_data.image.format,
            'url': pd.image_data.image.url,
            'imdata': im,
            'label': label}


class BinsegDataset(SparkDataset):
    """ Level5 image dataset class """
    def __init__(self, **job):
        super().__init__(**job)
    
    def _decode_imdata(self, url):
        bucket, image_key = self.aws.url_to_bnk(url, False)
        im_obj = self.aws.client.get_object(Bucket=bucket, Key=image_key)
        im_data = im_obj["Body"].read()
        im_array = np.fromstring(im_data, np.uint8)
        im = cv2.imdecode(im_array, cv2.IMREAD_COLOR)
        return im

    def _decode_mask(self, url):
        from PIL import Image
        from io import BytesIO

        if self.aws.S3_BUCKET_BASE in url:
            bucket, image_key = self.aws.url_to_bnk(url, False)
            im_obj = self.aws.client.get_object(Bucket=bucket, Key=image_key)
            im_data = im_obj["Body"].read()
            data_ = Image.open(BytesIO(im_data))
        else:
            data_ = Image.open(url)
        return np.copy(np.asarray(data_))
    
    def _row_generator(self, pd):
        """ generate information from an image proto

            Args:
            pd: image proto message

            Return:
            dictionary of image data and annotation
        """
        if self.aws.S3_BUCKET_BASE in pd.image_data.image.url:
            im = self._decode_imdata(pd.image_data.image.url)
        else:
            im = cv2.imread(pd.image_data.image.url)

        label = self._decode_mask(pd.image_data.annotation.semseg_labels.mask.url)
        
        if label is None or im is None:
            return None

        return {
            'width': pd.image_data.image.width,
            'height': pd.image_data.image.height,
            'depth': pd.image_data.image.depth,
            'format': pd.image_data.image.format,
            'label_format': pd.image_data.image.format,
            'url': pd.image_data.image.url,
            'imdata': im,
            'label': label}