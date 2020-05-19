from abc import abstractmethod
import os
import pickle
from . import utils

class ImgInfo():
    def __init__(self,img_path, width, height):
        self.img_path = img_path
        self.width = float(width)
        self.height = float(height)
        self.objs = []

    def set_objs(self, Obj):
        self.objs.append(Obj)


class Obj():
    def __init__(self, class_name, class_index, box, **kwags):
        self.class_name = class_name
        self.class_index = class_index
        self.box = box
        for k in kwags:
            self.__setattr__(k, kwags[k])


class IOD():
    # Image Object Dataset
    def __init__(self, cache_file, data_dir=None, download_url=None):
        self.data_dir = data_dir
        self.cache_file = cache_file
        self.download_url = download_url

        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

        # 关于图像数据，如果本地没有则直接下载
        # 下载能被用于生成供训练的cache文件
        self.init_images(self.data_dir)

        # 关于供训练的数据，首先是
        # 本地的cache_file优先
        # 其次是download cache文件
        # 最后是解析gt.txt生成cache文件以供网络使用
        if os.path.exists(self.cache_file):
            self.img_infos = self.load_dataset_cache(self.cache_file)
        elif self.download_url is not None:
            # download cache
            utils.download_data(self.download_url, self.cache_file)
            self.img_infos = self.load_dataset_cache(self.cache_file)
        else:
            self.img_infos = self.parse_anno(self.data_dir)
            self.save_dataset_cache(self.img_infos, self.cache_file)

        self.numbers = len(self.img_infos)
        self.index = list(range(self.numbers))


    @abstractmethod
    def init_images(self, data_dir):
        pass


    @abstractmethod
    def parse_anno(self, data_dir):
        pass


    def load_dataset_cache(self, cache_file):
        with open(cache_file, 'rb') as f:
            return pickle.load(f)

    def save_dataset_cache(self, img_infos, cache_file):
        with open(cache_file, 'wb') as f:
            pickle.dump(img_infos, f)

